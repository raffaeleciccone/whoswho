# Who's Who — SPEC (cosa e perché)

> Questo file dice COSA deve fare il programma, non COME.
> Il "come" (tabelle, Docker, codice) sta in PIANO.md.
> Stato: APPROVATA il 14/11/2026, tranne la sezione 3b (fonti dati) che aspetta il prof (lunedì).

## 1. Problema
Conosco molte persone (a eventi, al lavoro) e poi non ricordo chi sono:
dove le ho incontrate, dove hanno lavorato, cosa sanno fare.

## 2. Uso principale
- U1. Cerco una persona per nome e vedo la sua "scheda".

## 3. Cosa fa
- F1. Ricerca per nome: scrivo nome e/o cognome (anche solo un pezzo: "Mar" trova Marco e Maria), il programma mi mostra le persone che corrispondono.
- F2. Scheda persona: per una persona mostra
  - nome, cognome, foto, professione
  - dove l'ho incontrata (eventi)
  - dove ha lavorato (aziende)
  - cosa sa fare (skill tecniche)
- F3. Ricerca per azienda: scrivo un'azienda, vedo chi ci ha lavorato.
- F4. Ricerca per skill: scrivo una skill, vedo chi la sa fare.
- F5. Ricerca per evento: scelgo un evento, vedo chi ho incontrato lì.
- Da ogni risultato di ricerca (F1, F3, F4, F5) posso aprire la scheda (F2).
- F6. Persone collegate: nella scheda (F2) vedo le persone collegate, divise per tipo:
  - Colleghi: hanno lavorato nella stessa azienda in periodi che si sovrappongono (calcolato dal programma)
  - Conosciuti allo stesso evento: li ho incontrati allo stesso evento (calcolato dal programma)
  - Collegamenti a mano: scritti da me, con una descrizione (es. "Mario è il capo di Luca")
- F7. Posso aggiungere e cancellare un collegamento a mano tra due persone.
- F8. Navigazione (aggiunta 14/11 su richiesta): su ogni pagina c'è una barra in alto con
  - "Home", "Persone" (elenco di tutte), "Eventi" (elenco di tutti)
  - la casella di ricerca (nome / azienda / skill), così cerco da qualsiasi pagina
  - "← Indietro" su tutte le pagine tranne la Home
  - nella scheda: "‹ Precedente" e "Successiva ›" per scorrere le persone in ordine alfabetico

## 3b. Da dove arrivano i dati (ipotesi, da confermare col prof)
- D1. Persone (nome, foto, professione, aziende, skill): da LinkedIn.
- D2. Eventi e chi c'era (partecipanti/speaker): dal sito eventi del prof.
- D3. Collegamenti a mano: li scrivo io (F7).

## 4. Cosa NON fa
- Non considera colleghi due persone che hanno lavorato nella stessa azienda in anni diversi.
- Non gestisce utenti/login: lo usa una persona sola.
- Non manda messaggi né contatta le persone.
- Non modifica a mano i dati delle persone (arrivano dall'import); a mano si gestiscono solo i collegamenti (F7).

## 5. Criteri di controllo
Ogni criterio diventa un test automatico. "Finito" = tutti i test passano.

- C1 (F1). Cerco "rossi": escono tutte le persone con cognome Rossi; maiuscole/minuscole non contano.
- C2 (F1). Cerco un nome che non c'è: messaggio "nessun risultato", nessun errore.
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
- C13 (D1/D2). Un dato in ingresso senza nome o cognome viene scartato e segnalato, senza bloccare il resto.
- C14 (F8). Home, Persone, Eventi, risultati e scheda hanno tutte la barra con Home, Persone, Eventi e la casella di ricerca.
- C15 (F8). "← Indietro" c'è su tutte le pagine tranne la Home.
- C16 (F8). Persone: elenca tutte le persone in ordine alfabetico (cognome, nome). Eventi: elenca tutti gli eventi, dal più recente.
- C17 (F8). Nella scheda di Bianchi, "Successiva" porta a Esposito (la persona dopo in ordine alfabetico);
  la prima persona non ha "Precedente", l'ultima non ha "Successiva".

## 6. Vincoli (richiesti dal prof)
- Python
- MySQL
- Programma e database in due container Docker separati
- I dati delle persone arrivano da scraping fatto in Python
- Specifiche e skill conservate in file .md
- Si usa da una pagina web semplice aperta nel browser (deciso 14/11)

## 7. Domande aperte
- Lo scopo l'ha deciso il prof: va chiesto a lui se l'uso principale è giusto?
- LinkedIn: scraping diretto (vietato dai termini LinkedIn, blocchi anti-bot, dati personali/GDPR)
  oppure import del CSV dei collegamenti che LinkedIn fa scaricare? (il CSV però non ha foto né skill)
- Il prof ha parlato di CSV? Se sì: CSV di cosa e con quali colonne?
- Sito eventi del prof: quale indirizzo? Mostra la lista partecipanti/speaker? Si può esportare in CSV?
