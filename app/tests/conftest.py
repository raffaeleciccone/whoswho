"""Ogni test parte da un database vuoto (whoswho_test, mai quello vero)."""
import os

import pytest

from whoswho import db

DB_TEST = os.environ.get("MYSQL_TEST_DATABASE", "whoswho_test")


@pytest.fixture
def conn():
    c = db.connetti(DB_TEST)
    db.crea_tabelle(c)
    db.svuota(c)
    yield c
    c.close()


@pytest.fixture
def client_per():
    """Client della pagina web collegato al database di test."""
    from whoswho.web import crea_app

    def _client(_conn):
        app = crea_app(DB_TEST)
        app.testing = True
        return app.test_client()
    return _client


def persona(nome, cognome, esperienze=(), skill=(), eventi=(), **altro):
    """Scorciatoia per costruire una persona nel formato della porta d'ingresso."""
    return {"nome": nome, "cognome": cognome, "esperienze": list(esperienze),
            "skill": list(skill), "eventi": list(eventi), **altro}


def esp(azienda, inizio, fine=None, ruolo=""):
    return {"azienda": azienda, "inizio": inizio, "fine": fine, "ruolo": ruolo}


def nomi(righe):
    return [f"{r['nome']} {r['cognome']}" for r in righe]
