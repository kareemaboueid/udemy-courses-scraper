"""
html_builder.py
---------------
Generate the HTML report from a Course object.

Responsible only for converting application models into HTML.

Input:
    Course object

Output:
    HTML string

Author : Kareem Aboueid
Version: 2.0
"""

from __future__ import annotations

from pathlib import Path

from modules.config import (
    HTML_TEMPLATE,
    OUTPUT_HTML,
    PLACEHOLDER_SCRIPT_NAME,
    PLACEHOLDER_TIME,
    PLACEHOLDER_DATA_LENGTH,
    PLACEHOLDER_SCRAPING_URL,
    PLACEHOLDER_COURSE_NAME,
    PLACEHOLDER_ALL_DATA,
    HTML_ENCODING,
    PLACEHOLDER_TOTAL_SECTIONS,
    PLACEHOLDER_TOTAL_LECTURES,
    PLACEHOLDER_TOTAL_DURATION,
)

from modules.models import (
    Course,
    Section,
    Lecture,
)

from modules.utils import (
    escape_html,
    minutes_to_string,
    ensure_directories,
)


# ============================================================================
# Template
# ============================================================================

def _load_template() -> str:
    """
    Load the HTML template.

    If the template file does not exist,
    create it using the built-in template.
    """

    if not HTML_TEMPLATE.exists():
        raise FileNotFoundError(
            f"Template not found: {HTML_TEMPLATE}"
        )

    return HTML_TEMPLATE.read_text(
        encoding=HTML_ENCODING,
    )


# ============================================================================
# Save
# ============================================================================

def save_html(html: str):

    ensure_directories()

    print("WRITING TO:", OUTPUT_HTML.resolve())

    OUTPUT_HTML.write_text(
        html,
        encoding=HTML_ENCODING,
    )

    print("WRITE COMPLETE")

    return OUTPUT_HTML


# ============================================================================
# Lecture Builder
# ============================================================================

def _build_lecture(
    lecture: Lecture,
) -> str:
    """
    Build the HTML for a single lecture.
    """

    return f"""
            <div class="single_data_section lecture">
                <div class="title" title="Click to copy">
                    <p onclick="copy_text(this)" class="txt">{lecture.index}. {escape_html(lecture.title)}</p>
                </div>

                <div class="duration" title="Click to copy">
                    <p onclick="copy_text(this)" class="txt">{lecture.duration}</p>
                </div>
            </div>
    """


# ============================================================================
# Section Builder
# ============================================================================

def _build_section(
    section: Section,
) -> str:
    """
    Build the HTML for a single section.
    """

    lectures_html = "".join(
        _build_lecture(lecture)
        for lecture in section.lectures
    )

    return f"""
        <div class="course_section">

            <div class="single_data_section section">

                <div class="title" title="Click to copy">
                    <p onclick="copy_text(this)" class="txt">Section {section.index}: {escape_html(section.title)}</p>
                </div>

            </div>

            <div class="section_lectures">

                {lectures_html}

            </div>

        </div>
        <div class="separator"></div>
    """


# ============================================================================
# Sections Builder
# ============================================================================

def _build_sections(
    course: Course,
) -> str:
    """
    Build all course sections.
    """

    return "\n".join(
        _build_section(section)
        for section in course.sections
    )


# ============================================================================
# Placeholder Replacement
# ============================================================================

def _replace_placeholders(
    template: str,
    course: Course,
    script_name: str,
    elapsed_time: float,
) -> str:
    """
    Replace all HTML template placeholders.
    """

    replacements = {
        PLACEHOLDER_SCRIPT_NAME: script_name,
        PLACEHOLDER_TIME: f"{elapsed_time:.2f}",

        PLACEHOLDER_TOTAL_SECTIONS: str(course.total_sections),
        PLACEHOLDER_TOTAL_LECTURES: str(course.total_lectures),
        PLACEHOLDER_TOTAL_DURATION: minutes_to_string(course.total_duration),

        PLACEHOLDER_DATA_LENGTH: str(course.total_lectures),
        PLACEHOLDER_COURSE_NAME: escape_html(course.title),
        PLACEHOLDER_SCRAPING_URL: course.url,
        PLACEHOLDER_ALL_DATA: _build_sections(course),
    }

    for placeholder, value in replacements.items():
        template = template.replace(
            placeholder,
            value,
        )

    return template


# ============================================================================
# Public API
# ============================================================================

def build_html(
    course: Course,
    script_name: str,
    elapsed_time: float,
) -> str:
    """
    Generate the complete HTML report.

    Parameters
    ----------
    course
        Scraped course.

    script_name
        Running script filename.

    elapsed_time
        Total scraping time in seconds.

    Returns
    -------
    str
        Complete HTML document.
    """

    template = _load_template()

    html = _replace_placeholders(
        template=template,
        course=course,
        script_name=script_name,
        elapsed_time=elapsed_time,
    )

    return html


# ============================================================================
# Convenience API
# ============================================================================

def build_and_save_html(
    course: Course,
    script_name: str,
    elapsed_time: float,
) -> Path:
    """
    Build the HTML report and save it to disk.

    Returns
    -------
    Path
        Generated HTML file path.
    """

    html = build_html(
        course=course,
        script_name=script_name,
        elapsed_time=elapsed_time,
    )

    return save_html(html)


__all__ = [
    "build_html",
    "save_html",
    "build_and_save_html",
]
