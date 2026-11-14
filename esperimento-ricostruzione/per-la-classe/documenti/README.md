# Who's Who

Ricordarsi chi si è conosciuto: **dove** l'ho incontrato, **dove** ha lavorato, **cosa** sa fare,
e **con chi** è collegato. Python + MySQL in due container Docker.

Il progetto è sviluppato *by spec*:
- [SPEC.md](SPEC.md): **cosa** fa il programma e i criteri per dire che funziona (C1-C13)
- [PIANO.md](PIANO.md): **come** è costruito, con il motivo di ogni scelta
- `app/tests/`: un test automatico per ogni criterio della spec

## Avvio

Serve [Docker Desktop](https://www.docker.com/products/docker-desktop/) acceso.

```bash
cp .env.example .env          # Windows PowerShell: Copy-Item .env.example .env
docker compose up -d --build
```

Apri **http://localhost:8000**. Al primo avvio, se il database è vuoto, vengono caricate
alcune persone inventate (`dati/esempio.json`) per provare.

Fermare: `docker compose down` · Cancellare anche i dati: `docker compose down -v`

## Come si usa

In alto, su **ogni pagina**, c'è la barra di navigazione:

| Elemento | Cosa fa |
|---|---|
| **Who's Who** / **Home** | torna alla pagina iniziale |
| **Persone** | elenco di tutte le persone, in ordine alfabetico |
| **Eventi** | elenco di tutti gli eventi, dal più recente |
| **Casella di ricerca** | scegli *Nome*, *Azienda* o *Skill*, scrivi e premi **Cerca** (il nome va bene anche a pezzi: "Mar" trova Marco e Maria) |

Le pagine:

| Pagina | Indirizzo | Cosa trovi |
|---|---|---|
| Home | `/` | spiegazione e ultimi eventi |
| Persone | `/persone` | tutte le persone; clic su una → scheda |
| Eventi | `/eventi` | tutti gli eventi; clic su uno → chi ho incontrato lì |
| Risultati | `/cerca` | le persone trovate dalla ricerca |
| Scheda | `/persona/<id>` | eventi, aziende, skill, persone collegate, collegamenti a mano |

Per muoversi:
- **← Indietro** (sotto la barra, su tutte le pagine tranne la Home) torna alla pagina di prima.
- Nella **scheda** quasi tutto è cliccabile: un evento, un'azienda o una skill
  aprono la ricerca corrispondente; una persona collegata apre la sua scheda.
- In fondo alla scheda, **‹ Precedente** e **Successiva ›** scorrono le persone in ordine alfabetico.

## Test

```bash
docker compose run --rm app pytest -v
```

I test usano un database separato (`whoswho_test`), non toccano i dati veri.

## Importare dati

Ogni sorgente produce persone nel formato descritto in [PIANO.md](PIANO.md) (sezione 2).
Un file JSON in quel formato si importa così:

```bash
docker compose run --rm -v "$PWD/dati:/dati" app python -m whoswho.avvio importa /dati/mio-file.json
```

Le sorgenti LinkedIn e sito eventi (`app/whoswho/sorgenti/`) sono da completare:
vedi le domande aperte in [SPEC.md](SPEC.md), sezione 7.

## Cosa c'è dentro

```
SPEC.md, PIANO.md     cosa e come
docker-compose.yml    container db (MySQL 8.4) + app (Python 3.12, Flask)
db/                   script che crea il database dei test
dati/esempio.json     persone inventate di prova
app/whoswho/          codice: importa.py (porta d'ingresso), ricerche.py, web.py
app/whoswho/templates/  pagine HTML: base.html (barra su tutte le pagine), home, persone, eventi, risultati, persona
app/tests/            test dei criteri della spec
```
