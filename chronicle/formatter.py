from __future__ import annotations

import json
from datetime import date
from typing import Optional

import sys

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .grouper import DayGroup, WeekGroup
from .summarizer import estimate_hours, summarize_commits

# Force UTF-8 on Windows to support block characters
console = Console(highlight=False)

_BAR_MAX = 8
# ASCII fallback for terminals that can't render block chars (e.g. Windows CP1252)
_BAR_UNICODE = "█"
_BAR_ASCII = "#"


def _supports_unicode() -> bool:
    try:
        "█".encode(sys.stdout.encoding or "utf-8")
        return True
    except (UnicodeEncodeError, LookupError):
        return False


def _bar(count: int, max_count: int) -> str:
    if max_count == 0:
        return ""
    char = _BAR_UNICODE if _supports_unicode() else _BAR_ASCII
    filled = round((count / max_count) * _BAR_MAX)
    return char * filled or char


def format_terminal(week: WeekGroup) -> None:
    if not week.days:
        console.print("[dim]No commits found for this period.[/dim]")
        return

    max_commits = max(d.total_commits for d in week.days)

    sep = " - " if not _supports_unicode() else " – "
    period = f"{week.start.strftime('%b %d')}{sep}{week.end.strftime('%b %d, %Y')}"
    console.print()
    console.print(Panel(f"[bold]Chronicle[/bold]  [dim]{period}[/dim]", expand=False))
    console.print()

    for day in week.days:
        day_label = Text(day.date.strftime("%A, %b %d"), style="bold blue")
        bar = Text(_bar(day.total_commits, max_commits), style="cyan")
        count_label = Text(f"  {day.total_commits} commit{'s' if day.total_commits != 1 else ''}", style="dim")

        console.print(day_label, bar, count_label)

        for repo_name, commits in day.repos.items():
            summary = summarize_commits(commits)
            repo_text = Text(f"  {repo_name}", style="green")
            summary_text = Text(f"  {summary}")
            console.print(repo_text, summary_text)

        console.print()

    hours = estimate_hours([c for d in week.days for c in d.all_commits])
    repos_str = ", ".join(week.repos_touched)
    dot = " | " if not _supports_unicode() else "  ·  "
    console.print(
        f"[dim]Total:[/dim] [bold]{week.total_commits}[/bold] commits"
        f"{dot}[bold]{hours:.1f}h[/bold] estimated"
        f"{dot}[dim]{repos_str}[/dim]"
    )
    console.print()


def format_standup(yesterday: Optional[DayGroup], today: Optional[DayGroup]) -> None:
    lines: list[str] = []

    def _section(label: str, day: Optional[DayGroup]) -> list[str]:
        out = [f"[bold]{label}[/bold]"]
        if day is None or day.total_commits == 0:
            out.append("  [dim]No commits[/dim]")
        else:
            for repo_name, commits in day.repos.items():
                summary = summarize_commits(commits)
                out.append(f"  [green]{repo_name}[/green]: {summary}")
        return out

    lines += _section("Yesterday", yesterday)
    lines.append("")
    lines += _section("Today", today)

    console.print(Panel("\n".join(lines), title="Standup", expand=False))


def format_markdown(week: WeekGroup) -> str:
    if not week.days:
        return "_No commits found for this period._\n"

    period = f"{week.start.strftime('%b %d')} - {week.end.strftime('%b %d, %Y')}"
    lines = [f"# Chronicle - {period}", ""]

    for day in week.days:
        lines.append(f"## {day.date.strftime('%A, %B %d')}")
        for repo_name, commits in day.repos.items():
            lines.append(f"- **{repo_name}**")
            for c in commits:
                lines.append(f"  - {c.message} `{c.short_hash}`")
        lines.append("")

    hours = estimate_hours([c for d in week.days for c in d.all_commits])
    lines += [
        "---",
        f"**Total:** {week.total_commits} commits | {hours:.1f}h estimated",
        "",
    ]
    return "\n".join(lines)


def format_slack(week: WeekGroup) -> str:
    if not week.days:
        return "_No commits found for this period._"

    period = f"{week.start.strftime('%b %d')} - {week.end.strftime('%b %d, %Y')}"
    lines = [f"*Chronicle - {period}*", ""]

    for day in week.days:
        lines.append(f"*{day.date.strftime('%A, %b %d')}*")
        for repo_name, commits in day.repos.items():
            summary = summarize_commits(commits)
            lines.append(f"  • *{repo_name}*: {summary}")
        lines.append("")

    hours = estimate_hours([c for d in week.days for c in d.all_commits])
    lines.append(f"_{week.total_commits} commits | {hours:.1f}h estimated_")
    return "\n".join(lines)


def format_json(week: WeekGroup) -> str:
    hours = estimate_hours([c for d in week.days for c in d.all_commits])
    data = {
        "period": {
            "start": week.start.isoformat(),
            "end": week.end.isoformat(),
        },
        "total_commits": week.total_commits,
        "estimated_hours": hours,
        "repos_touched": week.repos_touched,
        "days": [
            {
                "date": day.date.isoformat(),
                "total_commits": day.total_commits,
                "repos": {
                    repo_name: [
                        {
                            "hash": c.short_hash,
                            "message": c.message,
                            "author": c.author_email,
                            "files_changed": c.files_changed,
                        }
                        for c in commits
                    ]
                    for repo_name, commits in day.repos.items()
                },
            }
            for day in week.days
        ],
    }
    return json.dumps(data, indent=2)
