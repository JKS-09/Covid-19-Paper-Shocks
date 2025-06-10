import os
import shutil
import glob
import time
import requests
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract


START_DATE = "2020-02-01"
END_DATE   = "2020-04-30"

# Ensure the output directories exist
BASE_OUTPUT = os.path.join(os.getcwd(), "output")
CAPTCHA_DIR = os.path.join(BASE_OUTPUT, "captchas")
EXCEL_DIR   = os.path.join(BASE_OUTPUT, "excels")
os.makedirs(CAPTCHA_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)
DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")


# Configure Tesseract OCR path if needed
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)
driver.get("https://fcainfoweb.nic.in/reports/report_menu_web.aspx")
time.sleep(3)

def date_range(start_date, end_date):
    d1 = datetime.strptime(start_date, "%Y-%m-%d")
    d2 = datetime.strptime(end_date, "%Y-%m-%d")
    for n in range((d2 - d1).days + 1):
        yield d1 + timedelta(n)

for d in date_range(START_DATE, END_DATE):
    date_str = d.strftime('%d/%m/%Y')
    print(f"\nProcessing date: {date_str}")

    # Navigate to the report page
    try:
        radio_btn = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_Rbl_Rpt_type_0")))
        driver.execute_script("arguments[0].click();", radio_btn)
        time.sleep(1.2)
        select_elem = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_Ddl_Rpt_Option0")))
        select = Select(select_elem)
        select.select_by_visible_text("Daily Prices")
        time.sleep(0.8)
        date_box = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_Txt_FrmDate")))
        date_box.clear()
        date_box.send_keys(date_str)
        time.sleep(0.8)
    except Exception as e:
        print("Page preparation failed:", e)
        continue

    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        attempts += 1
        try:
            captcha_elem = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_captchalogin")))
            captcha_img_file = os.path.join(CAPTCHA_DIR, f"captcha_{d.strftime('%Y%m%d')}_try{attempts}.png")
            captcha_elem.screenshot(captcha_img_file)
            print(f"Saved captcha screenshot as {captcha_img_file}")
        except Exception as e:
            print("Captcha image not found or not scannable:", e)
            break

        # Perform OCR on the captcha image
        try:
            img = Image.open(captcha_img_file)
            ocr_text = pytesseract.image_to_string(img, config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
            ocr_text = ''.join(filter(str.isalnum, ocr_text)).strip()
            print(f"OCR-detected captcha: {ocr_text}")
        except Exception as e:
            print("OCR failed:", e)
            break

        # Input captcha text
        try:
            captcha_box = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_Captcha")))
            captcha_box.clear()
            captcha_box.send_keys(ocr_text)
            time.sleep(0.6)
        except Exception as e:
            print("Captcha box not found:", e)
            break

        # Click Get Data button
        try:
            getdata_btn = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_MainContent_btn_getdata1")))
            driver.execute_script("arguments[0].focus();", getdata_btn)
            print("Clicking 'Get Data' button automatically.")
            getdata_btn.click()
            print("Clicked Get Data button. Waiting for results table...")
            wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(., 'Daily Retail Prices Of Essential Commodities')]")))
            print("Results table found!")
            time.sleep(1.5)
        except Exception as e:
            print(f"Get Data failed (likely bad captcha), retrying... (attempt {attempts}/{max_attempts})", e)
            continue

        # Download Excel
        try:
            excel_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnsave")))
            excel_btn.click()
            print("Clicked Excel download. Waiting for download to complete...")
            time.sleep(7)
            excel_files = sorted(glob.glob(os.path.join(DOWNLOADS_PATH, "*.xls*")), key=os.path.getmtime, reverse=True)
            if excel_files:
                latest_excel = excel_files[0]
                dest = os.path.join(EXCEL_DIR, f"excel_{d.strftime('%Y%m%d')}_{os.path.basename(latest_excel)}")
                shutil.move(latest_excel, dest)
                print(f"Moved Excel file to {dest}")
            else:
                print("No new Excel file found in Downloads.")
        except Exception as e:
            print("Excel button not found or not clickable:", e)
        
        # Click Back button to reset for next date
        try:
            back_btn = wait.until(EC.element_to_be_clickable((By.ID, "btn_back")))
            back_btn.click()
            print("Clicked Back button. Ready for next date.")
            time.sleep(1.8)
        except Exception as e:
            print("Back button not found or not clickable:", e)
            continue  # If back button fails, we can still try the next date


        break  # Finished this date successfully

driver.quit()
print("All done.")
