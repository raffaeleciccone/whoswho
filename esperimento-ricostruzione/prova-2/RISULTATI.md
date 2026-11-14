# Prova 2: stessa prova, con i documenti corretti (14/11/2026)

Stesso prompt della prova 1 ([../per-la-classe/prompt.md](../per-la-classe/prompt.md)), stesso controllo,
un altro Claude nuovo. Unica differenza: i documenti erano quelli **corretti dopo la prova 1**
(regole D4-D7, criteri C18-C24, PIANO sez. 2 e 3b).

## Confronto

| | Prova 1 | Prova 2 |
|---|---|---|
| Programma funzionante | sì | sì |
| Test scritti da lui | 28, tutti verdi | 36, tutti verdi |
| **Prova decisiva**: il nostro `esempio.json` entra senza modifiche? | **no** ("il file non contiene una lista di persone") | **sì**: 7 persone, 0 scartate |
| Mario Rossi doppio dopo l'import dei nostri dati? | **sì**, due persone | **no**: riconosciuto come la stessa persona e aggiornato |
| Secondo import dello stesso file | — | 0 nuove, 7 aggiornate: nessun doppione |
| Dubbi scritti in DUBBI.md | 36 | **51** |

## Ma i dubbi sono aumentati: è andata peggio?

No. **Il numero dei dubbi non è la misura giusta: conta il loro peso.**

Nella prova 1 l'AI aveva deciso da sola le cose che rompono il programma quando incontra il mondo esterno:
com'è fatto il file dei dati, quando due persone sono la stessa. Infatti la prova decisiva era fallita.
Nella prova 2 quelle cose erano scritte, e la prova decisiva è passata.

I dubbi sono di più perché i documenti sono più ricchi (più regole = più domande sui dettagli) e
perché questo Claude ha elencato anche le piccolezze. Divisi per peso:

| Tipo | Quanti | Esempi |
|---|---|---|
| Dovuti all'esperimento, non sono buchi | 8 | porte diverse, cartelle citate ma non copiate, "non ho potuto fare domande" |
| Libertà accettabili (aspetto, testi, dettagli) | ~25 | formato delle date nella scheda, 5 eventi in Home, iniziali al posto della foto, pagina 404 |
| Dettagli tecnici, decisi bene da lui | ~13 | versioni delle librerie, lunghezza dei campi, healthcheck di MySQL |
| **Da decidere davvero** | **5** | qui sotto |

## I 5 punti che contano

1. **Un errore nei criteri (dubbio 1).** C17 dice "dopo Bianchi viene Esposito" e C24 dice che "éboli" sta tra
   Bianchi ed Esposito: **non possono essere veri sugli stessi dati**. Un criterio non deve dipendere da dati che
   non sono scritti nel criterio stesso. Va riscritto C17 con le sue persone ("con Bianchi, Esposito e Rossi, ...").
2. **"Fine 2022" diventa il 1° gennaio 2022 (dubbio 29).** Il PIANO dice che una data di solo anno diventa il
   1° gennaio, ma per la **fine** di un lavoro è sbagliato: Mario 2019-2022 e Luca dal marzo 2022 non risultano
   colleghi. **Questo errore c'è anche nella versione originale.** Per la fine servirebbe il 31 dicembre (e
   l'ultimo giorno del mese per "AAAA-MM"). Decisione dell'utente.
3. **Profili "uguali" (dubbio 30).** `http://` e `https://`, con e senza `www.`: stessa persona o no?
4. **Ricerca per nome con più parole (dubbio 7).** "Mario Rossi" deve trovare chi ha *tutte* le parole?
   La spec non lo dice (le due versioni si comportano quasi uguali per caso).
5. **Ricerca vuota (dubbio 8).** Messaggio "Scrivi qualcosa da cercare" o "nessun risultato"?

Più un dettaglio tecnico da scrivere nel PIANO (dubbio 42): nei test, una connessione che legge dati scritti da
un'altra (la pagina web) deve usare l'isolamento READ COMMITTED, altrimenti non li vede.

## Cosa abbiamo corretto (stesso giorno, un punto alla volta con l'utente)

| Punto | Decisione | Dove |
|---|---|---|
| 1. C17 dipendeva dai dati | C17 riscritto con le sue tre persone; nuova regola: "ogni criterio contiene i suoi dati" | SPEC sez. 5, CLAUDE.md |
| 2. Data di fine incompleta | inizio = primo giorno, **fine = ultimo** ("fine 2022" = 31/12/2022) | SPEC C25, PIANO sez. 2 |
| 3. Profili scritti in modi diversi | contano solo sito + percorso (via http/https, www., "it.", "/", "?...") | SPEC D4 e C26, PIANO sez. 3 |
| 4. Ricerca con più parole | ogni parola, anche a pezzi, nel nome o nel cognome | SPEC F1 e C27, PIANO sez. 3 |
| 5. Ricerca vuota | messaggio "Scrivi qualcosa da cercare." | SPEC C28, PIANO sez. 3 |
| tecnico | READ COMMITTED per le connessioni dei test | PIANO sez. 5 |

Per ogni punto: prima la spec, poi i test (falliti), poi il codice, poi la prova "rompo apposta e il test se ne accorge".
Test: da 37 a **44**, tutti verdi.

**Un episodio utile per la lezione:** nel punto 4 il test è fallito dopo aver scritto il codice, ma il codice era
giusto: era sbagliato l'**esempio nella spec** ("mario r" doveva trovare solo Mario Rossi, ma la "r" c'è anche in
"Mario"). Il test ha trovato una contraddizione dentro la spec stessa. Si è corretto il criterio, non il codice.

## Cosa impariamo dalla prova 2

1. **Le correzioni hanno funzionato** sui punti che contavano: file e "stessa persona" ora non si indovinano più.
2. **Ogni giro trova buchi più piccoli.** Prova 1: il formato dei dati. Prova 2: le date di fine e un criterio scritto male.
3. **Il punto 2 era un errore anche nostro.** Ricostruire da zero non controlla solo i documenti:
   è anche una revisione del progetto fatta da occhi nuovi.
4. **Una spec perfetta non esiste.** Ci si ferma quando i dubbi rimasti sono libertà accettabili
   e poche decisioni esplicite, non quando i dubbi sono zero.
