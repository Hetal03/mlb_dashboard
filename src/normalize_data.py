# src/normalize_data.py

import pandas as pd

input_file = "../data/mlb_stats_all_years_cleaned.csv"
output_file = "../data/mlb_stats_all_years_normalized.csv"

print(f"✅ Loading cleaned data from {input_file}")
df = pd.read_csv(input_file)

# -------------------------------
# Step 1: Ensure proper column names
# -------------------------------
expected_cols = ["Statistic", "Player", "Team", "Value", "Rank", "Year"]
df.columns = expected_cols[:len(df.columns)]  # adjust if fewer columns

# -------------------------------
# Step 2: Clean numeric columns
# -------------------------------
# Remove commas and convert to numeric
df["Value"] = df["Value"].astype(str).str.replace(",", "", regex=False)
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")

# 🔹 Ensure Year is integer (helps with dropdown sorting)
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

# -------------------------------
# Step 3: Drop rows with missing key data
# -------------------------------
df = df.dropna(subset=["Player", "Statistic", "Value", "Year"])

# -------------------------------
# Step 4: Remove invalid Statistic or Team rows (extra safeguard)
# -------------------------------
invalid_patterns = r"click|navigation|previous|next|All Star|World Series|Roster|Season|Team|Navigation"
df = df[~df["Statistic"].str.contains(invalid_patterns, case=False, regex=True)]
df = df[df["Player"].str.len() > 0]
df = df[df["Team"].str.len() > 0]

# -------------------------------
# Step 5: Reset index
# -------------------------------
df = df.reset_index(drop=True)

# -------------------------------
# Step 6: Save normalized CSV
# -------------------------------
df.to_csv(output_file, index=False)
print(f"✅ Normalized data saved to {output_file}")
print(f"Data shape after normalization: {df.shape}")
print("\nSample data:")
print(df.head())
