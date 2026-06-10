from __future__ import annotations

from datetime import date, datetime, timezone

from chronicle.grouper import group_by_day, group_by_week
from chronicle.reader import Commit


def _make_commit(msg: str, day: date, repo: str = "myrepo") -> Commit:
    return Commit(
        hash="abc1234def5678",
        short_hash="abc1234",
        message=msg,
        date=datetime.combine(day, datetime.min.time(), tzinfo=timezone.utc),
        author_email="dev@example.com",
        repo_name=repo,
        repo_path=f"/repos/{repo}",
        files_changed=["README.md"],
    )


def test_group_by_day_empty():
    assert group_by_day([]) == []


def test_group_by_day_single():
    d = date(2024, 6, 3)
    commits = [_make_commit("first", d)]
    groups = group_by_day(commits)
    assert len(groups) == 1
    assert groups[0].date == d
    assert groups[0].total_commits == 1


def test_group_by_day_multiple_days():
    c1 = _make_commit("a", date(2024, 6, 3))
    c2 = _make_commit("b", date(2024, 6, 4))
    c3 = _make_commit("c", date(2024, 6, 4))
    groups = group_by_day([c1, c2, c3])
    assert len(groups) == 2
    # Most recent first
    assert groups[0].date == date(2024, 6, 4)
    assert groups[0].total_commits == 2
    assert groups[1].date == date(2024, 6, 3)


def test_group_by_day_multiple_repos():
    d = date(2024, 6, 3)
    c1 = _make_commit("a", d, repo="repo-a")
    c2 = _make_commit("b", d, repo="repo-b")
    groups = group_by_day([c1, c2])
    assert len(groups) == 1
    assert set(groups[0].repos.keys()) == {"repo-a", "repo-b"}


def test_group_by_week_totals():
    commits = [
        _make_commit("a", date(2024, 6, 3)),
        _make_commit("b", date(2024, 6, 4)),
        _make_commit("c", date(2024, 6, 4)),
    ]
    week = group_by_week(commits)
    assert week.total_commits == 3
    assert "myrepo" in week.repos_touched


def test_group_by_week_empty():
    week = group_by_week([])
    assert week.total_commits == 0
    assert week.days == []
    assert week.repos_touched == []
