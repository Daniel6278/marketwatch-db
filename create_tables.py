"""
Portfolio Management Database - Table Creation Script
Creates all tables, triggers, and stored procedures in the marketwatchDB
Does not load any data - only creates the schema
"""

import pymysql
import os
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Database connection configuration
DB_CONFIG = {
    "host": os.getenv(
        "DB_HOST", "main-marketwatch-db.c74uqiecyemg.us-east-2.rds.amazonaws.com"
    ),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "portfolio_db"),
}


def get_connection():
    """Establish database connection"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print(f"✓ Connected to database: {DB_CONFIG['database']}")
        return connection
    except Exception as e:
        print(f"✗ Error connecting to database: {e}")
        sys.exit(1)


def drop_existing_tables(cursor):
    """Drop existing tables if they exist (for clean re-runs)"""
    print("\nDropping existing tables if they exist...")

    drop_statements = [
        "DROP TABLE IF EXISTS AuditLog",
        "DROP TABLE IF EXISTS Alert",
        "DROP TABLE IF EXISTS Holdings",
        "DROP TABLE IF EXISTS PriceHistory",
        "DROP TABLE IF EXISTS Portfolio",
        "DROP TABLE IF EXISTS Ticker",
        "DROP TABLE IF EXISTS User",
    ]

    for statement in drop_statements:
        cursor.execute(statement)
        print(f"  ✓ {statement}")


def create_user_table(cursor):
    """Create User table"""
    print("\nCreating User table...")

    sql = """
    CREATE TABLE User (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(60) NOT NULL,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_email (email)
    ) ENGINE=InnoDB
    """

    cursor.execute(sql)
    print("  ✓ User table created")


def create_ticker_table(cursor):
    """Create Ticker table"""
    print("\nCreating Ticker table...")

    sql = """
    CREATE TABLE Ticker (
        ticker_symbol VARCHAR(10) PRIMARY KEY,
        company_name VARCHAR(255) NOT NULL,
        sector VARCHAR(100),
        industry VARCHAR(100),
        country VARCHAR(100),
        INDEX idx_company_name (company_name)
    ) ENGINE=InnoDB
    """

    cursor.execute(sql)
    print("  ✓ Ticker table created")


def create_price_history_table(cursor):
    """Create PriceHistory table"""
    print("\nCreating PriceHistory table...")

    sql = """
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
        CONSTRAINT chk_volume_positive CHECK (volume > 0),
        CONSTRAINT chk_low_not_greater_than_high CHECK (low_price <= high_price),

        INDEX idx_ticker_date (ticker_symbol, date),
        INDEX idx_date (date)
    ) ENGINE=InnoDB
    """

    cursor.execute(sql)
    print("  ✓ PriceHistory table created")


def create_portfolio_table(cursor):
    """Create Portfolio table"""
    print("\nCreating Portfolio table...")

    sql = """
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
    ) ENGINE=InnoDB
    """

    cursor.execute(sql)
    print("  ✓ Portfolio table created")


def create_holdings_table(cursor):
    """Create Holdings table"""
    print("\nCreating Holdings table...")

    sql = """
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
    ) ENGINE=InnoDB
    """

    cursor.execute(sql)
    print("  ✓ Holdings table created")


def create_alert_table(cursor):
    """Create Alert table"""
    print("\nCreating Alert table...")

    sql = """
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
            ON DELETE RESTRICT,

        CONSTRAINT fk_alert_ticker
            FOREIGN KEY (ticker_symbol)
            REFERENCES Ticker(ticker_symbol)
            ON DELETE RESTRICT,

        CONSTRAINT chk_target_price_positive CHECK (target_price > 0),

        INDEX idx_user_id (user_id),
        INDEX idx_ticker_symbol (ticker_symbol),
        INDEX idx_active_alerts (is_active)
    ) ENGINE=InnoDB
    """

    cursor.execute(sql)
    print("  ✓ Alert table created")


def create_audit_log_table(cursor):
    """Create AuditLog table"""
    print("\nCreating AuditLog table...")

    sql = """
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
    ) ENGINE=InnoDB
    """

    cursor.execute(sql)
    print("  ✓ AuditLog table created")


def create_holdings_trigger(cursor):
    """Create trigger for Holdings table audit logging"""
    print("\nCreating Holdings audit trigger...")

    # Drop trigger if it exists
    cursor.execute("DROP TRIGGER IF EXISTS trg_after_holdings_insert")

    sql = """
    CREATE TRIGGER trg_after_holdings_insert
    AFTER INSERT ON Holdings
    FOR EACH ROW
    BEGIN
        DECLARE v_user_id INT;

        SELECT user_id INTO v_user_id
        FROM Portfolio
        WHERE portfolio_id = NEW.portfolio_id;

        INSERT INTO AuditLog (
            table_name,
            operation_type,
            record_id,
            ticker_symbol,
            quantity,
            purchase_price,
            user_id,
            timestamp
        ) VALUES (
            'Holdings',
            'INSERT',
            NEW.holding_id,
            NEW.ticker_symbol,
            NEW.quantity,
            NEW.purchase_price,
            v_user_id,
            CURRENT_TIMESTAMP
        );
    END
    """

    cursor.execute(sql)
    print("  ✓ Holdings audit trigger created")


def create_stored_procedure(cursor):
    """Create stored procedure for user portfolio details"""
    print("\nCreating stored procedure...")

    # Drop procedure if it exists
    cursor.execute("DROP PROCEDURE IF EXISTS sp_GetUserPortfolioDetails")

    sql = """
    CREATE PROCEDURE sp_GetUserPortfolioDetails(
        IN p_user_id INT
    )
    BEGIN
        SELECT
            u.user_id,
            u.email,
            CONCAT(u.first_name, ' ', u.last_name) AS full_name,
            p.portfolio_id,
            p.portfolio_name,
            p.description AS portfolio_description,
            h.holding_id,
            h.ticker_symbol,
            t.company_name,
            t.sector,
            t.industry,
            h.quantity,
            h.purchase_price,
            h.purchase_date,
            (h.quantity * h.purchase_price) AS total_investment_value,
            p.created_at AS portfolio_created_at
        FROM User u
        INNER JOIN Portfolio p ON u.user_id = p.user_id
        INNER JOIN Holdings h ON p.portfolio_id = h.portfolio_id
        INNER JOIN Ticker t ON h.ticker_symbol = t.ticker_symbol
        WHERE u.user_id = p_user_id
        ORDER BY p.portfolio_name, h.ticker_symbol;

        SELECT
            COUNT(DISTINCT p.portfolio_id) AS total_portfolios,
            COUNT(h.holding_id) AS total_holdings,
            SUM(h.quantity * h.purchase_price) AS total_portfolio_value
        FROM Portfolio p
        LEFT JOIN Holdings h ON p.portfolio_id = h.portfolio_id
        WHERE p.user_id = p_user_id;
    END
    """

    cursor.execute(sql)
    print("  ✓ Stored procedure sp_GetUserPortfolioDetails created")


def verify_tables(cursor):
    """Verify all tables were created successfully"""
    print("\nVerifying tables...")

    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]

    expected_tables = [
        "User",
        "Ticker",
        "PriceHistory",
        "Portfolio",
        "Holdings",
        "Alert",
        "AuditLog",
    ]

    print(f"\nTables created: {len(tables)}")
    for table in tables:
        print(f"  ✓ {table}")

    missing_tables = set(expected_tables) - set(tables)
    if missing_tables:
        print(f"\n✗ Missing tables: {missing_tables}")
        return False

    return True


def main():
    """Main execution function"""
    print("=" * 70)
    print("Portfolio Management Database - Table Creation Script")
    print("=" * 70)

    # Check if password is set
    if not DB_CONFIG["password"]:
        print("\n✗ Error: DB_PASSWORD environment variable is not set")
        print("  Please create a .env file with DB_PASSWORD=your_password")
        sys.exit(1)

    # Connect to database
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Drop existing tables
        drop_existing_tables(cursor)
        connection.commit()

        # Create tables in dependency order
        create_user_table(cursor)
        create_ticker_table(cursor)
        create_price_history_table(cursor)
        create_portfolio_table(cursor)
        create_holdings_table(cursor)
        create_alert_table(cursor)
        create_audit_log_table(cursor)
        connection.commit()

        # Create trigger and stored procedure
        create_holdings_trigger(cursor)
        create_stored_procedure(cursor)
        connection.commit()

        # Verify tables
        if verify_tables(cursor):
            print("\n" + "=" * 70)
            print(
                "✓ SUCCESS: All tables, triggers, and procedures created successfully!"
            )
            print("=" * 70)
        else:
            print("\n✗ ERROR: Some tables are missing")
            sys.exit(1)

    except Exception as e:
        connection.rollback()
        print(f"\n✗ Error during table creation: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        connection.close()
        print("\nDatabase connection closed")


if __name__ == "__main__":
    main()
