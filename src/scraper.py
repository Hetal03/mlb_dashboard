# src/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# -------------------------------
# STEP 1: Setup Chrome WebDriver
# -------------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# -------------------------------
# STEP 2: Open the MLB History page
# -------------------------------
url = "https://www.baseball-almanac.com/yearmenu.shtml"
driver.get(url)
time.sleep(5)  # wait for the page to fully load

# -------------------------------
# STEP 3: Extract data elements
# -------------------------------
# Note: we’ll locate each event block — year, title, and description
events = driver.find_elements(By.CSS_SELECTOR, "section.mlb-history__year-section")

data = []

for event in events:
    try:
        year = event.find_element(By.CSS_SELECTOR, "h2").text.strip()
        items = event.find_elements(By.CSS_SELECTOR, "li.mlb-history__event")
        
        for i in items:
            title = i.find_element(By.CSS_SELECTOR, "h3").text.strip() if i.find_elements(By.CSS_SELECTOR, "h3") else "N/A"
            desc = i.find_element(By.CSS_SELECTOR, "p").text.strip() if i.find_elements(By.CSS_SELECTOR, "p") else "N/A"
            data.append({"year": year, "event": title, "description": desc})
    except Exception as e:
        print("Error while parsing:", e)

# ----------------------------------
# STEP 4: Save to CSV
# -------------------------------

df = pd.DataFrame(data)
df.to_csv("../data/mlb_history_events.csv", index=False)
print(f"✅ Scraped {len(df)} events and saved to ../data/mlb_history_events.csv")

# -------------------------------
# STEP 5: Close driver
# -------------------------------
driver.quit()
