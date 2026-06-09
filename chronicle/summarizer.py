from __future__ import annotations

import re
from datetime import date

from .reader import Commit

_CONVENTIONAL_PREFIX = re.compile(
    r"^(feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert)(\(.+?\))?!?:\s*",
    re.IGNORECASE,
)


def _clean(message: str) -> str:
    return _CONVENTIONAL_PREFIX.sub("", message).strip()


def summarize_commits(commits: list[Commit]) -> str:
    if not commits:
        return ""

    cleaned = [_clean(c.message) for c in commits]

    if len(cleaned) == 1:
        return cleaned[0]

    if len(cleaned) <= 3:
        joined = ", ".join(cleaned)
        return joined if len(joined) <= 80 else joined[:77] + "..."

    rest = len(cleaned) - 1
    first = cleaned[0]
    suffix = f" and {rest} more"
    max_first = 80 - len(suffix)
    if len(first) > max_first:
        first = first[: max_first - 3] + "..."
    return first + suffix


def estimate_hours(commits: list[Commit]) -> float:
    if not commits:
        return 0.0

    by_day: dict[date, list[Commit]] = {}
    for c in commits:
        by_day.setdefault(c.date.date(), []).append(c)

    total = 0.0
    for day_commits in by_day.values():
        n = len(day_commits)
        hours = 1.0 + (n - 1) * 0.5
        total += min(hours, 8.0)

    return total
