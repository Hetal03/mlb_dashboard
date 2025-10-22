# src/visualize_data.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -------------------------------
# Step 1: Load normalized data
# -------------------------------
data_path = "../data/mlb_stats_all_years_normalized.csv"
df = pd.read_csv(data_path)
print(f"✅ Loaded normalized data from {data_path}")
print(f"Data shape: {df.shape}")

# Ensure plots folder exists
plots_dir = "../plots"
os.makedirs(plots_dir, exist_ok=True)

# -------------------------------
# Step 2: Top players per year
# -------------------------------
top_stats = ['Hits', 'Home Runs', 'Batting Average', 'Base on Balls']

for stat in top_stats:
    plt.figure(figsize=(12,6))
    # Filter for the stat
    stat_df = df[df['Statistic'] == stat].copy()
    # Take top 5 players per year
    top_players = stat_df.sort_values(['Year', 'Value'], ascending=[True, False]).groupby('Year').head(5)
    sns.barplot(x='Year', y='Value', hue='Player', data=top_players)
    plt.title(f"Top 5 Players per Year: {stat}")
    plt.xticks(rotation=90)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"{plots_dir}/top5_{stat.replace(' ', '_')}.png")
    plt.close()
    print(f"✅ Saved top 5 {stat} plot")

# -------------------------------
# Step 3: Trend of average stats over time
# -------------------------------
for stat in top_stats:
    plt.figure(figsize=(12,6))
    stat_df = df[df['Statistic'] == stat].copy()
    avg_per_year = stat_df.groupby('Year')['Value'].mean().reset_index()
    sns.lineplot(x='Year', y='Value', data=avg_per_year, marker='o')
    plt.title(f"Average {stat} per Year")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{plots_dir}/avg_{stat.replace(' ', '_')}.png")
    plt.close()
    print(f"✅ Saved average {stat} trend plot")

# -------------------------------
# Step 4: Distribution of stats
# -------------------------------
for stat in top_stats:
    plt.figure(figsize=(10,6))
    stat_df = df[df['Statistic'] == stat].copy()
    sns.histplot(stat_df['Value'], bins=20, kde=True)
    plt.title(f"Distribution of {stat}")
    plt.tight_layout()
    plt.savefig(f"{plots_dir}/dist_{stat.replace(' ', '_')}.png")
    plt.close()
    print(f"✅ Saved {stat} distribution plot")

# -------------------------------
# Step 5: Correlation between key stats
# -------------------------------
# Pivot data to wide format for correlations
pivot_df = df.pivot_table(index=['Player', 'Year'], columns='Statistic', values='Value').reset_index()
corr_stats = ['Hits', 'Home Runs', 'Batting Average', 'Base on Balls']
corr_matrix = pivot_df[corr_stats].corr()

plt.figure(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between Key Stats")
plt.tight_layout()
plt.savefig(f"{plots_dir}/stats_correlation.png")
plt.close()
print("✅ Saved correlation heatmap")

print("🎉 All visualizations saved in ../plots/")
