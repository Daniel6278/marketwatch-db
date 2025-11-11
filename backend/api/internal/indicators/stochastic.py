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

def stochastic(ticker, range=14):
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT date, high_price, low_price, close_price FROM PriceHistory WHERE ticker_symbol='{ticker}' ORDER BY date ASC;", conn)
    conn.close()


    df['L14'] = df['low_price'].rolling(window=range).min()
    df['H14'] = df['high_price'].rolling(window=range).max()
    df['%K'] = (df['close_price'] - df['L14']) / (df['H14'] - df['L14']) * 100
    df['%D'] = df['%K'].rolling(window=3).mean()
    print(df.tail())
    return df[['date', '%K', '%D']]