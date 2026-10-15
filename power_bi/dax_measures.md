# Production DAX Measures Library
**Project:** Retail Consumer Shopping Behavior Analysis  
**Table Location:** Create a dedicated measure table called `_Measures` in Power BI.

---

## 1. Core Financial & Volume Measures

### Total Revenue ($)
```dax
Total Revenue = 
SUM(fact_transactions[purchase_amount_usd])
```
*Format:* Currency `\$#,##0`

### Total Transactions
```dax
Total Transactions = 
COUNTROWS(fact_transactions)
```
*Format:* Whole Number `#,##0`

### Total Unique Customers
```dax
Total Customers = 
DISTINCTCOUNT(fact_transactions[customer_id])
```
*Format:* Whole Number `#,##0`

### Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE(
    [Total Revenue],
    [Total Transactions],
    0
)
```
*Format:* Currency `\$#,##0.00`

### Average Customer Rating
```dax
Average Customer Rating = 
AVERAGE(fact_transactions[review_rating])
```
*Format:* Decimal Number `0.00`

---

## 2. Strategic Ratios & Penetration Rates

### Subscription Penetration Rate (%)
```dax
Subscription Rate % = 
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(fact_transactions[customer_id]),
        dim_customers[subscription_status] = "Yes"
    ),
    [Total Customers],
    0
)
```
*Format:* Percentage `0.0%`

### Discount Penetration Rate (%)
```dax
Discount Penetration % = 
DIVIDE(
    CALCULATE(
        [Total Transactions],
        fact_transactions[discount_applied] = "Yes"
    ),
    [Total Transactions],
    0
)
```
*Format:* Percentage `0.0%`

### Online Shipping Share (%)
```dax
Online Shipping Share % = 
DIVIDE(
    CALCULATE(
        [Total Revenue],
        dim_shipping[sales_channel] = "Online Shipping"
    ),
    [Total Revenue],
    0
)
```
*Format:* Percentage `0.0%`

### In-Store Pickup Share (%)
```dax
In-Store Pickup Share % = 
DIVIDE(
    CALCULATE(
        [Total Revenue],
        dim_shipping[sales_channel] = "In-Store Pickup"
    ),
    [Total Revenue],
    0
)
```
*Format:* Percentage `0.0%`

---

## 3. Demographics & Gender Equity Measures

### Female Revenue ($)
```dax
Female Revenue = 
CALCULATE(
    [Total Revenue],
    dim_customers[gender] = "Female"
)
```
*Format:* Currency `\$#,##0`

### Male Revenue ($)
```dax
Male Revenue = 
CALCULATE(
    [Total Revenue],
    dim_customers[gender] = "Male"
)
```
*Format:* Currency `\$#,##0`

### Female Customer Share (%)
```dax
Female Customer Share % = 
DIVIDE(
    CALCULATE([Total Customers], dim_customers[gender] = "Female"),
    [Total Customers],
    0
)
```
*Format:* Percentage `0.0%`

### Female Subscription Count
```dax
Female Subscribed Customers = 
CALCULATE(
    [Total Customers],
    dim_customers[gender] = "Female",
    dim_customers[subscription_status] = "Yes"
)
```
*Format:* Whole Number `#,##0`

---

## 4. Customer Lifetime Value & Loyalty Depth

### Average Estimated CLV ($)
```dax
Avg Estimated CLV = 
AVERAGE(fact_transactions[estimated_clv])
```
*Format:* Currency `\$#,##0.00`

### Total Pipeline Estimated CLV ($)
```dax
Total Pipeline CLV = 
SUM(fact_transactions[estimated_clv])
```
*Format:* Currency `\$#,##0`

### Repeat Purchase Depth (Average Past Orders)
```dax
Average Past Orders = 
AVERAGE(fact_transactions[previous_purchases])
```
*Format:* Decimal Number `0.0`

### High Loyalty Customer Volume (30+ Purchases)
```dax
VIP Loyal Customers Count = 
CALCULATE(
    [Total Customers],
    fact_transactions[previous_purchases] >= 30
)
```
*Format:* Whole Number `#,##0`

---

## 5. Dynamic KPI Formatting & Conditional Titles

### Dynamic Executive KPI Card Title
```dax
KPI Card Title = 
"Performance Summary | " & 
SELECTEDVALUE(dim_customers[gender], "All Genders") & " | " &
SELECTEDVALUE(dim_products[category], "All Categories")
```

### Rating Sentiment Color Code (For Visual Backgrounds)
```dax
Rating Color Hex = 
SWITCH(
    TRUE(),
    [Average Customer Rating] >= 3.8, "#2ecc71", -- Emerald Green
    [Average Customer Rating] >= 3.5, "#f1c40f", -- Amber Yellow
    "#e74c3c"                                     -- Coral Red
)
```
