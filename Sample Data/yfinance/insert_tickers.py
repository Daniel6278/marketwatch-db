from io import StringIO
import os
import requests
import pandas as pd
import pymysql
from dotenv import load_dotenv
from tqdm import tqdm

# === Load environment variables ===
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'main-marketwatch-db.c74uqiecyemg.us-east-2.rds.amazonaws.com'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE', 'portfolio_db')
}


def get_conn():
    return pymysql.connect(**DB_CONFIG)


def get_sp500_tickers():
    print("→ Fetching S&P 500 tickers from Wikipedia...")

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    html_data = StringIO(response.text)
    tables = pd.read_html(html_data)

    # --- pick the right table (it always has a 'Symbol' or 'Security' column) ---
    sp500_table = None
    for t in tables:
        cols = [str(c).lower() for c in t.columns]
        if any("symbol" in c for c in cols) and any("security" in c or "company" in c for c in cols):
            sp500_table = t
            break

    if sp500_table is None:
        raise ValueError(f"Could not locate the S&P 500 table. Found {len(tables)} tables total.")

    table = sp500_table
    table.columns = [str(c).strip().lower() for c in table.columns]

    print("Detected columns:", table.columns.tolist())

    symbol_col = next((c for c in table.columns if "symbol" in c), None)
    name_col = next((c for c in table.columns if "security" in c or "company" in c), None)
    sector_col = next((c for c in table.columns if "gics" in c and "sector" in c), None)
    industry_col = next((c for c in table.columns if "sub" in c or "industry" in c), None)
    hq_col = next((c for c in table.columns if "headquarters" in c or "location" in c), None)

    cols = [symbol_col, name_col, sector_col, industry_col, hq_col]
    if any(c is None for c in cols):
        raise ValueError(f"Missing expected columns. Found: {table.columns.tolist()}")

    df = table[[symbol_col, name_col, sector_col, industry_col, hq_col]]
    df.columns = ["ticker_symbol", "company_name", "sector", "industry", "country"]

    df["ticker_symbol"] = df["ticker_symbol"].str.replace('.', '-', regex=False)
    df["country"] = df["country"].apply(
        lambda x: x.split(",")[-1].strip() if isinstance(x, str) else "United States"
    )

    print(f"✓ Retrieved {len(df)} tickers")
    print(df.head(5).to_string(index=False))
    return df


def insert_tickers(df):
    """Insert or update tickers in the database."""
    conn = get_conn()
    cursor = conn.cursor()

    sql = """
          INSERT INTO Ticker (ticker_symbol, company_name, sector, industry, country)
          VALUES (%s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE
                                   company_name = VALUES(company_name),
                                   sector = VALUES(sector),
                                   industry = VALUES(industry),
                                   country = VALUES(country); \
          """

    try:
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Inserting tickers"):
            cursor.execute(sql, tuple(row))
        conn.commit()
        print(f"Successfully inserted or updated {len(df)} tickers.")
    except Exception as e:
        conn.rollback()
        print(f"Database insert failed: {e}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    tickers_df = get_sp500_tickers()
    insert_tickers(tickers_df)
