from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv
import os

# --- CONFIGURATION ---
# Load the environment variables from the .env file
load_dotenv()

# EMAIL = os.getenv("EMAIL", "your_email@example.com")  # Use environment variables
# PASSWORD = os.getenv("PASSWORD", "your_password")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
NEW_SUMMARY = "Software Developer with 3 years of experience in building high-performance web apps using Java, Spring Boot, JPA, SQL, and React. Skilled in integrating APIs, AWS services, and object detection models. Passionate about performance optimization."

# --- FASTAPI SETUP ---
app = FastAPI()

def update_naukri_resume():
    print("▶️ Running update at", time.strftime("%Y-%m-%d %H:%M:%S"))

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # STEP 1: Open Naukri and Login
        driver.get("https://www.naukri.com/")
        time.sleep(3)

        driver.find_element(By.ID, "login_Layer").click()
        time.sleep(2)

        email_input = driver.find_element(By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']")
        email_input.send_keys(EMAIL)
        time.sleep(1)

        password_input = driver.find_element(By.XPATH, "//input[@placeholder='Enter your password']")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # STEP 2: Go to Profile Page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # STEP 3: Click 'Edit' in Resume Headline Section
        edit_button = driver.find_element(By.XPATH, "//div[@id='lazyResumeHead']//span[@class='edit icon']")
        edit_button.click()
        time.sleep(2)

        # STEP 4: Update Resume Headline
        textarea = driver.find_element(By.ID, "resumeHeadlineTxt")
        driver.execute_script("arguments[0].scrollIntoView(true);", textarea)
        time.sleep(1)

        textarea.clear()
        textarea.click()
        time.sleep(1)

        textarea.send_keys(NEW_SUMMARY)
        time.sleep(2)

        driver.execute_script("arguments[0].blur();", textarea)
        time.sleep(1)

        # STEP 5: Save
        save_button = driver.find_element(By.XPATH, "//form[@name='resumeHeadlineForm']//button[text()='Save']")
        save_button.click()
        time.sleep(3)

        print("✅ Resume headline updated successfully!")

    except Exception as e:
        print("❌ Error occurred:", e)

    finally:
        driver.quit()

# --- SCHEDULER SETUP ---
scheduler = BackgroundScheduler()

# Schedule the task to run everyday at 4:00 AM
scheduler.add_job(update_naukri_resume, 'cron', hour=4, minute=0)

scheduler.start()

# --- ROUTES FOR TESTING ---
@app.get("/")
def root():
    return {"message": "Naukri Auto Updater is Running!"}

@app.get("/test-update")
def test_update():
    update_naukri_resume()
    return {"message": "Manual update triggered!"}
