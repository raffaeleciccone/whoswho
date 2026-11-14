# Prompt da dare all'assistente AI "nuovo"

Va bene per **qualsiasi assistente che lavora sui file e può usare il terminale**: Claude Code,
Antigravity, Cursor, Codex, Gemini CLI... Come aprirlo con ogni strumento: [STRUMENTI.md](STRUMENTI.md).

Usalo in una conversazione **nuova**, con l'assistente aperto nella cartella preparata con
`prepara-cartella.ps1`. Sostituisci `<CARTELLA>` con il percorso della cartella.

---

```
Nella cartella <CARTELLA> ci sono SOLO i documenti di un progetto: SPEC.md, PIANO.md, AGENTS.md,
CLAUDE.md, README.md, HANDOFF.md e la bozza grafica approvata design/bozza.html (nella versione
"prova 1" mancano AGENTS.md e la bozza). Il codice non c'è. Il tuo compito: ricostruire il progetto
completo e funzionante in quella cartella, basandoti esclusivamente su questi documenti.
Le istruzioni per l'assistente AI sono in AGENTS.md (CLAUDE.md rimanda allo stesso contenuto):
valgono anche se non sei Claude.

Regole dell'esperimento:
- Lavora SOLO dentro <CARTELLA>. Non leggere altre cartelle del computer e non cercare il progetto
  su internet: lo scopo è verificare se la documentazione da sola basta.
- Nessuno risponderà alle tue domande: non farne (anche se AGENTS.md dice di chiedere all'utente,
  in questo esperimento l'utente non c'è). Quando la documentazione è ambigua, incompleta o
  contraddittoria, decidi tu nel modo più ragionevole e annota la cosa in <CARTELLA>/DUBBI.md
  (una voce per punto: cosa mancava o era ambiguo, cosa hai deciso, quale documento e sezione).
  Questo file è il risultato più importante dell'esperimento: sii onesto e completo, anche sulle
  piccole cose che hai dovuto inventare.
- Non modificare i file .md esistenti né design/bozza.html.
- Crea anche i dati di esempio previsti dai documenti, con persone inventate.
- Scrivi i test come richiesto dai documenti ed eseguili dentro Docker finché passano; esegui anche
  le misure e i controlli previsti dai documenti. Poi avvia il programma e verifica che risponda.
- Lascia i container accesi alla fine. Non fare commit git.

Alla fine rispondi con: elenco dei file creati, risultato dei test (quanti passano), risultato delle
misure, se il sito risponde, e un riassunto delle voci di DUBBI.md.
```

---

**Se sul PC gira già un'altra copia del progetto**, aggiungi in fondo al prompt:
"le porte 8000 e 3307 sono occupate: il sito deve rispondere su 8001 e MySQL sulla porta 3308".
