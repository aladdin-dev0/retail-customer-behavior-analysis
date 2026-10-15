"""
01_data_cleaning.py
Data Cleaning, Transformation, and Feature Engineering
Project: Retail Customer Shopping Behavior Analysis
"""

import os
import pandas as pd
import numpy as np

def load_data(raw_data_path: str) -> pd.DataFrame:
    """Loads raw dataset from csv."""
    if not os.path.exists(raw_data_path):
        raise FileNotFoundError(f"File not found: {raw_data_path}")
    print(f"[INFO] Loading raw data from: {raw_data_path}")
    df = pd.read_csv(raw_data_path)
    print(f"[INFO] Loaded shape: {df.shape}")
    return df

def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans columns, handles missing values, and performs feature engineering."""
    df_clean = df.copy()

    # Standardize column names to snake_case
    df_clean.columns = (
        df_clean.columns.str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('(', '', regex=False)
        .str.replace(')', '', regex=False)
    )

    # Validate duplicates
    duplicate_count = df_clean.duplicated().sum()
    print(f"[INFO] Duplicate rows detected: {duplicate_count}")

    # Handle missing values in review_rating
    missing_ratings = df_clean['review_rating'].isnull().sum()
    print(f"[INFO] Missing review_rating count: {missing_ratings}")
    
    # Track imputation with indicator
    df_clean['review_rating_imputed'] = df_clean['review_rating'].isnull().astype(int)
    
    # Impute missing review_rating with category-level median
    category_medians = df_clean.groupby('category')['review_rating'].transform('median')
    df_clean['review_rating'] = df_clean['review_rating'].fillna(category_medians).round(2)

    # --- Feature Engineering ---

    # 1. Age Demographics
    bins = [17, 25, 35, 50, 70]
    labels = ['18-25 (Young Adult)', '26-35 (Early Career)', '36-50 (Mid Career)', '51-70 (Senior)']
    df_clean['age_group'] = pd.cut(df_clean['age'], bins=bins, labels=labels)

    # 2. Sales Channel: Offline vs Online Delivery
    # 'Store Pickup' represents in-store/BOPIS, all other shipping types are online parcel shipping
    df_clean['sales_channel'] = np.where(
        df_clean['shipping_type'].str.lower() == 'store pickup',
        'In-Store Pickup',
        'Online Shipping'
    )

    # 3. Frequency mapping to annualized frequency
    freq_map = {
        'Weekly': 52,
        'Bi-Weekly': 26,
        'Fortnightly': 26,
        'Monthly': 12,
        'Every 3 Months': 4,
        'Quarterly': 4,
        'Annually': 1
    }
    df_clean['annual_purchase_frequency'] = df_clean['frequency_of_purchases'].map(freq_map).fillna(12).astype(int)

    # 4. Estimated Annual Spend
    df_clean['estimated_annual_spend'] = (
        df_clean['annual_purchase_frequency'] * df_clean['purchase_amount_usd']
    ).round(2)

    # 5. Customer Lifetime Value (CLV/LTV) Estimate based on previous purchases + current purchase
    df_clean['estimated_clv'] = (
        (df_clean['previous_purchases'] + 1) * df_clean['purchase_amount_usd']
    ).round(2)

    # 6. Spending Tier
    # min: 20, 25%: 39, median: 60, 75%: 81, max: 100
    spending_bins = [0, 40, 70, 1000]
    spending_labels = ['Budget (<$40)', 'Standard ($40-$70)', 'Premium (>$70)']
    df_clean['spending_tier'] = pd.cut(df_clean['purchase_amount_usd'], bins=spending_bins, labels=spending_labels)

    # 7. Loyalty Tier based on Previous Purchases
    loyalty_bins = [-1, 15, 30, 45, 100]
    loyalty_labels = ['Bronze (1-15)', 'Silver (16-30)', 'Gold (31-45)', 'Platinum (46+)']
    df_clean['loyalty_tier'] = pd.cut(df_clean['previous_purchases'], bins=loyalty_bins, labels=loyalty_labels)

    # 8. Customer Satisfaction Band
    satisfaction_bins = [0, 2.99, 3.99, 5.0]
    satisfaction_labels = ['Low (<3.0)', 'Moderate (3.0-3.9)', 'High (4.0-5.0)']
    df_clean['satisfaction_level'] = pd.cut(df_clean['review_rating'], bins=satisfaction_bins, labels=satisfaction_labels)

    print(f"[INFO] Cleaned data shape: {df_clean.shape}")
    return df_clean

def export_star_schema(df: pd.DataFrame, processed_dir: str):
    """Normalizes the flat dataset into dimensional star schema tables for SQL and Power BI."""
    os.makedirs(processed_dir, exist_ok=True)

    # 1. dim_customers
    dim_customers = df[[
        'customer_id', 'age', 'age_group', 'gender', 'location', 
        'subscription_status', 'loyalty_tier'
    ]].drop_duplicates().sort_values('customer_id')

    # 2. dim_products
    dim_products = df[[
        'item_purchased', 'category', 'size', 'color'
    ]].drop_duplicates().reset_index(drop=True)
    dim_products['product_id'] = dim_products.index + 1
    dim_products = dim_products[['product_id', 'item_purchased', 'category', 'size', 'color']]

    # 3. dim_shipping_channel
    dim_shipping = df[['shipping_type', 'sales_channel']].drop_duplicates().reset_index(drop=True)
    dim_shipping['shipping_id'] = dim_shipping.index + 1
    dim_shipping = dim_shipping[['shipping_id', 'shipping_type', 'sales_channel']]

    # 4. dim_payment
    dim_payment = df[['payment_method']].drop_duplicates().reset_index(drop=True)
    dim_payment['payment_id'] = dim_payment.index + 1
    dim_payment = dim_payment[['payment_id', 'payment_method']]

    # Merge keys to build fact_transactions
    fact = df.merge(dim_products, on=['item_purchased', 'category', 'size', 'color'], how='left')
    fact = fact.merge(dim_shipping, on=['shipping_type', 'sales_channel'], how='left')
    fact = fact.merge(dim_payment, on=['payment_method'], how='left')

    fact['transaction_id'] = np.arange(1001, 1001 + len(fact))
    fact_transactions = fact[[
        'transaction_id', 'customer_id', 'product_id', 'shipping_id', 'payment_id',
        'season', 'purchase_amount_usd', 'review_rating', 'review_rating_imputed',
        'discount_applied', 'promo_code_used', 'previous_purchases',
        'frequency_of_purchases', 'annual_purchase_frequency',
        'estimated_annual_spend', 'estimated_clv', 'spending_tier', 'satisfaction_level'
    ]]

    # Save flat cleaned table
    flat_path = os.path.join(processed_dir, 'cleaned_customer_shopping_behavior.csv')
    df.to_csv(flat_path, index=False)
    print(f"[SUCCESS] Exported flat cleaned dataset: {flat_path}")

    # Save Star Schema tables
    dim_customers.to_csv(os.path.join(processed_dir, 'dim_customers.csv'), index=False)
    dim_products.to_csv(os.path.join(processed_dir, 'dim_products.csv'), index=False)
    dim_shipping.to_csv(os.path.join(processed_dir, 'dim_shipping.csv'), index=False)
    dim_payment.to_csv(os.path.join(processed_dir, 'dim_payment.csv'), index=False)
    fact_transactions.to_csv(os.path.join(processed_dir, 'fact_transactions.csv'), index=False)
    print(f"[SUCCESS] Exported Star Schema tables to: {processed_dir}")

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_path = os.path.join(base_dir, 'data', 'raw', 'customer_shopping_behavior.csv')
    processed_dir = os.path.join(base_dir, 'data', 'processed')

    df_raw = load_data(raw_path)
    df_clean = clean_and_transform(df_raw)
    export_star_schema(df_clean, processed_dir)
    print("[ALL DONE] Data Preparation and Star Schema modeling completed successfully.")

if __name__ == '__main__':
    main()
