# Rifare l'esperimento a lezione (traccia per chi la guida)

**Domanda dell'esperimento:** un assistente AI che non ha mai visto il progetto riesce a ricostruirlo
leggendo **solo la documentazione**? E dove deve indovinare?

Tutto quello che serve agli studenti è in una cartella sola: **[kit-ricostruzione/](../../kit-ricostruzione/)**
(istruzioni passo passo in [LEGGIMI.md](../../kit-ricostruzione/LEGGIMI.md)).

Durata: circa 45 minuti (15-25 di lavoro dell'AI, il resto per il confronto e la discussione).

## Idea: gruppi con assistenti diversi

Dividete la classe in gruppi e date a ogni gruppo un assistente diverso (per esempio Claude Code,
Antigravity, Cursor). Tutti partono dallo **stesso kit** e dallo **stesso prompt**. Alla fine si
confrontano i risultati: è il modo migliore per vedere quanto conta la documentazione e quanto l'assistente.

## Svolgimento

1. Ogni gruppo segue [LEGGIMI.md](../../kit-ricostruzione/LEGGIMI.md) del kit fino al passo 3 (prompt incollato).
2. **Mentre l'AI lavora**, leggete insieme `progetto/SPEC.md` e chiedetevi: *"dove dovrà indovinare?"*.
   Scrivete le ipotesi alla lavagna.
3. Quando ha finito, ogni gruppo fa i controlli di [VERIFICA.md](../../kit-ricostruzione/VERIFICA.md).
4. Ogni gruppo legge il suo `DUBBI.md` e divide i dubbi in 4 tipi:
   - **A. Buchi nella spec**: decisioni che spettavano all'utente (le più importanti)
   - **B. Buchi nel piano**: scelte tecniche giuste, ma non scritte
   - **C. Errori nei documenti**: contraddizioni, frasi rimaste vecchie
   - **D. Libertà accettabili**: aspetto, testi, dettagli che non serve specificare
5. Confronto tra i gruppi e con le nostre prove: [prova 1](../RISULTATI.md), [prova 2](../prova-2/RISULTATI.md),
   [prova 3](../prova-3/RISULTATI.md).

## Domande per la discussione

- Quali dubbi erano decisioni che doveva prendere l'utente e non l'AI? (tipo A)
- Assistenti diversi hanno avuto gli stessi dubbi? Se no, chi ha visto cosa?
- La misura C34 è uguale tra le versioni (nella nostra è 579 px)? Se sì, perché la grafica si è potuta
  riprodurre al pixel? Se no, quale decisione mancava nei documenti?
- In un progetto fatto "a vibe coding", dove finiscono tutte queste decisioni prese in silenzio?

## Variante: prima e dopo

In [documenti-prova-1/](documenti-prova-1/) ci sono i documenti della **prima** prova, prima di tutte le
correzioni (senza grafica, senza AGENTS.md). Copiateli in una cartella vuota, usate lo stesso prompt del
kit e confrontate quanti e quali dubbi emergono rispetto ai documenti attuali.
