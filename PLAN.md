# Chronicle — Piano Completo del Progetto

## Il problema in una frase

Ogni developer del mondo perde 10-20 minuti ogni lunedì, ogni standup, ogni fine sprint a rispondere a "cosa hai fatto?". Git sa già tutto. Nessun tool lo racconta bene.

## La soluzione in una frase

Chronicle legge la tua git history e risponde in 2 secondi, in modo leggibile, bello, senza AI, senza cloud, senza config.

---

## Perché può raggiungere 10k+ stelle

### Analisi dei competitor morti

| Tool | Stelle | Ultimo commit | Problema |
|------|--------|---------------|---------|
| git-standup | 7,200 | 2020 | Abbandonato, solo nomi autori |
| git-hours | 6,100 | 2019 | Solo time tracking, output brutto |
| git-recap | 800 | 2021 | Quasi sconosciuto |
| gitstats | 6,000 | 2022 | HTML statico, lento, non CLI-friendly |
| git-fame | 3,100 | attivo | Solo statistiche per autore, non daily use |

**Il mercato è scoperto.** Nessun tool moderno, mantenuto, con bella UX risolve "cosa ho fatto?" nel 2025.

### Perché questo specifico tool diventa virale

1. **Problema quotidiano** — standup meeting esistono in ogni team del mondo
2. **"Wow factor" immediato** — installi, esegui, vedi output bello in 5 secondi
3. **Condivisibile** — la gente screenshotta il terminal e posta su X/Reddit/HN
4. **Zero friction** — funziona su qualsiasi repo git senza config
5. **Nome corto e memorabile** — `chronicle`
6. **Use case da README perfetto** — il problema si spiega in 2 righe

---

## Architettura tecnica

### Stack

- **Linguaggio:** Python 3.9+
- **Dipendenze core:**
  - `gitpython` — leggere git history
  - `rich` — output colorato e tabelle nel terminale
  - `typer` — CLI moderna
- **Dipendenze zero per l'utente** — installa con `pip install chronicle-git`
- **Nessun server, nessun database, nessun account**

### Struttura file

```
chronicle/
├── chronicle/
│   ├── __init__.py
│   ├── cli.py          # Entry point Typer (today, week, standup, month, since)
│   ├── reader.py       # Legge git log da uno o più repo
│   ├── formatter.py    # Formatta output (terminal, markdown, slack, json)
│   ├── grouper.py      # Raggruppa commit per giorno/settimana/repo
│   ├── summarizer.py   # Genera titoli leggibili dai messaggi di commit
│   └── scanner.py      # Trova tutti i repo git in una directory
├── tests/
│   ├── test_reader.py
│   ├── test_formatter.py
│   └── test_grouper.py
├── pyproject.toml
├── README.md
├── LICENSE            # MIT
└── .github/
    └── workflows/
        └── ci.yml
```

### Moduli — responsabilità precise

**`reader.py`**
- Dato un path, apre il repo git
- Legge i commit filtrati per autore (default: git config user.email) e periodo
- Restituisce lista di oggetti `Commit(hash, message, date, repo_name, files_changed)`

**`grouper.py`**
- Prende lista di Commit
- Raggruppa per giorno, per repo, per settimana
- Restituisce struttura gerarchica `Week > Day > Repo > [Commits]`

**`summarizer.py`**
- Prende un gruppo di commit message
- Genera un riassunto leggibile senza AI:
  - Deduplica messaggi simili
  - Estrae verbi principali (fix, add, refactor, update)
  - Conta commit per contesto
- Nessuna AI — pura manipolazione di stringhe

**`formatter.py`**
- Prende la struttura gerarchica
- Produce output in formato: terminal (rich), markdown, slack, json
- `--format=terminal` default con colori e simboli
- `--format=markdown` per incollare su Notion/Obsidian
- `--format=slack` per il blocco di testo standup
- `--format=json` per integrazioni custom

**`scanner.py`**
- Dato un path (default: `~`), trova tutti i repo git
- Usato da `chronicle week --all` per scan multi-repo
- Restituisce lista di path repo ordinati per attività recente

**`cli.py`**
- `chronicle today` — commit di oggi
- `chronicle standup` — ieri + oggi (formato standup)
- `chronicle week` — settimana corrente
- `chronicle month` — mese corrente
- `chronicle since "3 days ago"` — periodo custom
- Flag globali: `--author EMAIL`, `--format FORMAT`, `--all` (multi-repo), `--repo PATH`

---

## Milestone di sviluppo

### v0.1 — MVP (2-3 giorni)
- [x] `chronicle today` e `chronicle week` su repo singolo
- [x] Output terminal con Rich (colori, tabelle)
- [x] Filtro automatico per autore (git config)
- [x] `pip install chronicle-git` funzionante
- [x] README con GIF demo

### v0.2 — Multi-repo (1 settimana dopo)
- [ ] `chronicle week --all` scansiona tutti i repo nella home
- [ ] `chronicle week --dir ~/projects` per cartella specifica
- [ ] Mostra da quale repo viene ogni attività
- [ ] Deduplicazione repo (ignora fork, ignora node_modules)

### v0.3 — Formati export (1 settimana dopo)
- [ ] `--format=markdown` per Notion, Obsidian, GitHub
- [ ] `--format=slack` per copy-paste diretto
- [ ] `--format=json` per automazioni
- [ ] `chronicle standup --copy` copia negli appunti automaticamente

### v0.4 — Report visivo (3 settimane dopo MVP) ← **questo porta le stelle**
- [ ] `chronicle report` genera HTML statico bellissimo
- [ ] Heatmap tipo GitHub contribution graph
- [ ] Timeline visiva dei progetti toccati
- [ ] Esportabile come PNG (screenshot condivisibile)
- [ ] Questo è il momento di postare su HN e Reddit

### v0.5 — Config e maturità
- [ ] `.chronicle.yml` per escludere repo, rinominare, impostare autore
- [ ] `chronicle alias standup "week --format=slack"` per shortcut custom
- [ ] Shell completion (bash, zsh, fish)
- [ ] Packaging per Homebrew (Mac) e Scoop (Windows)

---

## Output design — esempi esatti

### `chronicle standup`

```
╭─ Chronicle · Standup · Jun 9, 2026 ─────────────────────────────╮
│                                                                   │
│  Yesterday (Fri Jun 8)                                           │
│    auth-service    ██  3 commits                                 │
│                        refactored JWT validation                  │
│                        fixed token expiry edge case              │
│    frontend        █   1 commit                                  │
│                        updated login form error states           │
│                                                                   │
│  Today (Mon Jun 9)                                               │
│    auth-service    █   1 commit (so far)                         │
│                        started refresh token endpoint            │
│                                                                   │
╰──────────────────────────────────────────────────────────────────╯
```

### `chronicle week`

```
Week 23 · Jun 3–9 · 4 repos · 23 commits

  Mon Jun 3   auth-service   Started OAuth2 integration
  Tue Jun 4   auth-service   ████  OAuth2 complete + 4 tests
  Wed Jun 5   frontend       ██    Login/logout flow, token storage
              infra          █     Docker compose update
  Thu Jun 6   auth-service   ██    JWT refactor, expiry fix
  Fri Jun 8   auth-service   █     Refresh token (in progress)

  Top files: auth/jwt.py (8×)  components/Login.tsx (5×)
  Total: 23 commits across 4 repos  ~14h estimated
```

---

## Metriche di successo

| Metrica | Target 1 mese | Target 6 mesi |
|---------|--------------|--------------|
| GitHub stars | 500 | 5,000 |
| PyPI downloads/mese | 2,000 | 20,000 |
| Issues aperte | 20 | 100+ |
| Contributors | 5 | 30+ |
| HN front page | — | 1 volta |

---

## Cosa NON fare mai

- Non aggiungere AI (rompe il posizionamento "zero dependency, local")
- Non aggiungere cloud sync (idem)
- Non aggiungere time tracking da keystroke (già esistono Wakatime etc.)
- Non aggiungere project management (non è Jira)
- Non rendere la config obbligatoria
- Non aggiungere autenticazione per nessun motivo

---

## Nome e packaging

- **Package PyPI:** `chronicle-git` (chronicle è già preso)
- **Comando CLI:** `chronicle` (nessun conflitto su sistema pulito)
- **Repo GitHub:** `chronicle` oppure `git-chronicle`
- **Tagline:** "Your git history, told as a story."
- **Alternativa tagline:** "What did you do this week? Ask your git log."

---

## Licenza

MIT. Sempre. Nessuna discussione.
