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

def bollinger(ticker, range=20):
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT date, close_price FROM PriceHistory WHERE ticker_symbol='{ticker}' ORDER BY date ASC;", conn)
    conn.close()


    df['MA'] = df['close_price'].rolling(window=range).mean()
    df['STD'] = df['close_price'].rolling(window=range).std()
    df['Upper'] = df['MA'] + (2 * df['STD'])
    df['Lower'] = df['MA'] - (2 * df['STD'])
    print(df.tail())
    return df[['date', 'MA', 'Upper', 'Lower']]