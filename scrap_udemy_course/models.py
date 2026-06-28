"""
models.py
---------
Domain models used throughout the application.

Author : Kareem Aboueid
Version: 2.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


# ============================================================================
# Lecture
# ============================================================================

@dataclass(slots=True)
class Lecture:
    """
    Represents a single lecture.
    """

    index: int
    title: str
    duration: int  # minutes


# ============================================================================
# Section
# ============================================================================

@dataclass(slots=True)
class Section:
    """
    Represents a course section.
    """

    index: int
    title: str

    # Values scraped directly from Udemy
    lecture_count: int
    duration: int

    lectures: list[Lecture] = field(default_factory=list)

    @property
    def total_lectures(self) -> int:
        """
        Number of lectures contained in this section.
        """

        return len(self.lectures)

    @property
    def total_duration(self) -> int:
        """
        Total duration of all lectures in this section.
        """

        return sum(
            lecture.duration
            for lecture in self.lectures
        )


# ============================================================================
# Course
# ============================================================================

@dataclass(slots=True)
class Course:
    """
    Represents an entire Udemy course.
    """

    title: str
    url: str
    scraped_at: datetime

    sections: list[Section] = field(default_factory=list)

    @property
    def total_sections(self) -> int:
        """
        Number of course sections.
        """

        return len(self.sections)

    @property
    def total_lectures(self) -> int:
        """
        Total number of lectures in the course.
        """

        return sum(
            section.total_lectures
            for section in self.sections
        )

    @property
    def total_duration(self) -> int:
        """
        Total course duration in minutes.
        """

        return sum(
            section.total_duration
            for section in self.sections
        )


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "Course",
    "Section",
    "Lecture",
]
