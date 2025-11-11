from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from dotenv import load_dotenv
from os import getenv

load_dotenv()

API_KEY = getenv("API_KEY")


def fetch_daily(symbol: str, days: int = 365) -> pd.DataFrame:
    ts = TimeSeries(key=API_KEY, output_format="pandas")
    data, meta_data = ts.get_daily(symbol=symbol, outputsize="full")

    # Sort newest first, trim to desired days
    data = data.sort_index(ascending=False)
    return data.head(days)
