-- =====================================================================
-- 01_schema_setup.sql
-- Star Schema DDL & Analytical Views
-- Project: Retail Customer Shopping Behavior Analysis
-- =====================================================================

-- Drop existing tables if re-running
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS dim_products;
DROP TABLE IF EXISTS dim_shipping;
DROP TABLE IF EXISTS dim_payment;

-- 1. Dimension: Customers
CREATE TABLE dim_customers (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL,
    age_group TEXT NOT NULL,
    gender TEXT NOT NULL,
    location TEXT NOT NULL,
    subscription_status TEXT NOT NULL,
    loyalty_tier TEXT NOT NULL,
    cluster_id INTEGER,
    customer_segment TEXT
);

-- 2. Dimension: Products
CREATE TABLE dim_products (
    product_id INTEGER PRIMARY KEY,
    item_purchased TEXT NOT NULL,
    category TEXT NOT NULL,
    size TEXT NOT NULL,
    color TEXT NOT NULL
);

-- 3. Dimension: Shipping & Sales Channel
CREATE TABLE dim_shipping (
    shipping_id INTEGER PRIMARY KEY,
    shipping_type TEXT NOT NULL,
    sales_channel TEXT NOT NULL
);

-- 4. Dimension: Payment Method
CREATE TABLE dim_payment (
    payment_id INTEGER PRIMARY KEY,
    payment_method TEXT NOT NULL
);

-- 5. Fact: Transactions
CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    shipping_id INTEGER NOT NULL,
    payment_id INTEGER NOT NULL,
    season TEXT NOT NULL,
    purchase_amount_usd INTEGER NOT NULL,
    review_rating REAL NOT NULL,
    review_rating_imputed INTEGER NOT NULL,
    discount_applied TEXT NOT NULL,
    promo_code_used TEXT NOT NULL,
    previous_purchases INTEGER NOT NULL,
    frequency_of_purchases TEXT NOT NULL,
    annual_purchase_frequency INTEGER NOT NULL,
    estimated_annual_spend REAL NOT NULL,
    estimated_clv REAL NOT NULL,
    spending_tier TEXT NOT NULL,
    satisfaction_level TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
    FOREIGN KEY (shipping_id) REFERENCES dim_shipping(shipping_id),
    FOREIGN KEY (payment_id) REFERENCES dim_payment(payment_id)
);

-- Indexes for performance optimization
CREATE INDEX idx_fact_customer ON fact_transactions(customer_id);
CREATE INDEX idx_fact_product ON fact_transactions(product_id);
CREATE INDEX idx_fact_shipping ON fact_transactions(shipping_id);
CREATE INDEX idx_fact_payment ON fact_transactions(payment_id);
CREATE INDEX idx_fact_season ON fact_transactions(season);

-- Analytical View combining Dimensions & Fact for seamless reporting
CREATE VIEW IF NOT EXISTS view_shopping_analytics AS
SELECT 
    f.transaction_id,
    c.customer_id,
    c.age,
    c.age_group,
    c.gender,
    c.location,
    c.subscription_status,
    c.loyalty_tier,
    c.customer_segment,
    p.item_purchased,
    p.category,
    p.size,
    p.color,
    s.shipping_type,
    s.sales_channel,
    pm.payment_method,
    f.season,
    f.purchase_amount_usd,
    f.review_rating,
    f.discount_applied,
    f.promo_code_used,
    f.previous_purchases,
    f.frequency_of_purchases,
    f.annual_purchase_frequency,
    f.estimated_annual_spend,
    f.estimated_clv,
    f.spending_tier,
    f.satisfaction_level
FROM fact_transactions f
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_products p ON f.product_id = p.product_id
JOIN dim_shipping s ON f.shipping_id = s.shipping_id
JOIN dim_payment pm ON f.payment_id = pm.payment_id;
