# udemy-sections-scraper.py
# Version 5.4
# @Author: Kareem Aboeid https://github.com/kareemaboueid

import os
import time
import webbrowser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Print messages with a prefix for clarity:


def print_agent(msg, prefix="MSG: "):
    print(f"{prefix}{msg}")

# Convert duration string to total minutes:


def convert_duration_to_minutes(duration_text):
    try:
        minutes = 0
        if "hr" in duration_text:
            hr_part = duration_text.split("hr")
            minutes += int(hr_part[0].strip()) * 60
            duration_text = hr_part[1].strip() if len(hr_part) > 1 else ""
        if "min" in duration_text:
            minutes += int(duration_text.split("min")[0].strip())
        return minutes
    except:
        return 0


# Default HTML template if file doesn't exist:


default_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="./style.css" />
    <title>%SCRIPT_NAME%</title>
</head>
<body>
    <section class="result_wrapper">
        <section class="result_header">
            <div>
                <h1>Udemy sections successfully scraped</h1>
            </div>
            <div class="result_header_actions">
                <button onclick="save_to_file()">Save</button>
                <button onclick="window.close()">Close</button>
            </div>
        </section>
        <div class="result_info">
            <div class="info_details">
                <p><strong>Script: </strong>%SCRIPT_NAME%</p>
                <p>
                    <strong>Time: </strong>
                    <span id="scraping_time">%TIME_TAKEN%</span>s
                </p>
                <p><strong>length: </strong>%DATA_LENGTH%</p>
            </div>
            <div class="info_details">
                <p>
                    <strong>Course: </strong>
                    <a href="%SCRAPING_URL%">%COURSE_NAME%</a>
                </p>
            </div>
        </div>
        <div class="separator"></div>
        <div class="data_header">
            <div class="title">
                <p>Title</p>
            </div>
            <div class="duration">
                <p>Duration</p>
            </div>
        </div>
        <div class="result_body">%ALL_DATA%</div>
    </section>
    <footer>
        <p>
            Made by
            <a href="https://github.com/kareemaboueid">Kareem Aboueid</a>
        </p>
    </footer>
    <script src="./script.js"></script>
</body>
</html>
'''

# Main scraping logic:


def scrape_sections(url, chromedriver_path="./chromedriver.exe"):
    start_time = time.time()
    script_name = os.path.basename(__file__)
    section_count = 0
    elapsed = 0

    print_agent("Initiating data extraction sequence...\n")
    print_agent("Open browser instance...")

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
    except WebDriverException as e:
        print_agent("ERROR: ChromeDriver initialization failed.")
        print(e)
        return

    try:
        driver.get(url)
        print_agent("Target URL loaded. Waiting for curriculum content...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "section--panel--qYPjj"))
        )

        # Check and click "Show more" button if it exists
        try:
            show_more_btn = driver.find_element(
                By.CSS_SELECTOR, "button.curriculum--curriculum-show-more--hf-k5")
            if show_more_btn.is_displayed():
                print_agent("Hidden sections detected. Expanding content...")
                show_more_btn.click()
                WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "section--panel--qYPjj"))
                )
        except NoSuchElementException:
            print_agent(
                "All curriculum sections are already exposed. Proceeding.")

        print_agent("Extraction in progress...")

        course_name = driver.find_element(
            By.CSS_SELECTOR, '[data-purpose="lead-title"]')

        lecture_elements = driver.find_elements(
            By.CLASS_NAME, "section--section-title--svpHP")

        duration_elements = driver.find_elements(
            By.CSS_SELECTOR, "span.section--section-content--2mUJ7 span")

        lecture_titles = [el.text.strip()
                          for el in lecture_elements if el.text.strip()]
        duration_texts = [el.text.strip()
                          for el in duration_elements if el.text.strip()]
        duration_minutes = [convert_duration_to_minutes(
            d) for d in duration_texts]

        lectures = list(zip(lecture_titles, duration_minutes))
        section_count = len(lectures)

        # Prepare HTML block
        os.makedirs("./dist", exist_ok=True)
        output_path = "./dist/result.html"
        html_output = []
        for idx, (title, mins) in enumerate(lectures, 1):
            html_output.append(f'''
            <div class="single_data_section">
                <div class="title" title="Click to copy">
                    <p onclick="copy_text(this)" class="txt">({idx}) {title}</p>
                </div>
                <div class="duration" title="Click to copy">
                    <p onclick="copy_text(this)" class="txt">{mins}</p>
                </div>
            </div>
        ''')

        # Load template
        template_path = "./result.html"
        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as template_file:
                template = template_file.read()
        else:
            template = default_template

        elapsed = round(time.time() - start_time, 2)
        template = template.replace("%SCRIPT_NAME%", script_name)
        template = template.replace("%TIME_TAKEN%", str(elapsed))
        template = template.replace("%SCRAPING_URL%", url)
        template = template.replace(
            "%COURSE_NAME%", course_name.text.strip().capitalize())
        template = template.replace("%DATA_LENGTH%", str(section_count))
        template = template.replace("%ALL_DATA%", "\n".join(html_output))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(template)

        print_agent(
            f"Extraction completed successfully! {section_count} sections scraped.")
        print_agent(f"Exported data to '{output_path}'")

        # Open HTML in browser
        try:
            webbrowser.open_new_tab(os.path.abspath(output_path))
            print_agent("File opened in browser.")
        except Exception as e:
            print_agent(f"Failed to open browser: {e}")

    except Exception as e:
        print_agent("ERROR: Error occurred during scraping.")
        print(e)

    finally:
        driver.quit()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        log_entry = f"[{timestamp}] {script_name} {url} length={section_count} time={elapsed}sec\n"
        try:
            os.makedirs("./logs", exist_ok=True)
            with open("./logs/log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print_agent("Failed to write log:")
            print(e)
        print_agent("Logged entry to './logs/log.txt'")
        print_agent(f"Total processing duration: {elapsed} sec")


if __name__ == "__main__":
    url = input("Enter the Udemy course URL: ").strip()
    if not url.startswith("https://www.udemy.com/course/"):
        print("Invalid Udemy course URL.")
        exit(1)
    scrape_sections(url)
