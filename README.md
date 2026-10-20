# Retail Customer Shopping Behavior Analysis 🛍️📊

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite%20%7C%20Star%20Schema-orange.svg)](https://www.sqlite.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Fabric_PBIP_Cockpit-yellow.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, end-to-end retail data analytics and business intelligence project analyzing **3,900 consumer transactions**. This project leverages **Python** for automated data cleansing, feature engineering, and machine learning (K-Means customer clustering), **SQL** for relational dimensional modeling and analytical business queries, and **Power BI (PBIP / TMDL Developer Mode)** for an executive dark-themed decision cockpit with real-time What-If financial simulations.

---

## 📌 Business Problem Statement

A leading retail enterprise wants to better understand its customers' shopping behavior in order to improve sales, customer satisfaction, and long-term loyalty. Management observed key shifts in purchasing patterns across demographics, product categories, and sales channels (online shipping vs in-store pickup). They need to uncover which commercial levers—subscriptions, promotional discounts, review ratings, seasons, fulfillment methods, and payment options—drive consumer decisions and repeat purchases.

**Central Strategic Mandate:**
> *“Where does our revenue come from today, and what is the exact financial impact of unlocking female subscriptions?”*

---

## 🚀 Key Project Deliverables

1. **Automated Data Preparation & Dimensional Modeling (Python):** Automated cleaning, missing value imputation, 8 engineered features (age cohorts, channel mapping, annualized frequency, CLV estimates, loyalty tiers), and Kimball Star Schema generation.
2. **Customer Behavioral Clustering (Machine Learning):** Unsupervised K-Means clustering (evaluated with Elbow and Silhouette scores) establishing 4 distinct consumer personas.
3. **Relational Data Analysis (SQL):** Complete Star Schema DDL, transactional views, and a suite of 10 analytical SQL queries uncovering demographic, commercial, and operational performance.
4. **Interactive Executive Cockpit (Power BI Fabric PBIP):** Panoramic 1920×820 single-page cockpit in Developer Mode (`.pbip` + TMDL) with 18 DAX measures, Executive Dark Theme (`#0B1120`), and an interactive What-If simulation slider modeling female subscription adoption.
5. **C-Suite Strategic Presentations & Reports:** 
   - 12-section Board Report available in print-ready HTML (`reports/executive_report.html`) and Markdown (`reports/executive_project_report.md`).
   - 10-slide C-suite presentation deck in native 16:9 PowerPoint (`reports/retail_customer_behavior_presentation.pptx`) and interactive web format (`reports/interactive_presentation.html`).

---

## 🔍 Key Findings & Executive Insights

- **Commercial Baseline:** Generated **\$233,081 in gross revenue** across 3,900 orders, with an **Average Order Value (AOV) of \$59.76** and an average rating of **3.75 / 5.0**.
- **Category Leadership:** **Clothing (44.7% / \$104K)** and **Accessories (31.8% / \$74K)** command **76.5% of total revenue**. Top products: Blouses (\$10,410), Shirts (\$10,332), and Dresses (\$10,320).
- **The Female Engagement Paradox (Critical Strategic Finding):**
  - Female shoppers represent **32% of customers (1,248 shoppers)** with a **higher average spend per basket (\$60.25 vs \$59.54 for males)**.
  - However, **0.0% of female customers are enrolled in the subscription program** and **0.0% received promotional discounts** due to the company's historical origins as a Men's Grooming club.
  - Converting 40% of female shoppers unlocks **+\$94,000+ in pure organic ARR (+40.3% revenue lift)** with zero CAC.
- **The Discount Trap:** Orders with applied discounts produced a lower AOV (**\$59.28** vs **\$60.13**) with no improvement in review rating (**3.74** vs **3.76**). Universal blanket discounting functions as an unrewarded margin leak.
- **Omnichannel Distribution:** Online parcel delivery commands **83.3% of revenue (\$194K)**, while In-Store Pickup (BOPIS) drives **16.7% (\$39K)**, providing prime foot-traffic upsell opportunities.
- **Payment Method Diversity:** Evenly distributed across PayPal (17.4%), Credit Card (17.2%), Cash (17.2%), Debit Card (16.3%), Venmo (16.3%), and Bank Transfer (15.7%).

---

## 📂 Repository Structure

```text
retail-customer-behavior-analysis/
│
├── data/
│   ├── raw/
│   │   └── customer_shopping_behavior.csv    # Original raw dataset (3,900 rows)
│   └── processed/
│       ├── cleaned_customer_shopping_behavior.csv # Cleaned & enriched flat data
│       ├── dim_customers.csv                 # Customer dimension with K-Means clusters
│       ├── dim_products.csv                  # Product catalog dimension
│       ├── dim_shipping.csv                  # Shipping & fulfillment channel dimension
│       ├── dim_payment.csv                   # Payment method dimension
│       ├── fact_transactions.csv             # Star schema central fact transactions table
│       └── retail_shopping.db                # SQLite database binary
│
├── src/
│   ├── 01_data_cleaning.py                   # Data cleansing & Star Schema export
│   ├── 02_customer_segmentation.py           # K-Means clustering (K=4) & profiling
│   └── 03_generate_visualizations.py         # Visual chart generation (7 PNG figures)
│
├── sql/
│   ├── 01_schema_setup.sql                   # DDL scripts, tables, foreign keys, views
│   ├── 02_business_queries.sql               # 10 production analytical business queries
│   └── run_sql_analysis.py                   # Python runner generating markdown outputs
│
├── power_bi/
│   ├── powerbi report.pbip                   # Native Power BI Developer Mode entry point
│   ├── powerbi report.Report/                # PBIR visual containers, canvas, & dark theme
│   └── powerbi report.SemanticModel/         # Fabric TMDL semantic model, tables, & DAX
│
├── reports/
│   ├── executive_report.html                 # Complete board report (styled HTML & PDF-ready)
│   ├── executive_project_report.md           # Complete board report (Markdown version)
│   ├── interactive_presentation.html         # Interactive full-screen web slide deck
│   ├── retail_customer_behavior_presentation.pptx # Native 16:9 executive PowerPoint deck
│   ├── stakeholder_presentation.md           # Slide deck content & executive speaking notes
│   └── sql_query_results.md                  # Complete SQL execution output tables
│
├── figures/
│   ├── 01_kmeans_elbow_silhouette.png        # Elbow & Silhouette cluster evaluation
│   ├── 02_customer_segments_scatter.png      # Cluster spend vs loyalty scatter
│   ├── 03_executive_overview_dashboard.png   # 4-panel executive dashboard overview
│   ├── 04_gender_subscription_discount_gap.png # Gender disparity comparison
│   ├── 05_marketing_drivers_analysis.png     # Discounts, shipping, payment analysis
│   ├── 06_seasonality_category_heatmap.png   # Seasonal category revenue heatmap
│   └── 07_loyalty_clv_comparison.png         # Lifetime value by loyalty tier
│
├── .gitignore
├── LICENSE                                   # Standard MIT License
├── requirements.txt                          # Python dependencies
└── README.md                                 # Project documentation
```

---

## 🛠️ Quickstart Pipeline Execution

### 1. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Execute Python Data & ML Pipeline
Run the core analytical steps sequentially:
```bash
# 1. Clean data and generate Star Schema CSVs
python src/01_data_cleaning.py

# 2. Run unsupervised K-Means behavioral clustering
python src/02_customer_segmentation.py

# 3. Generate 7 publication-ready figures
python src/03_generate_visualizations.py
```

> **Direct Deliverables:**
> - **PowerPoint Presentation:** Ready to open at [`reports/retail_customer_behavior_presentation.pptx`](reports/retail_customer_behavior_presentation.pptx).
> - **Power BI Cockpit:** Ready to launch directly at [`power_bi/powerbi report.pbip`](power_bi/powerbi%20report.pbip) (or as standalone `.pbix`).

### 3. Run Relational SQL Engine
```bash
python sql/run_sql_analysis.py
```
This initializes `retail_shopping.db`, executes all 10 analytical business queries, and outputs formatted Markdown tables to `reports/sql_query_results.md`.

---

## 📊 Launching the Power BI Cockpit

Double-click to open the project directly in **Power BI Desktop**:
```text
power_bi/powerbi report.pbip
```
- **Canvas Resolution:** Panoramic `1920 × 820` (ratio 2.28:1 tailored for 1080p monitors with zero vertical scrollbars).
- **Theme:** Executive Modern Dark Cockpit (`#0B1120` canvas, `#1E293B` containers, `#10B981` emerald hero card, `#38BDF8` neon cyan accents).
- **Interactive Lever:** Use the bottom-left slider controller to simulate female subscription adoption rates (0% to 100%) and watch the dual cyan callout cards (`🎯 TARGET ADOPTION` and `👥 NEW SUBSCRIBERS`) and emerald hero metric (`+$95K`) update in real-time.

---

## 💡 Strategic Recommendations Roadmap

1. **Launch Inclusive Loyalty Tier ("Omni-Her"):** Eliminate the historical men's club legacy by creating a premium subscription tier tailored for female shoppers with seasonal preview access and styling perks.
2. **Rationalize Discounts (End Blanket Margins):** Replace universal promo codes with **threshold discounts** (e.g. *"Spend \$85, Save \$15"*) to lift AOV above the current \$59.76 benchmark.
3. **Monetize BOPIS Traffic:** Drive in-store attach rates by granting a *"\$5 Off Today"* store voucher to shoppers collecting online orders.
4. **Merchandise Bundling:** Cross-merchandise high-performing Accessories (Jewelry, Scarves) alongside core Apparel (Blouses, Dresses) along checkout pathways.

---

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
