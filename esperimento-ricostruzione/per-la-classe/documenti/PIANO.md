# Who's Who — PIANO (come)

> Il COSA sta in [SPEC.md](SPEC.md). Qui c'è il COME.
> Ogni scelta tecnica cita la frase della spec che la giustifica.
> Se una scelta qui contraddice la spec, vince la spec: si corregge il piano.

## 1. Architettura

```
 [ sorgenti dati ]  ──►  [ porta d'ingresso ]  ──►  [ MySQL ]  ◄──  [ pagina web ]
  sorgenti/*.py           importa.py                 container db      web.py
  (LinkedIn, eventi:      (controlla, pulisce,                         (ricerche, scheda,
   da fare lunedì)         evita doppioni)                              collegamenti)
```

Due container Docker (vincolo del prof):
- `db`: MySQL 8.4, dati in un volume Docker, healthcheck.
- `app`: Python 3.12 + Flask, parte solo quando `db` è pronto. Pagina web su http://localhost:8000

## 2. La "porta d'ingresso" (formato unico dei dati)

Qualsiasi sorgente (file di esempio, LinkedIn, sito eventi, CSV) deve produrre
una lista di persone in questo formato. Il resto del programma conosce solo questo.

```json
{
  "nome": "Mario",
  "cognome": "Rossi",
  "foto": "https://... (facoltativo)",
  "professione": "Data Engineer (facoltativo)",
  "profilo_url": "https://www.linkedin.com/in/... (facoltativo)",
  "esperienze": [
    {"azienda": "Accenture", "ruolo": "Consultant", "inizio": "2019-01-01", "fine": "2022-06-30"}
  ],
  "skill": ["Python", "Docker"],
  "eventi": [
    {"nome": "Data Summit 2026", "data": "2026-05-10", "luogo": "Milano", "note": "parlato di dbt"}
  ]
}
```

Lunedì, dopo le risposte del prof, si scrive solo un file in `app/whoswho/sorgenti/`
che trasforma LinkedIn / sito eventi / CSV in questo formato.

## 3. Database

| Tabella | Contenuto | Perché (spec) |
|---|---|---|
| `persone` | nome, cognome, foto, professione, profilo_url, `chiave` unica | F1, F2 |
| `aziende` | nome unico | F3 |
| `esperienze` | persona, azienda, ruolo, inizio, fine (NULL = ancora lì) | F2, F3, F6 colleghi |
| `skill` | nome unico | F4 |
| `persona_skill` | persona ↔ skill | F4 |
| `eventi` | nome, data, luogo (unico per nome+data) | F5 |
| `persona_evento` | persona ↔ evento + note | F5, F6 conosciuti |
| `collegamenti` | persona A, persona B, descrizione | F7 |

### Scelte e motivi
- **Skill in una tabella, non in un campo JSON.** Motivo: F4 (cercare per skill) e C5
  ("docker" = "Docker"). Con il JSON la ricerca sarebbe lenta e fragile.
- **Ricerche senza distinzione maiuscole/minuscole/accenti**: collation MySQL
  `utf8mb4_0900_ai_ci`. Motivo: C1, C4, C5. In più gli spazi in testa/coda si tolgono (C5).
- **Colleghi e "conosciuti allo stesso evento" non si salvano: si calcolano** con una query
  ogni volta che apro la scheda. Motivo: F6 dice "calcolato dal programma"; così sono
  sempre aggiornati dopo ogni import.
  - Colleghi: stessa azienda e `inizio_A <= fine_B` e `inizio_B <= fine_A`,
    con fine vuota = oggi (C7, C8, C9). Esperienza senza data di inizio: non conta.
- **Doppioni (C12)**: una persona è "la stessa" se ha lo stesso `profilo_url`;
  se manca, se ha stesso nome+cognome. Aziende e skill: stesso nome. Eventi: stesso nome+data.
- **Collegamenti a mano (F7)**: una riga sola per collegamento; la scheda li cerca
  sia come persona A sia come persona B, così compaiono in entrambe le schede (C11).
- **Dati incompleti (C13)**: la porta d'ingresso scarta la persona senza nome o cognome
  e la elenca nel resoconto dell'import; le altre vengono importate.

## 4. Struttura del codice

```
whoswho/
├── SPEC.md, PIANO.md, README.md
├── docker-compose.yml        # i due container
├── .env.example              # password e porte (copiare in .env)
├── db/crea-db-test.sh        # crea il database separato per i test
├── dati/esempio.json         # persone finte per provare
└── app/
    ├── Dockerfile, requirements.txt
    ├── whoswho/
    │   ├── schema.sql        # tabelle
    │   ├── db.py             # connessione e creazione tabelle
    │   ├── importa.py        # porta d'ingresso (C12, C13)
    │   ├── ricerche.py       # F1-F7
    │   ├── web.py            # pagine web
    │   ├── avvio.py          # comandi: avvia, importa
    │   ├── templates/        # HTML
    │   └── sorgenti/         # lettori dei dati (esempio.py ora; LinkedIn/eventi lunedì)
    └── tests/                # un test per ogni criterio C1-C13
```

## 4b. Navigazione (F8)
- La barra in alto sta in `templates/base.html`, quindi compare su tutte le pagine
  senza ripeterla (C14). Contiene Home, Persone, Eventi e la casella di ricerca.
- Due pagine nuove: `/persone` (tutte, in ordine alfabetico) e `/eventi` (tutti, dal più recente) (C16).
- "← Indietro" usa la cronologia del browser; se si è arrivati da un link diretto
  (nessuna pagina prima), porta alla Home. La Home non lo mostra (C15).
- "‹ Precedente / Successiva ›" nella scheda: la persona prima/dopo nello stesso ordine
  della pagina Persone (cognome, nome, id), calcolata con una query (C17).

## 5. Test

I test girano dentro Docker contro un MySQL vero, su un database separato
(`whoswho_test`), così non toccano i dati reali:

```
docker compose run --rm app pytest
```

Ogni test ha nel nome il criterio che controlla (es. `test_c8_...`).
`test_criteri.py` copre C1-C13, `test_navigazione.py` copre C14-C17.

## 6. Da fare lunedì (dopo il prof)
- [ ] Risposte alle domande aperte della SPEC (sezione 7) → aggiornare SPEC sezione 3b
- [ ] Scrivere `sorgenti/linkedin.py` (scraping o CSV, secondo il prof)
- [ ] Scrivere `sorgenti/eventi_prof.py` (sito eventi)
- [ ] Test sui dati veri
