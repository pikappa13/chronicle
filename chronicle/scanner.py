from __future__ import annotations

import os
from datetime import datetime, timezone

import git

_SKIP_DIRS = {
    "node_modules", ".venv", "venv", "__pycache__",
    ".git", "dist", "build", ".tox", ".eggs",
}
_MAX_REPOS = 50


def _last_commit_time(repo_path: str) -> datetime:
    try:
        repo = git.Repo(repo_path)
        commit = next(repo.iter_commits())
        dt = commit.committed_datetime
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)


def find_repos(root_path: str, max_depth: int = 4) -> list[str]:
    root_path = os.path.abspath(root_path)
    found: list[str] = []

    def _walk(path: str, depth: int) -> None:
        if depth > max_depth or len(found) >= _MAX_REPOS:
            return

        git_dir = os.path.join(path, ".git")
        if os.path.isdir(git_dir):
            # Exclude submodules stored inside another .git
            if not os.path.isfile(git_dir):
                found.append(path)
            return  # don't recurse into a repo

        try:
            entries = os.scandir(path)
        except PermissionError:
            return

        for entry in entries:
            if not entry.is_dir(follow_symlinks=False):
                continue
            if entry.name in _SKIP_DIRS or entry.name.startswith("."):
                continue
            _walk(entry.path, depth + 1)

    _walk(root_path, 0)
    found.sort(key=_last_commit_time, reverse=True)
    return found[:_MAX_REPOS]
