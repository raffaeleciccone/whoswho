"""Test della navigazione: SPEC.md F8, criteri C14-C17."""
import re

import pytest

from whoswho.importa import importa_persone

from .conftest import persona


@pytest.fixture
def sito(conn, client_per):
    """Tre persone e un evento; restituisce il client web e gli id."""
    evento = {"nome": "Data Summit", "data": "2026-05-10"}
    importa_persone(conn, [
        persona("Mario", "Rossi", eventi=[evento]),
        persona("Luca", "Bianchi", eventi=[evento]),
        persona("Giulia", "Esposito"),
    ])
    with conn.cursor() as cur:
        cur.execute("SELECT id, cognome FROM persone")
        ids = {r["cognome"]: r["id"] for r in cur.fetchall()}
        cur.execute("SELECT id FROM eventi")
        evento_id = cur.fetchone()["id"]
    return client_per(conn), ids, evento_id


def _pagine(ids, evento_id):
    return {
        "home": "/",
        "persone": "/persone",
        "eventi": "/eventi",
        "risultati": "/cerca?tipo=nome&q=rossi",
        "risultati evento": f"/cerca?tipo=evento&evento={evento_id}",
        "scheda": f"/persona/{ids['Rossi']}",
    }


def test_c14_barra_su_tutte_le_pagine(sito):
    client, ids, evento_id = sito
    for nome, url in _pagine(ids, evento_id).items():
        html = client.get(url).get_data(as_text=True)
        barra = re.search(r'<nav class="barra[^"]*".*?</nav>', html, re.S)
        assert barra, f"manca la barra in: {nome}"
        b = barra.group(0)
        assert 'href="/"' in b and ">Home<" in b, nome
        assert 'href="/persone"' in b, nome
        assert 'href="/eventi"' in b, nome
        assert 'action="/cerca"' in b and 'name="q"' in b, f"manca la ricerca in: {nome}"


def test_c15_indietro_tranne_home(sito):
    client, ids, evento_id = sito
    for nome, url in _pagine(ids, evento_id).items():
        html = client.get(url).get_data(as_text=True)
        if nome == "home":
            assert "Indietro" not in html
        else:
            assert "← Indietro" in html, f"manca Indietro in: {nome}"


def test_c16_pagina_persone_in_ordine_alfabetico(sito):
    client, _, _ = sito
    html = client.get("/persone").get_data(as_text=True)
    ordine = re.findall(r'<strong>([^<]+)</strong>', html)
    assert ordine == ["Luca Bianchi", "Giulia Esposito", "Mario Rossi"]


def test_c16_pagina_eventi(conn, client_per):
    importa_persone(conn, [persona("Mario", "Rossi", eventi=[
        {"nome": "Vecchio evento", "data": "2024-01-01"},
        {"nome": "Nuovo evento", "data": "2026-01-01"},
    ])])
    html = client_per(conn).get("/eventi").get_data(as_text=True)
    assert html.index("Nuovo evento") < html.index("Vecchio evento")


def _link(html, testo):
    m = re.search(r'<a [^>]*href="(/persona/\d+)"[^>]*>[^<]*' + testo, html)
    return m.group(1) if m else None


def test_c17_precedente_e_successiva(sito):
    client, ids, _ = sito
    # ordine: Bianchi, Esposito, Rossi
    bianchi = client.get(f"/persona/{ids['Bianchi']}").get_data(as_text=True)
    assert _link(bianchi, "Successiva") == f"/persona/{ids['Esposito']}"
    assert _link(bianchi, "Precedente") is None          # la prima non ha Precedente

    esposito = client.get(f"/persona/{ids['Esposito']}").get_data(as_text=True)
    assert _link(esposito, "Precedente") == f"/persona/{ids['Bianchi']}"
    assert _link(esposito, "Successiva") == f"/persona/{ids['Rossi']}"

    rossi = client.get(f"/persona/{ids['Rossi']}").get_data(as_text=True)
    assert _link(rossi, "Successiva") is None             # l'ultima non ha Successiva
