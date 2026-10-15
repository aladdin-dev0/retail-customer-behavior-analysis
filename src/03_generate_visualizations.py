"""
03_generate_visualizations.py
Generates executive-ready visual charts and dashboard previews.
Project: Retail Customer Shopping Behavior Analysis
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set professional plotting style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

def generate_charts(base_dir: str):
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    figures_dir = os.path.join(base_dir, 'figures')
    os.makedirs(figures_dir, exist_ok=True)

    csv_path = os.path.join(processed_dir, 'cleaned_customer_shopping_behavior.csv')
    df = pd.read_csv(csv_path)
    print(f"[INFO] Loaded cleaned dataset with shape: {df.shape}")

    # -------------------------------------------------------------
    # 1. Executive Summary Dashboard (4-panel overview)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1a. Revenue by Category
    cat_rev = df.groupby('category')['purchase_amount_usd'].sum().sort_values(ascending=False)
    sns.barplot(x=cat_rev.values, y=cat_rev.index, palette='Blues_r', ax=axes[0, 0])
    axes[0, 0].set_title('Total Revenue by Category ($)', fontsize=14, fontweight='bold', pad=10)
    axes[0, 0].set_xlabel('Revenue (USD)', fontsize=11)
    for i, v in enumerate(cat_rev.values):
        axes[0, 0].text(v + 1000, i, f"${v:,.0f}", va='center', fontweight='bold', fontsize=10)

    # 1b. Age Demographics & Gender Count
    sns.countplot(data=df, x='age_group', hue='gender', palette=['#ff7f0e', '#1f77b4'], ax=axes[0, 1])
    axes[0, 1].set_title('Customer Volume by Age Cohort & Gender', fontsize=14, fontweight='bold', pad=10)
    axes[0, 1].set_xlabel('Age Cohort', fontsize=11)
    axes[0, 1].set_ylabel('Number of Customers', fontsize=11)
    axes[0, 1].legend(title='Gender')

    # 1c. Sales Channel Share (Pie / Donut)
    channel_counts = df['sales_channel'].value_counts()
    colors = ['#2ca02c', '#17becf']
    axes[1, 0].pie(channel_counts, labels=channel_counts.index, autopct='%1.1f%%', startangle=140, 
                   colors=colors, wedgeprops=dict(width=0.4, edgecolor='w'))
    axes[1, 0].set_title('Sales Channel Fulfillment Share', fontsize=14, fontweight='bold', pad=10)

    # 1d. Top 8 Best-Selling Items by Total Sales
    top_items = df.groupby('item_purchased')['purchase_amount_usd'].sum().sort_values(ascending=False).head(8)
    sns.barplot(x=top_items.values, y=top_items.index, palette='crest', ax=axes[1, 1])
    axes[1, 1].set_title('Top 8 Items by Revenue ($)', fontsize=14, fontweight='bold', pad=10)
    axes[1, 1].set_xlabel('Revenue (USD)', fontsize=11)
    for i, v in enumerate(top_items.values):
        axes[1, 1].text(v + 150, i, f"${v:,.0f}", va='center', fontsize=9)

    plt.tight_layout()
    p1 = os.path.join(figures_dir, '03_executive_overview_dashboard.png')
    plt.savefig(p1, dpi=300)
    plt.close()
    print(f"[SUCCESS] Saved: {p1}")

    # -------------------------------------------------------------
    # 2. Gender Discrepancy & Opportunity: Subscription & Discounts
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Subscription Rate by Gender
    sub_gender = pd.crosstab(df['gender'], df['subscription_status'], normalize='index') * 100
    sub_gender.plot(kind='bar', stacked=True, color=['#d62728', '#2ca02c'], ax=axes[0], rot=0)
    axes[0].set_title('Subscription Adoption by Gender (% Stacked)', fontsize=13, fontweight='bold')
    axes[0].set_ylabel('Percentage (%)', fontsize=11)
    axes[0].set_xlabel('Gender', fontsize=11)
    axes[0].legend(title='Subscribed')

    # Discount Applied by Gender
    disc_gender = pd.crosstab(df['gender'], df['discount_applied'], normalize='index') * 100
    disc_gender.plot(kind='bar', stacked=True, color=['#7f7f7f', '#1f77b4'], ax=axes[1], rot=0)
    axes[1].set_title('Discount / Promo Penetration by Gender (% Stacked)', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('Percentage (%)', fontsize=11)
    axes[1].set_xlabel('Gender', fontsize=11)
    axes[1].legend(title='Discount Applied')

    plt.tight_layout()
    p2 = os.path.join(figures_dir, '04_gender_subscription_discount_gap.png')
    plt.savefig(p2, dpi=300)
    plt.close()
    print(f"[SUCCESS] Saved: {p2}")

    # -------------------------------------------------------------
    # 3. Marketing Drivers: Discounts, Shipping & Payment
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # AOV: Discount vs No Discount
    sns.boxplot(data=df, x='discount_applied', y='purchase_amount_usd', palette='Set2', ax=axes[0])
    axes[0].set_title('Basket Spend ($): Discount vs Full Price', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Discount Applied', fontsize=11)
    axes[0].set_ylabel('Purchase Amount (USD)', fontsize=11)

    # Shipping Type Satisfaction
    ship_rating = df.groupby('shipping_type')['review_rating'].mean().sort_values(ascending=True)
    sns.barplot(x=ship_rating.values, y=ship_rating.index, palette='mako', ax=axes[1])
    axes[1].set_title('Average Customer Rating by Shipping Type', fontsize=12, fontweight='bold')
    axes[1].set_xlim(3.0, 4.0)
    axes[1].set_xlabel('Mean Rating (1 to 5)', fontsize=11)

    # Payment Methods Popularity
    pay_counts = df['payment_method'].value_counts()
    sns.barplot(x=pay_counts.values, y=pay_counts.index, palette='flare', ax=axes[2])
    axes[2].set_title('Transaction Volume by Payment Method', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Transactions Count', fontsize=11)

    plt.tight_layout()
    p3 = os.path.join(figures_dir, '05_marketing_drivers_analysis.png')
    plt.savefig(p3, dpi=300)
    plt.close()
    print(f"[SUCCESS] Saved: {p3}")

    # -------------------------------------------------------------
    # 4. Seasonal & Category Heatmap Matrix
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    season_cat_pivot = pd.pivot_table(
        df, 
        values='purchase_amount_usd', 
        index='category', 
        columns='season', 
        aggfunc='sum'
    )
    sns.heatmap(season_cat_pivot, annot=True, fmt=',.0f', cmap='YlGnBu', cbar_kws={'label': 'Total Revenue ($)'})
    plt.title('Category Revenue Across Seasons (USD Heatmap)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Product Category', fontsize=12)
    plt.tight_layout()
    p4 = os.path.join(figures_dir, '06_seasonality_category_heatmap.png')
    plt.savefig(p4, dpi=300)
    plt.close()
    print(f"[SUCCESS] Saved: {p4}")

    # -------------------------------------------------------------
    # 5. Customer Loyalty & Lifetime Value (CLV)
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 5))
    loyalty_order = ['Bronze (1-15)', 'Silver (16-30)', 'Gold (31-45)', 'Platinum (46+)']
    sns.barplot(data=df, x='loyalty_tier', y='estimated_clv', order=loyalty_order, palette='viridis', ci=None)
    plt.title('Average Estimated Customer Lifetime Value (CLV) by Loyalty Tier', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel('Customer Loyalty Tier (Past Purchases)', fontsize=12)
    plt.ylabel('Estimated Lifetime Spend (USD)', fontsize=12)
    plt.tight_layout()
    p5 = os.path.join(figures_dir, '07_loyalty_clv_comparison.png')
    plt.savefig(p5, dpi=300)
    plt.close()
    print(f"[SUCCESS] Saved: {p5}")

if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    generate_charts(base_dir)
