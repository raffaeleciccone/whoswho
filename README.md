# 👥 Who's Who - Professional Network & Relation Graph

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker)](https://www.docker.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1.svg?logo=mysql)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Applicazione containerizzata in **Python** e **MySQL** per la raccolta, gestione e correlazione di profili professionali, esperienze lavorative, competenze tecniche ed eventi di incontro.

I dati vengono acquisiti tramite moduli di **web scraping** e memorizzati in un database relazionale, con supporto a campi **JSON** per le competenze tecniche e un motore di inferenza per le **relazioni professionali**.

---

## 🏛️ Architettura di Sistema

Il progetto è suddiviso in due container Docker distinti e orchestrati con **Docker Compose**:

```
+-------------------------------------------------------------------+
|                          DOCKER COMPOSE                           |
|                                                                   |
|   +-----------------------+           +-----------------------+   |
|   |   Container: app      |           |   Container: db       |   |
|   |   (Python 3.11)       | --------> |   (MySQL 8.0)         |   |
|   |                       |  Network  |                       |   |
|   |   - Web Scraping      |           |   - Persistenza Dati  |   |
|   |   - Parsing Dati      |           |   - Schema SQL        |   |
|   |   - Motore Relazioni  |           |   - Healthcheck       |   |
|   +-----------------------+           +-----------------------+   |
|               |                                   |               |
|               v                                   v               |
|      Volume Locale (Codice)              Volume Docker (Dati)     |
+-------------------------------------------------------------------+
```

---

## 📂 Struttura Attuale del Progetto

```text
whoswho/
├── .env.example             # Template configurazione variabili d'ambiente
├── .gitignore               # Regole di esclusione Git (sicurezza per credenziali e cache)
├── README.md                # Documentazione del progetto
└── SPECIFICHE.md            # Specifiche dettagliate dei dati, entità e campo JSON skill
```

I componenti applicativi (`docker-compose.yml`, `Dockerfile`, script di scraping e modelli) verranno implementati step-by-step partendo dalle specifiche.

---

## 🚀 Avvio Rapido

### 1. Prerequisiti
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installato e avviato.
* [Git](https://git-scm.com/) installato.

### 2. Configurazione
Crea il tuo file `.env` a partire dal template di esempio:

```bash
cp .env.example .env
```
*(Su Windows PowerShell: `Copy-Item .env.example .env`)*

Se necessario, modifica password e credenziali all'interno del file `.env`.

### 3. Avvio con Docker Compose
Esegui il comando di build e avvio:

```bash
docker compose up --build
```

Il sistema:
1. Avvierà il container **MySQL** e attenderà che sia pronto (healthcheck).
2. Avvierà il container **Python**, si connetterà al DB e creerà automaticamente tutte le tabelle.
3. Eseguirà il test dimostrativo con inserimento dati e stampa a video.

Per arrestare i container:
```bash
docker compose down
```

Per cancellare anche i volumi dati:
```bash
docker compose down -v
```

---

## 📊 Modello dei Dati

Le entità principali mappate nel database sono:
- **`persone`**: Dati anagrafici, professione, foto e campo nativo `skill_tecniche` (JSON).
- **`aziende`**: Aziende e organizzazioni.
- **`esperienze_lavorative`**: Storico lavorativo (relazione molti-a-molti con date e ruoli).
- **`eventi`**: Conferenze, meetup o occasioni d'incontro.
- **`persona_evento`**: Dettagli su dove e come si è incontrata ogni persona.
- **`relazioni_professionali`**: Collegamenti diretti o inferiti tra persone (colleghi, collaborazioni).

Tutti i dettagli approfonditi sono consultabili in [SPECIFICHE.md](SPECIFICHE.md).

---

## 📤 Come Pubblicare la Cartella su GitHub

Se desideri pubblicare questo progetto su GitHub come repository autonoma:

```bash
# 1. Posizionati nella cartella del progetto
cd whoswho

# 2. Inizializza la repository Git (se non già presente)
git init

# 3. Aggiungi tutti i file e fai il primo commit
git add .
git commit -m "feat: initial commit - Dockerized Python & MySQL Who's Who setup"

# 4. Rinomina il branch in main
git branch -M main

# 5. Collega il tuo repository remoto su GitHub (crealo prima su github.com)
git remote add origin https://github.com/<TUO-UTENTE-GITHUB>/<NOME-REPO>.git

# 6. Effettua il push
git push -u origin main
```

---

## 📄 Licenza

Progetto rilasciato per scopi didattici e di sviluppo open-source.
