USE financial_dashboard;

-- Transfer valid complaints from raw table to final table with company_id mapping
INSERT INTO consumer_complaints (date_received, company_id, company, product, state)
SELECT
    raw.date_received,
    companies.company_id, -- Map company_id from companies table
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
