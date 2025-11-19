SELECT 
    t.ticker_symbol,
    t.company_name,
    ph.close_price AS last_price
FROM Ticker t
LEFT JOIN (
    SELECT ph1.ticker_symbol, ph1.close_price
    FROM PriceHistory ph1
    JOIN (
        SELECT ticker_symbol, MAX(PriceHistory.date) AS max_date
        FROM PriceHistory
        GROUP BY ticker_symbol
    ) latest
    ON ph1.ticker_symbol = latest.ticker_symbol
    AND ph1.date = latest.max_date
) ph ON ph.ticker_symbol = t.ticker_symbol
WHERE t.ticker_symbol LIKE "$(starts_with)d%"
ORDER BY t.ticker_symbol
LIMIT %(limit)d
OFFSET %(offset)d;