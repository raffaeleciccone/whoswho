# DUBBI — cosa mancava, era ambiguo o contraddittorio nei documenti

Ricostruzione fatta leggendo solo SPEC.md, PIANO.md, CLAUDE.md, README.md e HANDOFF.md.
Per ogni voce: **cosa** mancava o era ambiguo · **cosa ho deciso** · **dove** (documento/sezione).

## A. Infrastruttura (Docker, porte, configurazione)

1. **Porte.** I documenti dicono ovunque `http://localhost:8000` e non dicono se MySQL è esposto sull'host
   né su quale porta (la 3307 la so solo dalle istruzioni dell'esperimento, non dai documenti).
   **Deciso:** porte in `.env` (`APP_PORT`, `DB_PORT`); `.env.example` tiene 8000/3307 come nei documenti,
   il `.env` di questo PC usa 8001/3308. Dentro il container l'app ascolta sempre sulla 8000.
   *(PIANO sez. 1, CLAUDE.md "Comandi", README "Avvio")*
2. **Contenuto di `.env.example`.** Si dice solo "password e porte". Nomi delle variabili inventati:
   `MYSQL_ROOT_PASSWORD`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `APP_PORT`, `DB_PORT`; password di esempio inventate.
   *(PIANO sez. 4)*
3. **Nome del database e dell'utente MySQL.** Non indicati. **Deciso:** database `whoswho`, utente `whoswho`
   (dedotto dal nome `whoswho_test` del database dei test). *(PIANO sez. 5)*
4. **Come entra `dati/esempio.json` nel container.** Il `Dockerfile` sta in `app/`, ma il file di esempio sta
   fuori da `app/` e deve essere caricato "al primo avvio" (README); il comando di import di CLAUDE.md monta
   `dati/` a mano, quindi di base non è montato. **Deciso:** contesto di build = cartella del progetto,
   `dockerfile: app/Dockerfile`, e il file di esempio viene copiato nell'immagine in `/app/dati/esempio.json`.
   *(PIANO sez. 4, README "Avvio", CLAUDE.md "Comandi")*
5. **Come e quando gira `db/crea-db-test.sh`.** Non detto. **Deciso:** montato in
   `/docker-entrypoint-initdb.d/` dell'immagine MySQL. Limite: gira solo quando il volume dei dati è vuoto
   (primo avvio); se il volume esiste già da prima, il database dei test va creato a mano.
   *(PIANO sez. 4 e 5)*
6. **Healthcheck del db.** Si dice solo "healthcheck". **Deciso:** `mysqladmin ping` via TCP su 127.0.0.1
   (così non risulta "pronto" durante l'inizializzazione), e in più l'app riprova la connessione per ~60 s.
   *(PIANO sez. 1)*
7. **Librerie e versioni.** Indicati solo Python 3.12, Flask, MySQL 8.4 e (solo in CLAUDE.md) waitress.
   **Deciso:** driver PyMySQL (+ `cryptography`, necessaria per l'autenticazione di default di MySQL 8.4),
   pytest; versioni fissate in `requirements.txt` scelte da me. *(PIANO sez. 1, CLAUDE.md "Comandi")*
8. **`.gitignore`.** CLAUDE.md dice "`.env` è già in `.gitignore`", ma il file non c'era. L'ho creato.
   Aggiunto anche `.gitattributes` (gli script `.sh` devono avere fine riga LF per girare nel container Linux),
   `.dockerignore` e `app/pytest.ini` (serve per far trovare il pacchetto `whoswho` ai test): non citati.
   *(CLAUDE.md "Git")*
9. **Comando di import da Git Bash.** Il comando di CLAUDE.md/README (`-v "$PWD/dati:/dati" ... /dati/file.json`)
   in Git Bash su Windows non funziona così com'è: Git Bash trasforma `/dati/...` in un percorso Windows.
   Serve `MSYS_NO_PATHCONV=1` davanti (provato). I documenti non lo dicono. *(CLAUDE.md "Comandi", README "Importare dati")*

## B. Database e "porta d'ingresso" (import)

10. **Tipi e lunghezze delle colonne, nomi delle colonne di collegamento** (`persona_id`, `azienda_id`,
    `persona_a`, `persona_b`...): non specificati, scelti da me. *(PIANO sez. 3)*
11. **Formato della colonna `chiave` delle persone.** Si dice solo "`chiave` unica". **Deciso:**
    `url:<profilo_url in minuscolo, senza / finale>` se c'è il profilo, altrimenti `nome:<nome>|<cognome>` in minuscolo.
    Conseguenza della collation `ai_ci`: "Mario Rossi" e "Màrio Rossi" sono considerati la stessa persona.
    *(PIANO sez. 3, "Doppioni")*
12. **Caso non coperto dei doppioni:** una persona importata prima senza `profilo_url` e poi con `profilo_url`
    (o viceversa) diventa due persone, perché le chiavi sono diverse. La regola del PIANO non dice cosa fare;
    ho lasciato così. Al contrario, due omonimi con profili diversi restano giustamente due persone.
    *(PIANO sez. 3, "Doppioni"; SPEC C12)*
13. **Cosa succede a un secondo import della stessa persona.** Non detto se aggiornare o ignorare.
    **Deciso:** si aggiornano nome/cognome e i campi non vuoti (un campo vuoto non cancella quello vecchio);
    esperienze, skill ed eventi si aggiungono senza doppioni; ciò che è sparito dalla fonte **non** viene cancellato.
    Un'esperienza è "la stessa" se ha stessa persona + azienda + ruolo + data di inizio (la data di fine si aggiorna).
    *(SPEC C12, PIANO sez. 3)*
14. **Evento senza data.** Il formato mostra sempre la data, ma non dice se è obbligatoria. **Deciso:**
    facoltativa; l'unicità nome+data vale anche senza data (colonna calcolata `data_chiave`).
    Il luogo di un evento già esistente si riempie solo se mancava. *(PIANO sez. 2 e 3)*
15. **Formato delle date.** Il formato unico usa `AAAA-MM-GG`, ma i criteri ragionano in anni ("Accenture 2019-2022").
    **Deciso:** accetto anche `AAAA` e `AAAA-MM` (inizio = primo giorno, fine = ultimo giorno del periodo).
    Una data non valida viene lasciata vuota e segnalata come avviso, senza scartare la persona.
    *(PIANO sez. 2; SPEC C7-C9)*
16. **C13 "segnalato": dove?** Non detto. **Deciso:** nel resoconto dell'import, stampato dal comando
    `importa` e nei log dell'app al primo avvio. Non esiste una pagina web di import. Contano come mancanti
    anche nome/cognome fatti solo di spazi; viene scartato (e segnalato) anche un elemento che non è un oggetto JSON.
    *(SPEC C13, PIANO sez. 3 "Dati incompleti")*
17. **Altri dati incompleti non previsti** (esperienza senza azienda, evento senza nome): la spec parla solo
    di persone senza nome/cognome. **Deciso:** si ignora solo quella voce, con un avviso; la persona viene importata.
    *(SPEC C13)*
18. **Pulizia dei testi in ingresso.** Oltre agli spazi in testa/coda (C5) tolgo anche gli spazi doppi interni.
    Skill e aziende scritte con maiuscole diverse ("docker"/"Docker") diventano una sola voce, e resta la grafia
    vista per prima. "Accenture" e "Accenture Italia" invece restano due aziende diverse (quindi non colleghi).
    *(PIANO sez. 3)*
19. **Collegamenti a mano nei dati di esempio.** Il formato unico non li prevede (D3: si scrivono solo a mano),
    quindi l'esempio non ne contiene. *(PIANO sez. 2, SPEC 3b D3)*

## C. Ricerche e pagine

20. **F1 "nome e/o cognome".** **Deciso:** il testo (anche a pezzi) si cerca in nome, cognome,
    "nome cognome" e "cognome nome". Nota: "Mar" trova Marco e Maria come chiede la spec, ma anche Mario.
    I caratteri `%` e `_` sono trattati come lettere normali. Una ricerca vuota dà "nessun risultato".
    *(SPEC F1, C1, C2)*
21. **F3 e F4: corrispondenza parziale o esatta?** La spec dice "anche a pezzi" solo per il nome.
    **Deciso:** azienda **a pezzi** (i nomi delle aziende cambiano: "Accenture" trova anche "Accenture Italia");
    skill **esatta** (ignorando maiuscole, accenti e spazi), altrimenti cercando "R" o "C" uscirebbe quasi tutti.
    *(SPEC F3, F4, C4, C5)*
22. **Indirizzo della ricerca per evento (F5).** Il README elenca solo `/cerca` per i risultati.
    **Deciso:** `/cerca?tipo=evento&id=<id>`; la casella in alto offre solo Nome/Azienda/Skill (come F8 e README),
    l'evento si sceglie dalla pagina Eventi, dalla Home o dalla scheda. *(SPEC F5, F8; README "Le pagine")*
23. **Scheda: dettagli non specificati.** Il periodo è mostrato come "gen 2019 – giu 2022", con "oggi" se manca
    la fine e "?" se manca l'inizio; senza foto si mostrano le iniziali; senza professione "Professione non indicata";
    il link al profilo si mostra se c'è `profilo_url`; le note dell'evento sono mostrate. Anche le tre sezioni delle
    persone collegate scrivono "nessuno" quando sono vuote (C3 lo chiede solo per eventi/aziende/skill).
    Accanto a ogni persona collegata mostro l'azienda o l'evento in comune. *(SPEC F2, F6, C3)*
24. **Collegamenti a mano (F7): direzione e controlli.** La descrizione è testo libero ("Mario è il capo di Luca"),
    salvata una volta sola e mostrata uguale in entrambe le schede, accanto al nome dell'altra persona.
    Rifiutati: descrizione vuota e collegamento con se stessi. Due collegamenti uguali sono ammessi.
    La cancellazione chiede conferma nel browser. Non si possono modificare (la spec dice solo aggiungere/cancellare).
    *(SPEC F7, C11; PIANO sez. 3)*
25. **"← Indietro".** Il PIANO dice "se si è arrivati da un link diretto porta alla Home". **Deciso:**
    se `history.length > 1` torna indietro nella cronologia, altrimenti va alla Home. È un'approssimazione
    (in una scheda nuova del browser funziona; in casi particolari può tornare a una pagina di un altro sito).
    *(PIANO sez. 4b)*
26. **Ordine alfabetico.** Per via della collation `ai_ci`, l'ordine ignora maiuscole e accenti ("Ávila" prima
    di "Bianchi"); a parità di cognome e nome decide l'id (come dice il PIANO). Eventi senza data in fondo,
    a parità di data in ordine di nome. *(SPEC C16, C17; PIANO sez. 4b)*
27. **Home "spiegazione e ultimi eventi".** Quanti eventi non è detto: **5**, più il numero di persone.
    La pagina Persone mostra "Cognome Nome" (coerente con l'ordine). *(README "Le pagine")*
28. **Pagine che non esistono** (persona o evento con id sbagliato): non previsto. **Deciso:** pagina
    "Pagina non trovata." con codice 404, sempre con la barra. *(non coperto)*
29. **Messaggi dopo aggiungi/cancella collegamento.** Non previsti; mostro un breve messaggio ("Collegamento
    aggiunto.") con i messaggi flash di Flask, che richiedono una chiave segreta (generata a caso a ogni avvio se
    non è nel `.env`). *(SPEC F7)*

## D. Test, dati di esempio, metodo

30. **Numero di test.** HANDOFF dice 27 test; non c'è l'elenco, quindi i test sono riscritti da zero:
    ne ho **28** (21 in `test_criteri.py` per C1-C13, 7 in `test_navigazione.py` per C14-C17), ognuno col
    criterio nel nome. Il numero diverso non indica un problema. *(HANDOFF "Stato", PIANO sez. 5)*
31. **Contraddizione README / HANDOFF.** Il README dice "criteri per dire che funziona (C1-C13)", ma la SPEC
    e l'HANDOFF arrivano a C17 (F8 aggiunta il 14/11): il README non è stato aggiornato. Ho seguito la SPEC (C1-C17).
    I file .md esistenti non li ho toccati, come richiesto. *(README intro vs SPEC sez. 5, HANDOFF)*
32. **Dati di esempio.** Contenuto e numero di persone non indicati. Ho inventato 7 persone (Bianchi, Esposito,
    Ferrari, Greco, Giulia e Mario Rossi, Romano), 6 aziende, 3 eventi. Ho fatto in modo che: ci siano più Rossi (C1),
    Marco e Maria (F1), Mario Rossi in Accenture 2019-2022 e Luca Bianchi 2021-2024 (C7), Maria Greco in Accenture
    2015-2017 (C8), qualcuno ancora al lavoro (C9), una persona senza eventi/aziende/skill (C3 "nessuno"), e che dopo
    Bianchi venga subito Esposito (C17 cita proprio "Bianchi → Esposito", quindi ho dedotto che fossero nei dati di
    esempio). Nessuna foto (per non inventare URL); due persone hanno un `profilo_url` di finto LinkedIn.
    *(CLAUDE.md "Regole", SPEC C17)*
33. **Isolamento dei test.** Il database `whoswho_test` viene svuotato prima di ogni test; il nome arriva dalla
    variabile `DB_TEST_NAME` (inventata). *(PIANO sez. 5)*
34. **`sorgenti/linkedin.py` e `eventi_prof.py`** "oggi vuoti" (HANDOFF): creati con solo un commento che spiega
    cosa manca. Nessuno scraper scritto, come chiede CLAUDE.md. C'è `sorgenti/esempio.py` che legge un JSON già
    nel formato unico. *(HANDOFF, PIANO sez. 4, CLAUDE.md "Regole")*
35. **Metodo di CLAUDE.md non applicabile per intero.** Approvazione della spec, test mostrati "rossi" prima del
    codice e apertura del browser all'utente non si potevano fare (utente non disponibile, codice ricostruito tutto
    insieme). Ho fatto invece la verifica "rompi la regola": tolta la condizione di sovrapposizione dei periodi,
    il test C8 fallisce; ripristinata, passano tutti. *(CLAUDE.md "Come si lavora", punti 2, 4, 6, 7)*
36. **Un dettaglio tecnico non documentato ma necessario:** le connessioni al database sono in autocommit
    (l'import usa una transazione esplicita, tutto o niente). Senza, una pagina aperta poteva non vedere
    un collegamento appena aggiunto da un'altra connessione. *(non coperto)*
