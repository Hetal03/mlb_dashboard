import requests
from bs4 import BeautifulSoup
import pandas as pd

# -------------------------------
# STEP 1: Fetch the page with headers
# -------------------------------
url = "https://www.baseball-almanac.com/yearmenu.shtml"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url, headers=headers)
response.raise_for_status()

# -------------------------------
# STEP 2: Parse HTML
# -------------------------------
soup = BeautifulSoup(response.text, "html.parser")

# -------------------------------
# STEP 3: Find all year links
# -------------------------------
links = soup.find_all("a", href=True)

year_data = []

for link in links:
    href = link["href"]
    text = link.get_text(strip=True)

    if href.startswith("yearly/yr") and text.isdigit():
        full_url = f"https://www.baseball-almanac.com/yearmenu.shtml/{href}"
        year_data.append({"year": int(text), "url": full_url})

# -------------------------------
# STEP 4: Save as CSV
# -------------------------------
df = pd.DataFrame(year_data)
df.to_csv("../data/mlb_year_links.csv", index=False)

print(f"✅ Extracted {len(df)} year links and saved to ../data/mlb_year_links.csv")
print(df.head())
