"""Comandi del programma.

    python -m whoswho.avvio avvia              crea le tabelle, (se vuoto) carica l'esempio, avvia il sito
    python -m whoswho.avvio importa FILE.json  importa persone da un file nel formato della porta d'ingresso
    python -m whoswho.avvio scheda-tipica      stampa la scheda della persona tipica di C34 (database dei test)
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


PERSONA_TIPICA = [  # SPEC C34: 1 evento, 2 lavori, 4 skill, 1 relazione, 3 colleghi, 2 conosciuti allo stesso evento
    {"nome": "Mario", "cognome": "Rossi", "professione": "Data Engineer",
     "esperienze": [{"azienda": "Nexa Data", "ruolo": "Senior Data Engineer", "inizio": "2022-07"},
                    {"azienda": "Accenture", "ruolo": "Consultant", "inizio": "2019-01", "fine": "2022-06"}],
     "skill": ["Python", "SQL", "Docker", "Airflow"],
     "eventi": [{"nome": "Data Summit 2026", "data": "2026-05-10", "luogo": "Milano",
                 "note": "Parlato di pipeline dati e dbt"}]},
    {"nome": "Luca", "cognome": "Bianchi", "esperienze": [{"azienda": "Accenture", "inizio": "2021-03", "fine": "2024-01"}]},
    {"nome": "Giulia", "cognome": "Esposito", "esperienze": [{"azienda": "Nexa Data", "inizio": "2023-01"}],
     "eventi": [{"nome": "Data Summit 2026", "data": "2026-05-10"}]},
    {"nome": "Maria", "cognome": "Romano", "esperienze": [{"azienda": "Nexa Data", "inizio": "2021-10"}],
     "eventi": [{"nome": "Data Summit 2026", "data": "2026-05-10"}]},
]


def scheda_tipica() -> None:
    """Stampa l'HTML della scheda della persona tipica di C34, costruita nel database dei TEST
    (i dati veri non vengono toccati). Lo usa strumenti/misura_c34.py."""
    from . import ricerche
    from .web import crea_app
    db_test = os.environ.get("MYSQL_TEST_DATABASE", "whoswho_test")
    conn = db.connetti(db_test)
    db.crea_tabelle(conn)
    db.svuota(conn)
    importa_persone(conn, PERSONA_TIPICA)
    ids = {r["cognome"]: r["id"] for r in ricerche.elenco_persone(conn)}
    ricerche.aggiungi_collegamento(conn, ids["Rossi"], ids["Bianchi"], "Mario è il capo di Luca")
    conn.close()
    client = crea_app(db_test).test_client()
    sys.stdout.write(client.get(f"/persona/{ids['Rossi']}").get_data(as_text=True))


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else "avvia"
    if comando == "avvia":
        avvia()
    elif comando == "importa" and len(sys.argv) == 3:
        importa_file(sys.argv[2])
    elif comando == "scheda-tipica":
        scheda_tipica()
    else:
        print(__doc__)
        sys.exit(1)
