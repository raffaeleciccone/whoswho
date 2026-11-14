"""Comandi del programma.

    python -m whoswho.avvio avvia              crea le tabelle, (se vuoto) carica l'esempio, avvia il sito
    python -m whoswho.avvio importa FILE.json  importa persone da un file nel formato della porta d'ingresso
"""
import os
import sys

from . import db
from .importa import importa_persone
from .sorgenti import file_json

ESEMPIO = "/dati/esempio.json"


def stampa_resoconto(res) -> None:
    print(f"Importate: {res.importate}")
    for s in res.scartate:
        print(f"  SCARTATA  {s}")
    for a in res.avvisi:
        print(f"  avviso    {a}")


def importa_file(percorso: str) -> None:
    conn = db.connetti()
    db.crea_tabelle(conn)
    stampa_resoconto(importa_persone(conn, file_json.leggi(percorso)))
    conn.close()


def avvia() -> None:
    conn = db.connetti()
    db.crea_tabelle(conn)
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS n FROM persone")
        vuoto = cur.fetchone()["n"] == 0
    if vuoto and os.environ.get("CARICA_ESEMPIO") == "1" and os.path.exists(ESEMPIO):
        print("Database vuoto: carico i dati di esempio")
        stampa_resoconto(importa_persone(conn, file_json.leggi(ESEMPIO)))
    conn.close()

    from waitress import serve
    from .web import crea_app
    print("Who's Who pronto su http://localhost:" + os.environ.get("HOST_APP_PORT", "8000"))
    serve(crea_app(), host="0.0.0.0", port=8000)


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else "avvia"
    if comando == "avvia":
        avvia()
    elif comando == "importa" and len(sys.argv) == 3:
        importa_file(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
