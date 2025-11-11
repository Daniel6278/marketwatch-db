import os
import pandas as pd
import pymysql
from dotenv import load_dotenv

# Shared DB connection helper
def get_db_connection():
    load_dotenv()
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
)

def atr(ticker, range=14):
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT date, high_price, low_price, close_price FROM PriceHistory WHERE ticker_symbol='{ticker}' ORDER BY date ASC;", conn)
    conn.close()


    df['H-L'] = df['high_price'] - df['low_price']
    df['H-PC'] = abs(df['high_price'] - df['close_price'].shift(1))
    df['L-PC'] = abs(df['low_price'] - df['close_price'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=range).mean()
    print(df.tail())