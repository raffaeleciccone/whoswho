# Kit: ricostruisci Who's Who dalla sola documentazione

**L'esperimento:** in `progetto/` c'è **solo la documentazione** di un programma (cosa deve fare, come è
costruito, la bozza grafica), **nemmeno una riga di codice**. Un assistente AI (Claude Code, Antigravity...)
deve ricostruire il programma completo leggendo solo quei documenti, e scrivere in `DUBBI.md` ogni punto
in cui ha dovuto indovinare.

Se la documentazione è scritta bene, il programma ricostruito si **comporta** come l'originale: stessi
criteri rispettati, stessi dati accettati, stessa grafica. Il codice sarà diverso, ed è normale.
I DUBBI dicono dove la documentazione non bastava: sono il risultato più interessante.

## Cosa c'è qui

| | |
|---|---|
| `progetto/` | i documenti: SPEC.md (cosa), PIANO.md (come), AGENTS.md (istruzioni per l'assistente), CLAUDE.md, README.md, HANDOFF.md, design/bozza.html |
| [PROMPT.md](PROMPT.md) | il testo da dare all'assistente |
| [STRUMENTI.md](STRUMENTI.md) | come usare Claude Code, Antigravity o altri |
| [VERIFICA.md](VERIFICA.md) | i controlli da fare alla fine, con i risultati attesi |
| `dati-di-prova/` | i dati del programma originale, per la prova decisiva |
| `misura_c34.py` | misura con Chrome se la scheda sta nello schermo (criterio C34) |

## Cosa serve sul PC

- **Docker Desktop**, acceso
- **Python 3** e **Google Chrome** (o Edge): servono solo per la misura finale
- un assistente AI che può **leggere/scrivere file e usare il terminale**: Claude Code, Antigravity, Cursor...

## I passi

1. **Scarica il kit e copialo FUORI dal repository**, per esempio in `C:\lezione\kit-ricostruzione`.
   Da GitHub: pulsante verde **Code → Download ZIP**, estrai, e copia solo la cartella `kit-ricostruzione`
   altrove. È importante: se il kit resta dentro il repository, l'assistente (e Docker) potrebbero
   trovare il programma originale nella cartella superiore, e l'esperimento non varrebbe più.
2. **Apri l'assistente nella cartella `progetto/`** (non nel kit intero), in una conversazione **nuova**.
   Come fare con ogni strumento: [STRUMENTI.md](STRUMENTI.md).
3. **Incolla il prompt** di [PROMPT.md](PROMPT.md) e aspetta: di solito 15-25 minuti.
   Se chiede il permesso di usare il terminale o Docker, concedilo.
4. **Quando ha finito**, fai i controlli di [VERIFICA.md](VERIFICA.md).
5. **Leggi `progetto/DUBBI.md`**: dove ha dovuto indovinare? Confrontalo con quello dei compagni che hanno
   usato un altro assistente.

## Da sapere

- Il programma usa le porte **8000** (sito) e **3307** (MySQL). Se sono già occupate, vedi la nota in fondo a PROMPT.md.
- Con **Claude Code** l'esperimento è stato fatto tre volte (risultati nel repository, cartella
  `esperimento-ricostruzione/`). Con **Antigravity** non è ancora stato provato: annotate come va.
