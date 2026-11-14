# Con quale assistente AI? (Claude Code, Antigravity, altri)

L'esperimento funziona con qualsiasi assistente AI che sappia **leggere e scrivere file** nella cartella
e **usare il terminale** (serve per Docker e per i test). Uno che risponde solo in chat non basta.

## Il punto chiave: il file delle istruzioni

Ogni assistente cerca le "istruzioni di progetto" in un file con un nome diverso:

| Assistente | File che legge da solo |
|---|---|
| Claude Code | `CLAUDE.md` |
| Antigravity (Google) | `AGENTS.md` o `GEMINI.md` ([documentazione ufficiale](https://www.antigravity.google/docs/rules/)) |
| Cursor, Codex e altri | di solito `AGENTS.md` |

Per questo il progetto ha **un solo file vero, `AGENTS.md`**, e `CLAUDE.md` contiene solo un rimando a
`AGENTS.md`. Così tutti leggono le stesse istruzioni. Il prompt ([PROMPT.md](PROMPT.md)) lo dice comunque
esplicitamente, per gli assistenti che non leggono nessuno dei due file da soli.

## Claude Code

1. Apri un terminale **nella cartella `progetto/`** del kit e avvia `claude` (conversazione nuova).
2. Incolla il prompt di [PROMPT.md](PROMPT.md).
3. Quando chiede il permesso per i comandi (Docker, test), concedilo.

## Antigravity

1. Apri **la cartella `progetto/`** del kit come area di lavoro (non il kit intero e non il repository
   originale: l'assistente non deve poter vedere altro).
2. Apri una conversazione nuova con l'agente e incolla il prompt di [PROMPT.md](PROMPT.md).
3. Permetti all'agente di usare il terminale, altrimenti non può avviare Docker né i test.
   Se si ferma a chiedere conferme per ogni comando, approvale: ci mette di più, ma va bene.

## Altri assistenti

Stessa procedura: cartella `progetto/` aperta, conversazione nuova, prompt incollato, terminale permesso.

## Da sapere

- **Antigravity non è ancora stato provato con questo esperimento**: le prove 1-3 sono state fatte con
  Claude Code. La prima volta in classe è anche la prima prova con Antigravity: annotate cosa succede.
- Assistenti diversi **trovano dubbi diversi**: confrontare i loro DUBBI.md è la parte più interessante.
- Se un assistente non riesce a usare Docker, il risultato è comunque utile: i suoi DUBBI.md dicono
  dove la documentazione non è stata chiara.
