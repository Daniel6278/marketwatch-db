# Technical Indicators Integration Guide

This document describes how to use the `indicators` package within the MarketWatch Database project. It is intended for GUI developers integrating live technical indicator analytics into visual interfaces.

---

## 1. Overview

The `indicators` module provides multiple technical indicators that operate directly on price data stored in the database. Each indicator automatically connects to the MySQL instance defined in your `.env` file and returns a pandas `DataFrame` ready for visualization.

**Usage:**

```python
from indicators import *
```

or individually:

```python
from indicators import rsi, macd, bollinger, moving_avg, atr, stochastic
```

---

## 2. Available Indicators

| Indicator | Example Call | Description |
|------------|--------------|--------------|
| **RSI** | `rsi("AAPL", period=14)` | Relative Strength Index |
| **MACD** | `macd("AAPL", fast=12, slow=26, signal=9)` | Moving Average Convergence Divergence |
| **Bollinger Bands** | `bollinger("AAPL", window=20, num_std=2)` | Upper and lower bands around SMA |
| **Moving Average** | `moving_avg("AAPL", window=20)` | Simple Moving Average |
| **ATR** | `atr("AAPL", period=14)` | Average True Range (volatility) |
| **Stochastic** | `stochastic("AAPL", k_period=14, d_period=3)` | Stochastic Oscillator |

---

## 3. Workflow

Each indicator function:

1. Connects to the MySQL database using environment credentials.
2. Queries the `PriceHistory` table for historical OHLCV data.
3. Computes the selected technical indicator.
4. Returns a pandas `DataFrame` suitable for plotting or merging with GUI data.

Example RSI output:

| date | ticker_symbol | close_price | rsi |
|------|----------------|--------------|------|
| 2025-10-25 15:00 | AAPL | 272.3 | 48.29 |
| 2025-10-25 16:00 | AAPL | 273.1 | 51.02 |
| 2025-10-25 17:00 | AAPL | 273.9 | 54.13 |

---

## 4. GUI Integration Notes

- Each function returns a DataFrame with a `date` column, ideal for x-axis plotting.
- Functions are synchronous; run them in background threads in a live UI.
- No API calls or external data are used; all queries come from the local database.
- Ensure the DB has been populated using:
  - `insert_tickers.py`
  - `insert_price_history.py`

---

## 5. Example Usage

```python
from indicators import *

# RSI for AAPL
rsi_df = rsi("AAPL", period=14)
print(rsi_df.tail())

# MACD for Microsoft
macd_df = macd("MSFT")

# Bollinger Bands for NVDA
bb_df = bollinger("NVDA")
```

All results are pandas DataFrames and ready for integration with charting libraries such as Matplotlib, Plotly, or PyQtGraph.

---

## 6. Extending the Indicators

To add a new indicator:

1. Create a new file in `/indicators/` (e.g., `ema.py`).
2. Define a function like this:

```python
def ema(ticker: str, window: int = 20):
    # connect to DB
    # query PriceHistory
    # compute EMA
    return df
```

3. Register it in `indicators/__init__.py`:

```python
from .ema import ema
```

---

## 7. Dependencies

Listed in `requirements.txt`:

```
pandas
pymysql
yfinance
tqdm
python-dotenv
```

---

## 8. Project Structure

```
marketwatch-db/
├── indicators/
│   ├── __init__.py
│   ├── atr.py
│   ├── bollinger.py
│   ├── macd.py
│   ├── moving_avg.py
│   ├── rsi.py
│   └── stochastic.py
├── insert_tickers.py
├── insert_price_history.py
├── create_tables.py
└── README.md
```

---

## 9. Summary

- Import all indicators with `from indicators import *`
- Each function connects to the DB and returns ready-to-plot data.
- Designed for seamless GUI analytics integration.