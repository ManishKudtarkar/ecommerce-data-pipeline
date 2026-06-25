-- Drop old analytics tables if they exist
DROP TABLE IF EXISTS daily_sales_summary;
DROP TABLE IF EXISTS country_sales_summary;
DROP TABLE IF EXISTS customer_revenue_summary;

-- =========================
-- Daily Sales Summary
-- =========================
CREATE TABLE daily_sales_summary AS
SELECT
    DATE(order_time) AS order_date,
    COUNT(order_id) AS total_orders,
    SUM(subtotal_usd) AS gross_sales_usd,
    SUM(total_usd) AS net_sales_usd,
    AVG(total_usd) AS avg_order_value_usd
FROM fact_orders
GROUP BY DATE(order_time)
ORDER BY order_date;

-- =========================
-- Country Sales Summary
-- =========================
CREATE TABLE country_sales_summary AS
SELECT
    country,
    COUNT(order_id) AS total_orders,
    SUM(total_usd) AS total_revenue_usd,
    AVG(total_usd) AS avg_order_value_usd
FROM fact_orders
GROUP BY country
ORDER BY total_revenue_usd DESC;

-- =========================
-- Customer Revenue Summary
-- =========================
CREATE TABLE customer_revenue_summary AS
SELECT
    c.customer_id,
    c.name,
    c.email,
    c.country,
    COUNT(f.order_id) AS total_orders,
    SUM(f.total_usd) AS total_spent_usd,
    AVG(f.total_usd) AS avg_order_value_usd
FROM fact_orders f
JOIN dim_customers c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.name,
    c.email,
    c.country
ORDER BY total_spent_usd DESC;