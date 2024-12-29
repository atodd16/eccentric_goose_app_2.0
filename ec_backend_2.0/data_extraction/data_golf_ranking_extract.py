# this script navigates to the data golf rankings webpage and downloads the most recent ranking csv and saves it to data_golf_ranking_files folder

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pandas as pd
from datetime import datetime, timedelta

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Specify the download directory
download_dir = r"C:\Users\aaron\OneDrive\Documents\Golf Modeling\eccentric_goose_model_app\ec_backend_2.0\data_files\raw_data_files\data_golf_ranking_files"
os.makedirs(download_dir, exist_ok=True)  # Ensure the directory exists

prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

options.add_experimental_option("prefs", prefs)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to the DataGolf Rankings page
driver.get('https://datagolf.com/datagolf-rankings')

# Allow time for the page to fully load
time.sleep(5)

# Extract the date string from the HTML element
date_element = driver.find_element(By.CSS_SELECTOR, 'span.selected-date')
date_string = date_element.text

# Convert the date string to a datetime object
date_object = datetime.strptime(date_string, '%B %d, %Y')

# Format the date in 'YYYYMMDD'
formatted_date = date_object.strftime('%Y%m%d')

# Wait for the download button to be clickable and then click it
try:
    wait = WebDriverWait(driver, 10)
    download_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "table-download"))
    )
    download_button.click()
    print("Download initiated.")
except Exception as e:
    print("An error occurred:", e)

# Allow time for the download to complete
time.sleep(10)  # Increased time to ensure download is complete

# Find the most recently downloaded file
list_of_files = os.listdir(download_dir)
latest_file = max([os.path.join(download_dir, f) for f in list_of_files], key=os.path.getctime)

# Name the new file
new_file_name = f"datagolf_rankings_{formatted_date}.csv"
new_file_path = os.path.join(download_dir, new_file_name)

# Rename the most recent file to the new file name
try:
    os.rename(latest_file, new_file_path)
    print(f"File renamed to {new_file_name}")
except Exception as e:
    print(f"An error occurred while renaming the file: {e}")

# Quit the WebDriver
driver.quit()

print('data golf ranking rile successfully saved')