import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")

service = Service("D:/video_automation/chromedriver.exe")   
driver = webdriver.Chrome(service=service, options=chrome_options)

def upload_video(video_path):
    video_path = os.path.abspath(video_path) 
    driver.get("https://studio.youtube.com")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//ytcp-button[contains(@label, 'Create')]")))
    create_button = driver.find_element(By.XPATH, "//ytcp-button[contains(@label, 'Create')]")
    create_button.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//yt-formatted-string[text()='Upload videos']"))).click()

    file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
    file_input.send_keys(video_path)  
    time.sleep(5)  

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    try:
        not_made_for_kids = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-radio-button[@name='VIDEO_MADE_FOR_KIDS_NOT_MFK']")))
        driver.execute_script("arguments[0].click();", not_made_for_kids)
    except Exception as e:
        print("Error clicking 'Not made for kids':", e)

    while True:
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//ytcp-button[contains(@label, 'Next')]")
            ))
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)
            print("Clicked Next button...")
        except:
            print("No more Next buttons, moving to Visibility section.")
            break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    try:
        unlisted_option = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//tp-yt-paper-radio-button[@name='UNLISTED']")))
        driver.execute_script("arguments[0].scrollIntoView();", unlisted_option)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", unlisted_option)
        time.sleep(2)
        print(" Unlisted visibility selected.")
    except Exception as e:
        print(" Error setting visibility to Unlisted:", e)

    for _ in range(5):  
        try:
            save_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='done-button']")
            ))
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", save_button)
            time.sleep(5)
            print(" Save clicked successfully.")
            break
        except:
            print(" Retrying Save button click...")
            time.sleep(2)
    else:
        print(" Error clicking Save button after multiple attempts.")

    driver.quit()

video_file = input("Enter the full path of the video file: ").strip().strip('"') 

if not os.path.isabs(video_file):
    print(" Error: Please enter a valid absolute file path.")
    exit()

upload_video(video_file) 