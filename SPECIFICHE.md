# Who's Who - Specifiche di Progetto e Architettura

Questo documento contiene le specifiche funzionali, il modello dei dati, la tassonomia delle skill e l'architettura tecnica del progetto **Who's Who**.

---

## 1. Obiettivo del Progetto
Costruire un'applicazione in **Python** containerizzata con **Docker** e supportata da un database relazionale **MySQL** (su container separato), capace di:
1. Raccogliere dati anagrafici e professionali tramite **web scraping** in Python.
2. Memorizzare e normalizzare persone, aziende, competenze (skill tecniche) ed eventi d'incontro.
3. Creare ed estrarre **relazioni professionali** tra le persone (es. colleghi nella stessa azienda, collaborazioni, partecipazioni agli stessi eventi).

---

## 2. Architettura di Sistema (Docker)

L'architettura è suddivisa in due container orchestrati con `docker-compose`:

```
+-------------------------------------------------------+
|                    DOCKER COMPOSE                     |
|                                                       |
|  +---------------------+     +---------------------+  |
|  |  Servizio: app      |     |  Servizio: db       |  |
|  |  (Python 3.11/3.12) | --> |  (MySQL 8.x)        |  |
|  |  - Web Scraping     |     |  - Volume dati      |  |
|  |  - Ingestione Dati  |     |  - Healthcheck      |  |
|  |  - Motore Relazioni |     |  - Schema relazionale| |
|  +---------------------+     +---------------------+  |
+-------------------------------------------------------+
```

---

## 3. Modello dei Dati (Entità e Relazioni)

### 3.1 Entità Principali

#### A. Persona (`persone`)
* `id` (INT, PK, Auto Increment)
* `nome` (VARCHAR)
* `cognome` (VARCHAR)
* `foto` (VARCHAR / TEXT - URL o percorso file locale)
* `professione` (VARCHAR - es. "Senior Data Engineer", "Full-Stack Dev")
* `skill_tecniche` (JSON - campo JSON nativo MySQL con l'albero/lista delle skill)
* `created_at`, `updated_at` (TIMESTAMP)

#### B. Azienda (`aziende`)
* `id` (INT, PK, Auto Increment)
* `nome` (VARCHAR, UNIQUE)
* `settore` (VARCHAR, facoltativo)
* `sito_web` (VARCHAR, facoltativo)

#### C. Skill Tecnica (`skills`)
* `id` (INT, PK, Auto Increment)
* `nome` (VARCHAR, UNIQUE - es. Python, Docker, MySQL, FastAPI, PyTorch)
* `categoria` (VARCHAR - es. Backend, DevOps, Data Science, Frontend)

#### D. Evento (`eventi`)
* `id` (INT, PK, Auto Increment)
* `nome` (VARCHAR - es. "PyCon Italia 2024", "Meetup DevOps Milano")
* `data` (DATE / DATETIME)
* `luogo` (VARCHAR)
* `descrizione` (TEXT)

---

### 3.2 Tabelle Ponte e Relazioni

#### 1. Persone - Aziende (`esperienze_lavorative`)
Mappa lo storico lavorativo di ogni persona:
* `id` (INT, PK)
* `persona_id` (FK -> `persone.id`)
* `azienda_id` (FK -> `aziende.id`)
* `ruolo` (VARCHAR)
* `data_inizio` (DATE)
* `data_fine` (DATE, NULL se attuale)
* `attuale` (BOOLEAN)

#### 2. Skill Tecniche (Direttamente in `persone.skill_tecniche`)
Le competenze sono memorizzate direttamente nel campo **`JSON`** della tabella `persone` (vedi Sezione 5), evitando complessità di join per le skill e garantendo massima flessibilità durante lo scraping.

#### 3. Persone - Eventi (`persona_evento`)
Traccia gli incontri con le persone:
* `persona_id` (FK -> `persone.id`)
* `evento_id` (FK -> `eventi.id`)
* `note_incontro` (TEXT - dettagli su di cosa si è parlato o contesto dell'incontro)

#### 4. Relazioni Professionali tra Persone (`relazioni_professionali`)
Definisce i collegamenti diretti e indiretti:
* `id` (INT, PK)
* `persona_a_id` (FK -> `persone.id`)
* `persona_b_id` (FK -> `persone.id`)
* `tipo_relazione` (VARCHAR - es. "Collega", "Responsabile", "Collaboratore", "Ex-collega", "Co-speaker")
* `azienda_id` (FK -> `aziende.id`, facoltativo)
* `note` (TEXT)

> **Inferenziazione Automatica**: il sistema potrà calcolare in automatico relazioni di tipo *Collega* se due persone hanno lavorato nella stessa azienda in periodi sovrapposti, oppure *Partecipante allo stesso evento*.

---

## 4. Pipeline Dati & Scraping

1. **Scraper Python**:
   * Moduli modulari per estrarre informazioni da fonti definite.
   * Gestione del download/salvataggio delle foto profilo (cartella `media/` montata in volume).
2. **Parser & Normalizzatore**:
   * Pulizia delle stringhe (skill duplicate, normalizzazione nomi aziende).
3. **Caricamento DB (Upsert)**:
   * Inserimento idempotente (evita duplicati su scraping ripetuti).
4. **Graph / Relation Builder**:
   * Algoritmo che calcola e aggiorna la matrice delle relazioni professionali.

---

## 5. Struttura e Tassonomia del Campo JSON `skill_tecniche`

Il campo `skill_tecniche` nella tabella `persone` sfrutta il tipo nativo **JSON** di MySQL. Questo consente flessibilità nell'ingestione tramite scraping e facilita la correlazione.

### 5.1 Struttura del JSON
Possiamo memorizzare le skill raggruppate per macro-categoria oppure come lista strutturata.

**Esempio di struttura consigliata (categorizzata):**
```json
{
  "languages": ["Python", "SQL", "JavaScript", "Bash"],
  "frameworks": ["FastAPI", "Flask", "Django"],
  "databases": ["MySQL", "Redis", "PostgreSQL"],
  "devops_cloud": ["Docker", "Docker Compose", "Git", "Linux"],
  "data_tools": ["Pandas", "BeautifulSoup", "Selenium", "Playwright"]
}
```

**Oppure struttura con livello/esperienza:**
```json
[
  {"name": "Python", "category": "Backend", "level": "Senior"},
  {"name": "Docker", "category": "DevOps", "level": "Mid"},
  {"name": "MySQL", "category": "Database", "level": "Senior"}
]
```

### 5.2 Vantaggi con MySQL 8.x:
- **Query native**: Possibilità di usare funzioni come `JSON_CONTAINS()`, `JSON_EXTRACT()`, `JSON_SEARCH()`.
- **Intersezione e Relazioni**: L'applicazione Python può calcolare istantaneamente l'intersezione tra le skill di due profili per trovare affinità tecniche e sinergie professionali.

---

## 6. Prossimi Passi
- [x] Definizione campo JSON per skill tecniche.
- [ ] Ricezione lista skill specifiche o formato scraper preferito.
- [ ] Creazione del `docker-compose.yml` e configurazione MySQL.
- [ ] Creazione del `Dockerfile` e `requirements.txt` per il servizio Python.
- [ ] Implementazione modelli SQLAlchemy / script DDL per creazione tabelle.
- [ ] Implementazione modulo scraper e logica di correlazione professionale.
