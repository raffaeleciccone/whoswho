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

**Il file** (es. `dati/esempio.json`, UTF-8) può essere in una di queste due forme, e la porta
d'ingresso le accetta entrambe:
- una lista di persone: `[ {persona}, {persona}, ... ]`
- un oggetto con la chiave `"persone"`: `{"nota": "...", "persone": [ ... ]}`; le altre chiavi si ignorano.

**Una persona:**

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

Regole dei campi:
- `nome` e `cognome` obbligatori; tutto il resto facoltativo. Campi sconosciuti: ignorati.
- Spazi in testa/coda e spazi doppi si tolgono da tutti i testi.
- Date: `AAAA-MM-GG`, oppure `AAAA-MM`, oppure `AAAA`. Se mancano giorno o mese (SPEC C25):
  per l'**inizio** di un'esperienza e per la data di un evento si usa il **primo** giorno
  (`2019` → 1/1/2019, `2022-03` → 1/3/2022); per la **fine** di un'esperienza l'**ultimo**
  (`2022` → 31/12/2022, `2022-06` → 30/6/2022).
  Una data non valida diventa vuota e finisce negli avvisi; la persona entra lo stesso.
- Esperienza senza `azienda` o evento senza `nome`: ignorati con un avviso.
- Collegamenti a mano: non fanno parte dell'import (si scrivono solo dalla pagina, F7).

Il comando `python -m whoswho.avvio importa <file>` stampa un **resoconto**: quante persone
importate, quali scartate e perché, gli avvisi (SPEC D7).

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
- **Stessa persona (C12, D4, D5, C18-C20)**, in quest'ordine:
  1. se il dato nuovo ha `profilo_url`: cerco una persona con lo stesso profilo
     (profilo **normalizzato**, SPEC C26: minuscolo; senza `http://`/`https://`; senza la parte dopo
     `?` o `#`; dal nome del sito si toglie `www.` e un prefisso di 2 lettere come `it.` se dopo resta
     ancora un punto; senza `/` finale → `linkedin.com/in/mario-rossi`) → trovata = è lei;
  2. altrimenti cerco per nome+cognome (maiuscole/accenti non contano):
     - con profilo nel dato nuovo: è la persona omonima **senza** profilo, se c'è (e le aggiungo il profilo);
       se tutti gli omonimi hanno un profilo diverso, è una persona nuova (omonimo vero);
     - senza profilo nel dato nuovo: nessun omonimo → nuova; uno solo → è lui;
       più omonimi → è quello senza profilo se c'è, altrimenti **ambiguo**: scartata e segnalata (C20).
  La colonna `chiave` (unica) contiene il profilo normalizzato, oppure "nome cognome" in minuscolo.
- **Reimport (D6, C23)**: i campi presenti aggiornano quelli vecchi, quelli vuoti non cancellano;
  esperienze, skill ed eventi si aggiungono, mai si tolgono.
- **Aziende e skill: stesso nome = stessa** (maiuscole non contano). Eventi: stesso nome + stessa data
  (anche "nessuna data"). Esperienze: stessa persona + azienda + ruolo + data di inizio.
- **Collegamenti a mano (F7)**: una riga sola per collegamento; la scheda li cerca
  sia come persona A sia come persona B, così compaiono in entrambe le schede (C11).
  Prima di salvarlo controllo che non esista già la stessa coppia (in qualsiasi ordine) con la stessa
  descrizione (maiuscole non contano) → altrimenti "Collegamento già presente." (C22).
- **Ricerca azienda "contiene", ricerca skill "uguale"** (F3, F4, C21): `LIKE %testo%` per le aziende,
  `=` per le skill, così "Java" non trova "JavaScript".
- **Ordine alfabetico** (C16, C24): `ORDER BY cognome, nome, id` con la stessa collation, quindi
  maiuscole e accenti non contano.
- **Dati incompleti (C13)**: la porta d'ingresso scarta la persona senza nome o cognome
  e la elenca nel resoconto dell'import; le altre vengono importate.

- **Ricerca per nome con più parole** (F1, C27): il testo si divide in parole; per ogni parola
  `(nome LIKE %parola% OR cognome LIKE %parola%)`, tutte in AND.

- **Ricerca vuota** (C28): `/cerca` con testo vuoto mostra la pagina risultati con il messaggio
  "Scrivi qualcosa da cercare." invece dei risultati.

## 3b. Dettagli tecnici (scritti dopo l'esperimento di ricostruzione)
- **Librerie** (versioni esatte in `app/requirements.txt`): Flask, PyMySQL + `cryptography`
  (serve per l'autenticazione di MySQL 8), waitress (server web), pytest.
- **Variabili d'ambiente** (`.env`, modello in `.env.example`): `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`
  (`whoswho_db`), `MYSQL_USER` (`whoswho_user`), `MYSQL_PASSWORD`, `MYSQL_TEST_DATABASE` (`whoswho_test`),
  `HOST_MYSQL_PORT` (3307: MySQL raggiungibile dal PC, per DBeaver/Workbench), `HOST_APP_PORT` (8000),
  `CARICA_ESEMPIO` (1 = al primo avvio, se il database è vuoto, carica `dati/esempio.json`).
- **Cartelle montate** nel container `app`: `./app` → `/app` (il codice) e `./dati` → `/dati` (sola lettura).
- **Database dei test**: lo crea `db/crea-db-test.sh`, che MySQL esegue **solo la prima volta**
  (volume vuoto). Se il volume esisteva già: `docker compose down -v` e poi `up` (cancella i dati),
  oppure lanciare a mano i comandi SQL dello script.
- **Salvataggi**: ogni operazione che scrive fa subito `commit`; ogni richiesta web apre la sua
  connessione e la chiude alla fine. Così una pagina vede sempre i dati appena scritti.
- **Indirizzi delle pagine**: `/`, `/persone`, `/eventi`, `/cerca?tipo=nome|azienda|skill&q=...`,
  `/cerca?tipo=evento&evento=<id>`, `/persona/<id>`, `POST /persona/<id>/collegamenti`,
  `POST /persona/<id>/collegamenti/<id collegamento>/elimina`.
- **Git Bash su Windows**: i comandi con percorsi dentro il container (es. `/dati/file.json`)
  vogliono `MSYS_NO_PATHCONV=1` davanti, altrimenti Git Bash trasforma il percorso.

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
    └── tests/                # un test per ogni criterio della spec
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
`test_criteri.py` copre C1-C13, `test_navigazione.py` C14-C17, `test_esperimento.py` C18-C28.

Se un test legge con la sua connessione dati scritti da un'altra (es. dalla pagina web), quella
connessione deve vedere i dati appena salvati: MySQL di default (REPEATABLE READ) potrebbe mostrarle
una "fotografia" vecchia. Soluzione: livello di isolamento READ COMMITTED per le connessioni dei test,
oppure leggere tramite la pagina web. (Trovato nella prova 2 dell'esperimento.)

## 6. Da fare lunedì (dopo il prof)
- [ ] Risposte alle domande aperte della SPEC (sezione 7) → aggiornare SPEC sezione 3b
- [ ] Scrivere `sorgenti/linkedin.py` (scraping o CSV, secondo il prof)
- [ ] Scrivere `sorgenti/eventi_prof.py` (sito eventi)
- [ ] Test sui dati veri
