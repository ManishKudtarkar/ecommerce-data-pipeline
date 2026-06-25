-- Clear warehouse tables before loading
TRUNCATE TABLE fact_orders RESTART IDENTITY;
TRUNCATE TABLE dim_products RESTART IDENTITY;
TRUNCATE TABLE dim_customers RESTART IDENTITY;

-- =========================
-- Load dim_customers
-- =========================
INSERT INTO dim_customers (
    customer_id,
    name,
    email,
    country,
    age,
    signup_date,
    marketing_opt_in
)
SELECT
    customer_id,
    name,
    email,
    country,
    age,
    signup_date,
    marketing_opt_in
FROM stg_customers;

-- =========================
-- Load dim_products
-- =========================
INSERT INTO dim_products (
    product_id,
    category,
    name,
    price_usd,
    cost_usd,
    margin_usd
)
SELECT
    product_id,
    category,
    name,
    price_usd,
    cost_usd,
    margin_usd
FROM stg_products;

-- =========================
-- Load fact_orders
-- =========================
INSERT INTO fact_orders (
    order_id,
    customer_id,
    order_time,
    payment_method,
    discount_pct,
    subtotal_usd,
    total_usd,
    country,
    device,
    source
)
SELECT
    order_id,
    customer_id,
    order_time,
    payment_method,
    discount_pct,
    subtotal_usd,
    total_usd,
    country,
    device,
    source
FROM stg_orders;