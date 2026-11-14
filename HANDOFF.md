# Who's Who — HANDOFF

Ultimo aggiornamento: 14/11/2026

## Stato

- **SPEC.md approvata** (F1-F9, criteri C1-C38, regole import D4-D7), tranne le fonti dati D1-D2, che aspettano il prof.
- **Programma funzionante** su http://localhost:8000 con persone inventate di esempio:
  ricerca per nome (anche a pezzi) / azienda / skill / evento, scheda persona, persone collegate
  (colleghi, stesso evento, collegamenti a mano), barra di navigazione, Indietro, Precedente/Successiva.
- **52 test, tutti verdi** (`docker compose run --rm app pytest -q`).
  Verificato che i test se ne accorgono se si rompe una regola (provato su C8, C22, C25, C26, C27, C28).
- **Esperimento di ricostruzione fatto** (`esperimento-ricostruzione/`): un Claude nuovo ha rifatto
  il progetto dai soli .md; i suoi 36 dubbi hanno portato a: regola "stessa persona" (D4-D5, C18-C20),
  niente collegamenti doppi (C22), formato del file di import e dettagli tecnici in PIANO.md sez. 2 e 3b.
- **Non ancora su GitHub**: tutto il lavoro del 14/11 è solo in locale, nessun commit.
  `SPECIFICHE.md` è stato rimosso (il contenuto ora è in PIANO.md).

## Grafica (14/11, fatta in SDD)
- SPEC sez. 3c (F9, C29-C38): tutte le decisioni prese dall'utente una alla volta (disposizione, testata,
  foto, misure, larghezza, skill, tonalità, tasti, icone, nome "Relazioni"); tecniche in sez. 6
  (HTML+CSS nostro, TRE container con nginx davanti, strumenti confermati).
- Bozza approvata: `design/bozza.html`. Programma aggiornato: 52 test verdi, C34 misurato e rispettato
  (scheda tipica finisce a 579 px su 650; telefono senza scorrimento laterale).
- Prova 3 fatta (`esperimento-ricostruzione/prova-3/`): ricostruzione riuscita, stessa misura C34 (579 px),
  aspetto uguale alla bozza; errori trovati e corretti (C32 rimasto vecchio, C30 deciso: secondari ≥ 13,5 px).
- Tutto su GitHub (14/11, commit 3f75104 e successivi), pushato con l'account raffaeleciccone.
- GitHub: il repo va SOLO sull'account raffaeleciccone. Su questo PC gh ha due account; per il push:
  `gh auth switch -u raffaeleciccone` (poi si può tornare a raffaeleciccone-analyst).

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

- Skill personale `spec-coding` (bozza del 14/11 in `~/.claude/skills/spec-coding/`): l'utente vuole
  rifarla bene in una conversazione dedicata, per lavorare sempre così su tutti i progetti.
- Prova 2 dell'esperimento fatta (`esperimento-ricostruzione/prova-2/`): prova decisiva passata.
  I 5 punti emersi sono stati decisi con l'utente e corretti (C17 riscritto, C25-C28); vedi prova-2/RISULTATI.md.
- Versioni ricostruite in `C:\dev\whoswho-ricostruito` (prova 2) e `...-prova1` (fuori dal repo; container prova 2 su 8001/3308
  ancora accesi): spegnere con `docker compose down` in quella cartella quando non serve più.
