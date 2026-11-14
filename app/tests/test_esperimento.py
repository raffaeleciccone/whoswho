"""Criteri C18-C28, aggiunti dopo le prove 1 e 2 dell'esperimento di ricostruzione (vedi esperimento-ricostruzione/)."""
import json

import pytest

from whoswho import ricerche
from whoswho.importa import importa_persone
from whoswho.sorgenti import file_json

from .conftest import esp, nomi, persona

URL_A = "https://www.linkedin.com/in/mario-rossi-a"
URL_B = "https://www.linkedin.com/in/mario-rossi-b"


def _persone(conn):
    return ricerche.cerca_per_nome(conn, "Mario Rossi")


# ---------- D4: stessa persona ----------
def test_c18_prima_con_profilo_poi_senza(conn):
    importa_persone(conn, [persona("Mario", "Rossi", profilo_url=URL_A, skill=["Python"])])
    importa_persone(conn, [persona("Mario", "Rossi", skill=["Docker"])])
    trovate = _persone(conn)
    assert len(trovate) == 1
    assert ricerche.scheda(conn, trovate[0]["id"])["skill"] == ["Docker", "Python"]


def test_c18_prima_senza_profilo_poi_con(conn):
    importa_persone(conn, [persona("Mario", "Rossi", skill=["Python"])])
    importa_persone(conn, [persona("mario", "ROSSI", profilo_url=URL_A, skill=["Docker"])])
    trovate = _persone(conn)
    assert len(trovate) == 1
    s = ricerche.scheda(conn, trovate[0]["id"])
    assert s["profilo_url"] == URL_A
    assert s["skill"] == ["Docker", "Python"]


def test_c19_profili_diversi_sono_due_persone(conn):
    importa_persone(conn, [persona("Mario", "Rossi", profilo_url=URL_A)])
    importa_persone(conn, [persona("Mario", "Rossi", profilo_url=URL_B)])
    assert len(_persone(conn)) == 2


def test_c20_senza_profilo_tra_due_omonimi_e_ambiguo(conn):
    importa_persone(conn, [persona("Mario", "Rossi", profilo_url=URL_A),
                           persona("Mario", "Rossi", profilo_url=URL_B)])
    res = importa_persone(conn, [persona("Mario", "Rossi", skill=["Docker"])])
    assert res.importate == 0
    assert len(res.scartate) == 1 and "ambigu" in res.scartate[0].lower()
    assert len(_persone(conn)) == 2
    assert ricerche.cerca_per_skill(conn, "Docker") == []


# ---------- F3/F4: azienda a pezzi, skill esatta ----------
def test_c21_azienda_a_pezzi_skill_esatta(conn):
    importa_persone(conn, [
        persona("Mario", "Rossi", esperienze=[esp("Accenture Italia", "2020-01")], skill=["JavaScript"]),
        persona("Luca", "Bianchi", skill=["Java"]),
    ])
    assert nomi(ricerche.cerca_per_azienda(conn, "accent")) == ["Mario Rossi"]
    assert nomi(ricerche.cerca_per_skill(conn, "Java")) == ["Luca Bianchi"]


# ---------- F7: niente collegamenti doppi ----------
def test_c22_collegamento_doppio_rifiutato(conn):
    importa_persone(conn, [persona("Mario", "Rossi"), persona("Luca", "Bianchi")])
    mario = _persone(conn)[0]["id"]
    luca = ricerche.cerca_per_nome(conn, "Luca")[0]["id"]
    ricerche.aggiungi_collegamento(conn, mario, luca, "Mario è il capo di Luca")
    with pytest.raises(ValueError, match="Relazione già presente"):
        ricerche.aggiungi_collegamento(conn, mario, luca, "Mario è il capo di Luca")
    with pytest.raises(ValueError, match="già presente"):   # dalla scheda di Luca, maiuscole diverse
        ricerche.aggiungi_collegamento(conn, luca, mario, "mario è il capo di luca")
    ricerche.aggiungi_collegamento(conn, mario, luca, "Hanno studiato insieme")  # descrizione diversa: ok
    assert len(ricerche.collegamenti_a_mano(conn, mario)) == 2


def test_c22_messaggio_nella_pagina(conn, client_per):
    importa_persone(conn, [persona("Mario", "Rossi"), persona("Luca", "Bianchi")])
    mario = _persone(conn)[0]["id"]
    luca = ricerche.cerca_per_nome(conn, "Luca")[0]["id"]
    client = client_per(conn)
    dati = {"altra_persona": luca, "descrizione": "capo"}
    client.post(f"/persona/{mario}/collegamenti", data=dati)
    html = client.post(f"/persona/{mario}/collegamenti", data=dati, follow_redirects=True).get_data(as_text=True)
    assert "Relazione già presente." in html


# ---------- D6: il reimport non cancella ----------
def test_c23_reimport_senza_skill_non_cancella(conn):
    importa_persone(conn, [persona("Mario", "Rossi", professione="Data Engineer", skill=["Python"],
                                   esperienze=[esp("Accenture", "2019-01")])])
    importa_persone(conn, [persona("Mario", "Rossi")])
    s = ricerche.scheda(conn, _persone(conn)[0]["id"])
    assert s["skill"] == ["Python"]
    assert s["professione"] == "Data Engineer"
    assert [e["azienda"] for e in s["esperienze"]] == ["Accenture"]


# ---------- F8: ordine alfabetico ----------
def test_c24_ordine_ignora_accenti_e_maiuscole(conn):
    importa_persone(conn, [persona("Anna", "Esposito"), persona("Bruno", "éboli"), persona("Carlo", "Bianchi")])
    assert nomi(ricerche.elenco_persone(conn)) == ["Carlo Bianchi", "Bruno éboli", "Anna Esposito"]


# ---------- Porta d'ingresso: le due forme del file (PIANO sez. 2) ----------
def test_file_lista_oppure_oggetto_con_persone(tmp_path):
    p = [{"nome": "Mario", "cognome": "Rossi"}]
    lista = tmp_path / "lista.json"
    lista.write_text(json.dumps(p), encoding="utf-8")
    oggetto = tmp_path / "oggetto.json"
    oggetto.write_text(json.dumps({"nota": "prova", "persone": p}), encoding="utf-8")
    assert file_json.leggi(lista) == p
    assert file_json.leggi(oggetto) == p


# ---------- C25: date incomplete (inizio = primo giorno, fine = ultimo) ----------
def test_c25_fine_di_solo_anno_vale_fino_a_dicembre(conn):
    importa_persone(conn, [
        persona("Mario", "Rossi", esperienze=[esp("Accenture", "2019", "2022")]),
        persona("Luca", "Bianchi", esperienze=[esp("Accenture", "2022-03")]),
    ])
    assert nomi(ricerche.colleghi(conn, _persone(conn)[0]["id"])) == ["Luca Bianchi"]
    s = ricerche.scheda(conn, _persone(conn)[0]["id"])
    assert str(s["esperienze"][0]["inizio"]) == "2019-01-01"
    assert str(s["esperienze"][0]["fine"]) == "2022-12-31"


def test_c25_fine_di_solo_mese_vale_fino_all_ultimo_giorno(conn):
    importa_persone(conn, [
        persona("Mario", "Rossi", esperienze=[esp("Accenture", "2020", "2022-06")]),
        persona("Luca", "Bianchi", esperienze=[esp("Accenture", "2022-07")]),
        persona("Anna", "Verdi", esperienze=[esp("Accenture", "2022-06-30")]),
    ])
    assert nomi(ricerche.colleghi(conn, _persone(conn)[0]["id"])) == ["Anna Verdi"]
    assert str(ricerche.scheda(conn, _persone(conn)[0]["id"])["esperienze"][0]["fine"]) == "2022-06-30"


def test_c25_febbraio_bisestile(conn):
    importa_persone(conn, [persona("Mario", "Rossi", esperienze=[esp("Accenture", "2023", "2024-02")])])
    assert str(ricerche.scheda(conn, _persone(conn)[0]["id"])["esperienze"][0]["fine"]) == "2024-02-29"


# ---------- C26: lo stesso profilo scritto in modi diversi ----------
def test_c26_profilo_scritto_in_modi_diversi(conn):
    for url in ("https://www.linkedin.com/in/mario-rossi",
                "http://linkedin.com/in/Mario-Rossi/",
                "https://it.linkedin.com/in/mario-rossi?originalSubdomain=it"):
        importa_persone(conn, [persona("Mario", "Rossi", profilo_url=url)])
    assert len(_persone(conn)) == 1
    importa_persone(conn, [persona("Mario", "Rossi", profilo_url="https://www.linkedin.com/in/mario-rossi-2")])
    assert len(_persone(conn)) == 2


def test_c26_normalizzazione():
    from whoswho.importa import normalizza_profilo
    atteso = "linkedin.com/in/mario-rossi"
    for url in ("https://www.linkedin.com/in/mario-rossi", "HTTP://LinkedIn.com/in/mario-rossi/",
                "https://it.linkedin.com/in/mario-rossi?x=1#top", "linkedin.com/in/mario-rossi"):
        assert normalizza_profilo(url) == atteso
    assert normalizza_profilo("https://ex.com/a") == "ex.com/a"   # "ex." non è un prefisso di lingua


# ---------- C27: ricerca per nome con più parole ----------
def test_c27_ogni_parola_anche_a_pezzi(conn):
    importa_persone(conn, [persona("Mario", "Rossi"), persona("Mario", "Bianchi")])
    for testo in ("mar ros", "rossi mario", "mario ros", "  MARIO   ROSSI "):
        assert nomi(ricerche.cerca_per_nome(conn, testo)) == ["Mario Rossi"], testo
    for testo in ("mario", "mario r"):   # la "r" è anche in "Mario"
        assert nomi(ricerche.cerca_per_nome(conn, testo)) == ["Mario Bianchi", "Mario Rossi"], testo
    assert ricerche.cerca_per_nome(conn, "mario verdi") == []


# ---------- C28: ricerca vuota ----------
def test_c28_ricerca_vuota(conn, client_per):
    importa_persone(conn, [persona("Mario", "Rossi")])
    client = client_per(conn)
    for tipo in ("nome", "azienda", "skill"):
        for q in ("", "   "):
            html = client.get("/cerca", query_string={"tipo": tipo, "q": q}).get_data(as_text=True)
            assert "Scrivi qualcosa da cercare." in html, (tipo, q)
            assert "Nessun risultato" not in html, (tipo, q)
