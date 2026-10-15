"""
02_customer_segmentation.py
Machine Learning Customer Segmentation using K-Means Clustering
Project: Retail Customer Shopping Behavior Analysis
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def perform_segmentation(base_dir: str):
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    figures_dir = os.path.join(base_dir, 'figures')
    os.makedirs(figures_dir, exist_ok=True)

    csv_path = os.path.join(processed_dir, 'cleaned_customer_shopping_behavior.csv')
    df = pd.read_csv(csv_path)
    print(f"[INFO] Loaded cleaned dataset with shape: {df.shape}")

    # Features selected for behavioral clustering:
    # 1. age: demographic profile
    # 2. purchase_amount_usd: monetary spend per order
    # 3. previous_purchases: customer loyalty/historical volume
    # 4. annual_purchase_frequency: engagement cadence
    # 5. review_rating: customer satisfaction sentiment
    feature_cols = ['age', 'purchase_amount_usd', 'previous_purchases', 'annual_purchase_frequency', 'review_rating']
    X = df[feature_cols].copy()

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Test K from 2 to 7 to evaluate Elbow & Silhouette
    k_range = range(2, 8)
    inertias = []
    sil_scores = []

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)
        sil_scores.append(silhouette_score(X_scaled, km.labels_))

    # Plot Elbow & Silhouette
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(k_range, inertias, 'o-', color='#1f77b4', linewidth=2, markersize=8)
    axes[0].set_title('Elbow Method For Optimal k', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Number of Clusters (k)')
    axes[0].set_ylabel('Inertia (WCSS)')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    axes[1].plot(k_range, sil_scores, 's-', color='#2ca02c', linewidth=2, markersize=8)
    axes[1].set_title('Silhouette Score For Each k', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Number of Clusters (k)')
    axes[1].set_ylabel('Silhouette Score')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    elbow_fig_path = os.path.join(figures_dir, '01_kmeans_elbow_silhouette.png')
    plt.savefig(elbow_fig_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved cluster evaluation plot to: {elbow_fig_path}")

    # Fit chosen k=4 for meaningful retail business personas
    optimal_k = 4
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    df['cluster_id'] = kmeans.fit_predict(X_scaled)

    # Profile clusters
    cluster_profiles = df.groupby('cluster_id')[feature_cols].mean()
    print("\n=== Cluster Centers (Mean Values) ===")
    print(cluster_profiles)

    # Assign intuitive retail personas based on profiles
    # We inspect the relative positioning:
    # High previous purchases & high frequency -> VIP Loyalists
    # Low previous purchases & low frequency -> New / Occasional Shoppers
    # High spend vs low spend, younger vs older
    persona_mapping = {}
    for cid in range(optimal_k):
        row = cluster_profiles.loc[cid]
        if row['previous_purchases'] >= cluster_profiles['previous_purchases'].median() and row['annual_purchase_frequency'] >= cluster_profiles['annual_purchase_frequency'].median():
            persona = "High-Engagement Champions"
        elif row['purchase_amount_usd'] >= cluster_profiles['purchase_amount_usd'].median():
            persona = "High-Basket Premium Shoppers"
        elif row['age'] <= cluster_profiles['age'].median():
            persona = "Young Emerging Shoppers"
        else:
            persona = "Value-Seeking Occasionals"
        
        # Ensure unique labels
        if persona in persona_mapping.values():
            persona = f"{persona} (Tier {cid+1})"
        persona_mapping[cid] = persona

    df['customer_segment'] = df['cluster_id'].map(persona_mapping)

    print("\n=== Customer Segment Distribution ===")
    print(df['customer_segment'].value_counts())

    # Save enriched datasets
    df.to_csv(csv_path, index=False)

    # Update dim_customers
    dim_cust_path = os.path.join(processed_dir, 'dim_customers.csv')
    if os.path.exists(dim_cust_path):
        dim_cust = pd.read_csv(dim_cust_path)
        dim_cust = dim_cust.merge(df[['customer_id', 'cluster_id', 'customer_segment']], on='customer_id', how='left')
        dim_cust.to_csv(dim_cust_path, index=False)
        print(f"[SUCCESS] Updated dim_customers with customer segments: {dim_cust_path}")

    # Plot Cluster Visualizations
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x='purchase_amount_usd',
        y='previous_purchases',
        hue='customer_segment',
        palette='Set2',
        alpha=0.7,
        s=50,
        ax=ax
    )
    ax.set_title('Customer Segmentation: Spend vs Previous Purchases', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Purchase Amount (USD)', fontsize=12)
    ax.set_ylabel('Previous Purchases (Loyalty Depth)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()
    cluster_scatter_path = os.path.join(figures_dir, '02_customer_segments_scatter.png')
    plt.savefig(cluster_scatter_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved cluster scatter plot to: {cluster_scatter_path}")

if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    perform_segmentation(base_dir)
