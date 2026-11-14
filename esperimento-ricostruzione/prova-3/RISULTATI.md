# Prova 3: ricostruzione con la grafica (14/11/2026)

Stesso prompt delle prove 1 e 2, un altro Claude nuovo. Documenti: SPEC, PIANO, CLAUDE, README, HANDOFF
**più la bozza grafica approvata** (`design/bozza.html`), perché ora fa parte della specifica (criterio C35).
Novità rispetto alla prova 2: grafica (F9, C29-C38), tre container con nginx, misura automatica di C34.

## Confronto

| | Prova 1 | Prova 2 | Prova 3 |
|---|---|---|---|
| Programma funzionante | sì | sì | sì, con nginx davanti |
| Test scritti da lui, tutti verdi | 28 | 36 | 50 |
| Prova "rompo apposta e il test se ne accorge" | 1 regola | 2 regole | 8 regole |
| **Prova decisiva**: il nostro `esempio.json` entra senza modifiche | no | sì | **sì** (7 persone, 0 scartate) |
| Mario Rossi doppio dopo l'import | sì | no | **no** |
| **C34**: la scheda tipica sta nel portatile 1366×768 | — | — | **sì: 579 px su 650**, lo stesso numero dell'originale |
| Aspetto confrontato con la bozza (C35) | — | — | screenshot "praticamente uguali" |
| Dubbi scritti | 36 | 51 | 56 |

## Il risultato più importante

**Due versioni costruite da Claude diversi, partendo dagli stessi documenti, hanno la stessa misura al pixel
(579 px) e lo stesso aspetto.** La grafica, che di solito è la parte più "a sensazione", è diventata
riproducibile: perché le decisioni erano scritte (misure, colori, disposizione) e c'era una bozza approvata.

## I dubbi che contano

Come nella prova 2, il numero conta poco; contano quelli che rivelano un errore vero:

1. **C32 contraddice F9 (errore nei documenti).** C32 diceva ancora "le persone collegate stanno dopo tutti
   gli altri riquadri": era rimasto dalla seconda versione della disposizione. Quando l'utente ha scelto la
   terza (persone nella testata), F9 e il PIANO sono stati aggiornati, C32 no. Il Claude nuovo ha seguito
   F9 e la bozza, quindi ha scelto bene, ma ha dovuto indovinare.
   **Lezione: quando cambia una decisione, vanno cercati tutti i punti che la citano**, non solo il primo.
2. **C30 contro la bozza.** C30 dice "testo almeno 18 px", ma nella bozza approvata date, ruoli e nomi sotto
   le miniature sono più piccoli (13,5-16 px). Anche la versione originale è così: il test controlla solo
   la base (18 px), non i testi secondari. **Decisione per l'utente**: i testi secondari possono essere più
   piccoli? Fino a quanto?
3. **Messaggio vecchio nel PIANO**: "Collegamento già presente." invece di "Relazione già presente." (errore).
4. **C2 dice "nessun risultato"**, la pagina dice "Nessun risultato." (dettaglio di scrittura).
5. **"incontrata" (F2) contro "incontrato" (titolo nella bozza)**: piccola incoerenza di testo.
6. **Le porte 8000/3307 erano date per scontate** anche nello strumento di misura (dettaglio tecnico).

Il resto (comportamenti minori inventati, dettagli tecnici, metodo non seguibile senza utente) è dello stesso
tipo della prova 2: libertà accettabili o scelte tecniche ragionevoli.

## Cosa abbiamo corretto (stesso giorno)

- **C32** riscritto: le persone collegate stanno nella testata (come F9 e la bozza).
- **C30**: decisione dell'utente, i testi secondari possono essere più piccoli ma **mai sotto 13,5 px**;
  nuovo controllo nel test (provato rompendolo apposta: il test se ne accorge).
- PIANO: messaggio "Relazione già presente."; "collegamenti a mano" → "Relazioni" anche in PIANO e README.
- C2: "Nessun risultato." scritto come nella pagina; titoli dei riquadri scritti in F9.
- `strumenti/misura_c34.py` legge la porta dal file `.env`.
- Test: 52 su 52; C34 misurato di nuovo: rispettato.

## Cosa impariamo dalla prova 3

1. **La grafica si può specificare** come il resto: con decisioni scritte, misure e una bozza approvata.
2. **Ogni prova trova errori diversi**: prova 1 il formato dei dati, prova 2 le date, prova 3 un criterio
   "dimenticato" dopo un cambio di decisione. Il metodo funziona come un controllo continuo dei documenti.
3. **Il pericolo nuovo con documenti lunghi** è l'incoerenza interna: più decisioni si cambiano,
   più è facile lasciare una frase vecchia da qualche parte.
