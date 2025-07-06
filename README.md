# Udemy Courses Scraper

A Python-based web automation script that extracts course sections and durations from any Udemy course page using Selenium. It generates a well-structured HTML report containing all scraped information, along with metadata such as script name, execution time, course name, and more.

## Project Structure

```txt
udemy-courses-scraper/
├── dist/
│ ├── result.html
│ ├── script.js
│ ├── style.css
├── logs/
│ ├── log.txt
├── chromedriver.exe
├── requirements.txt
├── udemy-courses-scraper.py
└── README.md
```

## Features

- Extracts all course section titles and durations.
- Converts duration strings to total minutes.
- Automatically captures course title from the Udemy page.
- Generates a styled HTML report with:
  - Execution metadata (script name, time, number of sections)
  - Copy-to-clipboard functionality for section titles and durations
  - One-click export to plain `.txt` file
- Automatically opens the result in the browser after scraping
- Logs each run with timestamp, URL, script name, and processing time
- Works with or without an existing `result.html` file (uses default template if missing)

## Installation

1. Clone the repository or download the source code.
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

**Note:** Ensure the correct version of chromedriver.exe is placed in the project root. It must match the version of your installed Chrome browser.

## Usage

Click on the udemy-courses-scraper.py file to run it.

A terminal window will open, prompting you to enter a valid Udemy course URL.

Type the URL in the terminal and press Enter.
The script will then execute the following steps:

1. Launch a Chrome browser instance using Selenium.
2. Navigate to the provided Udemy course URL.
3. Scrape all visible course sections and their durations.
4. Write the scraped data into `dist/result.html`.
5. Open the generated report in your default web browser.
6. Log the run details in `logs/log.txt`.

## Requirements

Python 3.7 or higher

Google Chrome browser installed

ChromeDriver (matching your browser version)

## Author

Kareem Aboueid
GitHub: <https://github.com/kareemaboueid>
