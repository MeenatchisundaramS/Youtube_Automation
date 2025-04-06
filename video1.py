import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")

service = Service("D:/video_automation/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

def upload_video(video_path, video_title, description, visibility):
    video_path = os.path.abspath(video_path)
    default_title = os.path.splitext(os.path.basename(video_path))[0]

    driver.get("https://studio.youtube.com")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//ytcp-button[contains(@label, 'Create')]")))
    create_button = driver.find_element(By.XPATH, "//ytcp-button[contains(@label, 'Create')]")
    create_button.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//yt-formatted-string[text()='Upload videos']"))).click()

    file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
    file_input.send_keys(video_path)
    print("Uploading video... Please wait for YouTube to process.")

    # Title Handling
    try:
        title_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='textbox' and @aria-label='Add a title that describes your video (type @ to mention a channel)']"))
        )
        driver.execute_script("arguments[0].innerText = '';", title_box)
        time.sleep(1)
        title_box.click()
        title_box.send_keys(video_title)
        print("Title entered successfully.")
    except Exception as e:
        print("Error setting video title:", e)

    # Description Handling
    try:
        description_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='description-container']//div[@id='textbox']"))
        )
        description_box.click()
        time.sleep(1)
        description_box.send_keys(description)
        print("Description entered successfully.")
    except Exception as e:
        print("Error entering description:", e)

    # Not Made for Kids Selection
    try:
        not_made_for_kids = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-radio-button[@name='VIDEO_MADE_FOR_KIDS_NOT_MFK']"))
        )
        driver.execute_script("arguments[0].click();", not_made_for_kids)
        print("Selected: Not made for kids")
    except Exception as e:
        print("Error clicking 'Not made for kids':", e)

    # Click "Next" Buttons
    while True:
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//ytcp-button[contains(@label, 'Next')]"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)
            print("Clicked Next button...")
        except:
            print("No more Next buttons. Moving to visibility section.")
            break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Visibility Setting
    try:
        visibility = visibility.lower()
        visibility_map = {
            "public": "PUBLIC",
            "unlisted": "UNLISTED",
            "private": "PRIVATE"
        }

        if visibility not in visibility_map:
            print("Invalid visibility input. Choose from: public, unlisted, private.")
            driver.quit()
            return

        option_xpath = f"//tp-yt-paper-radio-button[@name='{visibility_map[visibility]}']"
        visibility_option = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, option_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView();", visibility_option)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", visibility_option)
        time.sleep(2)
        print(f"Visibility set to '{visibility}'.")
    except Exception as e:
        print("Error setting visibility:", e)

    # Save Button
    for _ in range(5):
        try:
            save_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='done-button']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", save_button)
            time.sleep(5)
            print("Video saved and uploaded successfully.")
            break
        except:
            print("Retrying Save button click...")
            time.sleep(2)
    else:
        print("Error clicking Save button after multiple attempts.")

    driver.quit()

# ===== User Inputs =====
video_file = input("Enter the full path of the video file: ").strip().strip('"')
video_title = input("Enter the title of the video: ").strip()
description = input("Enter the video description: ").strip()
visibility = input("Enter video visibility (public / unlisted / private): ").strip().lower()

if not os.path.isabs(video_file):
    print("Error: Please enter a valid absolute file path.")
    exit()

upload_video(video_file, video_title, description, visibility)
