DROP TRIGGER IF EXISTS trg_after_holdings_insert;

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