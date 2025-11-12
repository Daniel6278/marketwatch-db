import os
import pymysql
from dotenv import load_dotenv
from tqdm import tqdm
import random
from datetime import datetime, timedelta

load_dotenv()

DB_CONFIG = {
    "host": os.getenv(
        "DB_HOST", "main-marketwatch-db.c74uqiecyemg.us-east-2.rds.amazonaws.com"
    ),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "marketwatchDB"),
}


def get_conn():
    return pymysql.connect(**DB_CONFIG)


def get_users():
    """Fetch all user IDs from the database"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM User;")
    users = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return users


def get_tickers_with_prices():
    """Fetch tickers with their recent closing prices"""
    conn = get_conn()
    cursor = conn.cursor()

    # Get tickers that have price history
    cursor.execute("""
        SELECT DISTINCT t.ticker_symbol,
               (SELECT close_price FROM PriceHistory
                WHERE ticker_symbol = t.ticker_symbol
                ORDER BY date DESC LIMIT 1) as recent_price
        FROM Ticker t
        WHERE EXISTS (
            SELECT 1 FROM PriceHistory ph
            WHERE ph.ticker_symbol = t.ticker_symbol
        );
    """)

    tickers = [(row[0], float(row[1])) for row in cursor.fetchall() if row[1]]
    cursor.close()
    conn.close()
    return tickers


def get_user_holdings(user_id):
    """Get tickers that a user holds in their portfolios"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT h.ticker_symbol
        FROM Holdings h
        JOIN Portfolio p ON h.portfolio_id = p.portfolio_id
        WHERE p.user_id = %s;
    """, (user_id,))
    holdings = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return holdings


def generate_alerts(users, tickers_with_prices):
    """Generate price alerts for users"""
    alerts = []

    print(f"→ Generating alerts for {len(users)} users...")

    for user_id in tqdm(users, desc="Generating alerts"):
        # Get user's holdings to prioritize
        user_holdings = get_user_holdings(user_id)

        # Each user gets 2-8 alerts
        num_alerts = random.randint(2, 8)

        # 70% chance alerts are for stocks they hold, 30% for other stocks
        selected_tickers = []

        for _ in range(num_alerts):
            if user_holdings and random.random() < 0.7:
                # Alert for a stock they hold
                ticker = random.choice(user_holdings)
                # Find the price for this ticker
                ticker_info = next((t for t in tickers_with_prices if t[0] == ticker), None)
                if ticker_info:
                    selected_tickers.append(ticker_info)
            else:
                # Alert for any random stock
                if tickers_with_prices:
                    selected_tickers.append(random.choice(tickers_with_prices))

        for ticker_symbol, current_price in selected_tickers:
            # Randomly choose alert type
            alert_type = random.choice(['ABOVE', 'BELOW'])

            # Set target price based on alert type
            if alert_type == 'ABOVE':
                # Target price 5-20% above current price
                target_price = round(current_price * random.uniform(1.05, 1.20), 2)
            else:
                # Target price 5-20% below current price
                target_price = round(current_price * random.uniform(0.80, 0.95), 2)

            # 80% of alerts are active, 20% are inactive
            is_active = random.random() < 0.8

            # Some alerts might have been triggered (only for inactive ones)
            triggered_at = None
            if not is_active and random.random() < 0.5:
                # Set a triggered date in the past (last 30 days)
                days_ago = random.randint(1, 30)
                triggered_at = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')

            alerts.append((user_id, ticker_symbol, alert_type, target_price, is_active, triggered_at))

    print(f"✓ Generated {len(alerts)} alerts")
    return alerts


def insert_alerts(alerts):
    """Insert alerts into the database."""
    conn = get_conn()
    cursor = conn.cursor()

    sql = """
        INSERT INTO Alert (user_id, ticker_symbol, alert_type, target_price, is_active, triggered_at)
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    try:
        for alert in tqdm(alerts, desc="Inserting alerts"):
            cursor.execute(sql, alert)
        conn.commit()
        print(f"✓ Successfully inserted {len(alerts)} alerts.")

        # Show sample of inserted alerts
        cursor.execute("""
            SELECT a.alert_id, a.ticker_symbol, t.company_name,
                   a.alert_type, a.target_price, a.is_active,
                   u.email
            FROM Alert a
            JOIN Ticker t ON a.ticker_symbol = t.ticker_symbol
            JOIN User u ON a.user_id = u.user_id
            LIMIT 5;
        """)
        print("\nSample of inserted alerts:")
        for row in cursor.fetchall():
            status = "Active" if row[5] else "Inactive"
            print(f"  {row[1]} ({row[2]}) - {row[3]} ${row[4]} [{status}]")
            print(f"    User: {row[6]}")

        # Show statistics
        cursor.execute("""
            SELECT
                COUNT(*) as total_alerts,
                SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active_alerts,
                SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) as inactive_alerts,
                SUM(CASE WHEN alert_type = 'ABOVE' THEN 1 ELSE 0 END) as above_alerts,
                SUM(CASE WHEN alert_type = 'BELOW' THEN 1 ELSE 0 END) as below_alerts,
                SUM(CASE WHEN triggered_at IS NOT NULL THEN 1 ELSE 0 END) as triggered_alerts
            FROM Alert;
        """)
        stats = cursor.fetchone()
        print(f"\nStatistics:")
        print(f"  Total alerts: {stats[0]}")
        print(f"  Active: {stats[1]}, Inactive: {stats[2]}")
        print(f"  Above alerts: {stats[3]}, Below alerts: {stats[4]}")
        print(f"  Triggered alerts: {stats[5]}")

        # Show alerts per user
        cursor.execute("""
            SELECT AVG(alert_count) as avg_alerts_per_user
            FROM (
                SELECT user_id, COUNT(*) as alert_count
                FROM Alert
                GROUP BY user_id
            ) as counts;
        """)
        avg = cursor.fetchone()[0]
        print(f"  Average alerts per user: {float(avg):.2f}")

    except Exception as e:
        conn.rollback()
        print(f"Database insert failed: {e}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    users = get_users()
    tickers_with_prices = get_tickers_with_prices()

    if not users:
        print("No users found in database. Please run insert_users.py first.")
    elif not tickers_with_prices:
        print("No tickers with price history found. Please run insert_tickers.py and insert_price_history.py first.")
    else:
        print(f"Found {len(users)} users and {len(tickers_with_prices)} tickers with prices.")
        alerts = generate_alerts(users, tickers_with_prices)
        insert_alerts(alerts)
