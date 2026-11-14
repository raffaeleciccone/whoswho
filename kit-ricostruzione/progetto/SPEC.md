# Who's Who — SPEC (cosa e perché)

> Questo file dice COSA deve fare il programma, non COME.
> Il "come" (tabelle, Docker, codice) sta in PIANO.md.
> Stato: APPROVATA il 14/11/2026, aggiornata il 14/11 dopo l'esperimento di ricostruzione
> (C18-C24),
> poi dopo la prova 2 (C25-C28, C17 riscritto). Le fonti dati (sezione 3b, D1-D2) aspettano il prof (lunedì).

## 1. Problema
Conosco molte persone (a eventi, al lavoro) e poi non ricordo chi sono:
dove le ho incontrate, dove hanno lavorato, cosa sanno fare.

## 2. Uso principale
- U1. Cerco una persona per nome e vedo la sua "scheda".

## 3. Cosa fa
- F1. Ricerca per nome: scrivo nome e/o cognome (anche solo un pezzo: "Mar" trova Marco e Maria), il programma mi mostra le persone che corrispondono.
  Con più parole, ognuna deve comparire (anche a pezzi) nel nome o nel cognome, in qualsiasi ordine.
- F2. Scheda persona: per una persona mostra
  - nome, cognome, foto, professione
  - dove l'ho incontrata (eventi)
  - dove ha lavorato (aziende)
  - cosa sa fare (skill tecniche)
- F3. Ricerca per azienda: scrivo un'azienda (anche solo un pezzo: "accent" trova Accenture), vedo chi ci ha lavorato.
- F4. Ricerca per skill: scrivo il nome esatto di una skill, vedo chi la sa fare. Maiuscole e spazi
  non contano, ma "Java" non trova "JavaScript" (sono skill diverse).
- F5. Ricerca per evento: scelgo un evento, vedo chi ho incontrato lì.
- Da ogni risultato di ricerca (F1, F3, F4, F5) posso aprire la scheda (F2).
- F6. Persone collegate: nella scheda (F2) vedo le persone collegate, divise per tipo:
  - Colleghi: hanno lavorato nella stessa azienda in periodi che si sovrappongono (calcolato dal programma)
  - Conosciuti allo stesso evento: li ho incontrati allo stesso evento (calcolato dal programma)
  - Relazioni: scritte da me, con una descrizione (es. "Mario è il capo di Luca")
- F7. Posso aggiungere e cancellare una relazione tra due persone (nell'app si chiamano "Relazioni",
  nome scelto dall'utente il 14/11). La stessa relazione
  (stesse due persone, stessa descrizione) non si può scrivere due volte. Prima di cancellare
  una relazione il programma chiede conferma ("Eliminare la relazione con <nome>?", OK / Annulla).
- F8. Navigazione (aggiunta 14/11 su richiesta): su ogni pagina c'è una barra in alto con
  - "Home", "Persone" (elenco di tutte), "Eventi" (elenco di tutti)
  - la casella di ricerca (nome / azienda / skill), così cerco da qualsiasi pagina
  - il tasto "Indietro" (con la freccia ←) su tutte le pagine tranne la Home
  - nella scheda: i tasti "Precedente: <nome>" e "Successiva: <nome>" (con le frecce, come nella bozza)
    per scorrere le persone in ordine alfabetico

## 3c. Aspetto grafico (F9) — bozza approvata dall'utente il 14/11: design/bozza.html
Chi la vede, in ordine di importanza:
- U2. Il prof, in aula, con l'app proiettata durante la presentazione.
- U3. Il prof sul suo telefono.
- U4. I compagni sul loro PC.

Cosa ne consegue:
- Proiettore: testo grande e molto contrastato, leggibile dal fondo dell'aula; tema sempre chiaro,
  anche se il PC è impostato sul tema scuro (sul proiettore i temi scuri si vedono spenti).
- Telefono: tutto si usa con una mano, niente scorrimento di lato, pulsanti grandi da toccare.

Impressione voluta: seria e pulita, da gestionale professionale. Riferimento di stile: i social
network dei primi anni (es. il primo Facebook): barra colorata in alto, sfondo chiaro, riquadri
con bordo sottile, profilo con foto e informazioni ordinate. È solo un'ispirazione di stile:
niente nomi, loghi o colori di marchi esistenti.

- F9. L'app ha questo aspetto (scelto dall'utente il 14/11):
  - barra in alto di colore pieno **blu notte** (blu scuro tendente al grigio), con testo bianco:
    nome dell'app, Home / Persone / Eventi, ricerca;
  - sfondo chiaro, contenuti in **riquadri** bianchi con bordo sottile e il **titolo su una fascia**
    grigio-azzurra chiara;
  - **scheda persona "testata con persone collegate + riquadri in una riga"** (decisione 1, terza versione,
    scelta dall'utente dopo aver misurato che le altre non stavano in 1366×768): in alto una riga con
    Indietro a sinistra e Precedente/Successiva a destra; poi la testata a tutta larghezza: a sinistra
    foto e dati principali, a destra le persone collegate (colleghi | conosciuti allo stesso evento) come
    miniature; sotto, i 4 riquadri affiancati in una sola riga, con questi titoli: "Dove l'ho incontrato",
    "Dove ha lavorato", "Cosa sa fare", "Relazioni". Su schermi più stretti le persone collegate vanno sotto i dati
    e i riquadri a due a due; sul telefono tutto in una colonna;
  - il modulo per aggiungere una relazione è nascosto e compare premendo "+ Aggiungi relazione" nel
    riquadro "Relazioni";
  - **nella testata** (decisione 2): foto, nome e cognome, professione, dove lavora ora
    (l'azienda dell'esperienza ancora in corso; se non ce n'è, non compare);
    e sotto il nome il link "Profilo online", se c'è;
  - **foto e iniziali quadrate con angoli arrotondati** (decisione 4);
  - **dimensioni medie** (decisione 5): foto della testata 140 px, miniature delle persone collegate 90 px,
    testo 18 px, titoli delle pagine 28 px;
  - **larghezza massima della pagina 1200 px, centrata** (decisione 6);
  - **skill come etichette colorate** (decisione 7): rettangolini pieni blu chiaro con testo blu notte,
    senza bordo, cliccabili;
  - **tonalità grigio-azzurro** (decisione 8): sfondo della pagina grigio-azzurro chiaro, fasce dei titoli
    azzurro-grigio, riquadri bianchi, tutto intonato al blu notte della barra;
  - **tasti** (decisioni tasti 1-3, progettati da noi, niente Bootstrap):
    - principali (Aggiungi): pieni blu notte con leggera sfumatura, bordo più scuro e ombra
      sottile, si "abbassano" quando li premi;
    - Cerca (sulla barra): casella e tasto formano un unico blocco bianco; il tasto è solo una lente blu
      notte sul lato destro (per chi non vede, si chiama comunque "Cerca"); si può anche premere Invio;
    - secondari (Precedente, Successiva, Indietro): a contorno;
    - Elimina: piccolo, a contorno rosso;
    - **icone** semplici disegnate da noi nelle voci della barra (Home, Persone, Eventi) e nei tasti
      (lente su Cerca, + su Aggiungi, X su Elimina, frecce su Precedente/Successiva);
  - **persone collegate come griglia di foto** con il nome sotto (le iniziali se la foto manca);
  - testo grande, leggibile sul proiettore.

## 3b. Da dove arrivano i dati (ipotesi, da confermare col prof)
- D1. Persone (nome, foto, professione, aziende, skill): da LinkedIn.
- D2. Eventi e chi c'era (partecipanti/speaker): dal sito eventi del prof.
- D3. Relazioni: le scrivo io (F7).

Regole valide per qualsiasi fonte:
- D4. Stessa persona: due persone sono la stessa se hanno lo stesso profilo online (contano solo sito
  e percorso: http/https, "www.", prefissi di lingua come "it.", "/" finale, maiuscole e la parte dopo
  "?" o "#" non contano); oppure se hanno
  stesso nome e cognome e almeno una delle due non ha il profilo. Due profili diversi = due persone
  diverse, anche con lo stesso nome (omonimi).
- D5. Se il nome corrisponde a più persone già presenti con profili diversi e il dato nuovo non ha
  profilo, non si può sapere chi è: il dato viene scartato e segnalato (proposta di Claude).
- D6. Reimportare una persona aggiorna i suoi dati e aggiunge le cose nuove, ma non cancella mai niente.
- D7. "Segnalato" vuol dire: elencato nel resoconto che l'import stampa alla fine (nel terminale).

## 4. Cosa NON fa
- Non considera colleghi due persone che hanno lavorato nella stessa azienda in anni diversi.
- Non gestisce utenti/login: lo usa una persona sola.
- Non manda messaggi né contatta le persone.
- Non modifica a mano i dati delle persone (arrivano dall'import); a mano si gestiscono solo le relazioni (F7).

## 5. Criteri di controllo
Ogni criterio diventa un test automatico. "Finito" = tutti i test passano.
Ogni criterio contiene i suoi dati: non dipende dai dati di esempio né da altri criteri.
[test] = controllato da un test automatico; [misura] = screenshot automatico a una dimensione data; [a vista] = controllato guardando le pagine (screenshot), approvato dall'utente.

- C1 (F1). Cerco "rossi": escono tutte le persone con cognome Rossi; maiuscole/minuscole non contano.
- C2 (F1). Cerco un nome che non c'è: messaggio "Nessun risultato.", nessun errore.
- C3 (F2). La scheda mostra eventi, aziende (con periodo) e skill della persona; se una sezione è vuota scrive "nessuno".
- C4 (F3). Cerco "accenture": escono tutte le persone che ci hanno lavorato, anche in passato.
- C5 (F4). Cerco "docker", "Docker" o " DOCKER ": stesso risultato.
- C6 (F5). Scelgo un evento: escono solo le persone incontrate a quell'evento.
- C7 (F6). Mario in Accenture 2019-2022, Luca in Accenture 2021-2024 → colleghi.
- C8 (F6). Mario in Accenture 2015-2017, Luca in Accenture 2020-2023 → NON colleghi.
- C9 (F6). Chi lavora ancora in un'azienda (nessuna data di fine) conta come "fino a oggi".
- C10 (F6). Mario e Luca allo stesso evento → compaiono l'uno nella scheda dell'altro come "conosciuti allo stesso evento".
- C11 (F7). Aggiungo "Mario è il capo di Luca" → compare in entrambe le schede; lo cancello → sparisce da entrambe.
- C12 (D1/D2). Importo due volte gli stessi dati: nessuna persona, azienda o evento duplicato.
- C13 (D1/D2). Un dato in ingresso senza nome o cognome viene scartato e segnalato nel resoconto dell'import (D7), senza bloccare il resto.
- C14 (F8). Home, Persone, Eventi, risultati e scheda hanno tutte la barra con Home, Persone, Eventi e la casella di ricerca.
- C15 (F8). Il tasto "Indietro" c'è su tutte le pagine tranne la Home.
- C16 (F8). Persone: elenca tutte le persone in ordine alfabetico (cognome, nome). Eventi: elenca tutti gli eventi, dal più recente.
- C17 (F8). Con tre persone, Luca Bianchi, Giulia Esposito e Mario Rossi: nella scheda di Bianchi,
  "Successiva" porta a Esposito; Bianchi non ha "Precedente", Rossi non ha "Successiva".

Aggiunti il 14/11 dopo l'esperimento di ricostruzione (vedi esperimento-ricostruzione/):
- C18 (D4). Importo Mario Rossi con profilo, poi Mario Rossi senza profilo (o al contrario): resta una persona sola, con i dati di tutti e due.
- C19 (D4). Importo due Mario Rossi con profili diversi: sono due persone.
- C20 (D5). Ci sono due Mario Rossi con profili diversi e importo un Mario Rossi senza profilo: scartato e segnalato come ambiguo, nessuna persona nuova.
- C21 (F3/F4). Cerco l'azienda "accent": trovo chi ha lavorato in Accenture. Cerco la skill "Java": non trovo chi sa solo JavaScript.
- C22 (F7). Aggiungo due volte "Mario è il capo di Luca" (anche partendo dalla scheda di Luca): la seconda volta messaggio "Relazione già presente.". Con una descrizione diversa invece si può.
- C23 (D6). Reimporto Mario senza skill: le skill che aveva restano.
- C25 (F6). Date incomplete: per l'inizio vale il primo giorno, per la fine l'ultimo. Mario in Accenture
  dal "2019" al "2022", Luca in Accenture da "2022-03" → colleghi. Mario fino a "2022-06", Luca da
  "2022-07" → NON colleghi.
- C26 (D4). Importo Mario Rossi tre volte con questi profili: "https://www.linkedin.com/in/mario-rossi",
  "http://linkedin.com/in/Mario-Rossi/", "https://it.linkedin.com/in/mario-rossi?originalSubdomain=it"
  → una persona sola. Con "https://www.linkedin.com/in/mario-rossi-2" → un'altra persona.
- C27 (F1). Con Mario Rossi e Mario Bianchi: "mar ros", "rossi mario" e "mario ros" trovano solo Mario Rossi;
  "mario" li trova tutti e due (anche "mario r", perché la "r" è anche in "Mario"); "mario verdi" non trova nessuno.
- C28 (F1/F3/F4). Premo "Cerca" senza scrivere niente (o solo spazi): messaggio "Scrivi qualcosa da cercare.",
  non "Nessun risultato".
- C29 (F9) [test]. Tutti i testi hanno un contrasto di almeno 4,5:1 con il loro sfondo (regola WCAG AA),
  compreso il testo bianco sulla barra blu notte.
- C30 (F9) [test]. Il testo normale è di almeno 18 px; i titoli delle pagine di almeno 28 px; i testi secondari
  (date, ruoli, dettagli sotto le miniature) mai sotto i 13,5 px (deciso dall'utente il 14/11, come nella bozza).
- C31 (F9) [test]. Il tema è sempre chiaro: la pagina non cambia colori se il PC usa il tema scuro.
- C32 (F9) [test]. Nella scheda ogni sezione è un riquadro con il titolo sulla fascia; la foto (o le iniziali)
  e i dati principali stanno nella testata, prima dei riquadri; le persone collegate stanno nella testata, a destra
  dei dati (decisione 1, terza versione).
- C33 (F9) [test]. Con Mario Rossi e Luca Bianchi colleghi: nella scheda di Mario, Luca compare nella griglia
  con la sua immagine (foto o iniziali "LB") e il nome sotto, e cliccandolo si apre la sua scheda.
- C34 (F9) [misura]. Una persona "tipica" (1 evento, 2 lavori, 4 skill, 1 relazione, 3 colleghi,
  2 conosciuti allo stesso evento) sta tutta, senza scorrere, in un portatile 1366×768: cioè in una finestra
  del browser di 1366×650 px (circa 110 px li occupa il browser stesso). A 390 px di larghezza (telefono)
  una sola colonna, e nessuna pagina scorre di lato. Si misura con uno screenshot automatico.
- C35 (F9) [a vista]. Il risultato somiglia alla bozza approvata (design/bozza.html) e non contiene nomi,
  loghi o colori di marchi esistenti.
- C36 (F7) [test]. Nella scheda di Mario, che ha una relazione con Luca Bianchi, il tasto Elimina chiede
  "Eliminare la relazione con Luca Bianchi?" prima di cancellare; se annullo, la relazione resta.
- C37 (F9) [test]. Le voci Home, Persone, Eventi e i tasti Cerca, Aggiungi, Elimina, Precedente, Successiva
  hanno ognuno un'icona.
- C38 (F9) [a vista]. I tasti principali hanno sfumatura e rilievo e si abbassano quando premuti; Elimina è a
  contorno rosso; come nella bozza approvata.
- C39 (D7, decisa dall'utente dopo la prova 4). Importo Mario Rossi con un lavoro in Accenture dal "2015" con
  fine scritta male ("2017-13") e Luca Bianchi in Accenture dal "2024": quel lavoro di Mario viene ignorato e
  segnalato nel resoconto; Mario entra lo stesso, ma non risulta collega di Luca.
- C24 (F8). Ordine alfabetico: maiuscole e accenti non contano ("éboli" sta tra "Bianchi" ed "Esposito").

## 6. Vincoli (richiesti dal prof)
- Python
- MySQL
- Programma e database in container Docker separati (richiesta del prof); in più un terzo container
  nginx che serve le pagine e i file grafici e passa il resto al programma Python (scelto dall'utente
  il 14/11, va oltre la richiesta del prof)
- I dati delle persone arrivano da scraping fatto in Python
- Specifiche e skill conservate in file .md
- Si usa da una pagina web semplice aperta nel browser (deciso 14/11)
- Grafica in HTML + CSS scritto da noi, senza librerie grafiche (Bootstrap, Tailwind, React...) (deciso 14/11)
- Strumenti confermati dall'utente il 14/11: Python 3.12 (immagine `python:3.12-slim`), Flask (pagine web),
  PyMySQL (collegamento a MySQL), waitress (server Python), MySQL 8.4 (immagine ufficiale `mysql:8.4`),
  nginx 1.27 (immagine ufficiale `nginx:1.27-alpine`)

## 7. Domande aperte
- Lo scopo l'ha deciso il prof: va chiesto a lui se l'uso principale è giusto?
- LinkedIn: scraping diretto (vietato dai termini LinkedIn, blocchi anti-bot, dati personali/GDPR)
  oppure import del CSV dei collegamenti che LinkedIn fa scaricare? (il CSV però non ha foto né skill)
- Il prof ha parlato di CSV? Se sì: CSV di cosa e con quali colonne?
- Sito eventi del prof: quale indirizzo? Mostra la lista partecipanti/speaker? Si può esportare in CSV?
- Il prof ha chiesto programma e database in due container: va bene il terzo container nginx davanti?
