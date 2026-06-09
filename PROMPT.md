# Prompt di implementazione — Chronicle

Questo è il prompt da dare a Claude Code (o qualsiasi AI coding assistant) per costruire Chronicle da zero. È scritto per essere copiato e incollato direttamente.

---

## PROMPT COMPLETO

```
Costruisci un tool CLI Python chiamato "chronicle" che legge la git history e risponde alla domanda "cosa ho fatto?".

## OBIETTIVO

Chronicle è un CLI tool open source, zero-config, che legge i commit git di uno o più repository e li presenta in modo leggibile nel terminale. Nessuna AI, nessun cloud, nessun account. Funziona su qualsiasi repo git esistente in 30 secondi dall'installazione.

## STACK

- Python 3.9+
- gitpython (leggere git history)
- rich (output terminale colorato)
- typer (CLI)
- pyproject.toml per packaging (installabile con pip install chronicle-git)

## STRUTTURA FILE DA CREARE

```
chronicle/
├── chronicle/
│   ├── __init__.py          # version = "0.1.0"
│   ├── cli.py               # entry point Typer
│   ├── reader.py            # legge git log
│   ├── grouper.py           # raggruppa commit per giorno/repo
│   ├── summarizer.py        # genera titoli leggibili
│   ├── formatter.py         # formatta output (terminal, markdown, slack, json)
│   └── scanner.py           # trova tutti i repo git in una directory
├── tests/
│   ├── __init__.py
│   ├── test_reader.py
│   ├── test_grouper.py
│   └── test_formatter.py
├── pyproject.toml
├── README.md
└── .github/workflows/ci.yml
```

## MODULI — SPECIFICHE PRECISE

### reader.py

```python
# Dataclass principale
@dataclass
class Commit:
    hash: str
    short_hash: str       # primi 7 caratteri
    message: str
    date: datetime
    author_email: str
    repo_name: str        # nome della cartella del repo
    repo_path: str        # path assoluto
    files_changed: list[str]  # lista file toccati

# Funzione principale
def read_commits(
    repo_path: str,
    since: datetime,
    until: datetime,
    author_email: str | None = None  # None = tutti gli autori
) -> list[Commit]:
    # Usa gitpython per leggere i commit
    # Se author_email è None, prova a leggere da git config user.email
    # Se non trovato, usa tutti i commit
    # Gestisci eccezioni: repo non valido, no commits, ecc.
    ...
```

### grouper.py

```python
@dataclass
class DayGroup:
    date: date
    repos: dict[str, list[Commit]]  # repo_name -> commits

@dataclass  
class WeekGroup:
    start: date
    end: date
    days: list[DayGroup]
    total_commits: int
    repos_touched: list[str]

def group_by_day(commits: list[Commit]) -> list[DayGroup]:
    # Raggruppa per data, poi per repo dentro ogni giorno
    ...

def group_by_week(commits: list[Commit]) -> WeekGroup:
    # Usa group_by_day internamente
    # Calcola start (lunedì) e end (domenica o oggi) della settimana
    ...
```

### summarizer.py

```python
def summarize_commits(commits: list[Commit]) -> str:
    # Senza AI — manipolazione di stringhe pura
    # Se 1 commit: restituisce il messaggio pulito
    # Se 2-3 commit: li concatena con virgola, tronca a 80 char
    # Se 4+ commit: prende il primo, aggiunge "and N more"
    # Pulizia: rimuove prefissi tipo "feat:", "fix:", "chore:" (conventional commits)
    # Restituisce stringa leggibile
    ...

def estimate_hours(commits: list[Commit]) -> float:
    # Euristica semplice: 
    # primo commit del giorno = 1h setup
    # ogni commit successivo = +0.5h
    # mai più di 8h al giorno
    # Restituisce ore stimate come float
    ...
```

### formatter.py

```python
def format_terminal(week: WeekGroup) -> None:
    # Usa rich per output colorato
    # Layout: tabella per giorno, con barre █ proporzionali al numero di commit
    # Colori: data in blu, repo in verde, summary in bianco, stat in grigio
    # Mostra in fondo: totale commit, repos toccati, ore stimate
    ...

def format_standup(yesterday: DayGroup | None, today: DayGroup | None) -> None:
    # Box rich con sezione "Yesterday" e sezione "Today"
    # Se oggi è lunedì, "Yesterday" = venerdì scorso
    # Formato compatto, adatto a essere letto in meeting
    ...

def format_markdown(week: WeekGroup) -> str:
    # Markdown puro (nessun import esterno)
    # Intestazione con periodo
    # Lista per giorno, sublista per repo
    # Adatto per Notion, Obsidian, GitHub PR description
    ...

def format_slack(week: WeekGroup) -> str:
    # Testo semplice formattato per Slack
    # Usa *bold* di Slack
    # Nessun emoji obbligatorio
    ...

def format_json(week: WeekGroup) -> str:
    # JSON strutturato, pretty-printed
    # Adatto per integrazioni custom
    ...
```

### scanner.py

```python
def find_repos(root_path: str, max_depth: int = 4) -> list[str]:
    # Traversal ricorsivo fino a max_depth
    # Identifica repo git dalla presenza di cartella .git
    # Esclude: node_modules, .venv, venv, __pycache__, .git/modules
    # Ordina per data ultimo commit (più recente prima)
    # Limita a 50 repo max per evitare scan troppo lunghi
    ...
```

### cli.py

```python
import typer
from typing import Optional
from datetime import datetime, timedelta

app = typer.Typer(
    name="chronicle",
    help="Your git history, told as a story.",
    add_completion=True,
)

@app.command()
def today(
    repo: Optional[str] = typer.Option(None, "--repo", "-r", help="Path to git repo (default: current directory)"),
    author: Optional[str] = typer.Option(None, "--author", "-a", help="Filter by author email"),
    format: str = typer.Option("terminal", "--format", "-f", help="Output format: terminal, markdown, slack, json"),
    all_repos: bool = typer.Option(False, "--all", help="Scan all repos in home directory"),
):
    """Show what you did today."""
    ...

@app.command()
def standup(
    repo: Optional[str] = typer.Option(None, "--repo", "-r"),
    author: Optional[str] = typer.Option(None, "--author", "-a"),
    format: str = typer.Option("terminal", "--format", "-f"),
    copy: bool = typer.Option(False, "--copy", "-c", help="Copy output to clipboard"),
    all_repos: bool = typer.Option(False, "--all"),
):
    """Show yesterday + today in standup format."""
    ...

@app.command()
def week(
    repo: Optional[str] = typer.Option(None, "--repo", "-r"),
    author: Optional[str] = typer.Option(None, "--author", "-a"),
    format: str = typer.Option("terminal", "--format", "-f"),
    all_repos: bool = typer.Option(False, "--all"),
    dir: Optional[str] = typer.Option(None, "--dir", "-d", help="Directory to scan for repos"),
):
    """Show what you did this week."""
    ...

@app.command()
def month(
    repo: Optional[str] = typer.Option(None, "--repo", "-r"),
    author: Optional[str] = typer.Option(None, "--author", "-a"),
    format: str = typer.Option("terminal", "--format", "-f"),
    all_repos: bool = typer.Option(False, "--all"),
):
    """Show what you did this month."""
    ...

@app.command()
def since(
    when: str = typer.Argument(..., help="e.g. '3 days ago', '2 weeks ago', 'last monday'"),
    repo: Optional[str] = typer.Option(None, "--repo", "-r"),
    author: Optional[str] = typer.Option(None, "--author", "-a"),
    format: str = typer.Option("terminal", "--format", "-f"),
    all_repos: bool = typer.Option(False, "--all"),
):
    """Show commits since a relative date."""
    # Parsa "3 days ago", "2 weeks ago", "last monday" senza librerie esterne
    # Usa dateparser se disponibile, altrimenti parsing manuale dei casi comuni
    ...

if __name__ == "__main__":
    app()
```

## pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "chronicle-git"
version = "0.1.0"
description = "Your git history, told as a story."
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.9"
keywords = ["git", "cli", "developer-tools", "productivity", "standup"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Version Control :: Git",
]
dependencies = [
    "gitpython>=3.1",
    "rich>=13.0",
    "typer>=0.9",
]

[project.scripts]
chronicle = "chronicle.cli:app"

[project.urls]
Homepage = "https://github.com/TUO_USERNAME/chronicle"
Repository = "https://github.com/TUO_USERNAME/chronicle"
Issues = "https://github.com/TUO_USERNAME/chronicle/issues"

[tool.hatch.version]
path = "chronicle/__init__.py"
```

## COMPORTAMENTO DEFAULT IMPORTANTE

Quando l'utente esegue `chronicle week` SENZA argomenti:
1. Cerca un repo git nella directory corrente
2. Se non trovato, cerca nella directory padre (fino a 3 livelli)
3. Se non trovato, stampa messaggio chiaro: "No git repository found. Use --repo PATH or --all to scan home directory."
4. Legge l'autore da `git config user.email` automaticamente
5. Se non configurato, mostra tutti i commit del repo

## GESTIONE ERRORI

- Repo non git → messaggio chiaro, non stack trace
- Nessun commit nel periodo → "No commits found for this period." (non errore)
- Autore non trovato → warning soft, mostra tutti i commit
- Permessi file → skip silenzioso con warning finale

## TEST

Scrivi test per:
- `test_reader.py`: crea un repo git temporaneo con commits fake, verifica che reader li legga correttamente
- `test_grouper.py`: dato un set di Commit con date diverse, verifica il raggruppamento
- `test_formatter.py`: verifica che format_markdown e format_json producano output valido

## QUALITÀ DEL CODICE

- Type hints ovunque
- Nessun commento ovvio — solo dove il perché non è chiaro
- Nessuna funzione più lunga di 40 righe
- Nessuna dipendenza fuori da quelle elencate

Costruisci tutto questo in modo completo e funzionante. Inizia da reader.py e grouper.py perché sono il cuore, poi formatter.py, poi cli.py. Alla fine i test e il pyproject.toml.
```

---

## Note per usare questo prompt

1. **Incollalo direttamente** in una nuova sessione Claude Code nella cartella `chronicle/`
2. **Non modificarlo** prima di averlo provato — è calibrato per ottenere il massimo in una sola sessione
3. **Dopo il primo run**, usa questi prompt di follow-up:

### Follow-up 1 — dopo aver visto il codice generato
```
Ora aggiungi --all flag funzionante con scanner.py. Testa che `chronicle week --all --dir ~/` trovi correttamente tutti i repo git nella home e aggreghi i risultati senza duplicati.
```

### Follow-up 2 — per la UX
```
Migliora l'output terminal. Voglio che `chronicle week` sembri bello come la dashboard di GitHub. Usa rich panels, colori coerenti (blu per date, verde per repo names, bianco per summary, grigio per metadati). Aggiungi una progress bar durante la scansione multi-repo.
```

### Follow-up 3 — per il lancio
```
Aggiungi `chronicle report` che genera un file HTML statico con:
- Heatmap settimanale dei commit (stile GitHub contribution graph)
- Lista cronologica degli interventi per repo
- CSS embedded (nessuna dipendenza esterna)
- Apribile con `chronicle report --open` direttamente nel browser
Deve sembrare professionale e condivisibile.
```
