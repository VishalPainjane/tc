import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def run_bot():
    # 1. Setup Cloud Browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Mask automation to look like a real Windows PC
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    # 2. Go to the domain first (Required to inject storage)
    print("Navigating to domain...")
    driver.get("https://toolkity.com/404") 
    time.sleep(2)

    # 3. Inject Your Keys
    storage_json = os.environ.get('TOOLKITY_DATA')
    if not storage_json:
        print("CRITICAL ERROR: 'TOOLKITY_DATA' secret is missing or empty.")
        driver.quit()
        return

    try:
        data = json.loads(storage_json)
        # Inject the specific keys you found
        for key, value in data.items():
            driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
        print("Authentication keys injected successfully.")
    except Exception as e:
        print(f"Error reading JSON secret: {e}")
        driver.quit()
        return

    # 4. Go to the Profile Page
    print("Loading Profile Page...")
    driver.get("https://toolkity.com/twitter/free-twitter-followers/profile")
    time.sleep(5) 

    # 5. Click the "Start" Button
    try:
        # Strategy 1: Find by the specific icon class you showed earlier
        try:
            print("Attempting to find button by Icon...")
            start_btn = driver.find_element(By.CSS_SELECTOR, "i.mdi-play-speed")
            # Click the parent button of the icon
            start_btn.find_element(By.XPATH, "./..").click()
            print("SUCCESS: Clicked button via Icon strategy.")
        except:
            # Strategy 2: Find by text "Start"
            print("Icon strategy failed. Trying Text strategy...")
            driver.find_element(By.XPATH, "//button[contains(., 'Start')]").click()
            print("SUCCESS: Clicked button via Text strategy.")

        # Wait to ensure the server registers the click
        time.sleep(10)
        
    except Exception as e:
        print(f"FAILED to find or click button. Error: {e}")
        # Debugging: Print title to see if we are actually logged in
        print("Current Page Title:", driver.title)

    driver.quit()

if __name__ == "__main__":
    run_bot()