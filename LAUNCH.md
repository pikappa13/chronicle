# Strategia di lancio — Chronicle

## Obiettivo

500 stelle nel primo mese. 5.000 stelle nei primi 6 mesi.

Non è un numero casuale: 500 stelle nei primi 30 giorni è la soglia che porta un progetto nella sezione "trending" di GitHub e genera effetto snowball organico.

---

## Prima di lanciare — checklist

### Il prodotto deve essere pronto

- [ ] `pip install chronicle-git` funziona in meno di 30 secondi
- [ ] `chronicle week` funziona nella directory corrente senza errori
- [ ] `chronicle standup` produce output bello nel terminale
- [ ] README ha una GIF animata che mostra l'output (OBBLIGATORIA)
- [ ] GitHub repo ha: description, topics, website
- [ ] PyPI package pubblicato con description e keywords corrette
- [ ] CI verde (GitHub Actions)
- [ ] LICENSE MIT presente

### La GIF è il 50% del successo

Registra un terminale pulito (sfondo scuro, font Fira Code o JetBrains Mono) che mostra:
1. `pip install chronicle-git` (veloce)
2. `cd` in un repo reale con storia significativa
3. `chronicle week` → output bello compare
4. `chronicle standup` → output standup compare

Usa `vhs` (https://github.com/charmbracelet/vhs) per generare GIF perfette da codice. Investi 2 ore su questo — è il tuo trailer.

**Dimensione GIF:** max 3MB. Ottimizza con `gifsicle`.

---

## Sequenza di lancio — giorno per giorno

### Giorno 0 — preparazione silenziosa

- Pubblica su GitHub ma NON annunciare
- Metti repo in public
- Aggiungi i topic GitHub: `git`, `cli`, `developer-tools`, `productivity`, `python`, `terminal`, `standup`, `git-history`
- Scrivi la descrizione del repo: "Answer 'what did you do this week?' from your git history. Zero config, no AI, no cloud."
- Pubblica su PyPI

### Giorno 1 — Hacker News (il più importante)

**Titolo del post Ask HN / Show HN:**
```
Show HN: Chronicle – answer "what did I do this week?" from your git history
```

**Testo del post:**
```
I got tired of reconstructing my work week from memory every Monday morning. 
Git already knows everything I did — I just couldn't read it easily.

Chronicle is a zero-config CLI that reads your git history and presents it 
in human-readable form. No AI, no cloud, no account, no config. Works on 
any existing repo.

    pip install chronicle-git
    chronicle week

It also does standup format (yesterday + today), multi-repo scanning, 
and exports to markdown/slack/json.

GitHub: https://github.com/TUO_USERNAME/chronicle

Would love feedback on the output format and any edge cases you've hit 
with your own repos.
```

**Timing:** Lunedì o martedì, ore 9-10 EST (15-16 ora italiana). Questo è il momento di picco di HN.

**Regola d'oro HN:** Rispondi a OGNI commento entro le prime 2 ore. La velocità di risposta influenza il ranking.

### Giorno 2 — Reddit

Post su questi subreddit in ordine:

**r/programming** (più grande, più difficile):
```
Title: I built a CLI that answers "what did you do this week?" from your git history
```

**r/commandline** (nicchia perfetta, alta conversione):
```
Title: chronicle – zero-config CLI to read your own git history as a human story
```

**r/Python** (per la community PyPI):
```
Title: Show r/Python: chronicle – pip install and ask your git log what you did this week
```

**r/webdev** e **r/devops** — post secondari con link al thread principale.

**Regola Reddit:** Non crosspostare lo stesso testo. Scrivi intro diverse per ogni sub. Non sembrare spam.

### Giorno 3 — Dev.to e Hashnode

Scrivi un articolo lungo (1500-2000 parole) intitolato:

```
I stopped reconstructing my work week from memory. Here's the CLI I built.
```

Struttura dell'articolo:
1. Il problema (standup, sprint review, performance review)
2. Perché git log non basta
3. Come funziona chronicle (con GIF e esempi)
4. Come è stato costruito (Python, gitpython, rich) — 5 paragrafi tecnici
5. Cosa viene dopo

Pubblica su Dev.to con tag: `#python #git #cli #productivity #opensource`
Pubblica su Hashnode con tag simili.

Questi articoli si indicizzano su Google e portano traffico organico per mesi.

### Giorno 7 — Twitter/X

Thread in inglese (non in italiano):

```
Tweet 1:
I got tired of reconstructing my work week every Monday morning.
So I built a CLI that reads your git history and answers "what did I do?"

pip install chronicle-git
chronicle week

[GIF dell'output]

Tweet 2:
It does standup format too.

Running `chronicle standup` shows yesterday + today in a clean layout.

No AI. No cloud. No account. Your git log is the database.

[screenshot standup]

Tweet 3:
Works across multiple repos too.

chronicle week --all

Scans all your repos, groups by day, shows which project you touched when.

[screenshot multi-repo]

Tweet 4:
Why build this vs using git log directly?

git log gives you raw commits. Chronicle gives you a story.
Same data, completely different readability.

Zero config. Works on any existing repo.

GitHub: [link]
PyPI: [link]

MIT licensed. PRs welcome.
```

Tagga: @github, @pypi, @realpython — non per mendicanza, ma perché il contenuto è genuinamente rilevante.

### Settimana 2 — community outreach

- Posta su **lobste.rs** (community tecnica di qualità, molto selettiva — ottimo per credibilità)
- Manda una email a **Python Weekly newsletter** (pythonweekly.com/submit) — gratuito, 60k iscritti
- Manda a **Cooperpress** (javascript non è rilevante, ma hanno DevOps Weekly)
- Cerca thread su HN tipo "What's in your .bashrc?" e "What CLI tools do you use daily?" e lascia un commento con link quando pertinente

### Settimana 3-4 — il moltiplicatore

Se hai 200+ stelle, scrivi un secondo articolo:

```
I released a CLI tool 2 weeks ago. Here's what I learned from the first 
200 GitHub stars and 50 issues.
```

Questo tipo di articolo "post-mortem / learnings" ha engagement altissimo e porta nuove stelle dai developer che seguono il progetto nel tempo.

---

## Topics GitHub — da impostare subito

Vai in Settings del repo e aggiungi tutti questi:
```
git cli developer-tools productivity python terminal
standup git-history open-source zero-config
```

I topic influenzano la ricerca interna di GitHub e la sezione "Explore".

---

## GitHub repo — ottimizzazione

**Description (161 char max):**
```
Answer "what did I do this week?" from your git history. Zero config, no AI, no cloud. Works on any repo.
```

**Website:** link alla documentazione o alla PyPI page

**Social preview image:** Crea un'immagine 1280x640px con:
- Sfondo scuro
- Nome "chronicle" in font grande
- Tagline "Your git history, told as a story."
- Screenshot dell'output terminale
- Questo appare quando condividi il link su Twitter/Slack

---

## Metriche da monitorare

| Settimana | Target stelle | Azione se sotto target |
|-----------|--------------|----------------------|
| 1 | 100 | Rilancia su Reddit con angolo diverso |
| 2 | 250 | Scrivi articolo tecnico più lungo |
| 4 | 500 | Post "2 weeks later" su HN |
| 8 | 1,500 | Aggiungi `chronicle report` (HTML visivo) e rilancia |
| 16 | 3,000 | Homebrew tap, package manager |
| 6 mesi | 5,000 | — |

---

## Il moltiplicatore nascosto: `chronicle report`

Quando aggiungi questo comando (v0.4), rilanciare diventa facile perché:
- Genera un HTML bellissimo con heatmap dei commit
- È visivamente condivisibile (screenshot)
- Il "before/after" (prima: brutto git log, dopo: bel report) è il miglior marketing

Implementa questo come seconda ondata, 3-4 settimane dopo il lancio iniziale, e rilancia con:
```
Show HN: Chronicle update – now generates a visual HTML report of your git activity
```

---

## Cosa NON fare

- Non pagare per promozione — le stelle comprate non portano contributors reali
- Non crosspostare lo stesso identico testo ovunque — vieni bannato e perdi credibilità
- Non rispondere male alle critiche su HN — ogni critica è un'opportunità di miglioramento visibile
- Non aggiungere feature non richieste nelle prime settimane — stabilità > features
- Non ignorare le issue — rispondere in 24h nelle prime settimane è fondamentale per la reputazione

---

## Template risposta issue (per uniformità)

```
Thanks for the report! 

[diagnosi del problema]

This should be fixed in the next release. If you want to track it: [link alla issue]

Happy to review a PR if you want to tackle it!
```

Breve, cordiale, con call to action per contribuire.

---

## Il giorno del lancio HN — playbook orario

| Ora | Azione |
|-----|--------|
| 09:00 EST | Pubblica il post Show HN |
| 09:00–09:30 | Condividi il link a 5 amici dev e chiedi upvote onesto |
| 09:30–11:00 | Rispondi a OGNI commento, anche i critici |
| 11:00 | Se sei in top 10 "new", sei in gioco per la front page |
| 14:00 | Post su Reddit r/programming |
| 17:00 | Post su r/commandline |
| 20:00 | Thread su Twitter/X |

---

## Budget: 0 euro

Tutto questo si fa a costo zero. L'unico investimento è tempo:
- 2 ore per la GIF perfetta
- 1 ora per scrivere il post HN
- 2 ore per gli articoli Dev.to/Hashnode
- 30 minuti/giorno per rispondere ai commenti la prima settimana
