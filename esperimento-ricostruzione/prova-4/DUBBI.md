# DUBBI — ricostruzione dai soli documenti

Ricostruzione fatta il 14/11/2026 leggendo solo SPEC.md, PIANO.md, AGENTS.md, CLAUDE.md, README.md,
HANDOFF.md e design/bozza.html. Qui sotto, una voce per ogni punto in cui la documentazione mancava,
era ambigua o si contraddiceva, con la decisione presa e dove sta il punto nei documenti.
Le voci sono raggruppate per argomento; quelle marcate **(importante)** possono cambiare il comportamento
visibile o il risultato dei criteri.

## A. Regole dell'esperimento contro istruzioni dei documenti

1. **Porte 8001 / 3308 (importante).** I documenti scrivono 8000 e 3307 in molti punti (AGENTS "Comandi",
   README "Avvio", PIANO sez. 1, 3b, 4c, HANDOFF). Le porte del PC sono già lette da `.env` (PIANO 3b:
   `HOST_APP_PORT`, `HOST_MYSQL_PORT`), quindi ho creato `.env` con 8001 e 3308 e lasciato
   `.env.example` con i valori dei documenti (8000/3307). Niente è scritto fisso nel codice.
2. **`<base href="http://localhost:8000/">` nella scheda tipica (PIANO 4c).** Il piano scrive la porta
   fissa 8000, ma con il sito su 8001 il foglio di stile non si caricherebbe. Deciso: `scheda-tipica`
   usa `HOST_APP_PORT` (passato al container `app` tramite `env_file: .env`); anche `misura_c34.py`
   lo legge da `.env`, come dice il piano.
3. **Container di un'altra copia accesi.** Sul PC girano già `whoswho-web/app/db` su 8000/3307 (HANDOFF
   ne parla). Il nome del progetto Compose non è indicato nei documenti: ho lasciato quello predefinito
   (nome della cartella → `progetto-*`), così non si scontra con l'altra copia.
4. **Metodo by spec (AGENTS "Come si lavora").** Chiede di fare domande una alla volta, far approvare la
   spec, scrivere i test PRIMA del codice e mostrarli rossi, aprire il programma all'utente, aggiornare
   SPEC/PIANO/README/HANDOFF. Nell'esperimento l'utente non c'è e i .md non vanno toccati: niente
   domande, niente modifiche ai documenti; test e codice scritti nella stessa sessione (il primo giro
   di test ha dato 3 rossi, vedi voce 60). Il passo 6 (rompere apposta le regole) l'ho fatto.
5. **Cartelle citate ma non ricostruite.** `incontro-prof/`, `kit-ricostruzione/`, `esperimento-ricostruzione/`
   e `strumenti/aggiorna_kit.py` (AGENTS punto 9, PIANO sez. 4, README "Cosa c'è dentro") riguardano il
   repository originale e cartelle fuori da questa: non li ho creati. Il README quindi cita cose che qui
   non esistono.
6. **`.env` creato da me.** Il README dice di copiarlo da `.env.example`; l'ho creato io per poter avviare.
   Password inventate (`cambiami_root`, `cambiami_utente`): i documenti non danno valori.

## B. Docker, nginx, database (PIANO sez. 1, 3b)

7. **Versioni delle librerie.** PIANO 3b dice "versioni esatte in `app/requirements.txt`" ma non le
   scrive. Scelte: Flask 3.0.3, PyMySQL 1.1.1, cryptography 43.0.3, waitress 3.0.0, pytest 8.3.3.
8. **Healthcheck di MySQL.** Citato (PIANO 1) ma non descritto. Scelto `mysqladmin ping -h 127.0.0.1`
   (via TCP: durante l'inizializzazione MySQL non ascolta in rete, così `app` non parte troppo presto);
   in più `app` riprova a collegarsi fino a 30 volte.
9. **Contenuto di `db/crea-db-test.sh`.** Solo il nome è nei documenti. Inventato: `CREATE DATABASE`
   con utf8mb4_0900_ai_ci + `GRANT ALL` all'utente `MYSQL_USER`. Per avere `MYSQL_TEST_DATABASE` nel
   container `db` gli ho dato anche lui `env_file: .env`.
10. **Configurazione nginx.** Solo "serve /static/ e passa il resto ad app" (PIANO 1). Inventati: cartella
    di montaggio `/usr/share/nginx/static`, `expires 1h`, intestazioni `Host`/`X-Forwarded-*`, porta 80
    interna mappata su `HOST_APP_PORT`.
11. **Avvio di `app`.** Il comando del container (`python -m whoswho.avvio avvia`), 8 thread di waitress,
    il nome del volume (`dati_mysql`) e `restart: unless-stopped` sono scelte mie.
12. **Tipi e lunghezze delle colonne** (VARCHAR 100/200/300/500, DATE, chiavi esterne con
    `ON DELETE CASCADE`): non scritti, scelti da me. La tabella PIANO 3 dà solo i contenuti.
13. **Unicità di eventi ed esperienze.** PIANO 3: eventi "unico per nome+data (anche nessuna data)",
    esperienze "persona + azienda + ruolo + inizio". In MySQL un indice UNIQUE non blocca i doppioni con
    data NULL, quindi il controllo è nel codice (`<=>`), senza indice unico. Il ruolo mancante vale "".
14. **`pytest.ini`** (cartella dei test, `pythonpath = .`) non è citato: serve perché `pytest -q` trovi il
    pacchetto `whoswho`.

## C. Porta d'ingresso / import (PIANO sez. 2 e 3, SPEC D4-D7)

15. **Reimport di un'esperienza già presente (D6).** Non è detto cosa succede alla data di fine.
    Deciso: una fine nuova non vuota aggiorna la vecchia; una fine vuota non cancella quella vecchia
    (quindi non si può "riaprire" un lavoro reimportandolo senza fine).
16. **Data di fine non valida (importante).** PIANO 2: "una data non valida diventa vuota". Ma una fine
    vuota significa "ci lavora ancora" (C9): un errore di battitura rende la persona collega di tutti
    quelli arrivati dopo. Ho seguito il piano alla lettera (con avviso nel resoconto) e lo segnalo come
    possibile contraddizione.
17. **Formato date.** Ho accettato anche mese/giorno di una cifra (`2022-3`); `2022/03` o `03-2022` sono
    "non valide". Non specificato.
18. **Elementi che non sono oggetti JSON** (es. una stringa nella lista persone) e campi `esperienze`,
    `skill`, `eventi` che non sono liste: non previsti. Deciso: persona scartata con motivo / campo
    ignorato con avviso.
19. **Testo del resoconto (D7).** Solo "quante importate, quali scartate e perché, avvisi". Formato
    inventato: "Persone importate: N (nuove X, aggiornate Y)", "Persone scartate: N" con l'elenco
    "#posizione Nome Cognome: motivo", "Avvisi: N". Una persona reimportata conta come "aggiornata"
    anche se non cambia niente.
20. **Stessa persona e accenti.** PIANO 3: per nome+cognome "maiuscole/accenti non contano". Quindi
    "Nicolò Éboli" e "Nicolo Eboli" senza profilo sono la stessa persona. Applicato (collation).
21. **Normalizzazione del profilo (C26).** Seguita alla lettera: si toglie un prefisso di **2 lettere**
    solo se dopo resta un punto (`it.linkedin.com` → `linkedin.com`); `m.linkedin.com` (1 lettera) resta
    diverso. Il link "Profilo online" mostra l'indirizzo originale, non quello normalizzato; a ogni
    reimport con profilo viene sostituito dall'ultima grafia ricevuta.
22. **Caso "dato con profilo + omonimo con un profilo diverso + omonimo senza profilo".** Il piano dice
    "è la persona omonima senza profilo, se c'è": applicato, anche se potrebbe essere l'altro.
23. **Errore su una persona durante l'import.** Ogni persona è salvata in una transazione sua; se va in
    errore viene annullata e finisce tra le scartate con il messaggio dell'errore (non previsto dai
    documenti, deriva da C13 "senza bloccare il resto").
24. **Evento già presente con luogo diverso** e **note diverse** per la stessa persona/evento: vince
    l'ultimo valore non vuoto (estensione di D6).

## D. Ricerche e pagine (SPEC F1-F8, PIANO 3b, 4b)

25. **Skill: "spazi non contano" (F4, C5).** Interpretato come: spazi in testa/coda tolti e spazi doppi
    ridotti a uno. Per via della collation anche gli accenti non contano. Le skill si confrontano con `=`.
26. **Caratteri `%` e `_`** scritti nella ricerca: trattati come caratteri normali (escape nel LIKE).
    Non specificato.
27. **`tipo` sconosciuto in `/cerca`**: si cerca per nome. `tipo=evento` con id inesistente: messaggio
    "Evento non trovato." (inventato).
28. **Titolo della pagina risultati.** Preso dalla bozza ("Skill: “Docker”" + "3 persone"); per nome e
    azienda ho fatto lo stesso ("Nome: “mar”"), per l'evento "Evento: <nome>" con data e luogo sotto.
    Nei risultati sotto il nome c'è sempre la professione (anche nella ricerca per azienda).
29. **Home: "spiegazione e ultimi eventi"** (README). Quanti eventi e quale testo non è detto: 5 eventi,
    testo scritto da me, più il numero totale di persone.
30. **Pagina Eventi.** Solo "elenco dal più recente". Aspetto inventato: riquadri come i risultati con
    icona calendario, data, luogo e numero di persone. Gli eventi senza data vanno in fondo
    ("data sconosciuta").
31. **Indietro (PIANO 4b).** "Se si è arrivati da un link diretto porta alla Home": realizzato con un
    link a `/` che, se `history.length > 1`, fa `history.back()`. È un'approssimazione (in una scheda
    nuova aperta dopo altra navigazione non è perfetto) e richiede JavaScript, mentre il piano evita
    JavaScript per il modulo delle relazioni.
32. **Etichette Precedente/Successiva (contraddizione SPEC/bozza).** SPEC F8 e README scrivono
    "‹ Precedente" e "Successiva ›" (con i caratteri ‹ ›); la bozza approvata e C37 usano icone SVG e il
    nome della persona ("Precedente: Maria Romano"). Ho seguito la bozza (icone + nome).
33. **Voce "Persone" evidenziata nella scheda.** Nella bozza la scheda ha `aria-current` su "Persone":
    l'ho riprodotto (sulla scheda la voce Persone risulta attiva).
34. **"Lavora ora in" con più lavori in corso.** La spec dice "l'azienda dell'esperienza ancora in
    corso" (singolare). Deciso: tutte, separate da virgola, ognuna cliccabile (ricerca per azienda),
    come il link della bozza.
35. **Ordine nella scheda.** Non specificato: esperienze in corso prima, poi per fine più recente
    (come nella bozza); eventi dal più recente; skill in ordine alfabetico; relazioni per nome
    dell'altra persona.
36. **Formati delle date.** Presi dalla bozza: eventi `10/05/2026`, periodi `01/2019 – 06/2022`,
    "oggi" se manca la fine. Inventati: "? – 06/2022" se manca l'inizio, "periodo sconosciuto" se mancano
    entrambe.
37. **Dettaglio sotto le miniature.** Dalla bozza: per i colleghi l'azienda, per i conosciuti l'evento.
    Se sono più di una, le elenco separate da virgola. Una persona che è collega e conosciuta allo
    stesso evento compare in entrambi i gruppi (come nella bozza).
38. **"nessuno" (C3).** C3 lo chiede per le sezioni vuote; l'ho usato anche per i gruppi vuoti della
    striscia (Colleghi, Conosciuti), per le Relazioni e per gli elenchi vuoti.
39. **Pagina 404** per una persona che non esiste: testo inventato, con la barra.

## E. Relazioni (F7, PIANO 4c)

40. **Messaggi non previsti.** Dati: "Relazione aggiunta.", "Relazione eliminata.", "Relazione già
    presente.". Inventati: "Scrivi una descrizione della relazione." (descrizione vuota),
    "Scegli un'altra persona: una relazione è tra due persone diverse." (relazione con se stessi:
    **vietata**, la spec non ne parla), "Scegli una persona dall'elenco.", "Relazione non trovata.".
41. **Come arrivano i messaggi.** Dopo il POST si torna alla scheda (`redirect` con `?msg=codice#relazioni`)
    e il messaggio compare dentro il riquadro "Relazioni". Non specificato.
42. **Doppione (C22).** "Maiuscole non contano"; per via della collation contano poco anche accenti e
    spazi in testa/coda. Descrizione lunga al massimo 300 caratteri (inventato).
43. **Elenco persone nel modulo.** La bozza mostra "Bianchi Luca" (cognome nome): seguito. La persona
    stessa è esclusa dall'elenco. Se non ci sono altre persone il modulo non compare.
44. **Testo della conferma (C36)** con nomi che contengono apostrofi (es. D'Amico): il testo va nel
    JavaScript di `onsubmit`; l'ho codificato in modo sicuro (`tojson`), quindi l'attributo è
    `return confirm("Eliminare la relazione con Luca Bianchi?")` con le virgolette doppie, mentre il piano
    scrive l'esempio con apici singoli.
45. **Elimina via GET.** L'indirizzo di eliminazione accetta solo POST (un GET risponde 405): usato nel
    test di C36. Nessuna protezione CSRF (non richiesta: un solo utente, niente login, SPEC sez. 4).

## F. Grafica (SPEC 3c, PIANO 4c, bozza)

46. **Coppie di colori controllate da C29.** PIANO 4c dice "coppie testo/sfondo controllate da
    test_grafica.py" ma non le elenca. Ho scelto le 17 coppie realmente usate nelle pagine
    (testo/tenue/link/blu notte/bianco/rosso sui rispettivi sfondi). Tutte ≥ 4,5:1 (la più bassa:
    `--tenue` su `--sfondo` 5,63:1). I colori di hover della bozza scritti senza variabile
    (`#f6f8fb`, `#fdf1f0`, `#36557f`, bordo `#e3a59f`) li ho tenuti come nella bozza: controllati a mano
    (≥ 5,9:1), non dal test.
47. **h1.** PIANO dice `h1 { font-size: 28px }`, la bozza `1.56rem` (28,08 px). Usato 28px.
48. **Pulsanti grandi sul telefono (SPEC 3c).** Nessuna misura data e la bozza non ne ha. Deciso: altezza
    minima 44 px per tasti, casella di ricerca e voci della barra **solo sotto i 700 px di larghezza**, così
    il PC resta identico alla bozza e C34 non cambia.
49. **Regole CSS aggiunte rispetto alla bozza** (la bozza copre solo scheda e risultati): messaggi,
    "nessuno" in corsivo grigio, elenco eventi, `img` dentro foto/miniature (`object-fit: cover`), a capo
    delle parole lunghe, `color-scheme: light` anche in `:root`, layout telefono della barra.
50. **Foto vere.** Il formato prevede `foto` come indirizzo: viene mostrata con `<img>` presa da internet.
    Nei dati di esempio non ho messo foto (indirizzi inventati darebbero immagini rotte): compaiono le
    iniziali. Un test (C33) prova comunque il caso con foto.
51. **"Profilo online" e sicurezza.** Il link usa l'indirizzo importato: lo mostro solo se inizia con
    `http://` o `https://` (un `javascript:` da un file importato sarebbe pericoloso). Si apre in una
    nuova scheda. Non previsto dai documenti.
52. **C35 e C38 "a vista, approvato dall'utente".** L'utente non c'è: ho confrontato io screenshot della
    scheda vera con la bozza a 1366 px (stessa disposizione, colori, tasti, icone) e a 500 px (una colonna).
    Non è un'approvazione dell'utente.
53. **C36 "se annullo, la relazione resta".** In pytest non c'è un browser che possa premere "Annulla":
    il test controlla che il modulo abbia la conferma giusta in `onsubmit`, che senza invio del modulo la
    relazione resti e che un GET non cancelli. Non ho provato il clic su "Annulla" in Chrome.

## G. Misura C34 (PIANO 4c)

54. **Dimensione della finestra (importante per la misura).** Con Chrome senza finestra
    `--window-size=1366,650` ha dato un'area utile di 1350×555, non 1366×650. Per misurare alla dimensione
    esatta carico la pagina in una cornice (`iframe`) di 1366×650, come il piano già fa per il telefono
    ("cornice larga 390 px"). Risultato: fondo di `div.quattro` a **579 px** su 650 (lo stesso valore
    scritto in HANDOFF).
55. **Altezza della cornice del telefono** (844 px) e **quali pagine** controllare a 390 px ("nessuna
    pagina scorre di lato"): scelte da me — scheda tipica, Home, Persone, Eventi, risultati, ricerca vuota,
    nessun risultato, una scheda vera. Tutte larghe 390 px su 390.
56. **Dati della persona tipica.** C34 dà solo i numeri (1 evento, 2 lavori, 4 skill, 1 relazione,
    3 colleghi, 2 conosciuti): nomi e testi li ho presi dalla bozza (Mario Rossi, Nexa Data, Accenture,
    Data Summit 2026...). Il comando `scheda-tipica` svuota il database dei test: non va lanciato mentre
    girano i test.
57. **Copia della pagina misurata.** Lo strumento salva `strumenti/misura_c34_scheda_tipica.html` (utile
    per guardarla), messo in `.gitignore`. Non previsto.

## H. Test e dati di esempio

58. **Divisione dei test** come PIANO sez. 5. C24 (che è F8) l'ho messo in `test_esperimento.py` perché
    sta nell'intervallo C18-C28 indicato dal piano. HANDOFF parla di 52 test: i miei sono **59** (C29 è
    un test per ogni coppia di colori: 17 + 1). Il numero non è un obiettivo dei documenti.
59. **Dati nei test.** Entrano dalla porta d'ingresso (`importa_persone`), come i dati veri; il database
    dei test viene svuotato (TRUNCATE) prima di ogni test.
60. **Primo giro dei test: 3 rossi.** Due per un errore del codice (PyMySQL restituisce una tupla vuota
    invece di una lista: le funzioni ora restituiscono sempre liste) e uno per un errore del test (C3
    controllava "nessuno" anche nel riquadro Relazioni, che giustamente era vuoto).
61. **Verifica che i test servano** (AGENTS punto 6): rotte apposta 9 regole (sovrapposizione colleghi,
    doppione relazione, `www.` nel profilo, parole in OR, caso ambiguo, skill "contiene", contrasto,
    testo piccolo, ordine alfabetico): ogni volta almeno un test è diventato rosso; poi ripristinato.
62. **Dati di esempio.** 12 persone inventate; aziende inventate tranne Accenture (usata come esempio
    dalla spec stessa); eventi inventati. I profili usano un dominio finto (`profili.example`) invece di
    linkedin.com, per non puntare a profili di persone vere. C'è "Nicolò Éboli" per mostrare C24.
    Il file usa la forma `{"nota": ..., "persone": [...]}`.
63. **Una relazione rimasta nel database vero.** Provando il programma acceso ho aggiunto "Mario è il
    capo di Luca" (Mario Rossi ↔ Luca Bianchi) e l'ho lasciata come esempio; le relazioni non fanno
    parte dell'import, quindi `esempio.json` non ne contiene.
