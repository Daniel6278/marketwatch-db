#!/usr/bin/env python3
"""Check database storage size"""

import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "marketwatchDB"),
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# Get size of each table
cursor.execute("""
    SELECT
        table_name AS 'Table',
        ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)',
        table_rows AS 'Rows'
    FROM information_schema.TABLES
    WHERE table_schema = %s
    ORDER BY (data_length + index_length) DESC;
""", (DB_CONFIG["database"],))

print("=" * 60)
print("DATABASE STORAGE BREAKDOWN")
print("=" * 60)
print(f"{'Table':<20} {'Size (MB)':<12} {'Rows':<12}")
print("-" * 60)

total_size = 0
for table, size, rows in cursor.fetchall():
    total_size += size
    print(f"{table:<20} {size:>10.2f} MB {rows:>10}")

print("-" * 60)
print(f"{'TOTAL':<20} {total_size:>10.2f} MB")
print("=" * 60)

# Get total database size
cursor.execute("""
    SELECT
        SUM(ROUND(((data_length + index_length) / 1024 / 1024), 2)) AS 'Total Size (MB)'
    FROM information_schema.TABLES
    WHERE table_schema = %s;
""", (DB_CONFIG["database"],))

db_size = cursor.fetchone()[0]
print(f"\nTotal Database Size: {db_size:.2f} MB ({db_size/1024:.3f} GB)")

cursor.close()
conn.close()
