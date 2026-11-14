# DUBBI — ricostruzione di Who's Who dai soli documenti (prova 3, 14/11/2026)

Per ogni punto: **cosa mancava / era ambiguo**, **cosa ho deciso**, **dove** (documento e sezione).
Ordine: prima le contraddizioni vere tra documenti, poi le cose che ho dovuto inventare, poi i dettagli tecnici.
Ho letto solo SPEC.md, PIANO.md, CLAUDE.md, README.md, HANDOFF.md e design/bozza.html.

---

## A. Contraddizioni tra documenti (o dentro lo stesso documento)

1. **Dove stanno le persone collegate nella scheda (C32 contro F9).**
   SPEC C32 dice "le persone collegate stanno *dopo tutti gli altri riquadri*"; SPEC F9 (decisione 1, "terza versione"),
   PIANO 4c e la bozza le mettono **nella testata, a destra, prima dei 4 riquadri**.
   *Deciso:* ho seguito F9 + bozza + PIANO (sono la decisione più recente e approvata, e C34 è stato misurato così).
   Il test `test_c32_...` controlla la posizione nuova (foto → nome → striscia persone collegate → 4 riquadri).
   C32 sembra un avanzo della versione precedente della disposizione. *(SPEC sez. 5 C32 vs sez. 3c F9; PIANO 4c)*

2. **Messaggio della relazione doppia.** PIANO sez. 3 ("Collegamenti a mano") dice `"Collegamento già presente."`;
   SPEC C22 e PIANO 4c dicono `"Relazione già presente."`. *Deciso:* "Relazione già presente." (vince la spec;
   nell'interfaccia si chiamano "Relazioni"). *(PIANO sez. 3 vs SPEC C22)*

3. **"nessun risultato" vs "Nessun risultato".** C2 lo scrive minuscolo tra virgolette, C28 maiuscolo.
   *Deciso:* "Nessun risultato." (con punto, come gli altri messaggi); il test di C2 non guarda le maiuscole. *(SPEC C2, C28)*

4. **Etichette Precedente/Successiva/Indietro.** SPEC F8 e README scrivono "‹ Precedente", "Successiva ›", "← Indietro"
   (caratteri freccia); la bozza usa icone SVG e mostra anche il nome: "Precedente: Maria Romano", "Successiva: Andrea Rossi".
   *Deciso:* come la bozza (icona SVG + "Precedente: Nome Cognome"); la freccia di Indietro è l'icona `i-indietro`.
   *(SPEC F8; README "Per muoversi"; design/bozza.html)*

5. **Dimensione del testo (C30) contro la bozza.** C30: "il testo normale è di almeno 18 px". La bozza però ha testi più
   piccoli: date e ruoli `.piccolo` 0,85rem (15,3 px), dettaglio sotto le miniature 0,75rem (13,5 px), tasto Elimina 0,8rem,
   nomi nelle miniature 0,9rem. *Deciso:* tenuti come nella bozza, interpretando "testo normale" come il testo base
   (html 18 px) e considerando quelli più piccoli "testo secondario". Il test controlla html 18 px, h1 28 px e che nessuna
   regola su body/main/p/li rimpicciolisca il testo. Se il prof misura *ogni* testo, C30 non è rispettato. *(SPEC C30; bozza)*

6. **Titolo h1: 28 px o 1,56rem?** La bozza usa `1.56rem` (28,08 px), PIANO 4c dice `h1 { font-size: 28px }`.
   *Deciso:* 28 px esatti. *(PIANO 4c; bozza)*

7. **"Dove l'ho incontrata" (F2) vs "Dove l'ho incontrato" (bozza, PIANO 4c).** *Deciso:* "Dove l'ho incontrato" come la bozza. *(SPEC F2)*

8. **"+ Aggiungi relazione"** (SPEC F9) vs bozza (icona + "Aggiungi relazione"). *Deciso:* come la bozza, il "+" è l'icona.

9. **Porte.** Tutti i documenti dicono 8000 (sito) e 3307 (MySQL), anche "dentro" lo strumento di misura
   (`<base href="http://localhost:8000/">`, PIANO 4c). Su questo PC servivano 8001 e 3308.
   *Deciso:* porte solo in `.env` (`HOST_APP_PORT=8001`, `HOST_MYSQL_PORT=3308`), con 8000/3307 come default in
   `docker-compose.yml` e in `.env.example`; `scheda-tipica` prende la porta da `HOST_APP_PORT` (o da `--base URL`)
   e `strumenti/misura_c34.py` la legge da `.env`. *(PIANO 3b, 4c; README; CLAUDE "Comandi")*

10. **Numero di test.** HANDOFF dice "52 test"; PIANO sez. 5 dice quali file coprono quali criteri ma non quanti test.
    *Deciso:* 50 test (alcuni criteri ne hanno due); non c'era modo di arrivare esattamente a 52 senza conoscere la divisione
    originale. In più ho aggiunto `test_porta_ingresso.py` (regole del formato di PIANO sez. 2), file non citato in PIANO sez. 5.
    *(HANDOFF "Stato"; PIANO sez. 5)*

11. **C24 è un criterio di F8 ma sta nella fascia C18-C28.** PIANO 5 dice `test_navigazione.py` = C14-C17 e
    `test_esperimento.py` = C18-C28. *Deciso:* C24 in `test_esperimento.py`. *(PIANO sez. 5; SPEC C24 messo in fondo all'elenco)*

12. **Riferimenti a cose che non ci sono.** CLAUDE.md e README citano la cartella `esperimento-ricostruzione/`
    ("lezione dell'esperimento"); HANDOFF cita `SPECIFICHE.md` rimosso, il commit c05f25c, prove 1 e 2.
    *Deciso:* non ricreati (non fanno parte del programma). *(CLAUDE "Regole"; README "Esperimento")*

## B. Comportamenti non descritti che ho dovuto decidere io (il "cosa")

13. **Persone collegate vuote.** C3 dice "nessuno" per le sezioni vuote, ma non dice cosa mostrare se non ci sono colleghi
    o conosciuti. *Deciso:* il sottotitolo resta ("Colleghi", "Conosciuti allo stesso evento") con sotto "nessuno". *(SPEC C3, F9)*

14. **Dettaglio sotto la miniatura.** La bozza mostra l'azienda (colleghi) o l'evento (conosciuti). Con più aziende/eventi
    in comune non è detto. *Deciso:* tutti, separati da virgola, in ordine alfabetico. Una persona compare una sola volta
    per gruppo. *(bozza; PIANO 4c "miniature con nome e dettaglio")*

15. **Ordine delle persone collegate, delle esperienze, degli eventi e delle skill nella scheda.** Non specificato.
    *Deciso:* persone collegate e relazioni in ordine alfabetico (cognome, nome); esperienze: prima quelle in corso, poi per
    data di fine decrescente; eventi dal più recente; skill in ordine alfabetico. *(SPEC F2; bozza)*

16. **"Lavora ora in" con più lavori in corso.** SPEC F9 parla di "l'esperienza ancora in corso" (singolare).
    *Deciso:* tutte le aziende con esperienza senza data di fine, separate da virgola, ognuna cliccabile
    (ricerca per azienda). Un'esperienza senza fine conta anche se non ha data di inizio. *(SPEC F9 decisione 2; PIANO 4c)*

17. **Periodo delle esperienze.** C3 chiede "aziende (con periodo)" senza formato. *Deciso:* come la bozza, "MM/AAAA – MM/AAAA"
    oppure "MM/AAAA – oggi"; inizio mancante = "?"; nessuna data = nessun periodo. *(SPEC C3; bozza)*

18. **Validazioni del modulo "Aggiungi relazione"** (non in spec): descrizione vuota → "Scrivi una descrizione della relazione.";
    relazione con se stessi o persona inesistente → "Scegli un'altra persona."; Elimina di una relazione che non c'è più →
    "Relazione non trovata.". Nel menu la persona stessa non compare; le persone sono scritte "Cognome Nome" come nella bozza.
    *(SPEC F7, C22)*

19. **Confronto dei doppioni delle relazioni.** PIANO: "maiuscole non contano". Uso la collation `ai_ci`, quindi anche
    accenti e spazi doppi non contano ("Mario e il capo" = "Mario è il capo"). *(PIANO sez. 3)*

20. **Pagina Home.** README/PIANO dicono solo "spiegazione e ultimi eventi". *Deciso:* titolo, una frase, riquadro
    "Come si usa" e riquadro "Ultimi eventi" (i 5 più recenti, cliccabili). Testi miei. *(README "Le pagine")*

21. **Pagina Eventi.** Non c'è nella bozza. *Deciso:* stessa griglia a schede dei risultati, con icona calendario, data · luogo
    e numero di persone; eventi senza data in fondo. *(SPEC C16; bozza vista 2)*

22. **Ricerca per evento (F5: "scelgo un evento").** Non è detto *dove* si sceglie (la barra ha solo Nome/Azienda/Skill, F8).
    *Deciso:* si sceglie cliccando un evento (pagina Eventi, Home, scheda). Pagina risultati con titolo "Evento: <nome>"
    e sotto data · luogo; id sbagliato o mancante → "Evento non trovato.". *(SPEC F5, F8; PIANO 3b indirizzi)*

23. **Titolo della pagina risultati.** Dalla bozza: `Skill: “Docker”`. Ho usato `Nome: “...”`, `Azienda: “...”`,
    `Skill: “...”` con il testo come scritto dall'utente (spazi tolti), più il conteggio "N persone". *(bozza vista 2)*

24. **Persona che non esiste** (`/persona/999`): pagina "Pagina non trovata" con la barra, codice 404. Non specificato.

25. **Voce attiva nella barra.** La bozza evidenzia "Persone" sulla scheda. *Deciso:* Home sulla Home, Persone su elenco
    persone e scheda, Eventi su elenco eventi; nessuna sui risultati. *(bozza)*

26. **Indietro.** PIANO 4b: usa la cronologia del browser, e "se si è arrivati da un link diretto, porta alla Home", ma non
    dice come capirlo. *Deciso:* `href="/"` + `onclick` che fa `history.back()` solo se `document.referrer` non è vuoto e
    c'è cronologia. Quindi serve un po' di JavaScript (PIANO dice "niente JavaScript" solo per il modulo `<details>`).
    Limite: se si arriva da un altro sito, Indietro torna a quel sito. *(PIANO 4b; SPEC F8)*

27. **"Profilo online"** si apre in una nuova scheda del browser (`target="_blank"`). Non specificato. *(SPEC F9 decisione 2)*

28. **Foto.** Il formato dice solo `"foto": "https://..."`. *Deciso:* è un indirizzo di immagine mostrato con `<img>`
    (quadrata con angoli arrotondati, `object-fit: cover`); niente caricamento di file. Le iniziali sono prima lettera del
    nome + prima del cognome, maiuscole. *(PIANO sez. 2; SPEC F9)*

29. **Telefono: "pulsanti grandi da toccare".** Nessun criterio misurabile e la bozza non ha regole per il telefono oltre alle
    colonne. *Deciso:* sotto 600 px i tasti e le voci della barra diventano più alti (media query aggiunta da me). *(SPEC 3c)*

30. **C36 "se annullo, la relazione resta".** In pytest non si può premere "Annulla" su un `confirm()` del browser.
    *Deciso:* il test controlla il testo esatto della conferma nell'`onsubmit` e che la cancellazione avvenga solo con POST
    (un GET risponde 405 e la relazione resta). Il dialogo vero OK/Annulla non è provato in automatico. Il nome nel
    `confirm` è passato con `tojson`, così un apostrofo (D'Amico) non rompe il JavaScript. *(SPEC C36; PIANO 4c)*

## C. Import ("porta d'ingresso") e database

31. **Firma di `trova_persona`** non descritta: `trova_persona(cur, nome, cognome, profilo_normalizzato)` → id, `None` (nuova)
    o `"ambigua"`. *(CLAUDE "Regole"; PIANO sez. 3)*

32. **Cosa si aggiorna al reimport (D6).** "I campi presenti aggiornano quelli vecchi". *Deciso:* si aggiornano foto e professione;
    il profilo si aggiunge solo se mancava; **nome e cognome non cambiano** (es. "mario ROSSI" reimportato non cambia la scrittura
    "Mario Rossi"). Per gli eventi si aggiorna il luogo e la nota della persona se presenti; per le esperienze già presenti
    (stessa azienda + ruolo + inizio) si aggiorna la data di fine se presente. Un ruolo diverso = esperienza nuova (come PIANO). *(SPEC D6; PIANO sez. 3)*

33. **Normalizzazione del profilo.** Tolgo qualsiasi schema `xxx://` (non solo http/https) e metto in minuscolo anche il
    percorso (lo chiede C26: "Mario-Rossi" = "mario-rossi"). Il prefisso di 2 lettere si toglie solo se dopo resta un punto
    (`it.linkedin.com` → `linkedin.com`, ma `ab.cd` resta). *(SPEC D4, C26; PIANO sez. 3)*

34. **Colonna `chiave`.** Quando una persona senza profilo riceve un profilo, la sua chiave passa da "nome cognome" al profilo
    normalizzato. Con la collation `ai_ci` due chiavi "nome cognome" che differiscono solo per accenti sono la stessa
    (coerente con la ricerca degli omonimi). *(PIANO sez. 3)*

35. **Eventi con data vuota.** PIANO vuole "stesso nome + stessa data (anche nessuna data)" e un vincolo unico; in MySQL un
    vincolo UNIQUE con NULL non blocca i doppioni. *Deciso:* vincolo unico nello schema + controllo vero in `importa.py` con
    `data <=> %s`. Stessa cosa per le esperienze (ruolo e inizio possono essere vuoti). *(PIANO sez. 3)*

36. **Date.** Accetto solo `AAAA`, `AAAA-MM`, `AAAA-MM-GG` (mese/giorno anche a una cifra). Tutto il resto ("31/12/2020",
    "2022-13", "ieri") → data vuota + avviso. Data di un evento incompleta → primo giorno. *(PIANO sez. 2)*

37. **Dati malformati non previsti:** un elemento della lista che non è un oggetto → scartato e segnalato; `esperienze`,
    `skill` o `eventi` che non sono liste → avviso e ignorati; skill vuota → avviso. Ogni persona è salvata con il suo
    `commit`, così un errore su una non blocca le altre (C13). *(PIANO sez. 2; SPEC C13)*

38. **Formato del resoconto** (D7) non dato: ho scelto "Persone importate: N (nuove X, aggiornate Y)", elenco degli scartati
    con il motivo ("manca il cognome", "ambigua: ... (SPEC D5)"), elenco degli avvisi. *(SPEC D7; PIANO sez. 2)*

39. **Colleghi: casi limite.** Esperienza senza inizio non conta (PIANO). Esperienza con inizio nel futuro e senza fine:
    "fino a oggi" è prima dell'inizio, quindi non si sovrappone a niente. La persona non è mai collega di se stessa. *(PIANO sez. 3)*

40. **Ricerca a pezzi.** I caratteri `%` e `_` scritti dall'utente vengono cercati come caratteri normali (non come jolly di LIKE).
    Tipo di ricerca sconosciuto → ricerca per nome. `/cerca` senza parametri → "Scrivi qualcosa da cercare.". *(PIANO sez. 3)*

41. **READ COMMITTED.** PIANO lo suggerisce "per le connessioni dei test"; l'ho messo su **tutte** le connessioni (anche quelle
    della pagina): è innocuo e semplifica. *(PIANO sez. 5)*

## D. Dati di esempio

42. **Aziende di esempio.** Le persone devono essere inventate (CLAUDE.md); per le aziende non è detto, ma la bozza e i criteri
    usano "Accenture" (marchio reale). *Deciso:* nei dati di esempio solo aziende inventate (Nexa Data, che è nella bozza,
    Orbita Consulting, Lumen Software, Fattoria Digitale, Stellare Analytics); nei test uso "Accenture" perché è scritto nei criteri.
    *(CLAUDE "Regole"; SPEC C35 "nessun marchio"; bozza)*

43. **Contenuto di `dati/esempio.json`**: 12 persone, 5 aziende, 4 eventi, tutto inventato da me. Ci ho messo apposta casi utili
    alla prova: due Rossi, un cognome accentato (Éboli, C24), un apostrofo (D'Amico), Java vs JavaScript (C21), date incomplete,
    persona senza esperienze, profili scritti in modi diversi. Formato "oggetto con nota + persone". *(PIANO sez. 2 e 4)*

44. **Relazione di esempio.** La bozza mostra "Mario è il capo di Luca", ma l'import non può creare relazioni (PIANO sez. 2).
    *Deciso:* l'ho aggiunta a mano dalla pagina dopo l'avvio, come farebbe l'utente; non è nel file e non torna dopo `down -v`.

45. **Persona tipica di C34** (`avvio.py scheda-tipica`): dati inventati da me ricalcando la bozza (Mario Rossi con 1 evento,
    2 lavori, 4 skill, 1 relazione, 3 colleghi, 2 conosciuti). Il comando **svuota ogni volta il database dei test**. *(SPEC C34; PIANO 4c)*

## E. Dettagli tecnici inventati (scritti qui perché PIANO non li dice)

46. **Versioni esatte** in `app/requirements.txt`: Flask 3.0.3, PyMySQL 1.1.1, cryptography 43.0.3, waitress 3.0.0, pytest 8.3.3. *(PIANO 3b)*
47. **docker-compose**: healthcheck `mysqladmin ping -h 127.0.0.1` (durante l'inizializzazione MySQL non ascolta su TCP, quindi
    "sano" solo a fine init); volume `db_dati`; nginx ascolta sulla 80 del container; `./app/whoswho/static` montata in sola
    lettura in `/srv/whoswho/static`; nginx passa `Host` con la porta (`$http_host`) così i redirect tengono la porta 8001;
    `expires 1h` sui file statici (attenzione: dopo un cambio di CSS il browser può tenere quello vecchio per un'ora).
48. **`crea-db-test.sh`** usa il client `mysql` come root via socket; serve fine riga LF (aggiunto `.gitattributes`).
49. **Messaggi dopo aggiungi/elimina**: schema POST → redirect alla scheda con `?esito=aggiunta|doppia|eliminata|...#relazioni`
    (niente sessioni/flash di Flask, così non serve una chiave segreta). In caso di errore il modulo `<details>` resta aperto.
50. **`pytest.ini`** con `pythonpath = .` e senza cache (la cartella `app` è montata dal PC); `PYTHONDONTWRITEBYTECODE=1`.
51. **Sorgenti LinkedIn / eventi del prof** ("oggi vuoti"): file con solo la spiegazione e una funzione `leggi()` che dà
    `NotImplementedError`. La lettura del JSON sta in `sorgenti/esempio.py` (PIANO la chiama "esempio.py ora"). *(HANDOFF; PIANO sez. 4)*
52. **`strumenti/misura_c34.py`**: PIANO dice "Chrome senza finestra" e "cornice larga 390 px" ma non come leggere i numeri.
    *Deciso:* un piccolo server HTTP locale temporaneo serve una pagina con una `<iframe>` (la cornice) della dimensione voluta;
    Chrome `--headless=new --dump-dom` la carica e uno script scrive le misure nella pagina. Ho scoperto che Chrome headless non
    stringe la finestra sotto ~500 px (uno screenshot diretto a 390 px risulta tagliato), il che spiega perché il piano parla di
    cornice. In più del piano controllo a 390 px anche Home, Persone, Eventi, risultati e una scheda vera
    (SPEC C34 dice "nessuna pagina scorre di lato").
53. **CSS aggiunto rispetto alla bozza**: `color-scheme: light` in `:root`, variabili `--tasto-alto/--tasto-basso` (da PIANO 4c),
    colori per i messaggi (verde per conferma, rosso per errore: `--avviso`, `--avviso-testo`, `--errore`, controllati da C29),
    `overflow-wrap` sui nomi lunghi, `minmax(0, 1fr)` nella griglia dei 4 riquadri, risultati con `min(300px, 100%)` per non
    sforare a 390 px.

## F. Metodo (CLAUDE.md) — cosa non ho potuto seguire alla lettera

54. **Domande all'utente e approvazioni**: impossibili in questo esperimento; ogni scelta "sul cosa" è in questo file.
55. **"Test prima del codice, i nuovi devono fallire"**: ho scritto codice e test nella stessa sessione, senza mostrare prima
    i test rossi. Al posto di questo ho fatto il passo 6 (rompere apposta le regole): ogni rottura è stata scoperta dai test
    (C8, C22, C27, C21/C5, C26, C20, C16/C17, C29), poi ho ripristinato il codice.
56. **C35 e C38 [a vista]**: ho confrontato io gli screenshot della scheda vera con la bozza a 1366×650 (praticamente uguali);
    manca l'approvazione dell'utente.
