USE financial_dashboard;

-- Transfer valid complaints from raw table to final table with ticker mapping
INSERT INTO consumer_complaints (date_received, ticker, company, product, state)
SELECT
    raw.date_received,
    companies.ticker,  -- Map ticker from companies table
    raw.company,
    raw.product,
    raw.state
FROM
    consumer_complaints_raw AS raw
LEFT JOIN
    companies ON raw.company LIKE CONCAT('%', companies.name, '%') -- Use partial matching for company names
ON DUPLICATE KEY UPDATE
    product = VALUES(product),
    state = VALUES(state);
