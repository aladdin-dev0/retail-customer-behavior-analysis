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
    persona_mapping = {
        0: "Young Emerging Shoppers",
        1: "Value-Seeking Occasionals",
        2: "High-Engagement Core Loyalists",
        3: "High-Basket Premium Shoppers"
    }

    df['customer_segment'] = df['cluster_id'].map(persona_mapping)

    # Calculate counts and percentages for display in the legend
    seg_counts = df['customer_segment'].value_counts()
    total_customers = len(df)
    display_map = {
        seg: f"{seg} (n={count:,} | {count/total_customers*100:.1f}%)"
        for seg, count in seg_counts.items()
    }
    df['segment_legend'] = df['customer_segment'].map(display_map)

    print("\n=== Customer Segment Distribution ===")
    for seg, count in seg_counts.items():
        print(f"{seg}: {count:,} customers ({count/total_customers*100:.1f}%)")

    # Save enriched datasets
    df.to_csv(csv_path, index=False)

    # Update dim_customers
    dim_cust_path = os.path.join(processed_dir, 'dim_customers.csv')
    if os.path.exists(dim_cust_path):
        dim_cust = pd.read_csv(dim_cust_path)
        if 'customer_segment' in dim_cust.columns:
            dim_cust.drop(columns=['cluster_id', 'customer_segment'], inplace=True, errors='ignore')
        dim_cust = dim_cust.merge(df[['customer_id', 'cluster_id', 'customer_segment']], on='customer_id', how='left')
        dim_cust.to_csv(dim_cust_path, index=False)
        print(f"[SUCCESS] Updated dim_customers with customer segments: {dim_cust_path}")

    # Plot Cluster Visualizations with enriched legend
    fig, ax = plt.subplots(figsize=(11, 6.5))
    sns.scatterplot(
        data=df,
        x='purchase_amount_usd',
        y='previous_purchases',
        hue='segment_legend',
        palette=['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728'],
        alpha=0.75,
        s=55,
        ax=ax
    )
    ax.set_title('Customer Segmentation: Spend vs Loyalty Depth', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Purchase Amount (USD)', fontsize=12)
    ax.set_ylabel('Previous Purchases (Loyalty Depth)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(title='Customer Persona (Size & Share)', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, fontsize=10, title_fontsize=11)
    plt.tight_layout()
    cluster_scatter_path = os.path.join(figures_dir, '02_customer_segments_scatter.png')
    plt.savefig(cluster_scatter_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved enhanced cluster scatter plot to: {cluster_scatter_path}")

if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    perform_segmentation(base_dir)
