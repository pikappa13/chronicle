from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Tuple

import git


@dataclass
class Commit:
    hash: str
    short_hash: str
    message: str
    date: datetime
    author_email: str
    repo_name: str
    repo_path: str
    files_changed: list[str] = field(default_factory=list)


def _get_local_author(repo: git.Repo) -> Optional[str]:
    try:
        return repo.config_reader().get_value("user", "email", None)
    except Exception:
        return None


def _to_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def read_commits(
    repo_path: str,
    since: datetime,
    until: datetime,
    author_email: Optional[str] = None,
) -> Tuple[list[Commit], Optional[str]]:
    """Returns (commits, resolved_author_email).
    resolved_author_email is None if no author filter was applied."""
    try:
        repo = git.Repo(repo_path, search_parent_directories=False)
    except (git.InvalidGitRepositoryError, git.NoSuchPathError):
        raise ValueError(f"Not a git repository: {repo_path}")

    repo_name = os.path.basename(os.path.abspath(repo_path))

    resolved_author = author_email
    if resolved_author is None:
        resolved_author = _get_local_author(repo)

    since_aware = _to_aware(since)
    until_aware = _to_aware(until)

    commits: list[Commit] = []
    try:
        for raw in repo.iter_commits(all=True):
            committed_dt = _to_aware(raw.committed_datetime)
            if committed_dt < since_aware or committed_dt > until_aware:
                continue
            if resolved_author and raw.author.email.lower() != resolved_author.lower():
                continue

            try:
                files = list(raw.stats.files.keys())
            except Exception:
                files = []

            commits.append(
                Commit(
                    hash=raw.hexsha,
                    short_hash=raw.hexsha[:7],
                    message=raw.message.strip().splitlines()[0],
                    date=committed_dt,
                    author_email=raw.author.email,
                    repo_name=repo_name,
                    repo_path=os.path.abspath(repo_path),
                    files_changed=files,
                )
            )
    except Exception:
        pass

    return commits, resolved_author
