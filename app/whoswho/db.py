"""Connessione a MySQL e creazione delle tabelle."""
import os
from pathlib import Path

import pymysql

SCHEMA = Path(__file__).with_name("schema.sql")


def connetti(database: str | None = None) -> pymysql.connections.Connection:
    return pymysql.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=database or os.environ["MYSQL_DATABASE"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def crea_tabelle(conn) -> None:
    istruzioni = [s.strip() for s in SCHEMA.read_text(encoding="utf-8").split(";")]
    with conn.cursor() as cur:
        for sql in istruzioni:
            # toglie le righe di solo commento
            sql = "\n".join(r for r in sql.splitlines() if not r.strip().startswith("--")).strip()
            if sql:
                cur.execute(sql)
    conn.commit()


TABELLE = [
    "collegamenti", "persona_evento", "persona_skill", "esperienze",
    "eventi", "skill", "aziende", "persone",
]


def svuota(conn) -> None:
    """Cancella tutti i dati (usato solo dai test)."""
    with conn.cursor() as cur:
        cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        for t in TABELLE:
            cur.execute(f"TRUNCATE TABLE {t}")
        cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()
