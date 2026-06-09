from __future__ import annotations

import json
from datetime import date, datetime, timezone

from chronicle.formatter import format_json, format_markdown, format_slack
from chronicle.grouper import group_by_week
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
        files_changed=["main.py"],
    )


def _sample_week():
    commits = [
        _make_commit("feat: add login", date(2024, 6, 3)),
        _make_commit("fix: null check", date(2024, 6, 3)),
        _make_commit("chore: update deps", date(2024, 6, 4), repo="other-repo"),
    ]
    return group_by_week(commits)


def test_format_markdown_structure():
    week = _sample_week()
    md = format_markdown(week)

    assert md.startswith("# Chronicle")
    assert "myrepo" in md
    assert "other-repo" in md
    assert "abc1234" in md
    assert "---" in md


def test_format_markdown_empty():
    week = group_by_week([])
    md = format_markdown(week)
    assert "No commits" in md


def test_format_json_valid():
    week = _sample_week()
    raw = format_json(week)
    data = json.loads(raw)  # must not raise

    assert "period" in data
    assert "total_commits" in data
    assert data["total_commits"] == 3
    assert "days" in data
    assert isinstance(data["days"], list)
    assert len(data["days"]) == 2


def test_format_json_empty():
    week = group_by_week([])
    raw = format_json(week)
    data = json.loads(raw)
    assert data["total_commits"] == 0
    assert data["days"] == []


def test_format_slack_contains_bold():
    week = _sample_week()
    slack = format_slack(week)
    assert "*Chronicle" in slack
    assert "*myrepo*" in slack


def test_format_slack_empty():
    week = group_by_week([])
    slack = format_slack(week)
    assert "No commits" in slack
