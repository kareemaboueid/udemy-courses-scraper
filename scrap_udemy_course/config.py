"""
config.py
---------
Application configuration.

This module contains all configurable values used throughout the
Udemy Courses Scraper application.

Author : Kareem Aboueid
Version: 2.0
"""

from pathlib import Path


# ============================================================================
# Project Metadata
# ============================================================================

APP_NAME = "Udemy Courses Scraper"

VERSION = "2.0"

AUTHOR = "Kareem Aboueid"

GITHUB = "https://github.com/kareemaboueid"


# ============================================================================
# Project Paths
# ============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DIST_DIR = PROJECT_ROOT / "dist"

LOG_DIR = PROJECT_ROOT / "logs"

DRIVER_DIR = PROJECT_ROOT / "drivers"

TEMPLATE_DIR = PROJECT_ROOT / "templates"


# ============================================================================
# Files
# ============================================================================

HTML_TEMPLATE = TEMPLATE_DIR / "result.html"

OUTPUT_HTML = DIST_DIR / "result.html"

LOG_FILE = LOG_DIR / "log.txt"

CHROMEDRIVER_PATH = DRIVER_DIR / "chromedriver.exe"


# ============================================================================
# Browser
# ============================================================================

BROWSER_WIDTH = 1920

BROWSER_HEIGHT = 1080

HEADLESS = False

PAGE_LOAD_TIMEOUT = 30

WAIT_TIMEOUT = 15

SHOW_MORE_TIMEOUT = 5

SCROLL_PAUSE = 0.20


# ============================================================================
# Output
# ============================================================================

HTML_ENCODING = "utf-8"

LOG_ENCODING = "utf-8"


# ============================================================================
# Logging
# ============================================================================

LOG_TIMESTAMP_FORMAT = "%Y-%m-%d_%H:%M:%S"

CONSOLE_PREFIX = "MSG"


# ============================================================================
# Emojis
# ============================================================================

EMOJI_COURSE = "🎓"

EMOJI_SECTION = "📂"

EMOJI_LECTURE = "📄"

EMOJI_COPY = "📋"

EMOJI_SUCCESS = "✅"

EMOJI_WARNING = "⚠️"

EMOJI_ERROR = "❌"

EMOJI_INFO = "ℹ️"


# ============================================================================
# HTML Placeholders
# ============================================================================


PLACEHOLDER_TOTAL_SECTIONS = "%TOTAL_SECTIONS%"
PLACEHOLDER_TOTAL_LECTURES = "%TOTAL_LECTURES%"
PLACEHOLDER_TOTAL_DURATION = "%TOTAL_DURATION%"

PLACEHOLDER_SCRIPT_NAME = "%SCRIPT_NAME%"

PLACEHOLDER_TIME = "%TIME_TAKEN%"

PLACEHOLDER_DATA_LENGTH = "%DATA_LENGTH%"

PLACEHOLDER_SCRAPING_URL = "%SCRAPING_URL%"

PLACEHOLDER_COURSE_NAME = "%COURSE_NAME%"

PLACEHOLDER_ALL_DATA = "%ALL_DATA%"


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    # Metadata
    "APP_NAME",
    "VERSION",
    "AUTHOR",
    "GITHUB",

    # Paths
    "PROJECT_ROOT",
    "DIST_DIR",
    "LOG_DIR",
    "DRIVER_DIR",
    "TEMPLATE_DIR",

    # Files
    "HTML_TEMPLATE",
    "OUTPUT_HTML",
    "LOG_FILE",
    "CHROMEDRIVER_PATH",

    # Browser
    "BROWSER_WIDTH",
    "BROWSER_HEIGHT",
    "HEADLESS",
    "PAGE_LOAD_TIMEOUT",
    "WAIT_TIMEOUT",
    "SHOW_MORE_TIMEOUT",
    "SCROLL_PAUSE",

    # Output
    "HTML_ENCODING",
    "LOG_ENCODING",

    # Logging
    "LOG_TIMESTAMP_FORMAT",
    "CONSOLE_PREFIX",

    # Emojis
    "EMOJI_COURSE",
    "EMOJI_SECTION",
    "EMOJI_LECTURE",
    "EMOJI_COPY",
    "EMOJI_SUCCESS",
    "EMOJI_WARNING",
    "EMOJI_ERROR",
    "EMOJI_INFO",

    # HTML
    "PLACEHOLDER_SCRIPT_NAME",
    "PLACEHOLDER_TIME",
    "PLACEHOLDER_DATA_LENGTH",
    "PLACEHOLDER_SCRAPING_URL",
    "PLACEHOLDER_COURSE_NAME",
    "PLACEHOLDER_ALL_DATA",
]
