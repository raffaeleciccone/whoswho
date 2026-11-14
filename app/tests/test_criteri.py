"""Un test per ogni criterio di SPEC.md sezione 5.
Il nome di ogni test inizia con il criterio che controlla (test_c1_..., test_c2_...)."""
from whoswho import ricerche
from whoswho.importa import importa_persone

from .conftest import esp, nomi, persona


def _id(conn, nome, cognome):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM persone WHERE nome=%s AND cognome=%s", (nome, cognome))
        return cur.fetchone()["id"]


# ---------- F1: ricerca per nome ----------
def test_c1_ricerca_cognome_senza_distinzione_maiuscole(conn):
    importa_persone(conn, [persona("Mario", "Rossi"), persona("Andrea", "Rossi"), persona("Luca", "Bianchi")])
    assert nomi(ricerche.cerca_per_nome(conn, "rossi")) == ["Andrea Rossi", "Mario Rossi"]
    assert nomi(ricerche.cerca_per_nome(conn, "ROSSI")) == ["Andrea Rossi", "Mario Rossi"]


def test_c1_ricerca_con_un_pezzo_di_nome(conn):
    importa_persone(conn, [persona("Marco", "Ricci"), persona("Maria", "Romano"), persona("Luca", "Bianchi")])
    assert nomi(ricerche.cerca_per_nome(conn, "Mar")) == ["Marco Ricci", "Maria Romano"]
    assert nomi(ricerche.cerca_per_nome(conn, "maria romano")) == ["Maria Romano"]
    assert nomi(ricerche.cerca_per_nome(conn, "romano maria")) == ["Maria Romano"]


def test_c2_nome_che_non_esiste(conn):
    importa_persone(conn, [persona("Mario", "Rossi")])
    assert ricerche.cerca_per_nome(conn, "Zanetti") == []
    assert ricerche.cerca_per_nome(conn, "%") == []  # i caratteri speciali non trovano tutti


# ---------- F2: scheda ----------
def test_c3_scheda_completa(conn):
    importa_persone(conn, [persona(
        "Mario", "Rossi",
        esperienze=[esp("Accenture", "2019-01-01", "2022-06-30", "Consultant")],
        skill=["Python", "Docker"],
        eventi=[{"nome": "Data Summit", "data": "2026-05-10", "luogo": "Milano"}],
    )])
    s = ricerche.scheda(conn, _id(conn, "Mario", "Rossi"))
    assert [e["azienda"] for e in s["esperienze"]] == ["Accenture"]
    assert str(s["esperienze"][0]["inizio"]) == "2019-01-01"
    assert str(s["esperienze"][0]["fine"]) == "2022-06-30"
    assert s["skill"] == ["Docker", "Python"]
    assert [e["nome"] for e in s["eventi"]] == ["Data Summit"]


def test_c3_scheda_con_sezioni_vuote_dice_nessuno(conn, client_per):
    importa_persone(conn, [persona("Sara", "Conti")])
    pid = _id(conn, "Sara", "Conti")
    html = client_per(conn).get(f"/persona/{pid}").get_data(as_text=True)
    # eventi, aziende, skill, colleghi, stesso evento, a mano: 6 sezioni vuote
    assert html.count(">nessuno<") == 6


# ---------- F3: ricerca per azienda ----------
def test_c4_azienda_anche_esperienze_passate(conn):
    importa_persone(conn, [
        persona("Mario", "Rossi", esperienze=[esp("Accenture", "2019-01", "2022-06")]),   # passata
        persona("Luca", "Bianchi", esperienze=[esp("Accenture", "2023-01")]),            # attuale
        persona("Marco", "Ricci", esperienze=[esp("Orbita Cloud", "2022-05")]),
    ])
    assert nomi(ricerche.cerca_per_azienda(conn, "accenture")) == ["Luca Bianchi", "Mario Rossi"]


def test_c4_azienda_una_volta_sola_anche_con_piu_ruoli(conn):
    importa_persone(conn, [persona("Mario", "Rossi", esperienze=[
        esp("Accenture", "2015-01", "2017-01", "Analyst"),
        esp("Accenture", "2017-02", "2020-01", "Manager"),
    ])])
    assert nomi(ricerche.cerca_per_azienda(conn, "Accenture")) == ["Mario Rossi"]


# ---------- F4: ricerca per skill ----------
def test_c5_skill_maiuscole_e_spazi_non_contano(conn):
    importa_persone(conn, [
        persona("Mario", "Rossi", skill=["Docker"]),
        persona("Luca", "Bianchi", skill=["docker"]),      # stessa skill scritta diversa
        persona("Marco", "Ricci", skill=["Docker Compose"]),  # skill diversa
    ])
    attesi = ["Luca Bianchi", "Mario Rossi"]
    assert nomi(ricerche.cerca_per_skill(conn, "docker")) == attesi
    assert nomi(ricerche.cerca_per_skill(conn, "Docker")) == attesi
    assert nomi(ricerche.cerca_per_skill(conn, " DOCKER ")) == attesi


# ---------- F5: ricerca per evento ----------
def test_c6_solo_persone_di_quell_evento(conn):
    summit = {"nome": "Data Summit", "data": "2026-05-10"}
    meetup = {"nome": "Meetup DevOps", "data": "2026-03-21"}
    importa_persone(conn, [
        persona("Mario", "Rossi", eventi=[summit]),
        persona("Giulia", "Esposito", eventi=[summit, meetup]),
        persona("Luca", "Bianchi", eventi=[meetup]),
    ])
    eventi = {e["nome"]: e["id"] for e in ricerche.elenco_eventi(conn)}
    assert nomi(ricerche.cerca_per_evento(conn, eventi["Data Summit"])) == ["Giulia Esposito", "Mario Rossi"]
    assert nomi(ricerche.cerca_per_evento(conn, eventi["Meetup DevOps"])) == ["Luca Bianchi", "Giulia Esposito"]


# ---------- F6: persone collegate ----------
def test_c7_periodi_sovrapposti_sono_colleghi(conn):
    importa_persone(conn, [
        persona("Mario", "Rossi", esperienze=[esp("Accenture", "2019-01-01", "2022-12-31")]),
        persona("Luca", "Bianchi", esperienze=[esp("Accenture", "2021-01-01", "2024-12-31")]),
    ])
    assert nomi(ricerche.colleghi(conn, _id(conn, "Mario", "Rossi"))) == ["Luca Bianchi"]
    assert nomi(ricerche.colleghi(conn, _id(conn, "Luca", "Bianchi"))) == ["Mario Rossi"]


def test_c8_anni_diversi_non_sono_colleghi(conn):
    importa_persone(conn, [
        persona("Mario", "Rossi", esperienze=[esp("Accenture", "2015-01-01", "2017-12-31")]),
        persona("Luca", "Bianchi", esperienze=[esp("Accenture", "2020-01-01", "2023-12-31")]),
    ])
    assert ricerche.colleghi(conn, _id(conn, "Mario", "Rossi")) == []
    assert ricerche.colleghi(conn, _id(conn, "Luca", "Bianchi")) == []


def test_c8_aziende_diverse_non_sono_colleghi(conn):
    importa_persone(conn, [
        persona("Mario", "Rossi", esperienze=[esp("Accenture", "2020-01-01")]),
        persona("Luca", "Bianchi", esperienze=[esp("Deloitte", "2020-01-01")]),
    ])
    assert ricerche.colleghi(conn, _id(conn, "Mario", "Rossi")) == []


def test_c9_chi_lavora_ancora_conta_fino_a_oggi(conn):
    importa_persone(conn, [
        persona("Mario", "Rossi", esperienze=[esp("Accenture", "2018-01-01")]),          # ancora lì
        persona("Luca", "Bianchi", esperienze=[esp("Accenture", "2025-01-01", "2025-12-31")]),
    ])
    assert nomi(ricerche.colleghi(conn, _id(conn, "Mario", "Rossi"))) == ["Luca Bianchi"]


def test_c9_esperienza_senza_inizio_non_conta(conn):
    importa_persone(conn, [
        persona("Mario", "Rossi", esperienze=[esp("Accenture", None)]),
        persona("Luca", "Bianchi", esperienze=[esp("Accenture", "2020-01-01")]),
    ])
    assert ricerche.colleghi(conn, _id(conn, "Mario", "Rossi")) == []


def test_c10_stesso_evento(conn):
    summit = {"nome": "Data Summit", "data": "2026-05-10"}
    importa_persone(conn, [
        persona("Mario", "Rossi", eventi=[summit]),
        persona("Luca", "Bianchi", eventi=[summit]),
        persona("Marco", "Ricci", eventi=[{"nome": "Altro evento", "data": "2026-01-01"}]),
    ])
    assert nomi(ricerche.conosciuti_stesso_evento(conn, _id(conn, "Mario", "Rossi"))) == ["Luca Bianchi"]
    assert nomi(ricerche.conosciuti_stesso_evento(conn, _id(conn, "Luca", "Bianchi"))) == ["Mario Rossi"]
    assert ricerche.conosciuti_stesso_evento(conn, _id(conn, "Marco", "Ricci")) == []


# ---------- F7: collegamenti a mano ----------
def test_c11_collegamento_in_entrambe_le_schede_e_cancellazione(conn):
    importa_persone(conn, [persona("Mario", "Rossi"), persona("Luca", "Bianchi")])
    mario, luca = _id(conn, "Mario", "Rossi"), _id(conn, "Luca", "Bianchi")

    cid = ricerche.aggiungi_collegamento(conn, mario, luca, "Mario è il capo di Luca")
    for chi, altro in ((mario, "Luca Bianchi"), (luca, "Mario Rossi")):
        c = ricerche.collegamenti_a_mano(conn, chi)
        assert nomi(c) == [altro]
        assert c[0]["descrizione"] == "Mario è il capo di Luca"

    ricerche.elimina_collegamento(conn, cid)
    assert ricerche.collegamenti_a_mano(conn, mario) == []
    assert ricerche.collegamenti_a_mano(conn, luca) == []


def test_c11_collegamento_non_valido(conn):
    import pytest
    importa_persone(conn, [persona("Mario", "Rossi")])
    mario = _id(conn, "Mario", "Rossi")
    with pytest.raises(ValueError):
        ricerche.aggiungi_collegamento(conn, mario, mario, "con se stesso")
    with pytest.raises(ValueError):
        ricerche.aggiungi_collegamento(conn, mario, 99999, "persona inesistente")


def test_c11_dalla_pagina_web(conn, client_per):
    importa_persone(conn, [persona("Mario", "Rossi"), persona("Luca", "Bianchi")])
    mario, luca = _id(conn, "Mario", "Rossi"), _id(conn, "Luca", "Bianchi")
    client = client_per(conn)
    client.post(f"/persona/{mario}/collegamenti", data={"altra_persona": luca, "descrizione": "capo di Luca"})
    assert "capo di Luca" in client.get(f"/persona/{luca}").get_data(as_text=True)


# ---------- Import: doppioni e dati incompleti ----------
def _conta(conn, tabella):
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) AS n FROM {tabella}")
        return cur.fetchone()["n"]


def test_c12_importare_due_volte_non_crea_doppioni(conn):
    dati = [
        persona("Mario", "Rossi",
                esperienze=[esp("Accenture", "2019-01", "2022-06"), esp("Nexa", None)],
                skill=["Python", "python ", "Docker"],
                eventi=[{"nome": "Data Summit", "data": "2026-05-10"}, {"nome": "Senza data"}]),
        persona("Luca", "Bianchi", esperienze=[esp("accenture", "2021-01")], skill=["DOCKER"],
                eventi=[{"nome": "Data Summit", "data": "2026-05-10"}]),
    ]
    importa_persone(conn, dati)
    prima = {t: _conta(conn, t) for t in
             ("persone", "aziende", "esperienze", "skill", "persona_skill", "eventi", "persona_evento")}
    importa_persone(conn, dati)
    dopo = {t: _conta(conn, t) for t in prima}
    assert dopo == prima
    assert prima["persone"] == 2
    assert prima["aziende"] == 2      # "Accenture" e "accenture" sono la stessa
    assert prima["skill"] == 2        # Python, Docker
    assert prima["eventi"] == 2


def test_c12_stessa_persona_riconosciuta_dal_profilo(conn):
    url = "https://www.linkedin.com/in/mario-rossi"
    importa_persone(conn, [persona("Mario", "Rossi", profilo_url=url)])
    importa_persone(conn, [persona("Mario", "Rossi", profilo_url=url + "/", professione="CTO")])
    assert _conta(conn, "persone") == 1
    assert ricerche.cerca_per_nome(conn, "Rossi")[0]["professione"] == "CTO"


def test_c13_dati_senza_nome_scartati_e_segnalati(conn):
    res = importa_persone(conn, [
        persona("Mario", "Rossi"),
        {"cognome": "Senzanome"},
        persona("Luca", "  "),
        persona("Giulia", "Esposito"),
    ])
    assert res.importate == 2
    assert len(res.scartate) == 2
    assert nomi(ricerche.elenco_persone(conn)) == ["Giulia Esposito", "Mario Rossi"]


def test_c13_data_sbagliata_non_blocca(conn):
    res = importa_persone(conn, [persona("Mario", "Rossi", esperienze=[esp("Accenture", "ieri")])])
    assert res.importate == 1
    assert any("data non valida" in a for a in res.avvisi)
