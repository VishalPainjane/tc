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
    # Use a standard user-agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 2. Go to domain to set context
        print("Navigating to domain...")
        driver.get("https://toolkity.com/404")
        time.sleep(2)

        # 3. Inject Keys
        storage_json = os.environ.get('TOOLKITY_DATA')
        if not storage_json:
            print("CRITICAL ERROR: Secret is empty.")
            return

        data = json.loads(storage_json)
        for key, value in data.items():
            driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
        print("Keys injected.")

        # 4. Go to Profile
        print("Loading Profile Page...")
        driver.get("https://toolkity.com/twitter/free-twitter-followers/profile")
        time.sleep(8) # Wait longer for redirect/load

        # --- DIAGNOSTIC CHECK ---
        # print specific text to see if we are on the Login page
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print("PAGE TEXT PREVIEW (First 200 chars):")
        print(body_text[:200])
        
        if "Get a pin code" in body_text or "Login" in body_text:
            print("STATUS: LOGGED OUT (Login page detected)")
        else:
            print("STATUS: PROBABLY LOGGED IN")
        # ------------------------

        # 5. Try to Click
        try:
            start_btn = driver.find_element(By.XPATH, "//button[contains(., 'Start')]")
            start_btn.click()
            print("SUCCESS: Button Clicked!")
        except:
            print("ERROR: Start button not found.")

    except Exception as e:
        print(f"CRASH: {e}")

    finally:
        # 6. SAVE EVIDENCE (Screenshot & Source)
        print("Saving debug screenshots...")
        driver.save_screenshot("debug_screenshot.png")
        with open("debug_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        driver.quit()

if __name__ == "__main__":
    run_bot()