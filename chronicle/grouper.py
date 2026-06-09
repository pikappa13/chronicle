from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from .reader import Commit


@dataclass
class DayGroup:
    date: date
    repos: dict[str, list[Commit]] = field(default_factory=dict)

    @property
    def all_commits(self) -> list[Commit]:
        return [c for commits in self.repos.values() for c in commits]

    @property
    def total_commits(self) -> int:
        return sum(len(v) for v in self.repos.values())


@dataclass
class WeekGroup:
    start: date
    end: date
    days: list[DayGroup]
    total_commits: int
    repos_touched: list[str]


def group_by_day(commits: list[Commit]) -> list[DayGroup]:
    by_date: dict[date, dict[str, list[Commit]]] = {}
    for commit in commits:
        day = commit.date.date()
        by_date.setdefault(day, {}).setdefault(commit.repo_name, []).append(commit)

    return [
        DayGroup(date=d, repos=repos)
        for d, repos in sorted(by_date.items(), reverse=True)
    ]


def group_by_week(commits: list[Commit]) -> WeekGroup:
    days = group_by_day(commits)

    if commits:
        dates = [c.date.date() for c in commits]
        earliest = min(dates)
        # Monday of the week containing the earliest commit
        start = earliest - timedelta(days=earliest.weekday())
        end = max(dates)
    else:
        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = today

    total = sum(d.total_commits for d in days)
    repos: list[str] = []
    seen: set[str] = set()
    for day in days:
        for repo_name in day.repos:
            if repo_name not in seen:
                repos.append(repo_name)
                seen.add(repo_name)

    return WeekGroup(start=start, end=end, days=days, total_commits=total, repos_touched=repos)
