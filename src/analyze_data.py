# src/analyze_data.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Step 1: Load normalized data
# -------------------------------
df = pd.read_csv("../data/mlb_stats_all_years_normalized.csv")
print("✅ Loaded normalized data")
print(f"Data shape: {df.shape}")
print(df.head())

# -------------------------------
# Step 2: Compute ranks per Statistic per Year
# -------------------------------
df['Rank'] = df.groupby(['Year', 'Statistic'])['Value'] \
               .rank(ascending=False, method='min')

print("✅ Player ranks computed")

# -------------------------------
# Step 3: Save ranked data
# -------------------------------
df.to_csv("../data/mlb_stats_all_years_ranked.csv", index=False)
print("✅ Ranked data saved to ../data/mlb_stats_all_years_ranked.csv")

# -------------------------------
# Step 4: Visualizations
# -------------------------------

# Set plot style
sns.set_style("whitegrid")

# Example 1: Top 10 Home Run Hitters in a given year
year_to_plot = 1901
top_hr = df[(df['Year'] == year_to_plot) & (df['Statistic'] == 'Home Runs')] \
            .sort_values('Value', ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x='Value', y='Player', data=top_hr, palette='rocket')
plt.title(f"Top 10 Home Run Hitters in {year_to_plot}")
plt.xlabel("Home Runs")
plt.ylabel("Player")
plt.tight_layout()
plt.show()

# Example 2: Trend of Batting Average over years for a player
player_to_plot = "Nap Lajoie"
player_ba = df[(df['Player'] == player_to_plot) & (df['Statistic'] == 'Batting Average')]

plt.figure(figsize=(12,6))
sns.lineplot(x='Year', y='Value', data=player_ba, marker='o')
plt.title(f"Batting Average Trend Over Time: {player_to_plot}")
plt.xlabel("Year")
plt.ylabel("Batting Average")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Example 3: Top 5 Home Run Hitters per decade
df['Decade'] = (df['Year'] // 10) * 10
top_hr_decade = df[df['Statistic'] == 'Home Runs'].groupby(['Decade', 'Player'])['Value'] \
                 .sum().reset_index().sort_values(['Decade','Value'], ascending=[True, False])

top5_hr_decade = top_hr_decade.groupby('Decade').head(5)

plt.figure(figsize=(14,8))
sns.barplot(x='Value', y='Player', hue='Decade', data=top5_hr_decade)
plt.title("Top 5 Home Run Hitters per Decade")
plt.xlabel("Total Home Runs")
plt.ylabel("Player")
plt.legend(title='Decade')
plt.tight_layout()
plt.show()

print("✅ Visualization complete")
