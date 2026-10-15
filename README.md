# Retail Customer Shopping Behavior Analysis 🛍️📊

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite%20%7C%20PostgreSQL-orange.svg)](https://www.sqlite.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Interactive_Dashboard-yellow.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end retail data analytics and business intelligence project analyzing **3,900 consumer transactions**. This project leverages **Python** for automated data cleansing, feature engineering, and machine learning (K-Means customer clustering), **SQL** for relational dimensional modeling and analytical business queries, and **Power BI** for interactive executive decision-making dashboards.

---

## 📌 Business Problem Statement

A leading retail enterprise wants to better understand its customers' shopping behavior in order to improve sales, customer satisfaction, and long-term loyalty. The management team has observed shifts in purchasing patterns across demographics, product categories, and sales channels (online vs in-store). They need to uncover which factors—such as discounts, reviews, seasons, fulfillment methods, and payment preferences—drive consumer decisions and repeat purchases.

**Central Business Mandate:**
> *“How can the company leverage consumer shopping data to identify trends, improve customer engagement, and optimize marketing and product strategies?”*

---

## 🚀 Key Project Deliverables

1. **Data Preparation & Modeling (Python):** Automated cleaning, median review imputation, 8 engineered features (age cohorts, channel mapping, annualized frequency, CLV estimates, loyalty tiers), and Kimball Star Schema export.
2. **Customer Segmentation (Machine Learning):** Unsupervised K-Means clustering (evaluated with Elbow and Silhouette scores) establishing 4 actionable customer personas.
3. **Relational Data Analysis (SQL):** Complete Star Schema DDL, transactional views, and a suite of 12 analytical SQL queries uncovering demographic, commercial, and operational drivers.
4. **Interactive Visualization & Insights (Power BI):** 4-page executive dashboard blueprint, DAX measures library, and high-resolution chart exhibits.
5. **Executive Report & Presentation:** Comprehensive strategy report (`executive_project_report.md`) and a 10-slide C-suite presentation deck (`stakeholder_presentation.md`).

---

## 🔍 Key Findings & Executive Insights

- **Commercial Baseline:** Generated **\$233,081 in revenue** across 3,900 orders, with an **Average Order Value (AOV) of \$59.76** and an average rating of **3.75 / 5.0**.
- **Category Leadership:** **Clothing (44.7%)** and **Accessories (31.8%)** represent **76.5% of total revenue**. Top products: Blouses (\$10,410), Shirts (\$10,332), and Dresses (\$10,320).
- **The Female Engagement Paradox (Critical Finding):**
  - Female shoppers represent **32% of customers (1,248 shoppers)** with a **higher average spend per basket (\$60.25 vs \$59.54 for males)**.
  - However, **0.0% of female customers are enrolled in the subscription program** and **0.0% received promotional discounts**.
  - This highlights an urgent opportunity to launch a female-targeted loyalty program, projecting **+\$50,000+ in incremental recurring EBITDA**.
- **The Discount Trap:** Orders with applied discounts produced a lower AOV (**\$59.28** vs **\$60.13**) with no improvement in review rating (**3.74** vs **3.76**). Blanket discounts are causing margin erosion without lifting basket size.
- **Omnichannel Distribution:** Online parcel delivery generates **83.3% of orders**, while In-Store Pickup (BOPIS) drives **16.7%**, providing prime foot-traffic upsell opportunities.
- **Payment Method Diversity:** Evenly split across PayPal (17.4%), Credit Card (17.2%), Cash (17.2%), Debit Card (16.3%), Venmo (16.3%), and Bank Transfer (15.7%).

---

## 📂 Repository Structure

```text
retail-customer-behavior-analysis/
│
├── data/
│   ├── raw/
│   │   └── customer_shopping_behavior.csv    # Original raw dataset
│   └── processed/
│       ├── cleaned_customer_shopping_behavior.csv # Cleaned & enriched flat data
│       ├── dim_customers.csv                 # Customer dimension with clusters
│       ├── dim_products.csv                  # Product catalog dimension
│       ├── dim_shipping.csv                  # Shipping & channel dimension
│       ├── dim_payment.csv                   # Payment method dimension
│       ├── fact_transactions.csv             # Star schema fact transactions table
│       └── retail_shopping.db                # SQLite database binary
│
├── src/
│   ├── 01_data_cleaning.py                   # Data cleansing & Star Schema export
│   ├── 02_customer_segmentation.py           # K-Means clustering & profiling
│   └── 03_generate_visualizations.py         # Visual chart generation
│
├── sql/
│   ├── 01_schema_setup.sql                   # DDL scripts, tables, foreign keys, views
│   ├── 02_business_queries.sql               # 12 analytical business queries
│   └── run_sql_analysis.py                   # Python runner for executing SQL analysis
│
├── power_bi/
│   ├── data_model_star_schema.md             # Star Schema documentation & ERD
│   ├── dax_measures.md                       # Ready-to-use DAX measures library
│   └── power_bi_dashboard_guide.md           # Step-by-step 4-page dashboard blueprint
│
├── reports/
│   ├── executive_project_report.md           # Full strategic consulting report
│   ├── stakeholder_presentation.md           # 10-slide C-suite presentation deck
│   └── sql_query_results.md                  # Complete SQL execution output tables
│
├── figures/
│   ├── 01_kmeans_elbow_silhouette.png        # Elbow & Silhouette cluster evaluation
│   ├── 02_customer_segments_scatter.png      # Cluster spend vs loyalty scatter
│   ├── 03_executive_overview_dashboard.png   # 4-panel executive dashboard
│   ├── 04_gender_subscription_discount_gap.png # Gender discrepancy comparison
│   ├── 05_marketing_drivers_analysis.png     # Discounts, shipping, payment analysis
│   ├── 06_seasonality_category_heatmap.png   # Seasonal category revenue heatmap
│   └── 07_loyalty_clv_comparison.png         # Lifetime value by loyalty tier
│
├── .gitignore
├── requirements.txt                          # Python dependencies
└── README.md                                 # Project documentation
```

---

## 🛠️ Installation & Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/retail-customer-behavior-analysis.git
cd retail-customer-behavior-analysis
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run Data Pipeline (Cleaning & Segmentation)
```bash
python src/01_data_cleaning.py
python src/02_customer_segmentation.py
python src/03_generate_visualizations.py
```

### 4. Run SQL Analysis
```bash
python sql/run_sql_analysis.py
```
This initializes `retail_shopping.db`, executes all 12 analytical queries, and outputs the formatted markdown tables to `reports/sql_query_results.md`.

---

## 📊 Power BI Implementation

1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV** and select the 5 files in `data/processed/`.
3. In **Model View**, verify the Star Schema relationships:
   - `dim_customers[customer_id]` (1) ───< (*) `fact_transactions[customer_id]`
   - `dim_products[product_id]` (1) ───< (*) `fact_transactions[product_id]`
   - `dim_shipping[shipping_id]` (1) ───< (*) `fact_transactions[shipping_id]`
   - `dim_payment[payment_id]` (1) ───< (*) `fact_transactions[payment_id]`
4. Copy the production DAX formulas from `power_bi/dax_measures.md` into a new `_Measures` table.
5. Follow the layout blueprint in `power_bi/power_bi_dashboard_guide.md` to build the 4 pages.

---

## 💡 Strategic Recommendations Roadmap

1. **Launch Inclusive Loyalty Tier:** Create a specialized subscription tier tailored for female shoppers with benefits like seasonal preview access and premium styling perks.
2. **Rationalize Discounts (End Blanket Margins):** Replace universal promo codes with **threshold discounts** (e.g. *"$15 off orders of \$85+"*) to lift AOV above the current \$59.76 benchmark.
3. **Monetize BOPIS Traffic:** Drive in-store attach rates by granting a *"\$5 Off Today"* store voucher to shoppers collecting online orders.
4. **Merchandise Bundling:** Cross-merchandise high-performing Accessories (Jewelry, Scarves) alongside core Apparel (Blouses, Dresses).

---

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
