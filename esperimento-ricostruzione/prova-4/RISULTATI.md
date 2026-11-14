# Prova 4: "da studente", con il kit (15/11/2026)

Questa volta non si è preparata la cartella a mano: si è fatto **esattamente** quello che faranno i compagni.

1. Scaricato lo ZIP del repository da GitHub (pulsante Code → Download ZIP): il repository è pubblico.
2. Copiata **solo** la cartella `kit-ricostruzione/` fuori dal repository (`C:\dev\lezione-prova4\`).
3. Un Claude nuovo, aperto in `kit-ricostruzione/progetto/`, ha ricevuto **il testo di PROMPT.md così com'è**,
   più la nota sulle porte che PROMPT.md stesso suggerisce quando 8000/3307 sono occupate.
4. Alla fine, i controlli di `VERIFICA.md` del kit, fatti come li farebbe uno studente.

## Risultati

| | Prova 3 | Prova 4 (kit) |
|---|---|---|
| Programma funzionante, tre container | sì | sì |
| Test scritti da lui, tutti verdi | 50 | 59 |
| "Rompo apposta e il test se ne accorge" | 8 regole | 9 regole |
| Prova decisiva: i nostri dati entrano senza modifiche | sì | **sì** (7 persone, 0 scartate) |
| Mario Rossi doppio / secondo import crea doppioni | no / no | **no / no** |
| C34 misurato con `misura_c34.py` **del kit** | 579 px | **579 px su 650**, telefono senza scorrimento |
| Ricerche controllate a mano (C21, C28) | — | come atteso |
| Dubbi scritti | 56 | 63 |

**Il kit funziona da solo**, dall'inizio (ZIP da GitHub) alla fine (verifica). Quarta ricostruzione, quarta
volta 579 px.

## I dubbi che contano

1. **Una data di fine sbagliata crea colleghi falsi (errore vero, anche nel programma originale).**
   Una data non valida (es. "2017-13") diventa vuota (PIANO sez. 2), ma "fine vuota" vuol dire
   "ci lavora ancora" (C9). Verificato sulla versione originale: Mario, uscito da Accenture nel 2017 ma con
   la data scritta male, risulta collega di Luca, assunto nel 2024. **Decisione per l'utente.**
2. **SPEC F8 scrive "‹ Precedente / Successiva ›"**, la bozza approvata mostra icona + "Precedente: Nome".
   Il Claude nuovo ha seguito la bozza (giusto), ma la spec andava allineata.
3. **Le coppie di colori controllate da C29 non sono scritte nei documenti**: il PIANO elenca i colori ma
   non quali testi stanno su quali sfondi. Ognuno se le sceglie.
4. **PIANO 4c fissa la porta 8000** nel `<base href>` della misura C34: con un'altra porta non va.

Il resto: le solite libertà accettabili (testi, formati, pagina 404) e le scelte tecniche ragionevoli.

## Cosa abbiamo corretto (stesso giorno)

- **Punto 1, deciso dall'utente:** una fine scritta male fa **ignorare quel lavoro**, con un avviso nel
  resoconto; la persona entra lo stesso. Nuovo criterio **C39**, test scritto prima del codice (falliva),
  poi il codice; rompendo apposta la regola il test se ne accorge. Test: 53 su 53.
- **Punto 2:** SPEC F8 allineata alla bozza ("Precedente: <nome>", "Successiva: <nome>").
- **Punto 3:** le coppie di colori di C29 ora sono scritte nel PIANO (sez. 4c).
- **Punto 4:** nel PIANO la misura C34 usa la porta `HOST_APP_PORT`, non 8000 fissa.
- Kit rigenerato con `aggiorna_kit.py`.

## Cosa impariamo dalla prova 4

1. **Il kit è pronto per la classe**: scaricato da GitHub e usato alla lettera, funziona.
2. **Anche dopo tre prove si trova un errore vero** (punto 1). Più il programma è controllato, più gli
   errori che restano sono sottili: qui serve un dato sbagliato *e* due persone nella stessa azienda.
