-- =====================================================================
-- 02_business_queries.sql
-- Executive & Granular SQL Queries for Consumer Shopping Behavior
-- Project: Retail Customer Shopping Behavior Analysis
-- =====================================================================

-- ---------------------------------------------------------------------
-- QUERY 1: Executive KPI Summary
-- High-level snapshot of business volume, revenue, basket size, and sentiment
-- ---------------------------------------------------------------------
SELECT 
    COUNT(transaction_id) AS total_transactions,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(purchase_amount_usd) AS total_revenue_usd,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value_usd,
    ROUND(AVG(review_rating), 2) AS average_customer_rating,
    ROUND(100.0 * SUM(CASE WHEN subscription_status = 'Yes' THEN 1 ELSE 0 END) / COUNT(DISTINCT customer_id), 2) AS subscription_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END) / COUNT(transaction_id), 2) AS discount_penetration_pct
FROM view_shopping_analytics;

-- ---------------------------------------------------------------------
-- QUERY 2: Demographics Breakdown (Age Groups & Gender)
-- Evaluating revenue generation, customer count, and average spend across demographic cohorts
-- ---------------------------------------------------------------------
SELECT 
    age_group,
    gender,
    COUNT(customer_id) AS customer_count,
    ROUND(100.0 * COUNT(customer_id) / SUM(COUNT(customer_id)) OVER(), 2) AS pct_of_total_customers,
    SUM(purchase_amount_usd) AS total_revenue_usd,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_spend_per_customer,
    ROUND(AVG(previous_purchases), 1) AS avg_previous_purchases
FROM view_shopping_analytics
GROUP BY age_group, gender
ORDER BY age_group, gender;

-- ---------------------------------------------------------------------
-- QUERY 3: Gender Discrepancy & Opportunity Analysis
-- Revealing the dramatic gap in Subscription & Discount adoption between Male and Female shoppers
-- ---------------------------------------------------------------------
SELECT 
    gender,
    COUNT(customer_id) AS total_shoppers,
    SUM(CASE WHEN subscription_status = 'Yes' THEN 1 ELSE 0 END) AS subscribed_shoppers,
    ROUND(100.0 * SUM(CASE WHEN subscription_status = 'Yes' THEN 1 ELSE 0 END) / COUNT(customer_id), 2) AS subscription_rate_pct,
    SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END) AS discount_users,
    ROUND(100.0 * SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END) / COUNT(customer_id), 2) AS discount_usage_pct,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_order_value_usd,
    SUM(purchase_amount_usd) AS total_spend_usd
FROM view_shopping_analytics
GROUP BY gender;

-- ---------------------------------------------------------------------
-- QUERY 4: Product Category & Item Performance
-- Identifying revenue contribution, sales volume, and customer rating by category and top items
-- ---------------------------------------------------------------------
SELECT 
    category,
    COUNT(transaction_id) AS items_sold,
    SUM(purchase_amount_usd) AS category_revenue_usd,
    ROUND(100.0 * SUM(purchase_amount_usd) / SUM(SUM(purchase_amount_usd)) OVER(), 2) AS revenue_share_pct,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_item_price_usd,
    ROUND(AVG(review_rating), 2) AS avg_review_rating
FROM view_shopping_analytics
GROUP BY category
ORDER BY category_revenue_usd DESC;

-- Top 10 Best-Selling Individual Items
SELECT 
    item_purchased,
    category,
    COUNT(transaction_id) AS total_orders,
    SUM(purchase_amount_usd) AS total_revenue_usd,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_order_value,
    ROUND(AVG(review_rating), 2) AS avg_rating
FROM view_shopping_analytics
GROUP BY item_purchased, category
ORDER BY total_revenue_usd DESC
LIMIT 10;

-- ---------------------------------------------------------------------
-- QUERY 5: Discount & Promotion Effectiveness
-- Evaluating whether discounts stimulate higher order values or simply erode margins
-- ---------------------------------------------------------------------
SELECT 
    discount_applied,
    promo_code_used,
    COUNT(transaction_id) AS order_volume,
    ROUND(100.0 * COUNT(transaction_id) / SUM(COUNT(transaction_id)) OVER(), 2) AS order_share_pct,
    SUM(purchase_amount_usd) AS total_sales_usd,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_order_value_usd,
    ROUND(AVG(review_rating), 2) AS avg_customer_rating,
    ROUND(AVG(previous_purchases), 1) AS avg_previous_purchases
FROM view_shopping_analytics
GROUP BY discount_applied, promo_code_used;

-- ---------------------------------------------------------------------
-- QUERY 6: Customer Loyalty & Frequency Analysis
-- Correlation between previous purchase volume, frequency, and estimated lifetime value
-- ---------------------------------------------------------------------
SELECT 
    loyalty_tier,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(previous_purchases), 1) AS avg_past_orders,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_order_value_usd,
    ROUND(AVG(estimated_clv), 2) AS avg_estimated_clv_usd,
    ROUND(AVG(review_rating), 2) AS avg_rating,
    ROUND(100.0 * SUM(CASE WHEN subscription_status = 'Yes' THEN 1 ELSE 0 END) / COUNT(customer_id), 2) AS subscription_rate_pct
FROM view_shopping_analytics
GROUP BY loyalty_tier
ORDER BY avg_past_orders ASC;

-- ---------------------------------------------------------------------
-- QUERY 7: Sales Channel Performance: Online Shipping vs In-Store Pickup
-- Comparing fulfillment channel volume, revenue, basket size, and customer satisfaction
-- ---------------------------------------------------------------------
SELECT 
    sales_channel,
    shipping_type,
    COUNT(transaction_id) AS order_count,
    ROUND(100.0 * COUNT(transaction_id) / SUM(COUNT(transaction_id)) OVER(), 2) AS channel_order_share_pct,
    SUM(purchase_amount_usd) AS total_revenue_usd,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_order_value_usd,
    ROUND(AVG(review_rating), 2) AS avg_satisfaction_rating
FROM view_shopping_analytics
GROUP BY sales_channel, shipping_type
ORDER BY sales_channel, order_count DESC;

-- ---------------------------------------------------------------------
-- QUERY 8: Payment Method Preferences
-- Payment adoption across customer demographics and spending tiers
-- ---------------------------------------------------------------------
SELECT 
    payment_method,
    COUNT(transaction_id) AS transaction_count,
    ROUND(100.0 * COUNT(transaction_id) / SUM(COUNT(transaction_id)) OVER(), 2) AS payment_share_pct,
    SUM(purchase_amount_usd) AS total_collected_usd,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_ticket_size_usd,
    ROUND(100.0 * SUM(CASE WHEN sales_channel = 'In-Store Pickup' THEN 1 ELSE 0 END) / COUNT(transaction_id), 2) AS in_store_pickup_pct
FROM view_shopping_analytics
GROUP BY payment_method
ORDER BY total_collected_usd DESC;

-- ---------------------------------------------------------------------
-- QUERY 9: Seasonality & Category Demand Trends
-- Analyzing sales and average basket sizes across the four calendar seasons
-- ---------------------------------------------------------------------
SELECT 
    season,
    category,
    COUNT(transaction_id) AS orders_count,
    SUM(purchase_amount_usd) AS seasonal_revenue_usd,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_spend_usd
FROM view_shopping_analytics
GROUP BY season, category
ORDER BY season, seasonal_revenue_usd DESC;

-- ---------------------------------------------------------------------
-- QUERY 10: Customer Satisfaction Drivers (Review Ratings)
-- Uncovering which operational and product attributes correlate with top-tier ratings
-- ---------------------------------------------------------------------
SELECT 
    satisfaction_level,
    COUNT(customer_id) AS customer_count,
    ROUND(100.0 * COUNT(customer_id) / SUM(COUNT(customer_id)) OVER(), 2) AS customer_pct,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_spend,
    ROUND(AVG(previous_purchases), 1) AS avg_previous_purchases,
    ROUND(100.0 * SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END) / COUNT(customer_id), 2) AS discount_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN subscription_status = 'Yes' THEN 1 ELSE 0 END) / COUNT(customer_id), 2) AS subscription_rate_pct
FROM view_shopping_analytics
GROUP BY satisfaction_level
ORDER BY customer_count DESC;

-- ---------------------------------------------------------------------
-- QUERY 11: Top 10 Geographic Markets by Revenue
-- Identifying top revenue contributing locations across the US
-- ---------------------------------------------------------------------
SELECT 
    location AS state,
    COUNT(transaction_id) AS order_count,
    SUM(purchase_amount_usd) AS total_sales_usd,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_ticket_size_usd,
    ROUND(AVG(review_rating), 2) AS avg_rating,
    ROUND(100.0 * SUM(CASE WHEN subscription_status = 'Yes' THEN 1 ELSE 0 END) / COUNT(transaction_id), 2) AS subscriber_pct
FROM view_shopping_analytics
GROUP BY location
ORDER BY total_sales_usd DESC
LIMIT 10;

-- ---------------------------------------------------------------------
-- QUERY 12: Customer RFM Simulation & Value Segmentation
-- Using Window Functions to divide customers into quartiles of Frequency and Monetary spend
-- ---------------------------------------------------------------------
WITH customer_rfm_scores AS (
    SELECT 
        customer_id,
        gender,
        age_group,
        purchase_amount_usd,
        previous_purchases,
        annual_purchase_frequency,
        NTILE(4) OVER (ORDER BY previous_purchases ASC) AS loyalty_quartile,
        NTILE(4) OVER (ORDER BY annual_purchase_frequency ASC) AS frequency_quartile,
        NTILE(4) OVER (ORDER BY purchase_amount_usd ASC) AS monetary_quartile
    FROM view_shopping_analytics
),
rfm_segmented AS (
    SELECT 
        customer_id,
        gender,
        age_group,
        purchase_amount_usd,
        previous_purchases,
        (loyalty_quartile + frequency_quartile + monetary_quartile) AS total_rfm_score,
        CASE 
            WHEN (loyalty_quartile + frequency_quartile + monetary_quartile) >= 10 THEN 'Champions (High Value & Loyalty)'
            WHEN (loyalty_quartile + frequency_quartile + monetary_quartile) BETWEEN 7 AND 9 THEN 'Loyal Core Customers'
            WHEN (loyalty_quartile + frequency_quartile + monetary_quartile) BETWEEN 5 AND 6 THEN 'Potential Promising Customers'
            ELSE 'At-Risk / Low Engagement'
        END AS rfm_segment
    FROM customer_rfm_scores
)
SELECT 
    rfm_segment,
    COUNT(customer_id) AS customer_count,
    ROUND(100.0 * COUNT(customer_id) / SUM(COUNT(customer_id)) OVER(), 2) AS pct_of_customers,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_current_spend,
    ROUND(AVG(previous_purchases), 1) AS avg_past_orders,
    ROUND(100.0 * SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) / COUNT(customer_id), 2) AS female_ratio_pct
FROM rfm_segmented
GROUP BY rfm_segment
ORDER BY avg_past_orders DESC;
