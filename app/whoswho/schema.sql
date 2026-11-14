-- Who's Who: tabelle. Il perché di ogni scelta è in PIANO.md sezione 3.

CREATE TABLE IF NOT EXISTS persone (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    chiave       VARCHAR(500) NOT NULL UNIQUE,   -- profilo_url, oppure "nome cognome" (C12)
    nome         VARCHAR(100) NOT NULL,
    cognome      VARCHAR(100) NOT NULL,
    foto         VARCHAR(1000),
    professione  VARCHAR(200),
    profilo_url  VARCHAR(500),
    creato_il    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aggiornato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS aziende (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    nome  VARCHAR(200) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS esperienze (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    persona_id  INT NOT NULL,
    azienda_id  INT NOT NULL,
    ruolo       VARCHAR(200) NOT NULL DEFAULT '',
    inizio      DATE,
    fine        DATE,                              -- NULL = ci lavora ancora (C9)
    UNIQUE KEY esperienza_unica (persona_id, azienda_id, ruolo, inizio),
    FOREIGN KEY (persona_id) REFERENCES persone(id) ON DELETE CASCADE,
    FOREIGN KEY (azienda_id) REFERENCES aziende(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS skill (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    nome  VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS persona_skill (
    persona_id  INT NOT NULL,
    skill_id    INT NOT NULL,
    PRIMARY KEY (persona_id, skill_id),
    FOREIGN KEY (persona_id) REFERENCES persone(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skill(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS eventi (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nome   VARCHAR(200) NOT NULL,
    data   DATE,
    luogo  VARCHAR(200),
    UNIQUE KEY evento_unico (nome, data)
);

CREATE TABLE IF NOT EXISTS persona_evento (
    persona_id  INT NOT NULL,
    evento_id   INT NOT NULL,
    note        TEXT,
    PRIMARY KEY (persona_id, evento_id),
    FOREIGN KEY (persona_id) REFERENCES persone(id) ON DELETE CASCADE,
    FOREIGN KEY (evento_id) REFERENCES eventi(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS collegamenti (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    persona_a_id INT NOT NULL,
    persona_b_id INT NOT NULL,
    descrizione  VARCHAR(500) NOT NULL,
    creato_il    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (persona_a_id) REFERENCES persone(id) ON DELETE CASCADE,
    FOREIGN KEY (persona_b_id) REFERENCES persone(id) ON DELETE CASCADE
);
