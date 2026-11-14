# Risultati dell'esperimento (14/11/2026)

## In breve

| Domanda | Risposta |
|---|---|
| Il Claude nuovo ha ricostruito un programma funzionante? | **Sì.** App web su porta 8001, 28 test scritti da lui, tutti verdi. Circa 10 minuti di lavoro. |
| Ha rispettato i criteri della spec (C1-C17)? | **Sì**, nelle prove fatte: ricerche, scheda, colleghi, stesso evento, navigazione, nessun doppione. |
| Ha dovuto indovinare? | **Sì, 36 volte** (vedi [DUBBI-del-claude-nuovo.md](DUBBI-del-claude-nuovo.md)). |
| I nostri dati entrano nella sua versione? | **No, al primo colpo.** Ecco la scoperta più importante (sotto). |

## La prova decisiva: i nostri dati nella sua versione

Il PIANO dice che tutte le fonti di dati passano da una "porta d'ingresso" con un formato unico.
Se il formato è documentato bene, il nostro file `dati/esempio.json` deve entrare anche nella versione
ricostruita. Risultato:

```
Scartate: 1
  - il file non contiene una lista di persone
```

**Perché:** PIANO.md sezione 2 mostra com'è fatta *una* persona, ma non dice com'è fatto *il file*.
Il nostro file è `{"nota": ..., "persone": [ ... ]}`; il Claude nuovo si aspettava direttamente `[ ... ]`.
Nessuno dei due ha sbagliato: **il documento non lo diceva.** Dopo aver tolto l'involucro, le 7 persone sono entrate.

**Seconda sorpresa:** dopo l'import c'erano **due Mario Rossi**: il suo (con profilo LinkedIn) e il nostro (senza).
Il criterio C12 dice "nessun doppione", ma la spec non dice **quando due persone sono la stessa persona**.
È una regola che vale anche nella versione originale: il buco c'era già, l'esperimento l'ha solo fatto vedere.

## I 36 dubbi, divisi per tipo

Non tutti i dubbi sono uguali. Dividerli insegna dove va scritta ogni cosa.

### A. Buchi nella SPEC: decisioni che spettano all'utente, non all'AI
Questi sono i più importanti: l'AI ha deciso al posto dell'utente.
- **Quando due persone sono la stessa?** (stesso nome ma una con profilo e una senza → oggi diventano due)
- **Ricerca per azienda** a pezzi ("accent" trova Accenture) ma **skill** solo esatta: la spec non lo dice.
- **Collegamenti a mano doppi** (Mario→Luca scritto due volte): ammessi o no?
- **Reimportare una persona** aggiorna i dati ma non cancella mai niente: è quello che vogliamo?
- **"Segnalato" in C13**: segnalato dove? Nella pagina? Nel terminale?
- **Ordine alfabetico** con accenti e maiuscole.

### B. Buchi nel PIANO: scelte tecniche giuste da far decidere all'AI, ma da scrivere
- **Formato del file** della porta d'ingresso (lista o oggetto con "persone").
- Nomi delle **variabili d'ambiente**, del database, dell'utente; **porte** di MySQL sul PC.
- Libreria per parlare con MySQL e **versioni** delle librerie.
- Indirizzo della pagina **ricerca per evento**.
- Il **database dei test** viene creato solo al primo avvio (volume vuoto).
- Ogni modifica al database va **salvata subito** (autocommit), altrimenti una pagina può non vedere un dato appena inserito.
- In Git Bash su Windows il comando di import vuole `MSYS_NO_PATHCONV=1` davanti.

### C. Errori nei documenti
- Il README parlava di criteri **C1-C13**, la SPEC arriva a **C17**: il README non era stato aggiornato
  dopo l'aggiunta della navigazione. Esattamente il tipo di errore che lo spec coding vuole evitare.

### D. Libertà che vanno bene così
Colori, testi dei messaggi, pagina 404, iniziali al posto della foto, numero di eventi in Home.
Non serve scriverli: qualsiasi scelta ragionevole va bene. **Non tutto va specificato.**

## Cosa abbiamo imparato

1. **La documentazione bastava per rifare un programma funzionante**: è la prova che il metodo funziona.
2. **Ma non bastava per rifare *lo stesso* programma**: due versioni costruite dagli stessi documenti
   non si scambiano i dati. Il formato della porta d'ingresso va scritto fino all'ultimo dettaglio,
   perché è il punto in cui il programma incontra il mondo esterno.
3. **L'AI riempie i buchi in silenzio.** Senza la regola "scrivi in DUBBI.md ogni volta che indovini",
   le 36 decisioni sarebbero state prese senza dirlo a nessuno. Nel vibe coding succede sempre,
   solo che non lo vedi.
4. **Un buco era anche nel progetto originale** (la persona con e senza profilo): ricostruire da zero
   è un ottimo modo per fare una revisione della spec.

## Cosa abbiamo corretto (14/11, stesso giorno)

Seguendo il metodo: prima le decisioni dell'utente, poi spec, piano, test che falliscono, codice.

- **Punti A, decisi dall'utente** e scritti in SPEC.md come regole D4-D7 e criteri C18-C24:
  - stessa persona = stesso profilo, oppure stesso nome+cognome con almeno uno senza profilo;
    due profili diversi = omonimi (C18, C19); caso ambiguo scartato e segnalato (C20, proposta di Claude);
  - azienda a pezzi, skill esatta (C21);
  - collegamento uguale scritto due volte → "Collegamento già presente." (C22);
  - reimport non cancella (C23); "segnalato" = resoconto dell'import (D7); ordine senza accenti (C24).
- **Punti B** scritti in PIANO.md: formato del file (lista *oppure* `{"persone": [...]}`), regole dei campi,
  regola "stessa persona" passo per passo, librerie, variabili d'ambiente, porte, indirizzi delle pagine,
  database dei test, salvataggi, nota su Git Bash.
- **Punto C**: README corretto.
- **Test**: 10 nuovi (`test_esperimento.py`). Prima del codice 5 fallivano (i comportamenti nuovi),
  5 passavano già (comportamenti che esistevano ma non erano scritti). Ora 37 su 37.

Prossimo passo possibile: rifare l'esperimento con i documenti corretti e contare i dubbi.

I documenti usati in questo esperimento, **prima** delle correzioni, sono in
[per-la-classe/documenti/](per-la-classe/documenti/).
