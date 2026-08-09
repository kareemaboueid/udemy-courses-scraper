"""
browser.py
----------
Browser management for the Udemy Courses Scraper.

Responsible only for creating and destroying Selenium
WebDriver instances.

Author : Kareem Aboueid
Version: 2.0
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException

from .config import (
    CHROMEDRIVER_PATH,
    BROWSER_WIDTH,
    BROWSER_HEIGHT,
    HEADLESS,
)

from .utils import print_agent


# ============================================================================
# Chrome Options
# ============================================================================

def _build_options() -> Options:
    """
    Create and configure Chrome options.
    """

    options = Options()

    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size="
                         f"{BROWSER_WIDTH},{BROWSER_HEIGHT}")

    if HEADLESS:
        options.add_argument("--headless=new")

    return options


# ============================================================================
# Driver Factory
# ============================================================================

def create_driver() -> WebDriver:
    """
    Create a Chrome WebDriver instance.
    """

    print_agent(
        "Starting Chrome..."
    )

    options = _build_options()

    if CHROMEDRIVER_PATH.exists():
        try:
            return webdriver.Chrome(
                service=Service(CHROMEDRIVER_PATH),
                options=options,
            )
        except WebDriverException as e:
            message = str(e)

            if (
                "This version of ChromeDriver only supports Chrome version" in message
                or "session not created" in message
                or "ChromeDriver executable needs to be available" in message
            ):
                print_agent(
                    "Local ChromeDriver is incompatible. Falling back to Selenium Manager..."
                )
            else:
                raise RuntimeError(
                    f"Failed to initialize ChromeDriver:\n{e}"
                ) from e

    try:
        return webdriver.Chrome(
            options=options,
        )
    except WebDriverException as e:
        raise RuntimeError(
            f"Failed to initialize ChromeDriver with Selenium Manager:\n{e}"
        ) from e


# ============================================================================
# Cleanup
# ============================================================================

def close_driver(
    driver: WebDriver | None,
) -> None:
    """
    Safely close the browser.
    """

    if driver is None:
        return

    try:

        driver.quit()

        print_agent(
            "Browser closed."
        )

    except Exception:

        pass


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "create_driver",
    "close_driver",
]
