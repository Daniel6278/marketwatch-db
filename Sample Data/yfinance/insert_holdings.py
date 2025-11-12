import os
import pymysql
import pandas as pd
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


def get_portfolios():
    """Fetch all portfolio IDs from the database"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT portfolio_id FROM Portfolio;")
    portfolios = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return portfolios


def get_tickers():
    """Fetch all ticker symbols from the database"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT ticker_symbol FROM Ticker;")
    tickers = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tickers


def get_recent_price(ticker_symbol):
    """Get a recent closing price for a ticker to use as purchase price"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT close_price FROM PriceHistory
        WHERE ticker_symbol = %s
        ORDER BY date DESC
        LIMIT 1;
    """, (ticker_symbol,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        # Add some randomness (±10%) to simulate different purchase prices
        base_price = float(result[0])
        variation = random.uniform(0.9, 1.1)
        return round(base_price * variation, 2)
    else:
        # Default price if no price history exists
        return round(random.uniform(50, 500), 2)


def generate_holdings(portfolios, tickers):
    """Generate holdings for portfolios"""
    holdings = []

    print(f"→ Generating holdings for {len(portfolios)} portfolios...")

    for portfolio_id in tqdm(portfolios, desc="Generating holdings"):
        # Each portfolio gets 3-10 different holdings
        num_holdings = random.randint(3, 10)

        # Select random unique tickers for this portfolio
        selected_tickers = random.sample(tickers, min(num_holdings, len(tickers)))

        for ticker_symbol in selected_tickers:
            # Random quantity between 1 and 100 shares
            quantity = round(random.uniform(1, 100), 4)

            # Get a realistic purchase price based on actual data
            purchase_price = get_recent_price(ticker_symbol)

            # Random purchase date within the last 2 years
            days_ago = random.randint(1, 730)
            purchase_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')

            holdings.append((portfolio_id, ticker_symbol, quantity, purchase_price, purchase_date))

    print(f"✓ Generated {len(holdings)} holdings")
    return holdings


def insert_holdings(holdings):
    """Insert holdings into the database."""
    conn = get_conn()
    cursor = conn.cursor()

    sql = """
        INSERT INTO Holdings (portfolio_id, ticker_symbol, quantity, purchase_price, purchase_date)
        VALUES (%s, %s, %s, %s, %s);
    """

    try:
        for holding in tqdm(holdings, desc="Inserting holdings"):
            cursor.execute(sql, holding)
        conn.commit()
        print(f"✓ Successfully inserted {len(holdings)} holdings.")

        # Show sample of inserted holdings
        cursor.execute("""
            SELECT h.holding_id, h.ticker_symbol, t.company_name,
                   h.quantity, h.purchase_price, h.purchase_date,
                   p.portfolio_name
            FROM Holdings h
            JOIN Ticker t ON h.ticker_symbol = t.ticker_symbol
            JOIN Portfolio p ON h.portfolio_id = p.portfolio_id
            LIMIT 5;
        """)
        print("\nSample of inserted holdings:")
        for row in cursor.fetchall():
            total_value = float(row[3]) * float(row[4])
            print(f"  {row[1]} ({row[2]}) - {row[3]} shares @ ${row[4]} = ${total_value:.2f}")
            print(f"    Portfolio: {row[6]}, Purchased: {row[5]}")

        # Show statistics
        cursor.execute("""
            SELECT
                COUNT(*) as total_holdings,
                SUM(quantity * purchase_price) as total_investment,
                AVG(quantity * purchase_price) as avg_holding_value
            FROM Holdings;
        """)
        total, investment, avg = cursor.fetchone()
        print(f"\nStatistics:")
        print(f"  Total holdings: {total}")
        print(f"  Total investment value: ${float(investment):,.2f}")
        print(f"  Average holding value: ${float(avg):,.2f}")

        # Check AuditLog to verify trigger worked
        cursor.execute("""
            SELECT COUNT(*) FROM AuditLog
            WHERE table_name = 'Holdings' AND operation_type = 'INSERT';
        """)
        audit_count = cursor.fetchone()[0]
        print(f"\n✓ AuditLog entries created by trigger: {audit_count}")

    except Exception as e:
        conn.rollback()
        print(f"Database insert failed: {e}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    portfolios = get_portfolios()
    tickers = get_tickers()

    if not portfolios:
        print("No portfolios found in database. Please run insert_portfolios.py first.")
    elif not tickers:
        print("No tickers found in database. Please run insert_tickers.py first.")
    else:
        print(f"Found {len(portfolios)} portfolios and {len(tickers)} tickers.")
        holdings = generate_holdings(portfolios, tickers)
        insert_holdings(holdings)
