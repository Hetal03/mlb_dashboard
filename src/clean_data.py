
# src/clean_data.py
import pandas as pd

input_file = "../data/mlb_stats_all_years.csv"
output_file = "../data/mlb_stats_all_years_cleaned.csv"

print(f"✅ Loading data from {input_file}")
df = pd.read_csv(input_file)

print(f"\nData shape before cleaning: {df.shape}")
print(f"Columns: {list(df.columns)}")

# -------------------------------
# Step 1: Drop irrelevant columns
# -------------------------------
# Keep only first 6 columns if your data has extra junk columns
df = df.iloc[:, :6]

# -------------------------------
# Step 2: Rename columns
# -------------------------------
df.columns = ["Statistic", "Player", "Team", "Value", "Rank", "Year"]

# -------------------------------
# Step 3: Remove junk rows (headers, navigation, etc.)
# -------------------------------
df = df[~df["Statistic"].str.contains("Player Review|Statistic|navigation|previous|next|All Star|World Series", 
                                      case=False, na=False)]

# -------------------------------
# Step 4: Drop rows with missing or invalid values
# -------------------------------
df = df[df["Player"].notna() & df["Team"].notna() & df["Statistic"].notna()]

# -------------------------------
# Step 5: Convert numeric columns
# -------------------------------
df["Value"] = pd.to_numeric(df["Value"].astype(str).str.replace(",", ""), errors="coerce")
df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

df = df.dropna(subset=["Year"])
df["Year"] = df["Year"].astype(int)

# -------------------------------
# Step 6: Save cleaned file
# -------------------------------
df.to_csv(output_file, index=False)

print(f"✅ Cleaned data saved to {output_file}")
print(f"Data shape after cleaning: {df.shape}")
print("\nSample data:")
print(df.head())


""" # src/clean_data.py

import pandas as pd

# -------------------------------
# Step 1: Load scraped data
# -------------------------------
# input_file = "../data/mlb_stats_all_years_test.csv"
input_file = "../data/mlb_stats_all_years.csv"
output_file = "../data/mlb_stats_all_years_cleaned.csv"

print(f"✅ Loading data from {input_file}")
df = pd.read_csv(input_file)

print(f"\nData shape before cleaning: {df.shape}")
print(f"Columns: {list(df.columns)}")
print("\nSample data:")
print(df.head())

# -------------------------------
# Step 2: Drop rows that are not actual stats
# -------------------------------
# Remove rows where first column contains the year repeated or headers like 'Statistic'
df = df[~df['0'].str.contains('Player Review|Statistic', na=False)]
df = df[~df['0'].str.match(r'^\d{4}', na=False)]  # remove rows that start with year like '1901 ...'

# -------------------------------
# Step 3: Standardize column names
# -------------------------------
# We'll assume the scraped tables are mostly: Statistic | Player | Team | Value | Rank | Year
# Rename columns if there are exactly 6 columns
if df.shape[1] == 6:
    df.columns = ["Statistic", "Player", "Team", "Value", "Rank", "Year"]

# -------------------------------
# Step 4: Clean missing values
# -------------------------------
for col in df.columns:
    if df[col].dtype in ['float64', 'int64']:
        df[col] = df[col].fillna(0)
    else:
        df[col] = df[col].fillna("")


# 🔹 NEW STEP: Filter out invalid or junk rows
df = df[df["Player"].notna() & df["Team"].notna()]
df = df[~df["Statistic"].str.contains(
    r"click|navigation|previous|next|All Star|World Series|Roster|Season|Team|Navigation",
    case=False, regex=True
)]

# 🔹 NEW STEP: Keep only valid statistic names
valid_stats = [
    "Base on Balls", "Batting Average", "Doubles", "Hits", "Home Runs",
    "On Base Percentage", "RBI", "Runs", "Slugging Average", "Stolen Bases",
    "Total Bases", "Triples", "Complete Games", "ERA", "Games", "Saves",
    "Shutouts", "Strikeouts", "Winning Percentage", "Wins",
    "Fewest Hits Allowed", "Fewest Home Runs Allowed", "Fewest Walks Allowed"
]
df = df[df["Statistic"].isin(valid_stats)]

# 🔹 Convert Year to integer (to fix dropdown issue)
df["Year"] = df["Year"].astype(int, errors='ignore')




# -------------------------------
# Step 5: Save cleaned CSV
# -------------------------------
df.to_csv(output_file, index=False)
print(f"✅ Cleaned data saved to {output_file}")
print(f"Data shape after cleaning: {df.shape}")
 """