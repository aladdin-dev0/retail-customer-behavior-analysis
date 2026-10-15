# SQL Analytical Query Results & Business Insights

**Project:** Retail Customer Shopping Behavior Analysis  

**Database Engine:** SQLite 3  

**Total Records:** 3,900 Transactions & Customers  

---


### QUERY 1: Executive KPI Summary

```sql
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
FROM view_shopping_analytics
```


**Result Table:**


| total_transactions | total_customers | total_revenue_usd | average_order_value_usd | average_customer_rating | subscription_rate_pct | discount_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- |
| 3900.0 | 3900.0 | 233081.0 | 59.76 | 3.75 | 27.0 | 43.0 |


---


### QUERY 2: Demographics Breakdown (Age Groups & Gender)

```sql
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
ORDER BY age_group, gender
```


**Result Table:**


| age_group | gender | customer_count | pct_of_total_customers | total_revenue_usd | avg_spend_per_customer | avg_previous_purchases |
| --- | --- | --- | --- | --- | --- | --- |
| 18-25 (Young Adult) | Female | 173 | 4.44 | 10536 | 60.9 | 23.5 |
| 18-25 (Young Adult) | Male | 398 | 10.21 | 24094 | 60.54 | 25.1 |
| 26-35 (Early Career) | Female | 242 | 6.21 | 15019 | 62.06 | 25.0 |
| 26-35 (Early Career) | Male | 500 | 12.82 | 29323 | 58.65 | 24.6 |
| 36-50 (Mid Career) | Female | 375 | 9.62 | 21751 | 58.0 | 23.9 |
| 36-50 (Mid Career) | Male | 736 | 18.87 | 43878 | 59.62 | 25.4 |
| 51-70 (Senior) | Female | 458 | 11.74 | 27885 | 60.88 | 25.4 |
| 51-70 (Senior) | Male | 1018 | 26.1 | 60595 | 59.52 | 26.7 |


---


### QUERY 3: Gender Discrepancy & Opportunity Analysis

```sql
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
GROUP BY gender
```


**Result Table:**


| gender | total_shoppers | subscribed_shoppers | subscription_rate_pct | discount_users | discount_usage_pct | avg_order_value_usd | total_spend_usd |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Female | 1248 | 0 | 0.0 | 0 | 0.0 | 60.25 | 75191 |
| Male | 2652 | 1053 | 39.71 | 1677 | 63.24 | 59.54 | 157890 |


---


### QUERY 4: Product Category & Item Performance

```sql
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
ORDER BY category_revenue_usd DESC
```


**Result Table:**


| category | items_sold | category_revenue_usd | revenue_share_pct | avg_item_price_usd | avg_review_rating |
| --- | --- | --- | --- | --- | --- |
| Clothing | 1737 | 104264 | 44.73 | 60.03 | 3.72 |
| Accessories | 1240 | 74200 | 31.83 | 59.84 | 3.77 |
| Footwear | 599 | 36093 | 15.49 | 60.26 | 3.79 |
| Outerwear | 324 | 18524 | 7.95 | 57.17 | 3.75 |


---


### Query 5

```sql
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
LIMIT 10
```


**Result Table:**


| item_purchased | category | total_orders | total_revenue_usd | avg_order_value | avg_rating |
| --- | --- | --- | --- | --- | --- |
| Blouse | Clothing | 171 | 10410 | 60.88 | 3.68 |
| Shirt | Clothing | 169 | 10332 | 61.14 | 3.62 |
| Dress | Clothing | 166 | 10320 | 62.17 | 3.75 |
| Pants | Clothing | 171 | 10090 | 59.01 | 3.72 |
| Jewelry | Accessories | 171 | 10010 | 58.54 | 3.76 |
| Sunglasses | Accessories | 161 | 9649 | 59.93 | 3.75 |
| Belt | Accessories | 161 | 9635 | 59.84 | 3.76 |
| Scarf | Accessories | 157 | 9561 | 60.9 | 3.71 |
| Sweater | Clothing | 164 | 9462 | 57.7 | 3.76 |
| Shorts | Clothing | 157 | 9433 | 60.08 | 3.71 |


---


### QUERY 5: Discount & Promotion Effectiveness

```sql
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
GROUP BY discount_applied, promo_code_used
```


**Result Table:**


| discount_applied | promo_code_used | order_volume | order_share_pct | total_sales_usd | avg_order_value_usd | avg_customer_rating | avg_previous_purchases |
| --- | --- | --- | --- | --- | --- | --- | --- |
| No | No | 2223 | 57.0 | 133670 | 60.13 | 3.76 | 25.1 |
| Yes | Yes | 1677 | 43.0 | 99411 | 59.28 | 3.74 | 25.7 |


---


### QUERY 6: Customer Loyalty & Frequency Analysis

```sql
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
ORDER BY avg_past_orders ASC
```


**Result Table:**


| loyalty_tier | customer_count | avg_past_orders | avg_order_value_usd | avg_estimated_clv_usd | avg_rating | subscription_rate_pct |
| --- | --- | --- | --- | --- | --- | --- |
| Bronze (1-15) | 1179 | 7.9 | 59.7 | 526.08 | 3.75 | 24.94 |
| Silver (16-30) | 1172 | 23.0 | 59.48 | 1429.39 | 3.73 | 27.39 |
| Gold (31-45) | 1156 | 37.8 | 59.4 | 2307.6 | 3.78 | 28.81 |
| Platinum (46+) | 393 | 47.9 | 61.87 | 3027.31 | 3.73 | 26.72 |


---


### QUERY 7: Sales Channel Performance: Online Shipping vs In-Store Pickup

```sql
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
ORDER BY sales_channel, order_count DESC
```


**Result Table:**


| sales_channel | shipping_type | order_count | channel_order_share_pct | total_revenue_usd | avg_order_value_usd | avg_satisfaction_rating |
| --- | --- | --- | --- | --- | --- | --- |
| In-Store Pickup | Store Pickup | 650 | 16.67 | 38931 | 59.89 | 3.71 |
| Online Shipping | Free Shipping | 675 | 17.31 | 40777 | 60.41 | 3.72 |
| Online Shipping | Standard | 654 | 16.77 | 38233 | 58.46 | 3.82 |
| Online Shipping | Next Day Air | 648 | 16.62 | 37993 | 58.63 | 3.72 |
| Online Shipping | Express | 646 | 16.56 | 39067 | 60.48 | 3.77 |
| Online Shipping | 2-Day Shipping | 627 | 16.08 | 38080 | 60.73 | 3.77 |


---


### QUERY 8: Payment Method Preferences

```sql
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
ORDER BY total_collected_usd DESC
```


**Result Table:**


| payment_method | transaction_count | payment_share_pct | total_collected_usd | avg_ticket_size_usd | in_store_pickup_pct |
| --- | --- | --- | --- | --- | --- |
| Credit Card | 671 | 17.21 | 40310 | 60.07 | 15.5 |
| PayPal | 677 | 17.36 | 40109 | 59.25 | 15.21 |
| Cash | 670 | 17.18 | 40002 | 59.7 | 17.76 |
| Debit Card | 636 | 16.31 | 38742 | 60.92 | 16.51 |
| Venmo | 634 | 16.26 | 37374 | 58.95 | 16.88 |
| Bank Transfer | 612 | 15.69 | 36544 | 59.71 | 18.3 |


---


### QUERY 9: Seasonality & Category Demand Trends

```sql
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
ORDER BY season, seasonal_revenue_usd DESC
```


**Result Table:**


| season | category | orders_count | seasonal_revenue_usd | avg_spend_usd |
| --- | --- | --- | --- | --- |
| Fall | Clothing | 427 | 26220 | 61.41 |
| Fall | Accessories | 324 | 19874 | 61.34 |
| Fall | Footwear | 136 | 8665 | 63.71 |
| Fall | Outerwear | 88 | 5259 | 59.76 |
| Spring | Clothing | 454 | 27692 | 61.0 |
| Spring | Accessories | 301 | 17007 | 56.5 |
| Spring | Footwear | 163 | 9555 | 58.62 |
| Spring | Outerwear | 81 | 4425 | 54.63 |
| Summer | Clothing | 408 | 23078 | 56.56 |
| Summer | Accessories | 312 | 19028 | 60.99 |
| Summer | Footwear | 160 | 9393 | 58.71 |
| Summer | Outerwear | 75 | 4278 | 57.04 |
| Winter | Clothing | 448 | 27274 | 60.88 |
| Winter | Accessories | 303 | 18291 | 60.37 |
| Winter | Footwear | 140 | 8480 | 60.57 |
| Winter | Outerwear | 80 | 4562 | 57.02 |


---


### QUERY 10: Customer Satisfaction Drivers (Review Ratings)

```sql
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
ORDER BY customer_count DESC
```


**Result Table:**


| satisfaction_level | customer_count | customer_pct | avg_spend | avg_previous_purchases | discount_rate_pct | subscription_rate_pct |
| --- | --- | --- | --- | --- | --- | --- |
| High (4.0-5.0) | 1634 | 41.9 | 60.52 | 25.4 | 42.35 | 26.74 |
| Moderate (3.0-3.9) | 1586 | 40.67 | 59.52 | 25.4 | 43.76 | 27.24 |
| Low (<3.0) | 680 | 17.44 | 58.51 | 25.1 | 42.79 | 27.06 |


---


### QUERY 11: Top 10 Geographic Markets by Revenue

```sql
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
LIMIT 10
```


**Result Table:**


| state | order_count | total_sales_usd | avg_ticket_size_usd | avg_rating | subscriber_pct |
| --- | --- | --- | --- | --- | --- |
| Montana | 96 | 5784 | 60.25 | 3.82 | 26.04 |
| Illinois | 92 | 5617 | 61.05 | 3.64 | 23.91 |
| California | 95 | 5605 | 59.0 | 3.83 | 30.53 |
| Idaho | 93 | 5587 | 60.08 | 3.79 | 20.43 |
| Nevada | 87 | 5514 | 63.38 | 3.72 | 34.48 |
| Alabama | 89 | 5261 | 59.11 | 3.78 | 24.72 |
| New York | 87 | 5257 | 60.43 | 3.76 | 24.14 |
| North Dakota | 83 | 5220 | 62.89 | 3.75 | 28.92 |
| West Virginia | 81 | 5174 | 63.88 | 3.59 | 34.57 |
| Nebraska | 87 | 5172 | 59.45 | 3.73 | 28.74 |


---


### QUERY 12: Customer RFM Simulation & Value Segmentation

```sql
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
ORDER BY avg_past_orders DESC
```


**Result Table:**


| rfm_segment | customer_count | pct_of_customers | avg_current_spend | avg_past_orders | female_ratio_pct |
| --- | --- | --- | --- | --- | --- |
| Champions (High Value & Loyalty) | 707 | 18.13 | 82.5 | 36.9 | 29.56 |
| Loyal Core Customers | 1908 | 48.92 | 63.36 | 26.4 | 33.18 |
| Potential Promising Customers | 975 | 25.0 | 44.92 | 19.5 | 33.33 |
| At-Risk / Low Engagement | 310 | 7.95 | 32.47 | 10.7 | 26.13 |


---
