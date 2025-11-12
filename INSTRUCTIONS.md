# MarketWatch Database Project - Setup & Usage Guide

## Initial Setup

### 1. Clone the Repository
1. Accept GitHub invite
2. Generate local SSH key and add to GitHub SSH keys
3. Navigate to your projects folder and clone:
   ```bash
   git clone git@github.com:Daniel6278/marketwatch-db.git
   cd marketwatch-db
   ```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate environment (macOS/Linux)
source venv/bin/activate

# Activate environment (Windows)
venv\Scripts\activate

# Your terminal should now show (venv)
```

### 3. Install Dependencies
```bash
# Root level dependencies (for indicators & sample data scripts)
pip install -r requirements.txt

# Backend API dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### 4. Configure Database Connection
1. Copy `.env.example` to `.env`
2. Add your database credentials:
   ```
   DB_HOST=your-aws-endpoint
   DB_USER=admin
   DB_PASSWORD=your-password
   DB_NAME=marketwatch_db
   ```


## Running the Application

### Backend API (FastAPI)

```bash
# From project root
cd backend

# Run development server
uvicorn api.main:app --reload

# Or specify host and port
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

### Frontend (React + Vite)

```bash
# From project root
cd frontend

# Install dependencies (first time only)
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The frontend will be available at: http://localhost:5173 (default Vite port)

**Authorized Tables:**
- Alert
- User
- Ticker
- Portfolio
- PriceHistory
- Holdings
- AuditLog

## Technical Indicators

The `indicators` module provides technical analysis calculations that operate directly on database price data.

### MySQL Workbench Setup
1. Create a new Server Connection
2. **Hostname**: Your AWS endpoint
3. **Username**: admin
4. **Password**: From your `.env` file
5. Leave Default Schema blank
6. Test Connection to confirm

### Sample Data Scripts

Located in `Sample Data/` directory:

**Yahoo Finance (`yfinance/`)**:
- `fetch_tickers_csv.py` - Download ticker symbols
- `fetch_pricehistory_csv.py` - Download price history
- `insert_tickers.py` - Load tickers into database
- `insert_price_history.py` - Load price history into database
- `fake_users_csv.py` - Generate test user data

**Alpha Vantage (`alpha-vantage/`)**:
- `core/fetch_data.py` - Fetch data from Alpha Vantage API
- `core/load_data.py` - Load data into database
- `core/save_json.py` - Save API responses


