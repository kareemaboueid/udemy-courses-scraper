"""
utils.py
--------
General utility functions used throughout the application.

This module contains reusable helper functions for:

- Console output
- Text extraction
- HTML escaping
- Duration parsing
- Time formatting
- Directory creation
- URL validation
- Browser utilities
- File utilities

Author : Kareem Aboueid
Version: 2.0
"""

from __future__ import annotations

import re
import webbrowser
from datetime import datetime
from html import escape
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from modules import config


# ============================================================================
# Console
# ============================================================================

def print_agent(
    message: str,
    prefix: str | None = None,
) -> None:
    """
    Print a formatted console message.
    """

    if prefix is None:
        prefix = config.CONSOLE_PREFIX

    print(f"[{prefix}] {message}")


# ============================================================================
# Validation
# ============================================================================

def is_valid_udemy_course_url(
    url: str,
) -> bool:
    """
    Validate a Udemy course URL.
    """

    return url.startswith(
        "https://www.udemy.com/course/"
    )


# ============================================================================
# Filesystem
# ============================================================================

def ensure_directories() -> None:
    """
    Ensure required project directories exist.
    """

    config.DIST_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def write_text_file(
    path: Path,
    content: str,
    encoding: str = config.HTML_ENCODING,
) -> None:
    """
    Write text to a file.
    """

    path.write_text(
        content,
        encoding=encoding,
    )


# ============================================================================
# Browser
# ============================================================================

def open_browser(
    path: Path,
) -> None:
    """
    Open a local HTML file in the default browser.
    """

    webbrowser.open_new_tab(
        path.resolve().as_uri()
    )


# ============================================================================
# Time
# ============================================================================

def current_timestamp() -> str:
    """
    Return the current timestamp.
    """

    return datetime.now().strftime(
        config.LOG_TIMESTAMP_FORMAT
    )


def format_elapsed_time(
    seconds: float,
) -> str:
    """
    Format elapsed time.

    Example:

        6.42 sec
    """

    return f"{seconds:.2f} sec"


# ============================================================================
# Selenium
# ============================================================================

def safe_text(
    element: WebElement | None,
) -> str:
    """
    Safely extract text from a WebElement.
    """

    if element is None:
        return ""

    try:
        return element.text.strip()
    except AttributeError:
        return ""


def safe_find_text(
    parent,
    by: By,
    selector: str,
) -> str:
    """
    Find an element and safely return its text.
    """

    try:

        element = parent.find_element(
            by,
            selector,
        )

        return safe_text(element)

    except Exception:

        return ""


def safe_click(
    element: WebElement | None,
) -> bool:
    """
    Safely click an element.

    Returns
    -------
    bool
        True if clicked successfully.
    """

    if element is None:
        return False

    try:

        element.click()

        return True

    except Exception:

        return False


# ============================================================================
# HTML
# ============================================================================

def escape_html(
    text: str,
) -> str:
    """
    Escape HTML special characters.
    """

    return escape(text)


# ============================================================================
# Duration
# ============================================================================

def convert_duration_to_minutes(
    duration: str,
) -> int:
    """
    Convert a Udemy lecture duration into
    whole minutes.

    Examples
    --------
    6:45     -> 7
    12:00    -> 12
    35:14    -> 36
    1:02:30  -> 63
    """

    duration = duration.strip()

    if not duration:
        return 0

    try:

        parts = [
            int(part)
            for part in duration.split(":")
        ]

        # mm:ss
        if len(parts) == 2:

            minutes, seconds = parts

            return (
                minutes
                + (1 if seconds > 0 else 0)
            )

        # hh:mm:ss
        if len(parts) == 3:

            hours, minutes, seconds = parts

            total = (
                hours * 60
                + minutes
            )

            if seconds > 0:
                total += 1

            return total

    except ValueError:
        pass

    return 0


def minutes_to_string(
    minutes: int,
) -> str:
    """
    Convert minutes into a readable string.
    """

    if minutes <= 0:
        return "0 min"

    hours = minutes // 60
    mins = minutes % 60

    if hours == 0:
        return f"{mins} min"

    if mins == 0:
        return f"{hours} hr"

    return f"{hours} hr {mins} min"


def parse_section_statistics(
    text: str,
) -> tuple[int, int]:
    """
    Parse section statistics.

    Example:

        "8 lectures • 45min"
    """

    lecture_count = 0

    lecture_match = re.search(
        r"(\d+)\s+lecture",
        text.lower(),
    )

    if lecture_match:

        lecture_count = int(
            lecture_match.group(1)
        )

    duration = convert_duration_to_minutes(
        text
    )

    return (
        lecture_count,
        duration,
    )


# ============================================================================
# Formatting
# ============================================================================

def sanitize_filename(
    filename: str,
) -> str:
    """
    Remove characters invalid
    in Windows filenames.
    """

    return re.sub(
        r'[<>:"/\\|?*]',
        "",
        filename,
    ).strip()


def separator(
    length: int = 80,
    character: str = "-",
) -> str:
    """
    Return a separator line.
    """

    return character * length


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "print_agent",
    "is_valid_udemy_course_url",
    "ensure_directories",
    "write_text_file",
    "open_browser",
    "current_timestamp",
    "format_elapsed_time",
    "safe_text",
    "safe_find_text",
    "safe_click",
    "escape_html",
    "convert_duration_to_minutes",
    "minutes_to_string",
    "parse_section_statistics",
    "sanitize_filename",
    "separator",
]
