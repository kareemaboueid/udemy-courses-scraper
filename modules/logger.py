"""
logger.py
---------
Logging utilities for the Udemy Courses Scraper.

Responsible only for writing execution logs.

Author : Kareem Aboueid
Version: 2.0
"""

from __future__ import annotations

from datetime import datetime

from modules.config import (
    LOG_FILE,
    HTML_ENCODING,
)

from modules.utils import (
    ensure_directories,
    print_agent,
)


# ============================================================================
# Helpers
# ============================================================================

def _timestamp() -> str:
    """
    Return the current timestamp.
    """

    return datetime.now().strftime(
        "%Y-%m-%d_%H:%M:%S"
    )


def _build_log_entry(
    *,
    script_name: str,
    url: str,
    sections: int,
    lectures: int,
    elapsed_time: float,
) -> str:
    """
    Build a single log line.
    """

    return (
        f"[{_timestamp()}] "
        f"{script_name} "
        f"{url} "
        f"sections={sections} "
        f"lectures={lectures} "
        f"time={elapsed_time:.2f}sec"
    )


# ============================================================================
# Public API
# ============================================================================

def write_log(
    *,
    script_name: str,
    url: str,
    sections: int,
    lectures: int,
    elapsed_time: float,
) -> None:
    """
    Append a log entry to the log file.
    """

    ensure_directories()

    log_entry = _build_log_entry(
        script_name=script_name,
        url=url,
        sections=sections,
        lectures=lectures,
        elapsed_time=elapsed_time,
    )

    with LOG_FILE.open(
        mode="a",
        encoding=HTML_ENCODING,
    ) as log_file:

        log_file.write(
            log_entry + "\n"
        )

    print_agent(
        "Log entry written."
    )


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "write_log",
]
