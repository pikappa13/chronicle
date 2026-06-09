from __future__ import annotations

import os
import tempfile
from datetime import datetime, timezone

import git
import pytest

from chronicle.reader import Commit, read_commits


@pytest.fixture()
def fake_repo(tmp_path):
    repo = git.Repo.init(tmp_path)
    repo.config_writer().set_value("user", "name", "Test User").release()
    repo.config_writer().set_value("user", "email", "test@example.com").release()

    (tmp_path / "file.txt").write_text("hello")
    repo.index.add(["file.txt"])
    repo.index.commit("feat: initial commit")

    (tmp_path / "file.txt").write_text("world")
    repo.index.add(["file.txt"])
    repo.index.commit("fix: update file")

    return tmp_path


def test_read_commits_returns_commits(fake_repo):
    since = datetime(2000, 1, 1, tzinfo=timezone.utc)
    until = datetime(2099, 1, 1, tzinfo=timezone.utc)
    commits, resolved = read_commits(str(fake_repo), since, until)
    assert len(commits) == 2
    assert resolved == "test@example.com"


def test_read_commits_author_filter(fake_repo):
    since = datetime(2000, 1, 1, tzinfo=timezone.utc)
    until = datetime(2099, 1, 1, tzinfo=timezone.utc)

    commits, _ = read_commits(str(fake_repo), since, until, author_email="other@example.com")
    assert commits == []

    commits, _ = read_commits(str(fake_repo), since, until, author_email="test@example.com")
    assert len(commits) == 2


def test_commit_fields(fake_repo):
    since = datetime(2000, 1, 1, tzinfo=timezone.utc)
    until = datetime(2099, 1, 1, tzinfo=timezone.utc)
    commits, _ = read_commits(str(fake_repo), since, until)
    c = commits[0]

    assert len(c.short_hash) == 7
    assert c.hash.startswith(c.short_hash)
    assert c.author_email == "test@example.com"
    assert c.repo_name == fake_repo.name
    assert isinstance(c.message, str)


def test_invalid_repo_raises():
    with pytest.raises(ValueError, match="Not a git repository"):
        read_commits("/nonexistent/path/xyz", datetime(2000, 1, 1), datetime(2099, 1, 1))


def test_date_range_filter(fake_repo):
    since = datetime(2000, 1, 1, tzinfo=timezone.utc)
    until = datetime(2000, 1, 2, tzinfo=timezone.utc)
    commits, _ = read_commits(str(fake_repo), since, until)
    assert commits == []
