# Who's Who — HANDOFF

Ultimo aggiornamento: 14/11/2026

## Stato

- **SPEC.md approvata** (F1-F8, criteri C1-C17), tranne la sezione 3b (fonti dati), che aspetta il prof.
- **Programma funzionante** su http://localhost:8000 con persone inventate di esempio:
  ricerca per nome (anche a pezzi) / azienda / skill / evento, scheda persona, persone collegate
  (colleghi, stesso evento, collegamenti a mano), barra di navigazione, Indietro, Precedente/Successiva.
- **27 test, tutti verdi** (`docker compose run --rm app pytest -q`).
  Verificato che i test se ne accorgono se si rompe una regola (provato su C8).
- **Non ancora su GitHub**: tutto il lavoro del 14/11 è solo in locale, nessun commit.
  `SPECIFICHE.md` è stato rimosso (il contenuto ora è in PIANO.md).

## Prossimo passo: lunedì 16/11, incontro con il prof

Fargli le domande di SPEC.md sezione 7:
1. Lo scopo (ritrovare persone per nome, poi azienda/skill/evento) è quello che intendeva?
2. LinkedIn: scraping (vietato dai termini LinkedIn) oppure il CSV dei collegamenti che LinkedIn
   fa scaricare (niente foto né skill)?
3. Ha parlato di CSV? Di cosa e con quali colonne? (nei 3 prompt incollati il CSV non c'è)
4. Il suo sito eventi: indirizzo? Mostra partecipanti/speaker? Si può esportare in CSV?

Con le risposte:
- aggiornare SPEC.md (sezione 3b + criteri per i dati veri) e farla approvare
- scrivere `app/whoswho/sorgenti/linkedin.py` e `eventi_prof.py` (oggi vuoti) che producono
  il formato di PIANO.md sez. 2; il resto del programma non si tocca
- test sulle nuove sorgenti, poi prova con dati veri

## Da decidere con l'utente

- Commit + push su GitHub del lavoro del 14/11.
- Skill personale `spec-coding` creata il 14/11 in `~/.claude/skills/spec-coding/`: l'utente poi
  ha chiarito che intendeva questo CLAUDE.md. Chiedergli se tenerla (vale per tutti i progetti) o toglierla.
