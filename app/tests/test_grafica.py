"""Grafica: SPEC F9, criteri C29-C33, C36, C37 (C34 si misura con strumenti/misura_c34.py; C35, C38 a vista).
Valori e coppie di colori: PIANO.md sez. 4c."""
import re
from pathlib import Path

import pytest

from whoswho import ricerche
from whoswho.importa import importa_persone

from .conftest import esp, persona

CSS = Path(__file__).resolve().parents[1] / "whoswho" / "static" / "stile.css"

# coppie testo/sfondo usate davvero nelle pagine (PIANO sez. 4c)
COPPIE = [
    ("#ffffff", "--blu-notte"),       # testo della barra
    ("#ffffff", "--blu-notte-2"),     # voce attiva della barra
    ("#ffffff", "--tasto-alto"),      # tasto principale, parte chiara della sfumatura
    ("#ffffff", "--tasto-basso"),     # tasto principale, parte scura
    ("--testo", "--carta"), ("--testo", "--sfondo"),
    ("--tenue", "--carta"), ("--tenue", "--sfondo"), ("--tenue", "--fascia"),
    ("--blu-link", "--carta"), ("--blu-link", "--sfondo"),
    ("--blu-notte", "--fascia"), ("--blu-notte", "--etichetta"), ("--blu-notte", "--avatar"),
    ("--blu-notte", "--carta"),       # lente del tasto Cerca
    ("--rosso", "--carta"),
]


def _variabili():
    testo = CSS.read_text(encoding="utf-8")
    radice = re.search(r":root\s*\{(.*?)\}", testo, re.S).group(1)
    return dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{6})", radice))


def _luminanza(colore):
    r, g, b = (int(colore[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def _contrasto(a, b):
    la, lb = sorted((_luminanza(a), _luminanza(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ---------- C29: contrasto ----------
def test_c29_contrasto_almeno_4_5():
    v = _variabili()
    for testo, sfondo in COPPIE:
        a, b = v.get(testo, testo), v.get(sfondo, sfondo)
        assert a.startswith("#") and b.startswith("#"), f"variabile mancante: {testo} / {sfondo}"
        assert _contrasto(a, b) >= 4.5, f"{testo} su {sfondo}: {_contrasto(a, b):.2f}:1"


# ---------- C30: dimensioni del testo ----------
def test_c30_testo_18_titoli_28():
    css = CSS.read_text(encoding="utf-8")
    assert re.search(r"html\s*\{[^}]*font-size:\s*18px", css)
    assert re.search(r"(^|\n)\s*h1\s*\{[^}]*font-size:\s*28px", css)
    # testi secondari: mai sotto 13,5 px; solo px o rem (decisione dell'utente, PIANO 4c)
    for valore, unita in re.findall(r"font-size:\s*([\d.]+)(px|rem|em|%)", css):
        assert unita in ("px", "rem"), f"font-size in {unita}: usare px o rem"
        px = float(valore) * (18 if unita == "rem" else 1)
        assert px >= 13.5, f"font-size {valore}{unita} = {px:.1f} px, sotto 13,5 px"


# ---------- C31: tema sempre chiaro ----------
def test_c31_tema_sempre_chiaro(conn, client_per):
    assert "prefers-color-scheme" not in CSS.read_text(encoding="utf-8")
    html = client_per(conn).get("/").get_data(as_text=True)
    assert '<meta name="color-scheme" content="light">' in html
    assert 'href="/static/stile.css"' in html


# ---------- scheda di prova ----------
@pytest.fixture
def scheda_mario(conn, client_per):
    evento = {"nome": "Data Summit", "data": "2026-05-10"}
    importa_persone(conn, [
        persona("Mario", "Rossi", professione="Data Engineer",
                esperienze=[esp("Accenture", "2019-01", "2022-06"), esp("Nexa Data", "2022-07")],
                skill=["Python"], eventi=[evento]),
        persona("Luca", "Bianchi", esperienze=[esp("Accenture", "2021-01", "2024-01")], eventi=[evento]),
    ])
    ids = {r["cognome"]: r["id"] for r in ricerche.elenco_persone(conn)}
    ricerche.aggiungi_collegamento(conn, ids["Rossi"], ids["Bianchi"], "Mario è il capo di Luca")
    html = client_per(conn).get(f"/persona/{ids['Rossi']}").get_data(as_text=True)
    return html, ids


def _blocco(html, inizio_regex):
    """Testo dall'elemento che corrisponde a inizio_regex fino alla sua chiusura (section/div)."""
    m = re.search(inizio_regex, html)
    assert m, f"non trovato: {inizio_regex}"
    tag = re.match(r"<(\w+)", m.group(0)).group(1)
    profondita, i = 0, m.start()
    for t in re.finditer(rf"<(/?){tag}\b[^>]*>", html[m.start():]):
        profondita += -1 if t.group(1) else 1
        if profondita == 0:
            return html[m.start(): m.start() + t.end()]
    raise AssertionError("tag non chiuso")


# ---------- C32: struttura della scheda ----------
def test_c32_testata_e_riquadri(scheda_mario):
    html, _ = scheda_mario
    testata = _blocco(html, r'<section class="[^"]*\btestata\b[^"]*"')
    assert "<h1>Mario Rossi</h1>" in testata
    assert "Data Engineer" in testata
    assert re.search(r"Lavora ora in\s*<a[^>]*>Nexa Data</a>", testata)
    assert 'class="foto' in testata                       # foto o iniziali
    titoli = re.findall(r'<section class="riquadro">\s*<h2>([^<]+)</h2>', html)
    assert titoli == ["Dove l'ho incontrato", "Dove ha lavorato", "Cosa sa fare", "Relazioni"]
    assert html.index("testata") < html.index("Dove l'ho incontrato")


# ---------- C33: persone collegate come miniature nella testata ----------
def test_c33_collega_con_miniatura(scheda_mario):
    html, ids = scheda_mario
    striscia = _blocco(_blocco(html, r'<section class="[^"]*\btestata\b'), r'<div class="striscia"')
    link = re.search(rf'<a [^>]*href="/persona/{ids["Bianchi"]}"[^>]*>(.*?)</a>', striscia, re.S)
    assert link, "Luca non è nella striscia delle persone collegate"
    assert ">LB<" in link.group(1) and "Luca Bianchi" in link.group(1)


# ---------- C36: conferma prima di eliminare ----------
def test_c36_elimina_chiede_conferma(scheda_mario):
    html, _ = scheda_mario
    modulo = re.search(r'<form[^>]*action="[^"]*/elimina"[^>]*>', html).group(0)
    assert re.search(r"""return confirm\(["']Eliminare la relazione con Luca Bianchi\?["']\)""", modulo)


def test_c36_nomi_relazioni(conn, client_per):
    importa_persone(conn, [persona("Mario", "Rossi"), persona("Luca", "Bianchi")])
    ids = {r["cognome"]: r["id"] for r in ricerche.elenco_persone(conn)}
    client = client_per(conn)
    dati = {"altra_persona": ids["Bianchi"], "descrizione": "capo"}
    html = client.post(f"/persona/{ids['Rossi']}/collegamenti", data=dati, follow_redirects=True).get_data(as_text=True)
    assert "Relazione aggiunta." in html
    assert "Aggiungi relazione" in html


# ---------- C37: icone ----------
def test_c37_icone_su_barra_e_tasti(scheda_mario):
    html, _ = scheda_mario
    def con_icona(regex_elemento, nome):
        m = re.search(regex_elemento, html, re.S)
        assert m, f"non trovato: {nome}"
        assert '<svg class="icona"' in m.group(0), f"{nome} senza icona"
    for voce in ("Home", "Persone", "Eventi"):
        con_icona(rf'<a [^>]*>(?:(?!</a>).)*{voce}</a>', voce)
    con_icona(r'<button[^>]*aria-label="Cerca".*?</button>', "Cerca")
    con_icona(r'<summary[^>]*>(?:(?!</summary>).)*Aggiungi relazione', "Aggiungi relazione")
    con_icona(r'<button[^>]*>(?:(?!</button>).)*Elimina</button>', "Elimina")
    con_icona(r'<a [^>]*>(?:(?!</a>).)*Indietro</a>', "Indietro")
