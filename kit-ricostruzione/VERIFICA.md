# Verifica della versione ricostruita

I comandi `docker compose ...` si danno dalla cartella `progetto/`, dove l'assistente ha ricostruito il
programma. Sostituisci `8000` con la porta usata, se l'hai cambiata.
I risultati attesi sono stati controllati sulla versione originale, con i dati di
[dati-di-prova/esempio.json](dati-di-prova/esempio.json) (persone inventate).

## 1. Funziona?
- [ ] `docker compose run --rm app pytest -q` → tutti i test passano
- [ ] il sito si apre nel browser
- [ ] ci sono tre container: `docker compose ps` mostra web (nginx), app, db

## 2. La prova decisiva: i nostri dati entrano?

Copia `dati-di-prova/esempio.json` nella cartella `progetto/dati/` e importalo con il comando del README (di solito `docker compose run --rm app python -m whoswho.avvio importa /dati/esempio.json`;
in Git Bash su Windows metti `MSYS_NO_PATHCONV=1` davanti).

- [ ] le 7 persone entrano senza modificare il file
- [ ] "Mario Rossi" non risulta duplicato (se c'era già nei suoi dati di esempio)
- [ ] importando una seconda volta lo stesso file non si crea nessuna persona in più (C12)

Se qualcosa fallisce: quale documento non diceva abbastanza?

## 3. La misura C34

Dalla cartella del kit (quella che contiene `progetto/`), con il programma acceso:

```
python misura_c34.py
```

Se hai cambiato porta: `python misura_c34.py progetto 8001`.

- [ ] "C34: RISPETTATO" (la nostra versione: la scheda finisce a 579 px su 650)
- [ ] se dice che manca il comando `scheda-tipica`: la versione ricostruita non ha seguito PIANO sez. 4c

## 4. I criteri della spec, controllati a mano con i nostri dati

| Criterio | Prova | Risultato atteso |
|---|---|---|
| C1 | cerca per nome `rossi` | Andrea Rossi, Mario Rossi |
| C1 | cerca per nome `Mar` | Marco Ricci, Maria Romano, Mario Rossi |
| C27 | cerca per nome `mar ros` | solo Mario Rossi |
| C2 | cerca per nome `zzz` | "Nessun risultato.", nessun errore |
| C28 | premi Cerca senza scrivere niente | "Scrivi qualcosa da cercare." |
| C3 | scheda di Sara Conti | eventi, lavori, skill, relazioni, colleghi: "nessuno" |
| C4 | cerca azienda `accenture` | Luca Bianchi, Giulia Esposito, Mario Rossi |
| C21 | cerca azienda `accent` | come sopra (l'azienda si trova anche a pezzi) |
| C5 | cerca skill ` DOCKER ` | Luca Bianchi, Andrea Rossi, Mario Rossi |
| C21 | cerca skill `Java` | solo Marco Ricci (la skill va scritta intera) |
| C6 | evento "Data Summit 2026" | Giulia Esposito, Maria Romano, Mario Rossi |
| C7 | scheda di Mario Rossi → colleghi | Luca Bianchi (Accenture), Giulia Esposito e Maria Romano (Nexa Data) |
| C8 | scheda di Giulia Esposito → colleghi | **non** Luca Bianchi (Accenture in anni diversi) |
| C9 | scheda di Marco Ricci → colleghi | Luca Bianchi (Orbita Cloud: tutti e due ci lavorano ancora) |
| C10 | scheda di Marco Ricci → stesso evento | Luca Bianchi (Meetup DevOps Napoli) |
| C11 | aggiungi la relazione "Mario è il capo di Luca" | compare in tutte e due le schede |
| C22 | aggiungila una seconda volta | "Relazione già presente." |
| C36 | premi Elimina | chiede "Eliminare la relazione con Luca Bianchi?"; Annulla → resta; OK → sparisce da tutte e due le schede |
| C12 | importa due volte lo stesso file | nessuna persona in più |
| C14 | apri Home, Persone, Eventi, una ricerca, una scheda | barra con Home, Persone, Eventi e ricerca su tutte |
| C15 | stesse pagine | "Indietro" ovunque tranne la Home |
| C16 | pagina Persone | ordine alfabetico per cognome |
| C17 | scheda di Luca Bianchi → Successiva | Sara Conti (e nessun "Precedente": è il primo) |
| C31 | metti il PC in tema scuro e ricarica | la pagina resta chiara |
| C35 | confronta la scheda di Mario Rossi con `design/bozza.html` | stessa disposizione: testata con persone collegate a destra, 4 riquadri in una riga |
