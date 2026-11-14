# Verifica della versione ricostruita

Sostituisci `8000` con la porta usata dalla versione ricostruita.

## 1. Funziona?
- [ ] `docker compose run --rm app pytest -q` → tutti i test passano
- [ ] http://localhost:8000 si apre

## 2. La prova decisiva: i nostri dati entrano?

Importa [dati-di-prova/esempio.json](dati-di-prova/esempio.json) nella versione ricostruita
(il comando esatto dipende da come l'ha costruita: guarda il suo README).
In Git Bash su Windows metti `MSYS_NO_PATHCONV=1` davanti al comando.

- [ ] le 7 persone entrano senza modificare il file
- [ ] "Mario Rossi" non risulta duplicato (se c'era già nei suoi dati di esempio)

Se una delle due fallisce: quale documento non diceva abbastanza?

## 3. I criteri della spec, controllati a mano con i nostri dati

| Criterio | Prova | Risultato atteso |
|---|---|---|
| C1 | cerca per nome `rossi` | Andrea Rossi, Mario Rossi |
| C1 | cerca per nome `Mar` | Marco Ricci, Maria Romano, Mario Rossi |
| C2 | cerca per nome `zzz` | "nessun risultato", nessun errore |
| C3 | scheda di Sara Conti | eventi, aziende, skill: "nessuno" |
| C4 | cerca azienda `accenture` | Luca Bianchi, Giulia Esposito, Mario Rossi |
| C5 | cerca skill ` DOCKER ` | Luca Bianchi, Andrea Rossi, Mario Rossi |
| C6 | evento "Data Summit 2026" | Giulia Esposito, Mario Rossi, Maria Romano |
| C7 | scheda di Mario Rossi → colleghi | Luca Bianchi (Accenture), Giulia Esposito e Maria Romano (Nexa Data) |
| C8 | scheda di Giulia Esposito → colleghi | **non** Luca Bianchi (Accenture in anni diversi) |
| C10 | scheda di Marco Ricci → stesso evento | Luca Bianchi (Meetup DevOps Napoli) |
| C9 | scheda di Marco Ricci → colleghi | Luca Bianchi (Orbita Cloud: tutti e due ci lavorano ancora) |
| C11 | aggiungi "Mario è il capo di Luca" | compare in tutte e due le schede; elimina → sparisce da tutte e due |
| C12 | importa due volte lo stesso file | nessuna persona in più |
| C14 | apri Home, Persone, Eventi, una ricerca, una scheda | barra con Home, Persone, Eventi e casella di ricerca su tutte |
| C15 | stesse pagine | "← Indietro" ovunque tranne la Home |
| C16 | pagina Persone | ordine alfabetico per cognome |
| C17 | scheda di Luca Bianchi → Successiva | Sara Conti (e nessun "Precedente": è il primo) |

Le persone sono inventate (vedi `dati-di-prova/esempio.json`).
