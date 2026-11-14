# Prompt da inviare dopo l'incontro con il prof

Va bene per qualsiasi assistente AI che lavora sui file (Claude Code, Antigravity, Cursor, ...).
Apri l'assistente **nella cartella del progetto** (`whoswho`), sostituisci i testi tra `<< >>` con le
risposte del prof (copiale da [DOMANDE-PROF.md](DOMANDE-PROF.md)) e invia tutto il blocco qui sotto.

---

```
Lavoriamo sul progetto Who's Who in questa cartella. Il progetto si sviluppa "by spec":
prima di tutto leggi AGENTS.md (istruzioni per l'assistente), poi HANDOFF.md, SPEC.md e PIANO.md,
e segui il metodo descritto in AGENTS.md.

Ho incontrato il prof e ho le risposte alle domande aperte di SPEC.md (sezione 7):

1. Lo scopo: << risposta >>
2. LinkedIn, scraping o file scaricato: << risposta >>
3. Il CSV (di cosa, quali colonne; se ho un file di esempio dico dove l'ho messo): << risposta >>
4. Il sito degli eventi (indirizzo, partecipanti/speaker, si può scaricare?): << risposta >>
5. Il terzo container nginx: << risposta >>

Cosa voglio:
- Aggiorna SPEC.md con queste risposte: sezione 3b (fonti dei dati D1-D2), sezione 7 (togli le
  domande risolte, aggiungi quelle nuove) e i criteri per i dati veri. Se una risposta cambia
  qualcosa già deciso (per esempio il numero di container), dimmelo.
- Se qualcosa non è chiaro o va deciso da me, fammi UNA domanda alla volta, in italiano semplice,
  sul cosa e non sul come. Non decidere dettagli al posto mio senza dirmelo.
- Fammi approvare le modifiche alla spec prima di scrivere codice.
- Poi segui il giro di AGENTS.md: PIANO (con il motivo di ogni scelta), test che falliscono,
  codice, prova "rompo apposta e il test se ne accorge", documentazione (SPEC, PIANO, README,
  HANDOFF).
- Le nuove fonti di dati vanno solo in app/whoswho/sorgenti/ (linkedin.py, eventi_prof.py o
  altri file) e devono produrre il formato della "porta d'ingresso" di PIANO.md sezione 2:
  il resto del programma non va toccato.
- Niente scraping di LinkedIn se il prof non l'ha confermato esplicitamente.
- Non fare commit né push senza chiedermelo.
```
