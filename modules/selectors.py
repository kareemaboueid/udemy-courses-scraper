"""
selectors.py
------------
Centralized CSS selectors used by the scraper.

Author : Kareem Aboueid
Version: 3.1
"""

# ============================================================================
# Course
# ============================================================================

COURSE_TITLE = "h1"


# ============================================================================
# Curriculum
# ============================================================================

SECTION = (
    "div.curriculum-section-module-scss-module__9JCrHq__panel"
)

SECTION_HEADER = "span[class*='section-title']"

SECTION_STATS = "[data-purpose='section-content-stats']"


# ============================================================================
# Lectures
# ============================================================================

LECTURE = "li"

LECTURE_TITLE = "span[class*='course-lecture-title']"

LECTURE_DURATION = (
    "span[class*='item-content-summary'] span"
)
