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

Tre container Docker (SPEC sez. 6: programma e database separati come chiesto dal prof, più nginx
scelto dall'utente):
- `web`: nginx 1.27 (`nginx:1.27-alpine`). È l'unico raggiungibile dal PC: http://localhost:8000.
  Risponde da solo per i file grafici (`/static/...`) e passa tutto il resto ad `app`.
- `app`: Python 3.12 + Flask servito da waitress sulla porta 8000 **interna** (non esposta al PC).
- `db`: MySQL 8.4, dati in un volume Docker, healthcheck. `app` parte solo quando `db` è pronto.

```
 browser ──► web (nginx, porta 8000 del PC)
              ├── /static/stile.css ──► file letto da app/whoswho/static/ (montato in sola lettura)
              └── tutto il resto ─────► app:8000 (Flask) ──► db:3306 (MySQL)
```

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
  **Eccezione, la fine di un'esperienza** (SPEC C39): se è scritta ma non valida, l'esperienza intera viene
  ignorata (con avviso), perché "fine vuota" vorrebbe dire "ci lavora ancora" e creerebbe colleghi falsi.
- Esperienza senza `azienda` o evento senza `nome`: ignorati con un avviso.
- Relazioni (nel codice "collegamenti"): non fanno parte dell'import (si scrivono solo dalla pagina, F7).

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
- **Relazioni (F7; tabella `collegamenti`)**: una riga sola per relazione; la scheda li cerca
  sia come persona A sia come persona B, così compaiono in entrambe le schede (C11).
  Prima di salvarlo controllo che non esista già la stessa coppia (in qualsiasi ordine) con la stessa
  descrizione (maiuscole non contano) → altrimenti "Relazione già presente." (C22).
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
├── SPEC.md, PIANO.md, README.md, HANDOFF.md
├── AGENTS.md, CLAUDE.md      # istruzioni per l'assistente AI (CLAUDE.md rimanda ad AGENTS.md)
├── incontro-prof/            # domande per il prof + prompt per continuare
├── kit-ricostruzione/        # kit per la classe (copie dei documenti, aggiornate da strumenti/aggiorna_kit.py)
├── docker-compose.yml        # i tre container: web (nginx), app, db
├── nginx/default.conf        # nginx: /static/ dai file, il resto ad app:8000
├── design/bozza.html         # bozza grafica approvata (C35)
├── strumenti/misura_c34.py   # misura C34 con Chrome
├── strumenti/aggiorna_kit.py # allinea kit-ricostruzione/ ai documenti (--controlla per verificare)
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
    │   ├── avvio.py          # comandi: avvia, importa, scheda-tipica
    │   ├── static/stile.css  # l'unico foglio di stile (PIANO sez. 4c)
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

## 4c. Grafica (F9, C29-C38)

Riferimento: **`design/bozza.html`**, la bozza approvata dall'utente (C35). Le pagine vere devono somigliarle.

- **Un solo foglio di stile**: `app/whoswho/static/stile.css`, collegato da `templates/base.html` come
  `/static/stile.css`. Lo serve nginx (in Flask funziona lo stesso, utile per i test).
  Niente librerie grafiche (SPEC sez. 6).
- **Colori come variabili** in `:root` (valori e coppie testo/sfondo controllate da `test_grafica.py`, C29):

  | Variabile | Valore | Uso |
  |---|---|---|
  | `--blu-notte` | `#1e3250` | barra, titoli delle fasce, iniziali |
  | `--blu-notte-2` | `#2b4468` | voce attiva della barra |
  | `--blu-link` | `#2a4d7f` | link, tasti secondari |
  | `--fascia` | `#e3e9f1` | fascia dei titoli dei riquadri |
  | `--etichetta` | `#d6e2f1` | sfondo delle skill |
  | `--bordo` | `#c3cdda` | bordi |
  | `--sfondo` | `#eef1f5` | sfondo pagina |
  | `--carta` | `#ffffff` | riquadri |
  | `--testo` | `#1c2430` | testo |
  | `--tenue` | `#556070` | testo secondario |
  | `--avatar` | `#d5deea` | fondo delle iniziali |
  | `--rosso` | `#b42318` | tasto Elimina |
  | `--tasto-alto` / `--tasto-basso` | `#2f4a73` / `#1a2c47` | sfumatura dei tasti principali |

- **Coppie testo/sfondo controllate da C29** (tutte devono avere contrasto ≥ 4,5:1): bianco su `--blu-notte`,
  bianco su `--blu-notte-2`, bianco su `--tasto-alto` e su `--tasto-basso`; `--testo` su `--carta` e su `--sfondo`;
  `--tenue` su `--carta`, su `--sfondo` e su `--fascia`; `--blu-link` su `--carta` e su `--sfondo`;
  `--blu-notte` su `--fascia`, su `--etichetta`, su `--avatar` e su `--carta`; `--rosso` su `--carta`.
- **Misure** (C30, decisione 5): `html { font-size: 18px }`, `h1 { font-size: 28px }`; ogni `font-size` scritto in
  `px` o `rem` (mai `em` o `%`) e mai sotto 13,5 px (= 0.75rem); foto della testata
  140 px, miniature 90 px, angoli delle foto 12 px, pagina larga al massimo 1200 px.
- **Tema sempre chiaro** (C31): nessuna regola `prefers-color-scheme` e `<meta name="color-scheme" content="light">`.
- **Icone** (C37): disegnate in SVG una volta sola in `base.html` (`<symbol id="i-...">`) e usate con
  `<svg class="icona"><use href="#i-..."/></svg>`: casa, persone, calendario, lente, più, x, sinistra,
  destra, indietro.
- **Scheda persona** (C32-C34), dall'alto: riga con Indietro | Precedente, Successiva; testata
  (`section.testata`: foto o iniziali, nome in `h1`, professione, "Lavora ora in" = azienda di
  un'esperienza senza data di fine, link "Profilo online"; a destra `div.striscia` con Colleghi e
  Conosciuti allo stesso evento come miniature con nome e dettaglio); poi `div.quattro` con 4
  `section.riquadro` (Dove l'ho incontrato, Dove ha lavorato, Cosa sa fare, Relazioni), ognuna con il
  titolo in un `h2` (la fascia). Sezione vuota: "nessuno".
- **Relazioni** (F7, C36): nel codice e nel database restano `collegamenti` (nome tecnico); nell'interfaccia
  si chiamano "Relazioni". Il modulo per aggiungerle sta in un `<details>` aperto da "+ Aggiungi relazione"
  (niente JavaScript). Elimina è un modulo con `onsubmit="return confirm('Eliminare la relazione con <nome>?')"`.
  Messaggi: "Relazione aggiunta.", "Relazione eliminata.", "Relazione già presente.".
- **Ricerca nella barra**: casella e tasto lente in un unico blocco (`div.blocco-cerca`); il tasto ha
  `aria-label="Cerca"`.
- **Misura C34** (non è un test pytest, serve un browser): `python strumenti/misura_c34.py` con l'app accesa.
  La porta del sito la legge da `HOST_APP_PORT` nel file `.env` (8000 se manca).
  Usa Chrome senza finestra: a 1366 px di larghezza controlla che il fondo di `div.quattro` della scheda
  della persona tipica sia entro 650 px; in una cornice larga 390 px controlla che la pagina non sia più
  larga dello schermo. L'HTML della persona tipica lo produce `python -m whoswho.avvio scheda-tipica`
  dentro il container `app`, usando il database **dei test** (i dati veri non si toccano); la pagina usa
  il foglio di stile vero servito da nginx (`<base href="http://localhost:<HOST_APP_PORT>/">`, 8000 di default).

## 5. Test

I test girano dentro Docker contro un MySQL vero, su un database separato
(`whoswho_test`), così non toccano i dati reali:

```
docker compose run --rm app pytest
```

Ogni test ha nel nome il criterio che controlla (es. `test_c8_...`).
`test_criteri.py` copre C1-C13, `test_navigazione.py` C14-C17, `test_esperimento.py` C18-C28,
`test_grafica.py` C29-C33, C36, C37. C34 si misura con `strumenti/misura_c34.py`; C35 e C38 a vista.

Se un test legge con la sua connessione dati scritti da un'altra (es. dalla pagina web), quella
connessione deve vedere i dati appena salvati: MySQL di default (REPEATABLE READ) potrebbe mostrarle
una "fotografia" vecchia. Soluzione: livello di isolamento READ COMMITTED per le connessioni dei test,
oppure leggere tramite la pagina web. (Trovato nella prova 2 dell'esperimento.)

## 6. Da fare lunedì (dopo il prof)
- [ ] Risposte alle domande aperte della SPEC (sezione 7) → aggiornare SPEC sezione 3b
- [ ] Scrivere `sorgenti/linkedin.py` (scraping o CSV, secondo il prof)
- [ ] Scrivere `sorgenti/eventi_prof.py` (sito eventi)
- [ ] Test sui dati veri
