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
`AGENTS.md`. Così tutti leggono le stesse istruzioni, e quando cambiano si aggiornano in un posto solo.
Il prompt ([prompt.md](prompt.md)) lo dice comunque esplicitamente, per gli assistenti che non leggono
nessuno dei due file da soli.

## Claude Code

1. Prepara la cartella: `.\prepara-cartella.ps1 C:\lezione\ricostruito`
2. Apri un terminale in quella cartella e avvia `claude` (conversazione nuova).
3. Incolla il prompt di [prompt.md](prompt.md) con il percorso giusto.
4. Quando chiede il permesso per i comandi (Docker, test), concedilo.

## Antigravity

1. Prepara la cartella come sopra.
2. Apri **quella cartella** come area di lavoro in Antigravity (non la cartella del progetto originale:
   l'assistente non deve poterlo vedere).
3. Apri una conversazione nuova con l'agente e incolla il prompt di [prompt.md](prompt.md).
4. Permetti all'agente di usare il terminale, altrimenti non può avviare Docker né i test.
   Se si ferma a chiedere conferme per ogni comando, approvale: l'esperimento dura più a lungo, ma va bene.

## Altri assistenti

Stessa procedura: cartella preparata, conversazione nuova, prompt incollato, terminale permesso.

## Da sapere prima della lezione

- **Antigravity non è ancora stato provato con questo esperimento**: le prove 1-3 sono state fatte con
  Claude Code. La prima volta in classe è anche la prima prova con Antigravity: annotate cosa succede.
- Assistenti diversi **trovano dubbi diversi**: confrontare i loro DUBBI.md è la parte più interessante
  della lezione (vedi [ISTRUZIONI.md](ISTRUZIONI.md)).
- Se un assistente non riesce a usare Docker, il risultato è comunque utile: i suoi DUBBI.md dicono
  dove la documentazione non è stata chiara.
