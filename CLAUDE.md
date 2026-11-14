# Who's Who — istruzioni per Claude

Progetto universitario (richiesta del prof): ricordare chi ho conosciuto, dove, dove ha lavorato,
cosa sa fare e con chi è collegato. Python + MySQL in due container Docker, pagina web Flask.

Questo progetto si sviluppa **by spec**, non a vibe coding. L'utente sta imparando il metodo:
spiegagli cosa stai facendo e perché, in italiano semplice.

## Cosa leggere, in quest'ordine, prima di fare qualsiasi cosa

1. **HANDOFF.md**: a che punto siamo e cosa c'è da fare adesso
2. **SPEC.md**: COSA deve fare il programma (funzioni F, cosa NON fa, criteri C, domande aperte)
3. **PIANO.md**: COME è costruito, e il motivo di ogni scelta
4. Il codice, solo la parte che serve al compito

SPEC.md è la fonte di verità. Se il codice o il piano la contraddicono, vince la spec.

## Come si lavora (ogni richiesta, anche piccola)

1. **Spec prima di tutto.** Una richiesta nuova diventa una funzione F e uno o più criteri C in SPEC.md
   ("se faccio X → succede Y", con dati concreti scritti nel criterio stesso: un criterio non deve
   dipendere dai dati di esempio né da altri criteri). Se la richiesta contraddice la spec, dillo e
   aggiorna prima la spec. Se qualcosa non è chiaro, fai **una domanda alla volta** sul cosa,
   mai sul come; "non lo so" va nelle domande aperte.
2. **Approvazione.** Fai leggere all'utente le modifiche alla spec (aprigli il file nel Blocco note)
   e indica cosa hai proposto tu. Senza approvazione non si scrive codice.
3. **Piano.** Aggiorna PIANO.md: ogni scelta tecnica cita la F/C che la giustifica.
4. **Test prima del codice.** Un test per criterio, con il criterio nel nome (`test_c14_...`).
   Eseguili: i nuovi devono fallire. Mostralo all'utente.
5. **Codice** finché tutti i test passano. Se un test fallisce, di' se sbagliava il codice o il test.
6. **Verifica che i test servano**: rompi apposta la regola appena fatta, controlla che il test
   se ne accorga, ripristina.
7. **Prova il programma vero** (non solo i test) e aprilo all'utente nel browser.
8. **Documenta**: SPEC.md (stato), PIANO.md, README.md (solo cose che esistono davvero), HANDOFF.md.

## Comandi

```bash
docker compose up -d --build              # avvia db + app → http://localhost:8000
docker compose restart app                # dopo modifiche al codice (waitress non ricarica da solo)
docker compose run --rm app pytest -q     # tutti i test (database separato whoswho_test)
docker compose run --rm app python -m whoswho.avvio importa /dati/file.json   # file in dati/
docker compose down                       # ferma (down -v cancella anche i dati)
```

In Git Bash su Windows i comandi con percorsi del container (`/dati/...`) vogliono `MSYS_NO_PATHCONV=1` davanti.
Se il database dei test non esiste (volume creato prima dello script): vedi PIANO.md sez. 3b.

Docker Desktop deve essere acceso; se non lo è, avvialo
(`C:\Program Files\Docker\Docker\Docker Desktop.exe`) e aspetta che `docker info` risponda.

## Regole del progetto

- **I dati entrano solo dalla "porta d'ingresso"** (`app/whoswho/importa.py`, formato in PIANO.md sez. 2).
  Una nuova fonte (LinkedIn, sito eventi, CSV) è un file in `app/whoswho/sorgenti/` che produce quel
  formato: non scrive mai direttamente nel database. Doppioni e dati incompleti si fermano lì (C12, C13).
- Skill, aziende, eventi stanno in tabelle, non in campi JSON (motivo in PIANO.md).
- "Stessa persona" segue SPEC D4/D5 (funzione `trova_persona` in `importa.py`): non cambiarla senza cambiare prima la spec.
- Quando la documentazione non basta per decidere, non indovinare in silenzio: chiedi all'utente
  (se è una decisione sul cosa) o scrivi la scelta in PIANO.md (se è tecnica).
  Lezione dell'esperimento in `esperimento-ricostruzione/`.
- La barra di navigazione sta in `templates/base.html`: ogni pagina nuova la eredita (C14).
- Testi dell'interfaccia e messaggi in italiano.
- Persone di esempio solo inventate (`dati/esempio.json`).
- Scraping e dati personali: LinkedIn vieta lo scraping nei termini d'uso e ci sono di mezzo
  dati di altre persone (GDPR). Non scrivere uno scraper LinkedIn prima che l'utente abbia
  la risposta del prof (domande aperte in SPEC.md sez. 7).

## Git

- Commit e push solo quando l'utente lo chiede.
- Nei commit **nessuna** riga di attribuzione a Claude (niente `Co-authored-by`, niente `Claude-Session`).
- `.env` non va mai su GitHub (è già in `.gitignore`); le password di esempio stanno in `.env.example`.
