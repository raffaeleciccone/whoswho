# Prompt da dare al Claude "nuovo"

Usalo in una sessione **nuova** di Claude Code (nessuna conversazione precedente), aperta nella
cartella che contiene solo i documenti. Sostituisci `<CARTELLA>` con il percorso della cartella.

---

Nella cartella `<CARTELLA>` ci sono SOLO i documenti di un progetto (SPEC.md, PIANO.md, CLAUDE.md,
README.md, HANDOFF.md). Il codice non c'è. Il tuo compito: ricostruire il progetto completo e
funzionante in quella cartella, basandoti esclusivamente su questi documenti.

Regole dell'esperimento:
- Lavora SOLO dentro `<CARTELLA>`. Non leggere altre cartelle: lo scopo è verificare se la
  documentazione da sola basta.
- Nessuno risponderà alle tue domande: non farne. Quando la documentazione è ambigua, incompleta o
  contraddittoria, decidi tu nel modo più ragionevole e annota la cosa in `<CARTELLA>/DUBBI.md`
  (una voce per punto: cosa mancava o era ambiguo, cosa hai deciso, quale documento e sezione).
  Questo file è il risultato più importante dell'esperimento: sii onesto e completo, anche sulle
  piccole cose che hai dovuto inventare.
- Non modificare i file .md esistenti.
- Crea anche i dati di esempio previsti dai documenti, con persone inventate.
- Scrivi i test come richiesto dai documenti ed eseguili dentro Docker finché passano. Poi avvia
  l'app e verifica che risponda.
- Non fare commit git.

Alla fine rispondi con: elenco dei file creati, risultato dei test, se l'app risponde, e un
riassunto delle voci di DUBBI.md.

---

Nota: se sul PC gira già un'altra copia del progetto, aggiungi al prompt
"le porte 8000 e 3307 sono occupate: usa 8001 per l'app e 3308 per MySQL".
