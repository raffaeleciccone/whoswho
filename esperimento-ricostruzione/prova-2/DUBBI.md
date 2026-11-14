# DUBBI — ricostruzione di Who's Who dai soli documenti

Ogni voce dice: **cosa mancava, era ambiguo o contraddittorio**, **cosa ho deciso**, **dove** (documento e sezione).
Ho diviso le voci in: contraddizioni, decisioni sul COSA (comportamento visibile), decisioni sul COME (tecniche),
scostamenti dal metodo di lavoro. Le voci sono numerate per poterle citare.

## A. Contraddizioni o riferimenti a cose che non esistono

1. **C17 contro C24 sui dati di esempio.** C17 dice "nella scheda di Bianchi, Successiva porta a Esposito";
   C24 dice che "éboli" sta tra Bianchi ed Esposito. Le due frasi non possono valere sugli stessi dati.
   *Deciso:* C17 è testato su un insieme di persone senza "éboli", C24 su uno con "éboli". I dati di esempio
   (`dati/esempio.json`) contengono Giulia Éboli (per far vedere C24) e Sara Colombo, quindi nell'app vera
   la Successiva di Bianchi è Colombo, non Esposito. *Dove:* SPEC sez. 5, C17 e C24.
2. **Porte.** I documenti dicono 8000 (app) e 3307 (MySQL). Per l'esperimento servono 8001 e 3308.
   *Deciso:* le porte vengono da `HOST_APP_PORT` / `HOST_MYSQL_PORT` (PIANO 3b); `.env.example` tiene
   8000/3307 come da documenti, il mio `.env` usa 8001/3308. Dentro il container l'app ascolta sempre su 8000.
   (HANDOFF "Da decidere" cita già 8001/3308 per la versione ricostruita.) *Dove:* PIANO 1 e 3b, CLAUDE.md "Comandi".
3. **Cartella `esperimento-ricostruzione/`** citata da SPEC (C18-C24), CLAUDE.md e README ma non presente.
   *Deciso:* non l'ho creata (non ho il suo contenuto). *Dove:* SPEC sez. 5, README "Esperimento", CLAUDE.md "Regole".
4. **"Specifiche e skill conservate in file .md"**: la skill `spec-coding` non è nella cartella (HANDOFF dice che sta
   in `~/.claude/skills/`). *Deciso:* non creata. *Dove:* SPEC sez. 6, HANDOFF.
5. **HANDOFF dice "37 test".** Ne ho 36 (contando ogni caso parametrizzato): un test per criterio C1-C24 più alcuni
   in più (C1 a pezzi e nome+cognome, C3 vuoto e "oggi", C9 senza inizio, C13 comando/data non valida,
   C16 ×2, C17 ×2, C18 ×3, formato file). Non so come erano divisi i 37 originali. *Dove:* HANDOFF "Stato".
6. **PIANO 4b dice che Precedente/Successiva è "calcolata con una query".** *Deciso:* una query prende tutte le persone
   nell'ordine della pagina Persone e la posizione si trova in Python (più semplice e sicuro con la collation;
   va bene finché le persone sono poche centinaia). *Dove:* PIANO 4b.

## B. Decisioni sul COSA (comportamento che l'utente vede) — andrebbero confermate

7. **Ricerca per nome con più parole (F1).** "nome e/o cognome" non dice come trattare "Mario Rossi".
   *Deciso:* ogni parola scritta deve comparire (anche a pezzi) nel nome o nel cognome; quindi "mario rossi",
   "rossi mario" e "Mar" funzionano. `%` e `_` scritti dall'utente valgono come lettere. *Dove:* SPEC F1.
8. **Ricerca vuota.** Non specificato. *Deciso:* messaggio "Scrivi qualcosa da cercare." (non "Nessun risultato").
   Tipo di ricerca sconosciuto → "Tipo di ricerca sconosciuto."; evento inesistente → "Evento non trovato.". *Dove:* SPEC F1/F5, C2.
9. **Messaggio di C2.** La spec dice "nessun risultato": ho scritto "Nessun risultato." (il test non guarda le maiuscole). *Dove:* C2.
10. **Come si "sceglie" un evento (F5).** La barra (F8) ha solo nome/azienda/skill. *Deciso:* l'evento si sceglie
    cliccandolo nella pagina Eventi, negli ultimi eventi della Home o nella scheda; nessun menu a tendina. *Dove:* SPEC F5, F8.
11. **Cosa mostrano i risultati.** Non specificato. *Deciso:* "Cognome Nome · professione" con link alla scheda;
    per la ricerca per evento anche la nota di quell'incontro. Per la ricerca per azienda non mostro quale azienda/periodo. *Dove:* SPEC F1-F5.
12. **"nessuno" per le sezioni vuote (C3).** Ho usato "nessuno" anche per le skill (in italiano sarebbe "nessuna"),
    per le tre sezioni di persone collegate e per gli ultimi eventi della Home. *Dove:* SPEC C3.
13. **Formato del periodo delle aziende (C3).** Non specificato. *Deciso:* "gen 2019 – giu 2022"; senza fine "– oggi";
    senza inizio "?". Le date degli eventi come 10/05/2026, senza data "data sconosciuta". *Dove:* SPEC C3.
14. **Ordine dentro la scheda.** Non specificato. *Deciso:* eventi dal più recente; esperienze prima quelle in corso, poi per
    fine decrescente; skill in ordine alfabetico; colleghi/stesso evento in ordine alfabetico, con accanto l'azienda o
    l'evento in comune (una riga per persona anche se in comune ce ne sono più). *Dove:* SPEC F2, F6.
15. **Eventi senza data nella pagina Eventi (C16 "dal più recente").** *Deciso:* in fondo; a parità di data per nome. *Dove:* C16.
16. **Home.** README dice "spiegazione e ultimi eventi" senza dire quanti. *Deciso:* breve spiegazione + 5 eventi più recenti. *Dove:* README "Le pagine".
17. **Foto.** Nessuna indicazione su cosa mostrare senza foto, né foto per gli esempi. *Deciso:* se c'è l'URL mostro
    l'immagine; altrimenti un cerchio con le iniziali. Nei dati di esempio **nessuna foto** (non volevo usare
    facce di persone reali da siti di avatar). *Dove:* SPEC F2, CLAUDE.md "Persone di esempio solo inventate".
18. **Come si sceglie l'altra persona di un collegamento (F7).** Non specificato. *Deciso:* nella scheda, menu con tutte
    le altre persone (ordine alfabetico) + casella descrizione + "Aggiungi collegamento". *Dove:* SPEC F7, PIANO 3b (indirizzi).
19. **Regole del collegamento non scritte.** *Deciso:* descrizione obbligatoria ("Scrivi una descrizione del collegamento."),
    massimo 300 caratteri, niente collegamento di una persona con se stessa ("Non puoi collegare una persona a se stessa.").
    Messaggi "Collegamento aggiunto." / "Collegamento eliminato.". Cancellazione con richiesta di conferma del browser. *Dove:* SPEC F7.
20. **Come appare il collegamento nelle due schede.** La descrizione è testo libero ("Mario è il capo di Luca") e non ha
    un verso. *Deciso:* in tutte e due le schede appare "altra persona · descrizione". *Dove:* SPEC F6/F7, C11.
21. **Doppione di collegamento (C22).** La spec dice "maiuscole non contano". *Deciso:* anche spazi in testa/coda/doppi e
    **accenti** non contano (effetto della collation `ai_ci`): "Mario e il capo di Luca" = "Mario è il capo di Luca". *Dove:* PIANO 3 "Collegamenti a mano", C22.
22. **Accenti in aziende e skill.** PIANO dice "maiuscole non contano"; con la collation scelta anche gli accenti non contano
    ("Datapiù" = "Datapiu", skill "Python" = "Pythön"). Ho lasciato così, è coerente con PIANO 3 (collation). *Dove:* PIANO 3.
23. **"← Indietro" senza pagina precedente.** Non c'è un modo perfetto per saperlo. *Deciso:* se `history.length > 1` e
    `document.referrer` non è vuoto → `history.back()`, altrimenti va alla Home. *Dove:* PIANO 4b.
24. **Precedente/Successiva**: oltre al link mostro tra parentesi il nome della persona prima/dopo. *Dove:* SPEC F8.
25. **Persona inesistente** (`/persona/999`): pagina "Pagina non trovata" con la barra, codice 404. Non specificato. *Dove:* PIANO 3b.
26. **Resoconto dell'import: cosa vuol dire "importate"** (persone nuove o anche quelle aggiornate?).
    *Deciso:* "Persone importate: N (nuove: X, aggiornate: Y)", poi scartate con motivo, poi avvisi. *Dove:* PIANO 2, SPEC D7.
27. **Reimport e nome/cognome (D6).** "I campi presenti aggiornano quelli vecchi": l'ho applicato anche a nome e cognome,
    quindi se il secondo dato scrive "mario ROSSI" la scheda mostrerà "mario ROSSI". *Dove:* PIANO 3 "Reimport".
28. **Reimport ed esperienze (D6).** La stessa esperienza è persona+azienda+ruolo+inizio; se il nuovo dato ha una data di
    fine diversa, la aggiorno (una fine vuota non cancella quella vecchia). Ruolo mancante = ruolo vuoto per il confronto.
    Luogo dell'evento e nota dell'incontro: aggiornati se presenti. *Dove:* PIANO 3, D6.
29. **Date di sola annata come fine.** PIANO dice "AAAA → 1 gennaio" anche per la fine: "fine 2022" diventa 1/1/2022, quindi
    Mario 2019-2022 e Luca dal 2022-03 **non** risultano colleghi. Ho seguito il PIANO alla lettera, ma probabilmente per la
    fine sarebbe più giusto il 31 dicembre. Non controllo che inizio ≤ fine. Gli estremi contano (fine A = inizio B → colleghi).
    *Dove:* PIANO 2 "Date", PIANO 3 "Colleghi", C7-C8.
30. **Profili "uguali".** PIANO dice "senza maiuscole e senza / finale". Non tratto http/https, "www.", parametri `?...`:
    due URL diversi solo in questo sono due persone diverse. *Dove:* PIANO 3 "Stessa persona".
31. **Dato senza profilo e un solo omonimo che ha il profilo** → è lui (come scritto in PIANO 3). Con più omonimi senza
    profilo (non può succedere grazie alla `chiave` unica) prenderei il primo. *Dove:* PIANO 3.
32. **Dati di esempio senza errori.** Il file di esempio non contiene persone sbagliate (all'avvio il resoconto è pulito);
    i casi di errore stanno nei test. Le persone e le aziende sono inventate tranne "Accenture", citata dalla spec. *Dove:* CLAUDE.md, PIANO 4.

## C. Decisioni sul COME (tecniche)

33. **Versioni esatte delle librerie** ("in `app/requirements.txt`", ma il file non c'era): Flask 3.1.0, PyMySQL 1.1.1,
    cryptography 44.0.0, waitress 3.0.2, pytest 8.3.4; immagini `python:3.12-slim` e `mysql:8.4`. *Dove:* PIANO 3b.
34. **Password e valori di `.env.example`**: inventati (`cambiami_root`, `cambiami`). *Dove:* PIANO 3b.
35. **Variabili non elencate**: l'app usa anche `DB_HOST` (=`db`) e `DB_PORT` (=3306), impostate in `docker-compose.yml`.
    `SECRET_KEY` (serve a Flask per i messaggi dopo un redirect) non è nell'elenco: se manca viene generata a caso all'avvio. *Dove:* PIANO 3b.
36. **Healthcheck di MySQL**: non specificato. `mysqladmin ping -h 127.0.0.1` (via TCP, così non risulta "pronto" durante
    l'inizializzazione, quando MySQL accetta solo il socket); in più `db.py` riprova la connessione per 60 secondi. *Dove:* PIANO 1.
37. **`db/crea-db-test.sh`**: contenuto non scritto. Crea `whoswho_test` (utf8mb4, `utf8mb4_0900_ai_ci`) e dà tutti i permessi
    a `MYSQL_USER`. Salvato con fine riga LF (con CRLF Windows lo script non funzionerebbe nel container). *Dove:* PIANO 3b.
38. **Collation**: impostata sia sul server (`--collation-server`) sia su ogni tabella e sulla connessione (`SET NAMES`). *Dove:* PIANO 3.
39. **Lunghezza dei campi** non specificata: nome/cognome 100, professione 200, URL 500, aziende 200, skill 100,
    descrizione collegamento 300. Un testo più lungo fa scartare quella persona (errore del database riportato nel resoconto),
    non viene troncato. *Dove:* PIANO 3.
40. **"Unico per nome+data" degli eventi e unicità delle esperienze**: un UNIQUE di MySQL non funziona con le date NULL,
    quindi il controllo è nel codice (`<=>`), non nel database. *Dove:* PIANO 3.
41. **Come i test usano `whoswho_test`**: `conftest.py` sostituisce `MYSQL_DATABASE` con `MYSQL_TEST_DATABASE` prima di importare
    il codice; prima di ogni test cancella e ricrea tutte le tabelle. *Dove:* PIANO 5.
42. **Isolamento delle transazioni nei test**: la connessione del test non vedeva i collegamenti scritti dalla pagina web
    (un'altra connessione) per via di REPEATABLE READ di MySQL. Nei test la connessione usa READ COMMITTED.
    Nell'app non serve, perché ogni richiesta apre una connessione nuova (PIANO 3b). *Dove:* PIANO 3b "Salvataggi", PIANO 5.
43. **Un errore imprevisto durante l'import di una persona**: rollback solo di quella persona, che finisce tra le scartate;
    le altre continuano (C13). File JSON non valido, o oggetto senza chiave `"persone"`: messaggio di errore e niente importato.
    Elementi che non sono oggetti → scartati; `esperienze`/`skill`/`eventi` che non sono liste → avviso. Accetto anche date
    scritte come numero (2019) e file con BOM. *Dove:* PIANO 2.
44. **"Spazi doppi si tolgono da tutti i testi"**: applicato anche a URL di foto e profilo. *Dove:* PIANO 2.
45. **Comando di avvio**: CLAUDE.md/PIANO dicono che `avvio.py` ha i comandi "avvia, importa" ma non la sintassi di avvia.
    *Deciso:* `python -m whoswho.avvio avvia` (è il CMD del Dockerfile): crea le tabelle, carica l'esempio se
    `CARICA_ESEMPIO=1` e la tabella persone è vuota, poi avvia waitress su 0.0.0.0:8000. Anche `importa` crea le tabelle se mancano. *Dove:* PIANO 4.
46. **File in più non elencati in PIANO 4**: `templates/_persone.html` (pezzo di elenco riusato), `templates/non_trovata.html`,
    `app/pytest.ini`, `app/.dockerignore`, `.gitignore`, `whoswho/__init__.py`, `sorgenti/__init__.py`. *Dove:* PIANO 4.
47. **`sorgenti/linkedin.py` e `sorgenti/eventi_prof.py`**: lasciati vuoti (solo un commento), come dice HANDOFF; nessuno
    scraper LinkedIn (CLAUDE.md). `sorgenti/esempio.py` legge il file di esempio. *Dove:* HANDOFF, CLAUDE.md, PIANO 6.
48. **Modulo inviato con caratteri non UTF-8** (es. `curl -d` da Git Bash con lettere accentate): Flask non legge il modulo e
    compare "Scegli la persona da collegare.". I browser mandano sempre UTF-8, quindi l'ho lasciato così.

## D. Scostamenti dal metodo di lavoro di CLAUDE.md (dovuti all'esperimento)

49. **Domande e approvazioni**: CLAUDE.md chiede di fare domande all'utente, fargli approvare la spec, aprirgli i file nel
    Blocco note e il programma nel browser. Nell'esperimento non c'è l'utente: ho deciso da solo e scritto qui le scelte.
50. **"Test prima del codice, i nuovi devono fallire"**: ho scritto i test insieme al codice e non li ho visti fallire prima.
    In compenso ho fatto il passo 6 (rompere apposta una regola): togliendo il controllo del periodo (C8) e quello dei doppioni
    (C22) i rispettivi test falliscono; poi ho ripristinato e tutti passano. Due test erano sbagliati al primo giro
    (C11: la frase cercata compariva anche come esempio nella casella; C11/C22: problema di transazioni, voce 42), non il codice.
51. **Documentazione**: non ho toccato SPEC, PIANO, README, HANDOFF, CLAUDE.md (regola dell'esperimento), quindi le scelte qui
    sopra non sono riportate in PIANO.md come CLAUDE.md chiederebbe.
