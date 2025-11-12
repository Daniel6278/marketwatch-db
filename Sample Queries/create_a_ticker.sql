INSERT INTO Ticker (ticker_symbol, company_name, sector, industry, country)
VALUES ('TEST', 'Test Co', 'Utilities', 'Testing', 'USA');

SELECT EXISTS(
  SELECT 1 FROM Ticker WHERE ticker_symbol='TEST'
) AS exists_test;
