# Data Population Scripts

This directory contains scripts to populate all tables in the MarketWatch database with sample data.

## Prerequisites

1. Ensure your `.env` file is configured with database credentials
2. Install required packages: `pip install -r requirements.txt`
3. Ensure database tables are created (run database setup first)

## Execution Order

The scripts must be run in the following order due to foreign key dependencies:

### 1. Tickers (Foundation Data)
```bash
python insert_tickers.py
```
- Fetches S&P 500 ticker symbols from Wikipedia
- Populates the `Ticker` table with company information
- **Required for**: Price History, Holdings, Alerts

### 2. Price History
```bash
python insert_price_history.py
```
- Downloads 1 year of hourly price data from Yahoo Finance
- Populates the `PriceHistory` table with OHLCV data
- **Required for**: Technical indicators, realistic purchase prices
- **Note**: This can take 5-15 minutes depending on number of tickers

### 3. Users
```bash
python insert_users.py
```
- Generates fake user accounts with hashed passwords
- Populates the `User` table
- **Default**: Creates 20 users (configurable via `N_USERS` variable)
- **Required for**: Portfolios, Alerts

### 4. Portfolios
```bash
python insert_portfolios.py
```
- Creates 1-3 portfolios per user
- Populates the `Portfolio` table
- Each portfolio gets a unique name and description
- **Required for**: Holdings

### 5. Holdings
```bash
python insert_holdings.py
```
- Creates 3-10 stock holdings per portfolio
- Populates the `Holdings` table
- Uses realistic purchase prices based on price history
- **Triggers**: Automatically creates `AuditLog` entries via database trigger

### 6. Alerts
```bash
python insert_alerts.py
```
- Creates 2-8 price alerts per user
- Populates the `Alert` table
- 70% of alerts are for stocks users already hold
- Mix of active/inactive alerts, some triggered

## Quick Start - Run All Scripts

To populate the entire database in sequence:

```bash
# Navigate to the yfinance directory
cd "Sample Data/yfinance"

# Run scripts in order
python insert_tickers.py
python insert_price_history.py  # This takes the longest
python insert_users.py
python insert_portfolios.py
python insert_holdings.py
python insert_alerts.py
```

## Data Generation Summary

After running all scripts, you will have:

| Table | Approximate Records |
|-------|---------------------|
| Ticker | ~500 (S&P 500 companies) |
| PriceHistory | ~1-2 million (500 tickers × ~365 days × 24 hours) |
| User | 20 (configurable) |
| Portfolio | 30-60 (1-3 per user) |
| Holdings | 150-600 (3-10 per portfolio) |
| Alert | 40-160 (2-8 per user) |
| AuditLog | Same as Holdings (auto-generated) |

## Customization

### Adjust Number of Users
Edit `insert_users.py`:
```python
N_USERS = 50  # Change from default 20
```

### Adjust Holdings per Portfolio
Edit `insert_holdings.py`:
```python
num_holdings = random.randint(5, 15)  # Change from default 3-10
```

### Adjust Alerts per User
Edit `insert_alerts.py`:
```python
num_alerts = random.randint(5, 15)  # Change from default 2-8
```

## Verification

After running scripts, verify data with these queries:

```sql
-- Check all table counts
SELECT 'Users' as Table, COUNT(*) as Count FROM User
UNION ALL
SELECT 'Tickers', COUNT(*) FROM Ticker
UNION ALL
SELECT 'Portfolios', COUNT(*) FROM Portfolio
UNION ALL
SELECT 'Holdings', COUNT(*) FROM Holdings
UNION ALL
SELECT 'Alerts', COUNT(*) FROM Alert
UNION ALL
SELECT 'PriceHistory', COUNT(*) FROM PriceHistory
UNION ALL
SELECT 'AuditLog', COUNT(*) FROM AuditLog;
```

## Troubleshooting

### "No users found" error
- Run `insert_users.py` first

### "No tickers found" error
- Run `insert_tickers.py` first

### "No portfolios found" error
- Run `insert_portfolios.py` after creating users

### Connection errors
- Verify `.env` file has correct database credentials
- Check database server is accessible
- Ensure database name matches (default: `marketwatchDB`)

### Duplicate key errors
- Scripts use `ON DUPLICATE KEY UPDATE` where applicable
- Safe to re-run most scripts (will update existing records)
- Holdings and Alerts will create duplicates if re-run

## Resetting Data

To clear all data and start fresh:

```bash
# From backend directory
cd backend
python -c "from api.internal.setup_db import setup_db; setup_db()"
```

**Warning**: This will drop all tables and recreate them empty.
