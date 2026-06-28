# Udemy Courses Scraper

A Python-based web automation script that extracts course sections and durations from any Udemy course page using Selenium. It generates a well-structured HTML report containing all scraped information, along with metadata such as script name, execution time, course name, and more.

## Features

- Extracts all course section titles and durations.
- Converts duration strings to total minutes.
- Automatically captures course title from the Udemy page.
- Generates a styled HTML report with:
  - Execution metadata (script name, time, number of sections)
  - Copy-to-clipboard functionality for section and lectures titles and durations
- Automatically opens the result in the browser after scraping

## Installation

```bash
git clone ...
cd scrap-udemy-course

pip install -e .
```

## Usage

```bash
scrap-udemy-course
```

## Requirements

Python 3.7 or higher

Google Chrome browser installed

ChromeDriver (matching your browser version)

## Author

Kareem Aboueid
GitHub: <https://github.com/kareemaboueid>
