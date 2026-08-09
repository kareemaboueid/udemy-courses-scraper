"""
scraper.py
----------
Udemy Course Scraper.

Responsible for extracting the complete
course curriculum from a Udemy course page.

Author : Kareem Aboueid
Version: 3.1
"""

from __future__ import annotations

import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)

from .config import (
    WAIT_TIMEOUT,
)

from .selectors import (
    COURSE_TITLE,
    SECTION,
    SECTION_HEADER,
    SECTION_STATS,
    LECTURE,
    LECTURE_TITLE,
    LECTURE_DURATION,
)

from .models import (
    Course,
    Section,
    Lecture,
)

from .utils import (
    print_agent,
    safe_find_text,
    parse_section_statistics,
    convert_duration_to_minutes,
)


# ============================================================================
# Browser Helpers
# ============================================================================

EXPAND_ALL_BUTTON = (
    "button[data-purpose='expand-toggle']"
)


def _wait_for_curriculum(
    driver: WebDriver,
) -> None:
    """
    Wait until the curriculum is visible.
    """

    print_agent(
        "Waiting for curriculum..."
    )

    WebDriverWait(
        driver,
        WAIT_TIMEOUT,
    ).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                SECTION,
            )
        )
    )


def _expand_curriculum(
    driver: WebDriver,
) -> None:
    """
    Expand the entire curriculum.

    Udemy automatically loads every hidden
    section when this button is pressed.
    """

    print_agent(
        "Expanding curriculum..."
    )

    button = WebDriverWait(
        driver,
        WAIT_TIMEOUT,
    ).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                EXPAND_ALL_BUTTON,
            )
        )
    )

    if (
        button.get_attribute(
            "aria-expanded"
        )
        == "true"
    ):

        print_agent(
            "Curriculum already expanded."
        )

        return

    driver.execute_script(
        "arguments[0].click();",
        button,
    )

    WebDriverWait(
        driver,
        WAIT_TIMEOUT,
    ).until(
        lambda d:
        d.find_element(
            By.CSS_SELECTOR,
            EXPAND_ALL_BUTTON,
        ).get_attribute(
            "aria-expanded"
        )
        == "true"
    )

    print_agent(
        "Curriculum expanded."
    )

    WebDriverWait(
        driver,
        WAIT_TIMEOUT,
    ).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                LECTURE_TITLE,
            )
        )
    )


def _load_course(
    driver: WebDriver,
    url: str,
) -> None:
    """
    Open and prepare a course page.
    """

    print_agent(
        "Loading course..."
    )

    driver.get(
        url,
    )

    _wait_for_curriculum(
        driver,
    )

    _expand_curriculum(
        driver,
    )

# ============================================================================
# Course Helpers
# ============================================================================


def _get_course_title(
    driver: WebDriver,
) -> str:
    """
    Return the course title.
    """

    title = safe_find_text(
        driver,
        By.CSS_SELECTOR,
        COURSE_TITLE,
    ).strip()

    if title:
        return title

    try:

        return (
            driver.find_element(
                By.TAG_NAME,
                "h1",
            )
            .text
            .strip()
        )

    except NoSuchElementException:

        return ""


def _create_course(
    driver: WebDriver,
    url: str,
) -> Course:
    """
    Create an empty Course object.
    """

    return Course(
        title=_get_course_title(driver),
        url=url,
        scraped_at=datetime.now(),
    )


# ============================================================================
# Section Helpers
# ============================================================================

def _get_section_elements(
    driver: WebDriver,
) -> list[WebElement]:
    """
    Return all curriculum sections.
    """

    sections = driver.find_elements(
        By.CSS_SELECTOR,
        SECTION,
    )

    print_agent(
        f"Detected {len(sections)} sections."
    )

    return sections


def _scrape_section(
    section_element: WebElement,
    index: int,
) -> Section:
    """
    Scrape a single section.
    """

    title = safe_find_text(
        section_element,
        By.CSS_SELECTOR,
        SECTION_HEADER,
    ).strip()

    stats = safe_find_text(
        section_element,
        By.CSS_SELECTOR,
        SECTION_STATS,
    ).strip()

    lecture_count, duration = (
        parse_section_statistics(
            stats,
        )
    )

    return Section(
        index=index,
        title=title,
        lecture_count=lecture_count,
        duration=duration,
        lectures=[],
    )


def _scrape_sections(
    driver: WebDriver,
) -> list[Section]:
    """
    Scrape every course section.
    """

    section_elements = _get_section_elements(
        driver,
    )

    sections: list[Section] = []

    lecture_index = 1

    print_agent(
        f"Scraping {len(section_elements)} sections..."
    )

    for section_index, section_element in enumerate(
        section_elements,
        start=0,
    ):

        section = _scrape_section(
            section_element,
            section_index,
        )

        section.lectures = _scrape_lectures(
            section_element,
            lecture_index,
        )

        lecture_index += len(
            section.lectures,
        )

        sections.append(
            section,
        )

        print_agent(
            f"[{section.index}/{len(section_elements)}] "
            f"{section.title} "
            f"({len(section.lectures)} lectures)"
        )

    return sections

# ============================================================================
# Lecture Helpers
# ============================================================================


def _get_lecture_elements(
    section_element: WebElement,
) -> list[WebElement]:
    """
    Return all lecture elements within a section.
    """

    return section_element.find_elements(
        By.CSS_SELECTOR,
        LECTURE,
    )


def _scrape_lecture(
    lecture_element: WebElement,
    index: int,
) -> Lecture:
    """
    Scrape a single lecture.
    """

    title = safe_find_text(
        lecture_element,
        By.CSS_SELECTOR,
        LECTURE_TITLE,
    ).strip()

    duration_text = safe_find_text(
        lecture_element,
        By.CSS_SELECTOR,
        LECTURE_DURATION,
    ).strip()

    duration = convert_duration_to_minutes(
        duration_text,
    )

    # print(repr(duration_text))

    return Lecture(
        index=index,
        title=title,
        duration=duration,
    )


def _scrape_lectures(
    section_element: WebElement,
    start_index: int,
) -> list[Lecture]:
    """
    Scrape all lectures within a section.
    """

    lecture_elements = _get_lecture_elements(
        section_element,
    )

    lectures: list[Lecture] = []

    lecture_index = start_index

    for lecture_element in lecture_elements:

        lecture = _scrape_lecture(
            lecture_element,
            lecture_index,
        )

        if not lecture.title:
            continue

        lectures.append(
            lecture,
        )

        lecture_index += 1

    return lectures


# ============================================================================
# Summary Helpers
# ============================================================================

def _print_summary(
    course: Course,
) -> None:
    """
    Print scraping summary.
    """

    print_agent("")

    print_agent(
        "Course scraping completed."
    )

    print_agent(
        f"Course    : {course.title}"
    )

    print_agent(
        f"Sections  : {course.total_sections}"
    )

    print_agent(
        f"Lectures  : {course.total_lectures}"
    )

    print_agent(
        f"Duration  : {course.total_duration} min"
    )

# ============================================================================
# Public API
# ============================================================================


def scrape_course(
    driver: WebDriver,
    url: str,
) -> Course:
    """
    Scrape a complete Udemy course.

    Parameters
    ----------
    driver
        Selenium WebDriver.

    url
        Udemy course URL.

    Returns
    -------
    Course
        Fully populated Course object.
    """

    _load_course(
        driver,
        url,
    )

    course = _create_course(
        driver,
        url,
    )

    print_agent(
        f'Course "{course.title}" loaded.'
    )

    course.sections = _scrape_sections(
        driver,
    )

    _print_summary(
        course,
    )

    return course


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    "scrape_course",
]
