DROP PROCEDURE IF EXISTS sp_GetUserPortfolioDetails;
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