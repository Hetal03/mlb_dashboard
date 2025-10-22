import pandas as pd

# Step 7: Read in the CSV of MLB year links
year_links = pd.read_csv('../data/mlb_year_links.csv')

# Display the first few rows
print(year_links.head())

# Display how many years/rows we have
print("\nTotal years:", len(year_links))
