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

def macd(ticker):
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT date, close_price FROM PriceHistory WHERE ticker_symbol='{ticker}' ORDER BY date ASC;", conn)
    conn.close()


    df['EMA12'] = df['close_price'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['close_price'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    print(df.tail())
    return df[['date', 'MACD', 'Signal']]