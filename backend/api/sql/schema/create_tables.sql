-- Create User Table
CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(60) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- Create Ticker Table
CREATE TABLE Ticker (
    ticker_symbol VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    industry VARCHAR(100),
    country VARCHAR(100),
    INDEX idx_company_name (company_name)
);

-- Create PriceHistory Table
CREATE TABLE PriceHistory (
    price_history_id INT AUTO_INCREMENT PRIMARY KEY,
    ticker_symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open_price DECIMAL(19, 4) NOT NULL,
    high_price DECIMAL(19, 4) NOT NULL,
    low_price DECIMAL(19, 4) NOT NULL,
    close_price DECIMAL(19, 4) NOT NULL,
    volume BIGINT NOT NULL,

    UNIQUE KEY unique_ticker_date (ticker_symbol, date),

    CONSTRAINT fk_pricehistory_ticker
        FOREIGN KEY (ticker_symbol)
        REFERENCES Ticker(ticker_symbol)
        ON DELETE RESTRICT,

    CONSTRAINT chk_open_price_positive CHECK (open_price > 0),
    CONSTRAINT chk_high_price_positive CHECK (high_price > 0),
    CONSTRAINT chk_low_price_positive CHECK (low_price > 0),
    CONSTRAINT chk_close_price_positive CHECK (close_price > 0),
    CONSTRAINT chk_volume_0_or_positive CHECK (volume >= 0),
    CONSTRAINT chk_low_not_greater_than_high CHECK (low_price <= high_price),

    INDEX idx_ticker_date (ticker_symbol, date),
    INDEX idx_date (date)
);

-- Create Table Portfolio
CREATE TABLE Portfolio (
    portfolio_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    portfolio_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_portfolio_user
        FOREIGN KEY (user_id)
        REFERENCES User(user_id)
        ON DELETE RESTRICT,

    INDEX idx_user_id (user_id)
);

--- Create Holdings Table
CREATE TABLE Holdings (
    holding_id INT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id INT NOT NULL,
    ticker_symbol VARCHAR(10) NOT NULL,
    quantity DECIMAL(10, 4) NOT NULL,
    purchase_price DECIMAL(19, 4) NOT NULL,
    purchase_date DATE NOT NULL,

    CONSTRAINT fk_holdings_portfolio
        FOREIGN KEY (portfolio_id)
        REFERENCES Portfolio(portfolio_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_holdings_ticker
        FOREIGN KEY (ticker_symbol)
        REFERENCES Ticker(ticker_symbol)
        ON DELETE RESTRICT,

    CONSTRAINT chk_quantity_positive CHECK (quantity > 0),
    CONSTRAINT chk_purchase_price_positive CHECK (purchase_price > 0),

    INDEX idx_portfolio_id (portfolio_id),
    INDEX idx_ticker_symbol (ticker_symbol)
);

-- Create Alerts Table
CREATE TABLE Alert (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ticker_symbol VARCHAR(10) NOT NULL,
    alert_type ENUM('ABOVE', 'BELOW') NOT NULL,
    target_price DECIMAL(19, 4) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    triggered_at TIMESTAMP NULL,

    CONSTRAINT fk_alert_user
        FOREIGN KEY (user_id)
        REFERENCES User(user_id)
        ON DELETE CASCASE,

    CONSTRAINT fk_alert_ticker
        FOREIGN KEY (ticker_symbol)
        REFERENCES Ticker(ticker_symbol)
        ON DELETE CASCASE,

    CONSTRAINT chk_target_price_positive CHECK (target_price > 0),

    INDEX idx_user_id (user_id),
    INDEX idx_ticker_symbol (ticker_symbol),
    INDEX idx_active_alerts (is_active)
);

-- Create AuditLog Table
CREATE TABLE AuditLog (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation_type VARCHAR(20) NOT NULL,
    record_id INT NOT NULL,
    ticker_symbol VARCHAR(10),
    quantity DECIMAL(10, 4),
    purchase_price DECIMAL(19, 4),
    user_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_table_operation (table_name, operation_type),
    INDEX idx_timestamp (timestamp)
);