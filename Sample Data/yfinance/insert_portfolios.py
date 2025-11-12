import os
import pymysql
from faker import Faker
from dotenv import load_dotenv
from tqdm import tqdm
import random

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

# Portfolio name themes
PORTFOLIO_THEMES = [
    "Growth Portfolio",
    "Dividend Portfolio",
    "Tech Portfolio",
    "Retirement Fund",
    "Conservative Portfolio",
    "Aggressive Growth",
    "Value Investing",
    "Blue Chip Portfolio",
    "Swing Trading",
    "Long-term Holdings",
    "Income Portfolio",
    "Index Portfolio",
    "Small Cap Portfolio",
    "International Portfolio",
    "Sector Rotation Portfolio",
]


def get_conn():
    return pymysql.connect(**DB_CONFIG)


def get_users():
    """Fetch all user IDs from the database"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, first_name, last_name FROM User;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users


def generate_portfolios(users):
    """Generate portfolios for users"""
    fake = Faker()
    portfolios = []

    print(f"→ Generating portfolios for {len(users)} users...")

    for user_id, first_name, last_name in users:
        # Each user gets 1-3 portfolios
        num_portfolios = random.randint(1, 3)

        for i in range(num_portfolios):
            # Pick a unique portfolio name theme
            portfolio_name = random.choice(PORTFOLIO_THEMES)
            # Make it unique by adding user's name or number if needed
            if i > 0:
                portfolio_name = f"{first_name}'s {portfolio_name} {i+1}"
            else:
                portfolio_name = f"{first_name}'s {portfolio_name}"

            # Generate a description
            descriptions = [
                "Long-term investment strategy focused on steady growth.",
                "Diversified portfolio across multiple sectors.",
                "High-risk, high-reward investment approach.",
                "Conservative approach with stable dividend stocks.",
                "Technology sector focus for growth potential.",
                "Balanced mix of growth and value stocks.",
                "Income-generating portfolio with dividend stocks.",
                "Experimental portfolio for testing new strategies.",
            ]
            description = random.choice(descriptions)

            portfolios.append((user_id, portfolio_name, description))

    print(f"✓ Generated {len(portfolios)} portfolios")
    return portfolios


def insert_portfolios(portfolios):
    """Insert portfolios into the database."""
    conn = get_conn()
    cursor = conn.cursor()

    sql = """
        INSERT INTO Portfolio (user_id, portfolio_name, description)
        VALUES (%s, %s, %s);
    """

    try:
        for portfolio in tqdm(portfolios, desc="Inserting portfolios"):
            cursor.execute(sql, portfolio)
        conn.commit()
        print(f"✓ Successfully inserted {len(portfolios)} portfolios.")

        # Show sample of inserted portfolios
        cursor.execute("""
            SELECT p.portfolio_id, p.portfolio_name, u.email, p.description
            FROM Portfolio p
            JOIN User u ON p.user_id = u.user_id
            LIMIT 5;
        """)
        print("\nSample of inserted portfolios:")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, Name: {row[1]}, User: {row[2]}")

        # Show portfolio count per user
        cursor.execute("""
            SELECT COUNT(*) as total_portfolios,
                   AVG(portfolio_count) as avg_per_user
            FROM (
                SELECT user_id, COUNT(*) as portfolio_count
                FROM Portfolio
                GROUP BY user_id
            ) as counts;
        """)
        total, avg = cursor.fetchone()
        print(f"\nTotal portfolios: {total}, Average per user: {avg:.2f}")

    except Exception as e:
        conn.rollback()
        print(f"Database insert failed: {e}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    users = get_users()
    if not users:
        print("No users found in database. Please run insert_users.py first.")
    else:
        portfolios = generate_portfolios(users)
        insert_portfolios(portfolios)
