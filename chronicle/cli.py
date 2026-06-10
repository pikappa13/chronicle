from __future__ import annotations

import os
import re
import sys
from datetime import date, datetime, time, timedelta, timezone
from typing import Optional

import typer
from rich.console import Console

from . import __version__
from .formatter import (
    format_json,
    format_markdown,
    format_slack,
    format_standup,
    format_terminal,
)
from .grouper import group_by_day, group_by_week
from .reader import read_commits
from .scanner import find_repos

app = typer.Typer(
    name="chronicle",
    help="Your git history, told as a story.",
    add_completion=True,
    no_args_is_help=True,
)
console = Console()
err_console = Console(stderr=True)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"chronicle {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", callback=_version_callback, is_eager=True
    ),
) -> None:
    pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _start_of_day(d: date) -> datetime:
    return datetime.combine(d, time.min, tzinfo=timezone.utc)


def _end_of_day(d: date) -> datetime:
    return datetime.combine(d, time.max, tzinfo=timezone.utc)


def _find_repo(start: Optional[str]) -> Optional[str]:
    """Walk up from start (or cwd) looking for a .git directory."""
    path = os.path.abspath(start or os.getcwd())
    for _ in range(4):
        if os.path.isdir(os.path.join(path, ".git")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    return None


def _collect_repos(
    repo: Optional[str],
    all_repos: bool,
    scan_dir: Optional[str],
) -> list[str]:
    if repo:
        return [os.path.abspath(repo)]
    if all_repos:
        root = scan_dir or os.path.expanduser("~")
        repos = find_repos(root)
        if not repos:
            err_console.print("[yellow]No git repositories found.[/yellow]")
            raise typer.Exit(1)
        return repos
    found = _find_repo(None)
    if found:
        return [found]
    err_console.print(
        "[red]No git repository found.[/red] "
        "Use [bold]--repo PATH[/bold] or [bold]--all[/bold] to scan a directory."
    )
    raise typer.Exit(1)


def _load_commits(
    repos: list[str], since: datetime, until: datetime, author: Optional[str]
) -> list:
    from .reader import Commit
    all_commits: list[Commit] = []
    warned_author: set[str] = set()
    for r in repos:
        try:
            commits, resolved_author = read_commits(r, since, until, author)
            if not commits and resolved_author and resolved_author not in warned_author:
                # Check if the repo has any commits at all in this period (without author filter)
                all_in_period, _ = read_commits(r, since, until, author_email=None)
                if all_in_period:
                    err_console.print(
                        f"[yellow]No commits by[/yellow] [bold]{resolved_author}[/bold] "
                        f"[yellow]in[/yellow] [bold]{r}[/bold][yellow]. "
                        f"Use --author to specify a different email.[/yellow]"
                    )
                    warned_author.add(resolved_author)
            all_commits.extend(commits)
        except ValueError as e:
            err_console.print(f"[dim]Skipping {r}: {e}[/dim]")
    return all_commits


def _output(fmt: str, week, yesterday=None, today=None) -> None:
    if fmt == "terminal":
        if yesterday is not None or today is not None:
            format_standup(yesterday, today)
        else:
            format_terminal(week)
    elif fmt == "markdown":
        print(format_markdown(week))
    elif fmt == "slack":
        print(format_slack(week))
    elif fmt == "json":
        print(format_json(week))
    else:
        err_console.print(
            f"[red]Unknown format:[/red] {fmt}. Choose: terminal, markdown, slack, json"
        )
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# Date parser for `since` command
# ---------------------------------------------------------------------------

def _parse_relative_date(when: str) -> datetime:
    when = when.lower().strip()
    today = date.today()

    # "today" / "yesterday"
    if when == "today":
        return _start_of_day(today)
    if when == "yesterday":
        return _start_of_day(today - timedelta(days=1))

    # "N days ago", "N weeks ago", "N months ago"
    m = re.match(r"(\d+)\s+(day|week|month|year)s?\s+ago", when)
    if m:
        n = int(m.group(1))
        unit = m.group(2)
        if unit == "day":
            return _start_of_day(today - timedelta(days=n))
        if unit == "week":
            return _start_of_day(today - timedelta(weeks=n))
        if unit == "month":
            return _start_of_day(today - timedelta(days=n * 30))
        if unit == "year":
            return _start_of_day(today - timedelta(days=n * 365))

    # "last monday/tuesday/..."
    day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    m2 = re.match(r"last\s+(\w+)", when)
    if m2 and m2.group(1) in day_names:
        target_weekday = day_names.index(m2.group(1))
        days_back = (today.weekday() - target_weekday) % 7 or 7
        return _start_of_day(today - timedelta(days=days_back))

    # Try dateparser if available
    try:
        import dateparser
        result = dateparser.parse(when)
        if result:
            return result.replace(tzinfo=timezone.utc)
    except ImportError:
        pass

    raise typer.BadParameter(
        f"Cannot parse date: '{when}'. Try: '3 days ago', '2 weeks ago', 'last monday'."
    )


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

@app.command()
def today(
    repo: Optional[str] = typer.Option(None, "--repo", "-r", help="Path to git repo"),
    author: Optional[str] = typer.Option(None, "--author", "-a", help="Filter by author email"),
    format: str = typer.Option("terminal", "--format", "-f", help="terminal | markdown | slack | json"),  # noqa: E501
    all_repos: bool = typer.Option(False, "--all", help="Scan all repos in home directory"),
    dir: Optional[str] = typer.Option(None, "--dir", "-d", help="Directory to scan when using --all"),  # noqa: E501
) -> None:
    """Show what you did today."""
    repos = _collect_repos(repo, all_repos, dir)
    now = date.today()
    commits = _load_commits(repos, _start_of_day(now), _end_of_day(now), author)
    week = group_by_week(commits)
    _output(format, week)


@app.command()
def standup(
    repo: Optional[str] = typer.Option(None, "--repo", "-r"),
    author: Optional[str] = typer.Option(None, "--author", "-a"),
    format: str = typer.Option("terminal", "--format", "-f"),
    copy: bool = typer.Option(False, "--copy", "-c", help="Copy output to clipboard"),
    all_repos: bool = typer.Option(False, "--all"),
    dir: Optional[str] = typer.Option(None, "--dir", "-d"),
) -> None:
    """Show yesterday + today in standup format."""
    repos = _collect_repos(repo, all_repos, dir)
    today_date = date.today()
    # If Monday, yesterday = last Friday
    if today_date.weekday() == 0:
        yesterday_date = today_date - timedelta(days=3)
    else:
        yesterday_date = today_date - timedelta(days=1)

    since = _start_of_day(yesterday_date)
    until = _end_of_day(today_date)
    commits = _load_commits(repos, since, until, author)

    day_groups = {g.date: g for g in group_by_day(commits)}
    yesterday_group = day_groups.get(yesterday_date)
    today_group = day_groups.get(today_date)

    if format == "terminal":
        format_standup(yesterday_group, today_group)
    else:
        week = group_by_week(commits)
        _output(format, week)

    if copy:
        text = format_slack(group_by_week(commits))
        try:
            import subprocess
            if sys.platform == "win32":
                subprocess.run(["clip"], input=text.encode(), check=True)
            elif sys.platform == "darwin":
                subprocess.run(["pbcopy"], input=text.encode(), check=True)
            else:
                subprocess.run(
                    ["xclip", "-selection", "clipboard"], input=text.encode(), check=True
                )
            console.print("[dim]Copied to clipboard.[/dim]")
        except Exception:
            err_console.print("[yellow]Could not copy to clipboard.[/yellow]")


@app.command()
def week(
    repo: Optional[str] = typer.Option(None, "--repo", "-r"),
    author: Optional[str] = typer.Option(None, "--author", "-a"),
    format: str = typer.Option("terminal", "--format", "-f"),
    all_repos: bool = typer.Option(False, "--all"),
    dir: Optional[str] = typer.Option(None, "--dir", "-d", help="Directory to scan for repos"),
) -> None:
    """Show what you did this week."""
    repos = _collect_repos(repo, all_repos, dir)
    today_date = date.today()
    monday = today_date - timedelta(days=today_date.weekday())
    commits = _load_commits(repos, _start_of_day(monday), _end_of_day(today_date), author)
    week_group = group_by_week(commits)
    _output(format, week_group)


@app.command()
def month(
    repo: Optional[str] = typer.Option(None, "--repo", "-r"),
    author: Optional[str] = typer.Option(None, "--author", "-a"),
    format: str = typer.Option("terminal", "--format", "-f"),
    all_repos: bool = typer.Option(False, "--all"),
    dir: Optional[str] = typer.Option(None, "--dir", "-d"),
) -> None:
    """Show what you did this month."""
    repos = _collect_repos(repo, all_repos, dir)
    today_date = date.today()
    start = today_date.replace(day=1)
    commits = _load_commits(repos, _start_of_day(start), _end_of_day(today_date), author)
    week_group = group_by_week(commits)
    _output(format, week_group)


@app.command()
def since(
    when: str = typer.Argument(..., help="e.g. '3 days ago', '2 weeks ago', 'last monday'"),
    repo: Optional[str] = typer.Option(None, "--repo", "-r"),
    author: Optional[str] = typer.Option(None, "--author", "-a"),
    format: str = typer.Option("terminal", "--format", "-f"),
    all_repos: bool = typer.Option(False, "--all"),
    dir: Optional[str] = typer.Option(None, "--dir", "-d"),
) -> None:
    """Show commits since a relative date."""
    since_dt = _parse_relative_date(when)
    repos = _collect_repos(repo, all_repos, dir)
    until_dt = _end_of_day(date.today())
    commits = _load_commits(repos, since_dt, until_dt, author)
    week_group = group_by_week(commits)
    _output(format, week_group)


if __name__ == "__main__":
    app()
