# Who's Who — domande per il prof

Sono le domande aperte di SPEC.md (sezione 7). Le risposte servono per scrivere l'unica parte che manca:
da dove arrivano i dati. Tutto il resto del programma è già fatto e funziona con dati di prova.

Scrivi le risposte qui sotto (anche a parole, anche "non lo so").

---

**1. Lo scopo**
Ho capito che il programma serve a ritrovare una persona (per nome, azienda, skill o evento) e vedere
dove l'ho incontrata, dove ha lavorato, cosa sa fare e con chi è collegata. È quello che intendeva?

Risposta: _______________________________________________

**2. LinkedIn: scraping o file scaricato?**
Lo scraping di LinkedIn è vietato dai suoi termini d'uso (rischio blocco dell'account) e riguarda dati
personali di altre persone (GDPR). L'alternativa è il file CSV dei collegamenti che LinkedIn fa scaricare
(Impostazioni → Privacy dei dati → Ottieni una copia dei tuoi dati), che però contiene solo nome, cognome,
link al profilo, azienda e ruolo attuali: niente foto, niente skill, niente aziende passate.
Quale strada vuole?

Risposta: _______________________________________________

**3. Il CSV**
Ha parlato di un file CSV? Se sì: un CSV di cosa (persone, eventi, partecipanti?) e con quali colonne?
Me ne può dare uno di esempio?

Risposta: _______________________________________________

**4. Il sito degli eventi**
Qual è l'indirizzo del sito dei suoi eventi? Mostra la lista dei partecipanti o degli speaker?
Si può scaricare come file (CSV, Excel)?

Risposta: _______________________________________________

**5. I container**
Ha chiesto programma e database in due container separati. Ho aggiunto un terzo container (nginx)
davanti al programma, come nei siti veri: serve le pagine grafiche e passa il resto al programma Python.
Va bene, o preferisce solo i due container richiesti?

Risposta: _______________________________________________

---

Quando hai le risposte: apri [PROMPT-DOPO-PROF.md](PROMPT-DOPO-PROF.md), incollale nei punti indicati
e manda il prompt all'assistente AI (Claude Code, Antigravity o un altro).
