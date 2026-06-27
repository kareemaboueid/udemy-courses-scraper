"""
main.py
-------
Application entry point for the Udemy Courses Scraper.

Responsible only for orchestrating the application's workflow.

Author : Kareem Aboueid
Version: 2.0
"""

from __future__ import annotations

import os
import sys
import time
import webbrowser

from modules.browser import (
    create_driver,
    close_driver,
)

from modules.scraper import (
    scrape_course,
)

from modules.html_builder import (
    build_and_save_html,
)

from modules.logger import (
    write_log,
)

from modules.utils import (
    print_agent,
    is_valid_udemy_course_url,
)

from modules.config import (
    OUTPUT_HTML,
)


# ============================================================================
# Helpers
# ============================================================================

def _get_course_url() -> str:
    """
    Prompt the user for a Udemy course URL and validate it.
    """

    url = input(
        "Enter the Udemy course URL: "
    ).strip()

    if not is_valid_udemy_course_url(url):
        raise ValueError(
            "Invalid Udemy course URL."
        )

    return url


def _open_report() -> None:
    """
    Open the generated HTML report
    in the default web browser.
    """

    webbrowser.open_new_tab(
        OUTPUT_HTML.resolve().as_uri()
    )


# ============================================================================
# Public API
# ============================================================================

def main() -> None:
    """
    Execute the complete application workflow.
    """

    start_time = time.perf_counter()

    script_name = os.path.basename(
        sys.argv[0]
    )

    driver = None

    try:

        print_agent(
            "Starting application..."
        )

        url = _get_course_url()

        driver = create_driver()

        course = scrape_course(
            driver,
            url,
        )

        elapsed_time = (
            time.perf_counter() - start_time
        )

        report_path = build_and_save_html(
            course=course,
            script_name=script_name,
            elapsed_time=elapsed_time,
        )

        write_log(
            script_name=script_name,
            url=url,
            sections=course.total_sections,
            lectures=course.total_lectures,
            elapsed_time=elapsed_time,
        )

        _open_report()

        print_agent("")

        print_agent(
            "Mission completed successfully."
        )

        print_agent(
            f"Report : {report_path}"
        )

        print_agent(
            f"Sections : {course.total_sections}"
        )

        print_agent(
            f"Lectures : {course.total_lectures}"
        )

        print_agent(
            f"Duration : {course.total_duration} min"
        )

        print_agent(
            f"Time : {elapsed_time:.2f} sec"
        )

    except KeyboardInterrupt:

        print_agent(
            "Operation cancelled by user.",
            prefix="WARNING",
        )

    except Exception as e:

        print_agent(
            str(e),
            prefix="ERROR",
        )

    finally:

        close_driver(driver)


# ============================================================================
# Module Entry
# ============================================================================

__all__ = [
    "main",
]
