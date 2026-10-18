# Power BI Interactive Dashboard Implementation Guide
**Project:** Retail Consumer Shopping Behavior Analysis  
**Target Audience:** Executive Leadership, VP of Marketing, Head of Merchandising, VP of Customer Experience  

---

## 1. Environment & Data Import Setup

1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Import the five normalized Star Schema files from `data/processed/`:
   - `dim_customers.csv`
   - `dim_products.csv`
   - `dim_shipping.csv`
   - `dim_payment.csv`
   - `fact_transactions.csv`
4. In the **Model View**, verify the 1-to-Many (`1:*`) relationships with **Single** cross-filtering direction from each dimension to `fact_transactions`.
5. Create a new calculated table for clean measure organization:
   ```dax
   _Measures = ROW("Description", "Container for analytical measures")
   ```
6. Add the DAX measures detailed in [dax_measures.md](file:///C:/Users/BAH/.gemini/antigravity/scratch/retail-customer-behavior-analysis/power_bi/dax_measures.md).

---

## 2. Dashboard Layout Architecture (4 Pages)

### Page 1: Executive KPI & Revenue Performance
**Objective:** Provide C-suite stakeholders with an immediate overview of business volume, sales drivers, and seasonal trajectory.

#### Canvas Layout:
- **Top Header Banner:** Project Title, Dynamic Date/Season Indicator, Company Logo.
- **Top KPI Cards Ribbon (5 Cards):**
  1. `Total Revenue`: `$233.1K`
  2. `Total Customers`: `3,900`
  3. `Average Order Value (AOV)`: `$59.76`
  4. `Average Rating`: `3.75 / 5.0`
  5. `Subscription Penetration`: `27.0%`
- **Visual 1 (Top Left - Clustered Bar Chart):**
  - **Title:** Total Revenue by Product Category ($)
  - **Y-axis:** `dim_products[category]`
  - **X-axis:** `[Total Revenue]`
  - **Data Labels:** ON (`$104.3K` Clothing, `$74.2K` Accessories, `$36.1K` Footwear, `$18.5K` Outerwear).
- **Visual 2 (Top Right - Donut Chart):**
  - **Title:** Sales Fulfillment Channel Share
  - **Legend:** `dim_shipping[sales_channel]`
  - **Values:** `[Total Revenue]`
  - **Split:** Online Shipping (`83.3%`) vs In-Store Pickup (`16.7%`).
- **Visual 3 (Bottom Left - Line & Clustered Column Chart):**
  - **Title:** Seasonality Trend: Revenue & Basket Size by Season
  - **X-axis:** `fact_transactions[season]` (Spring, Summer, Fall, Winter)
  - **Column Values:** `[Total Revenue]`
  - **Line Values:** `[Average Order Value]`
- **Visual 4 (Bottom Right - Table / Matrix):**
  - **Title:** Top 10 Best-Selling Items
  - **Columns:** `item_purchased`, `category`, `Total Transactions`, `Total Revenue`, `Average Order Value`, `Average Customer Rating`.
- **Top Slicers Panel:** `Season`, `Sales Channel`, `Loyalty Tier`.

---

### Page 2: Customer Demographics, Equity & Subscription Opportunity
**Objective:** Deep-dive into customer cohorts, identify underserved segments, and highlight the critical female subscription gap.

#### Canvas Layout:
- **Callout Call-to-Action Card:**
  > ⚠️ **Critical Discovery:** 100% of Female shoppers (1,248 customers) have ZERO subscriptions and have received ZERO promotional discounts, despite having a higher AOV ($60.25 vs $59.54)!
- **Visual 1 (Clustered Column Chart):**
  - **Title:** Customer Volume & Total Revenue by Age Demographic
  - **X-axis:** `dim_customers[age_group]`
  - **Y-axis:** `[Total Customers]` & `[Total Revenue]`
- **Visual 2 (100% Stacked Bar Chart):**
  - **Title:** Subscription Adoption Status by Gender
  - **Y-axis:** `dim_customers[gender]`
  - **Legend:** `dim_customers[subscription_status]`
  - **Values:** `[Total Customers]`
- **Visual 3 (Scatter Plot):**
  - **Title:** Customer Lifetime Value vs Repeat Order Count
  - **X-axis:** `Average Past Orders`
  - **Y-axis:** `Avg Estimated CLV`
  - **Legend:** `dim_customers[customer_segment]`
  - **Size:** `[Total Revenue]`
- **Visual 4 (Filled Map / Shape Map):**
  - **Title:** Geographic Sales Revenue Across US States
  - **Location:** `dim_customers[location]`
  - **Color Saturation:** `[Total Revenue]`
- **Visual 5 (Interactive What-If Simulation Panel - Bottom Ribbon):**
  - **What-If Slicer Slider:** `Female Subscription Adoption Rate` (0% to 100%, step 5%, default 40%).
  - **Dynamic Card 1:** `Simulated Female Subscribers` (e.g., `499 Subscribers` at 40%).
  - **Dynamic Card 2:** `Simulated Incremental Revenue` (e.g., `+$84.2K`).
  - **Dynamic Card 3:** `Total Projected Revenue` (e.g., `$317.3K`).
  - **Dynamic Card 4:** `Projected Revenue Lift %` (e.g., `+36.1%`).
  - **Business Purpose:** Directly answers leadership's question on expected sales lift if the female subscription barrier is addressed.

---

### Page 3: Marketing Drivers, Pricing & Promotions
**Objective:** Analyze the ROI of discounts, shipping method satisfaction, and payment checkout friction.

#### Canvas Layout:
- **Visual 1 (Side-by-Side Comparison Matrix / Bar):**
  - **Title:** Discount Impact: Basket Value & Volume Comparison
  - **Categories:** `Full Price (No Promo)` vs `Discount Applied`
  - **Metrics:** Total Revenue (`$133.7K` vs `$99.4K`), AOV (`$60.13` vs `$59.28`), Avg Rating (`3.76` vs `3.74`).
  - **Takeaway:** Discounts are NOT increasing basket size.
- **Visual 2 (Horizontal Bar Chart):**
  - **Title:** Fulfillment Method vs Customer Review Satisfaction
  - **Y-axis:** `dim_shipping[shipping_type]`
  - **X-axis:** `[Average Customer Rating]`
  - **Color:** Gradient from low to high rating.
- **Visual 3 (Treemap / Donut Chart):**
  - **Title:** Payment Method Distribution
  - **Category:** `dim_payment[payment_method]`
  - **Values:** `[Total Transactions]` (PayPal, Credit Card, Cash, Debit Card, Venmo, Bank Transfer).
- **Visual 4 (Matrix with Heatmap):**
  - **Title:** Payment Method Preference by Age Cohort
  - **Rows:** `dim_customers[age_group]`
  - **Columns:** `dim_payment[payment_method]`
  - **Values:** `[Total Transactions]`

---

### Page 4: Product Category Deep-Dive & Customer Personas
**Objective:** Provide merchandise planners and inventory managers with item-level velocity and customer persona preferences.

#### Canvas Layout:
- **Visual 1 (Sunburst / Decomposition Tree):**
  - **Title:** Revenue Decomposition Tree
  - **Root:** `[Total Revenue]`
  - **Branches:** `Category` -> `Item Purchased` -> `Size` -> `Sales Channel`.
- **Visual 2 (Grouped Bar Chart):**
  - **Title:** Customer Persona Revenue Contribution
  - **X-axis:** `dim_customers[customer_segment]`
  - **Y-axis:** `[Total Revenue]` & `[Avg Estimated CLV]`
- **Visual 3 (Heatmap Table):**
  - **Title:** Product Category Cross-Season Revenue Matrix
  - **Rows:** `category`
  - **Columns:** `season`
  - **Values:** `[Total Revenue]`

---

## 3. Power BI Color Theme Palette
To ensure an executive-level aesthetic, use the following Hex color palette:
- **Primary Navy:** `#1A365D` (Headers, Primary Cards)
- **Accent Teal / Cyan:** `#0D9488` (Online Shipping, Positive KPIs)
- **Warm Coral / Amber:** `#E28743` (Discounts, Warnings, In-Store)
- **Neutral Background:** `#F8FAFC`
- **Text Primary:** `#0F172A`
