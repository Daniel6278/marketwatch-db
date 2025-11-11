import os
import pandas as pd
from core.fetch_data import fetch_daily
from datetime import datetime, timedelta


def load_or_update(symbol: str, folder="data", days: int = 365) -> pd.DataFrame:
    """
    Load existing JSON for a ticker if it exists.
    Fetch only new data from API and merge with old.
    Always trim to the last N days (default 365).
    """
    filename = os.path.join(folder, f"{symbol}.json")

    if os.path.exists(filename):
        # Load old data
        old_df = pd.read_json(filename)
        old_df.index = pd.to_datetime(old_df.index)
        old_df = old_df.sort_index()

        # Get the last stored date
        last_date = old_df.index.max()

        # Fetch new data from API
        new_df = fetch_daily(symbol, days=days * 2)  # extra buffer
        new_df.index = pd.to_datetime(new_df.index)
        new_df = new_df.sort_index()

        # Keep only rows newer than last_date
        new_df = new_df[new_df.index > last_date]

        if not new_df.empty:
            updated_df = pd.concat([old_df, new_df]).sort_index()
            print(f"[INFO] Updated {symbol} with {len(new_df)} new rows.")
        else:
            updated_df = old_df
            print(f"[INFO] {symbol} already up-to-date.")
    else:
        # No file exists → fetch full data
        updated_df = fetch_daily(symbol, days=days)
        updated_df.index = pd.to_datetime(updated_df.index)
        os.makedirs(folder, exist_ok=True)
        print(f"[INFO] Created new dataset for {symbol} with {len(updated_df)} rows.")

    # Trim to past N days
    cutoff = datetime.now() - timedelta(days=days)
    trimmed_df = updated_df[updated_df.index >= cutoff].sort_index()

    # Save trimmed dataset
    trimmed_df.to_json(filename, orient="records", date_format="iso")

    # Report coverage + latest price
    latest_date = trimmed_df.index.max().date()
    latest_price = trimmed_df["4. close"].iloc[-1]
    print(f"[INFO] {symbol} covers {trimmed_df.index.min().date()} → {latest_date}")
    print(f"[INFO] Most recent close: ${round(latest_price, 2)} on {latest_date}")

    return trimmed_df
