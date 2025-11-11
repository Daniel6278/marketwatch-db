import os
import pymysql
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
import time

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'main-marketwatch-db.c74uqiecyemg.us-east-2.rds.amazonaws.com'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'portfolio_db')
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def get_tickers():
    conn = get_connection()
    df = pd.read_sql("SELECT ticker_symbol FROM Ticker;", conn)
    conn.close()
    return df['ticker_symbol'].tolist()

def fetch_hourly_data(ticker):
    """Fetch 1 year of hourly price data for a given ticker safely."""
    try:
        data = yf.download(ticker, period='1y', interval='1h', progress=False, auto_adjust=False)
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return pd.DataFrame()

    if data.empty:
        print(f"No data returned for {ticker}")
        return pd.DataFrame()

    # Flatten multi-index columns if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    # Rename and clean
    rename_map = {
        "Open": "open_price",
        "High": "high_price",
        "Low": "low_price",
        "Close": "close_price",
        "Volume": "volume"
    }
    for old_col in rename_map:
        if old_col not in data.columns:
            print(f"Skipping {ticker}: missing '{old_col}' column")
            return pd.DataFrame()

    data = data.reset_index().rename(columns=rename_map)
    data = data.dropna(subset=["open_price", "high_price", "low_price", "close_price", "volume"])
    data = data[data["volume"] > 0]
    data["ticker_symbol"] = ticker

    return data[["ticker_symbol", "Datetime", "open_price", "high_price", "low_price", "close_price", "volume"]].rename(columns={"Datetime": "date"})



def insert_price_history(df):
    if df.empty:
        return

    #Replace NaNs with None for MySQL
    df = df.replace({pd.NA: None, float("nan"): None})

    conn = get_connection()
    cursor = conn.cursor()
    sql = """
          INSERT INTO PriceHistory (ticker_symbol, date, open_price, high_price, low_price, close_price, volume)
          VALUES (%s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE
                                   open_price = VALUES(open_price),
                                   high_price = VALUES(high_price),
                                   low_price = VALUES(low_price),
                                   close_price = VALUES(close_price),
                                   volume = VALUES(volume); \
          """
    try:
        cursor.executemany(sql, df.values.tolist())
        conn.commit()
    except Exception as e:
        print(f"Insert error for {df['ticker_symbol'].iloc[0]}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    tickers = get_tickers()
    print(f"Fetching hourly data for {len(tickers)} tickers (1 year)\n")

    for ticker in tqdm(tickers):
        df = fetch_hourly_data(ticker)
        if not df.empty:
            insert_price_history(df)
        time.sleep(1)  #Prevent Yahoo rate limiting

    print("\nPrice history insertion completed successfully.")
