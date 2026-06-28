# Udemy Courses Scraper

A lightweight Python CLI application that scrapes the complete curriculum of any Udemy course using Selenium and generates a structured HTML report optimized for organizing courses in a Notion tracker.

## Features

* Scrapes the complete course curriculum.
* Extracts:

  * Course title
  * Section titles
  * Lecture titles
  * Individual lecture durations
* Calculates section durations from lecture durations.
* Converts all lecture durations into total minutes for easy use in Notion formulas.
* Generates a clean, interactive HTML report.
* Includes:

  * Course summary (sections, lectures, total duration)
  * Global show/hide lectures toggle
  * Copy-to-clipboard support for titles and durations
  * Direct link to the original Udemy course
* Automatically opens the generated report in the default browser.
* Installable as a command-line application.

## Installation

Clone the repository:

```bash
git clone https://github.com/kareemaboueid/udemy-courses-scraper.git
cd udemy-courses-scraper
```

Install the project in editable mode:

```bash
pip install -e .
```

## Usage

Run from any terminal:

```bash
scrap-udemy-course
```

Enter the Udemy course URL when prompted.

## Requirements

* Python 3.12 or later
* Google Chrome
* ChromeDriver compatible with your installed Chrome version

## Author

**Kareem Aboueid**

GitHub: https://github.com/kareemaboueid
