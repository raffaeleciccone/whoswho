# Rifare l'esperimento a lezione

**Domanda dell'esperimento:** un assistente AI che non ha mai visto il progetto riesce a ricostruirlo
leggendo **solo la documentazione**? E dove deve indovinare?

Durata: circa 45 minuti (15-25 di lavoro dell'AI, il resto per il confronto e la discussione).

## Cosa serve

- Un PC per gruppo con **Docker Desktop** acceso e un **assistente AI che usa il terminale**
  (Claude Code, Antigravity, Cursor...): vedi [STRUMENTI.md](STRUMENTI.md).
- **Google Chrome** (o Edge) per la misura C34.
- Una copia di questo repository (`git clone`).

## Idea per la classe: gruppi con assistenti diversi

Dividete la classe in gruppi e date a ogni gruppo un assistente diverso (per esempio un gruppo con
Claude Code, uno con Antigravity, uno con un altro). Tutti partono dagli **stessi documenti** e dallo
**stesso prompt**. Alla fine si confrontano i risultati: è il modo migliore per vedere quanto conta la
documentazione e quanto l'assistente.

## Passi

1. **Prepara la cartella** con i soli documenti (dalla cartella `per-la-classe`):
   ```powershell
   .\prepara-cartella.ps1 C:\lezione\ricostruito
   ```
   (con `-Prova1` si usano i documenti della prova 1, prima delle correzioni: vedi "Variante")
2. **Apri l'assistente** in quella cartella, in una conversazione **nuova** ([STRUMENTI.md](STRUMENTI.md)).
3. **Incolla il prompt** di [prompt.md](prompt.md), con il percorso giusto.
4. **Mentre lavora**, leggete SPEC.md e chiedetevi: *"dove dovrà indovinare?"*. Scrivete le ipotesi alla lavagna.
5. **Quando ha finito**, fate i controlli di [VERIFICA.md](VERIFICA.md).
6. **Leggete il suo DUBBI.md** e dividete i dubbi in 4 tipi:
   - **A. Buchi nella spec**: decisioni che spettavano all'utente (le più importanti)
   - **B. Buchi nel piano**: scelte tecniche giuste, ma non scritte
   - **C. Errori nei documenti**: contraddizioni, frasi rimaste vecchie
   - **D. Libertà accettabili**: aspetto, testi, dettagli che non serve specificare
7. **Confrontate** con le nostre prove: [prova 1](../RISULTATI.md), [prova 2](../prova-2/RISULTATI.md),
   [prova 3](../prova-3/RISULTATI.md), e tra i gruppi.

## Domande per la discussione

- Quali dubbi erano decisioni che doveva prendere l'utente e non l'AI? (tipo A)
- Assistenti diversi hanno avuto gli stessi dubbi? Se no, chi ha visto cosa?
- La misura C34 è uguale tra le versioni (nella nostra è 579 px)? Se sì, perché la grafica si è potuta
  riprodurre al pixel? Se no, quale decisione mancava nei documenti?
- In un progetto fatto "a vibe coding", dove finiscono tutte queste decisioni prese in silenzio?

## Variante: prima e dopo

Rifate l'esperimento con `-Prova1`: sono i documenti della prima prova, **prima** di tutte le correzioni
(senza grafica, senza AGENTS.md). Confrontate quanti e quali dubbi emergono rispetto ai documenti attuali.
