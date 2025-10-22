# src/scrape_mlb_stats.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO  # Fix for FutureWarning

# -------------------------------
# Step 1: Load year links
# -------------------------------
year_links_df = pd.read_csv("../data/mlb_year_links.csv")

# -------------------------------
# Step 2: Fix URLs (remove incorrect prefix)
# -------------------------------
year_links_df['url'] = year_links_df['url'].str.replace(
    "yearmenu.shtml/", ""
)

# -------------------------------
# Step 3: Set headers for requests
# -------------------------------
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )
}

all_stats = []

# -------------------------------
# Step 4: Scrape each year
# -------------------------------
for _, row in year_links_df.iterrows():
    year = row["year"]
    url = row["url"]
    print(f"Scraping year: {year} -> {url}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Scrape all tables on the page
        tables = soup.find_all("table")
        for table in tables:
            # Wrap HTML string in StringIO to avoid FutureWarning
            df = pd.read_html(StringIO(str(table)))[0]
            df["Year"] = year
            all_stats.append(df)

        time.sleep(1)  # polite delay

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {year}: {e}")

# -------------------------------
# Step 5: Combine and save
# -------------------------------
if all_stats:
    final_df = pd.concat(all_stats, ignore_index=True)
    final_df.to_csv("../data/mlb_stats_all_years.csv", index=False)
    print(f"✅ Saved stats for all years to ../data/mlb_stats_all_years.csv")
else:
    print("No data scraped.")
