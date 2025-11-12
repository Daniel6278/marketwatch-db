import os
import pymysql
from faker import Faker
from hashlib import sha256
import base64
from dotenv import load_dotenv
from tqdm import tqdm

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

# Number of fake users to generate
N_USERS = 20


def get_conn():
    return pymysql.connect(**DB_CONFIG)


def generate_users(n):
    """Generate fake user data"""
    fake = Faker()
    users = []

    print(f"→ Generating {n} fake users...")

    for _ in range(n):
        email = fake.email()
        # Generate a password hash (using SHA256 + base64 encoding)
        password_hash = base64.b64encode(
            sha256(fake.password().encode("utf-8")).digest()
        ).decode("utf-8")
        first_name = fake.first_name()
        last_name = fake.last_name()

        users.append((email, password_hash, first_name, last_name))

    print(f"✓ Generated {len(users)} users")
    return users


def insert_users(users):
    """Insert users into the database."""
    conn = get_conn()
    cursor = conn.cursor()

    sql = """
        INSERT INTO User (email, password_hash, first_name, last_name)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            password_hash = VALUES(password_hash),
            first_name = VALUES(first_name),
            last_name = VALUES(last_name);
    """

    try:
        for user in tqdm(users, desc="Inserting users"):
            cursor.execute(sql, user)
        conn.commit()
        print(f"✓ Successfully inserted {len(users)} users.")

        # Show sample of inserted users
        cursor.execute("SELECT user_id, email, first_name, last_name FROM User LIMIT 5;")
        print("\nSample of inserted users:")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, Email: {row[1]}, Name: {row[2]} {row[3]}")

    except Exception as e:
        conn.rollback()
        print(f"Database insert failed: {e}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    users = generate_users(N_USERS)
    insert_users(users)
