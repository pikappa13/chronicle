# chronicle

**Your git history, told as a story.**

[![PyPI](https://img.shields.io/pypi/v/chronicle-git)](https://pypi.org/project/chronicle-git/)
[![Python](https://img.shields.io/pypi/pyversions/chronicle-git)](https://pypi.org/project/chronicle-git/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/chronicle-git)](https://pypi.org/project/chronicle-git/)

---

Every Monday morning, every standup, every sprint review — someone asks:

> "What did you work on this week?"

And you open five tabs, scroll through Slack, squint at git log, and reconstruct your week from memory.

**chronicle reads your git history and answers in 2 seconds.**

No AI. No cloud. No account. No config. Works on any repo you already have.

---

## Install

```bash
pip install chronicle-git
```

---

## Usage

```bash
chronicle today        # what you did today
chronicle standup      # yesterday + today, standup format
chronicle week         # full week view
chronicle month        # this month
chronicle since "3 days ago"
```

Works in any git repo. No setup required.

---

## Examples

### `chronicle standup`

```
╭─ Chronicle · Standup · Mon Jun 9 ───────────────────────────────╮
│                                                                   │
│  Friday Jun 6                                                    │
│    auth-service    ██  3 commits                                 │
│                        refactored JWT validation                  │
│                        fixed token expiry edge case              │
│    frontend        █   1 commit                                  │
│                        updated login form error states           │
│                                                                   │
│  Today                                                           │
│    auth-service    █   1 commit (so far)                         │
│                        started refresh token endpoint            │
│                                                                   │
╰──────────────────────────────────────────────────────────────────╯
```

### `chronicle week`

```
Week 23 · Jun 3–9 · 4 repos · 23 commits · ~14h

  Mon Jun 3   auth-service   Started OAuth2 integration
  Tue Jun 4   auth-service   ████  OAuth2 complete + tests
  Wed Jun 5   frontend       ██    Login/logout flow, token storage
              infra           █    Docker compose update
  Thu Jun 6   auth-service   ██    JWT refactor, expiry fix
  Fri Jun 8   auth-service   █     Refresh token (in progress)

  Top files: auth/jwt.py (8×)  components/Login.tsx (5×)
```

---

## Multiple repos

```bash
# scan all repos in your home directory
chronicle week --all

# scan a specific directory
chronicle week --dir ~/projects
```

---

## Export formats

```bash
chronicle week --format markdown   # paste into Notion, Obsidian, GitHub
chronicle week --format slack      # paste into Slack standup
chronicle week --format json       # pipe into other tools
chronicle standup --copy           # copy to clipboard directly
```

---

## Options

```
--repo    -r    Path to git repo (default: current directory)
--author  -a    Filter by author email (default: your git config)
--format  -f    Output format: terminal, markdown, slack, json
--all           Scan all repos in home directory
--dir     -d    Directory to scan for repos
--copy    -c    Copy output to clipboard (standup only)
```

---

## Why not just use `git log`?

`git log` is for archaeologists. chronicle is for humans.

```bash
# what you do now
git log --oneline --since="1 week ago" --author="you@email.com"
# → raw, ugly, repo-by-repo, no summary

# what you do with chronicle
chronicle week
# → readable, grouped, summarized, beautiful
```

---

## Philosophy

- **Zero config** — works on any repo without setup
- **Local only** — reads your git history, touches nothing else
- **No AI** — pure string manipulation, deterministic output
- **No cloud** — your data never leaves your machine
- **No account** — nothing to sign up for, nothing to pay
- **Open formats** — output is text you own

---

## Contributing

Issues and PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
git clone https://github.com/pikappa13/chronicle
cd chronicle
pip install -e ".[dev]"
pytest
```

---

## License

MIT
