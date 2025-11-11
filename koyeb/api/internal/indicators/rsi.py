import pandas as pd
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def rsi(ticker: str, range: int = 14) -> pd.DataFrame:
    conn = get_db_connection()
    query = f"""
        SELECT date, close_price
        FROM PriceHistory
        WHERE ticker_symbol = '{ticker}'
        ORDER BY date ASC;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # Ensure close_price is numeric (avoid dtype issues)
    df["close_price"] = pd.to_numeric(df["close_price"], errors="coerce")
    df = df.dropna(subset=["close_price"])

    # Compute RSI
    delta = df["close_price"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=range, min_periods=1).mean()
    avg_loss = loss.rolling(window=range, min_periods=1).mean()

    rs = avg_gain / avg_loss.replace(0, pd.NA)
    df["RSI"] = 100 - (100 / (1 + rs))

    print(df.tail())
    return df[["date", "RSI"]]
