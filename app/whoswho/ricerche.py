"""Ricerche, scheda persona e collegamenti (SPEC F1-F7).

Maiuscole/minuscole/accenti non contano grazie alla collation del database
(utf8mb4_0900_ai_ci, vedi PIANO.md). Gli spazi in più si tolgono con `pulisci`.
"""
from __future__ import annotations

from .importa import pulisci

ORDINE = "ORDER BY p.cognome, p.nome, p.id"
CAMPI = "p.id, p.nome, p.cognome, p.foto, p.professione"


def _contiene(testo: str) -> str:
    """Pattern LIKE 'contiene', con % e _ dell'utente presi alla lettera."""
    t = testo.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{t}%"


def _tutte(conn, sql: str, parametri=()) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(sql, parametri)
        return list(cur.fetchall())


# ---------- F1: ricerca per nome (anche un pezzo, più parole: C27) ----------
def cerca_per_nome(conn, testo: str) -> list[dict]:
    q = pulisci(testo)
    if not q:
        return []
    # C27: ogni parola deve comparire (anche a pezzi) nel nome o nel cognome
    parole = q.split(" ")
    condizioni = " AND ".join("(p.nome LIKE %s OR p.cognome LIKE %s)" for _ in parole)
    parametri = [x for parola in parole for x in (_contiene(parola), _contiene(parola))]
    return _tutte(conn, f"""
        SELECT {CAMPI} FROM persone p
        WHERE {condizioni}
        {ORDINE}""", parametri)


# ---------- F3: ricerca per azienda (anche esperienze passate, C4) ----------
def cerca_per_azienda(conn, testo: str) -> list[dict]:
    q = pulisci(testo)
    if not q:
        return []
    return _tutte(conn, f"""
        SELECT DISTINCT {CAMPI} FROM persone p
        JOIN esperienze e ON e.persona_id = p.id
        JOIN aziende a ON a.id = e.azienda_id
        WHERE a.nome LIKE %s
        {ORDINE}""", (_contiene(q),))


# ---------- F4: ricerca per skill (nome esatto, maiuscole non contano, C5) ----------
def cerca_per_skill(conn, testo: str) -> list[dict]:
    q = pulisci(testo)
    if not q:
        return []
    return _tutte(conn, f"""
        SELECT {CAMPI} FROM persone p
        JOIN persona_skill ps ON ps.persona_id = p.id
        JOIN skill s ON s.id = ps.skill_id
        WHERE s.nome = %s
        {ORDINE}""", (q,))


def elenco_skill(conn) -> list[str]:
    return [r["nome"] for r in _tutte(conn, "SELECT nome FROM skill ORDER BY nome")]


# ---------- F5: ricerca per evento ----------
def elenco_eventi(conn) -> list[dict]:
    return _tutte(conn, "SELECT id, nome, data, luogo FROM eventi ORDER BY data DESC, nome")


def evento(conn, evento_id: int) -> dict | None:
    righe = _tutte(conn, "SELECT id, nome, data, luogo FROM eventi WHERE id = %s", (evento_id,))
    return righe[0] if righe else None


def cerca_per_evento(conn, evento_id: int) -> list[dict]:
    return _tutte(conn, f"""
        SELECT {CAMPI} FROM persone p
        JOIN persona_evento pe ON pe.persona_id = p.id
        WHERE pe.evento_id = %s
        {ORDINE}""", (evento_id,))


# ---------- F2 + F6: scheda persona ----------
def scheda(conn, persona_id: int) -> dict | None:
    righe = _tutte(conn, "SELECT * FROM persone WHERE id = %s", (persona_id,))
    if not righe:
        return None
    s = righe[0]
    s["esperienze"] = _tutte(conn, """
        SELECT a.nome AS azienda, e.ruolo, e.inizio, e.fine
        FROM esperienze e JOIN aziende a ON a.id = e.azienda_id
        WHERE e.persona_id = %s
        ORDER BY e.fine IS NOT NULL, e.fine DESC, e.inizio DESC""", (persona_id,))
    s["skill"] = [r["nome"] for r in _tutte(conn, """
        SELECT s.nome FROM skill s JOIN persona_skill ps ON ps.skill_id = s.id
        WHERE ps.persona_id = %s ORDER BY s.nome""", (persona_id,))]
    s["eventi"] = _tutte(conn, """
        SELECT ev.id, ev.nome, ev.data, ev.luogo, pe.note
        FROM persona_evento pe JOIN eventi ev ON ev.id = pe.evento_id
        WHERE pe.persona_id = %s ORDER BY ev.data DESC""", (persona_id,))
    s["colleghi"] = colleghi(conn, persona_id)
    s["stesso_evento"] = conosciuti_stesso_evento(conn, persona_id)
    s["a_mano"] = collegamenti_a_mano(conn, persona_id)
    return s


def colleghi(conn, persona_id: int) -> list[dict]:
    """Stessa azienda in periodi che si sovrappongono (C7, C8).
    Fine vuota = ci lavora ancora, quindi conta fino a oggi (C9).
    Esperienza senza data di inizio: non si può dire, quindi non conta."""
    return _tutte(conn, """
        SELECT p.id, p.nome, p.cognome,
               GROUP_CONCAT(DISTINCT a.nome ORDER BY a.nome SEPARATOR ', ') AS dettaglio
        FROM esperienze e1
        JOIN esperienze e2 ON e2.azienda_id = e1.azienda_id AND e2.persona_id <> e1.persona_id
        JOIN persone p ON p.id = e2.persona_id
        JOIN aziende a ON a.id = e1.azienda_id
        WHERE e1.persona_id = %s
          AND e1.inizio IS NOT NULL AND e2.inizio IS NOT NULL
          AND e1.inizio <= COALESCE(e2.fine, CURDATE())
          AND e2.inizio <= COALESCE(e1.fine, CURDATE())
        GROUP BY p.id, p.nome, p.cognome
        ORDER BY p.cognome, p.nome""", (persona_id,))


def conosciuti_stesso_evento(conn, persona_id: int) -> list[dict]:
    """Persone incontrate in almeno un evento in comune (C10)."""
    return _tutte(conn, """
        SELECT p.id, p.nome, p.cognome,
               GROUP_CONCAT(DISTINCT ev.nome ORDER BY ev.nome SEPARATOR ', ') AS dettaglio
        FROM persona_evento pe1
        JOIN persona_evento pe2 ON pe2.evento_id = pe1.evento_id AND pe2.persona_id <> pe1.persona_id
        JOIN persone p ON p.id = pe2.persona_id
        JOIN eventi ev ON ev.id = pe1.evento_id
        WHERE pe1.persona_id = %s
        GROUP BY p.id, p.nome, p.cognome
        ORDER BY p.cognome, p.nome""", (persona_id,))


# ---------- F7: collegamenti a mano ----------
def collegamenti_a_mano(conn, persona_id: int) -> list[dict]:
    """Compaiono in entrambe le schede, chiunque sia A o B (C11)."""
    return _tutte(conn, """
        SELECT c.id AS collegamento_id, c.descrizione, p.id, p.nome, p.cognome
        FROM collegamenti c
        JOIN persone p ON p.id = IF(c.persona_a_id = %s, c.persona_b_id, c.persona_a_id)
        WHERE %s IN (c.persona_a_id, c.persona_b_id)
        ORDER BY c.creato_il, c.id""", (persona_id, persona_id))


def aggiungi_collegamento(conn, persona_a_id: int, persona_b_id: int, descrizione: str) -> int:
    descrizione = pulisci(descrizione)
    if persona_a_id == persona_b_id:
        raise ValueError("Una persona non può essere collegata a se stessa.")
    if not descrizione:
        raise ValueError("Scrivi una descrizione del collegamento.")
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS n FROM persone WHERE id IN (%s, %s)", (persona_a_id, persona_b_id))
        if cur.fetchone()["n"] != 2:
            raise ValueError("Persona non trovata.")
        # C22: stessa coppia (in qualsiasi ordine) e stessa descrizione = doppione
        cur.execute(
            """SELECT COUNT(*) AS n FROM collegamenti
               WHERE ((persona_a_id = %s AND persona_b_id = %s) OR (persona_a_id = %s AND persona_b_id = %s))
                 AND descrizione = %s""",
            (persona_a_id, persona_b_id, persona_b_id, persona_a_id, descrizione),
        )
        if cur.fetchone()["n"]:
            raise ValueError("Collegamento già presente.")
        cur.execute(
            "INSERT INTO collegamenti (persona_a_id, persona_b_id, descrizione) VALUES (%s, %s, %s)",
            (persona_a_id, persona_b_id, descrizione),
        )
        nuovo_id = cur.lastrowid
    conn.commit()
    return nuovo_id


def elimina_collegamento(conn, collegamento_id: int) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM collegamenti WHERE id = %s", (collegamento_id,))
    conn.commit()


def elenco_persone(conn) -> list[dict]:
    return _tutte(conn, f"SELECT {CAMPI} FROM persone p {ORDINE}")


# ---------- F8: persona precedente / successiva (stesso ordine di elenco_persone, C17) ----------
def precedente_successiva(conn, persona_id: int) -> tuple[dict | None, dict | None]:
    attuale = "(SELECT cognome, nome, id FROM persone WHERE id = %s)"
    prima = _tutte(conn, f"""
        SELECT id, nome, cognome FROM persone
        WHERE (cognome, nome, id) < {attuale}
        ORDER BY cognome DESC, nome DESC, id DESC LIMIT 1""", (persona_id,))
    dopo = _tutte(conn, f"""
        SELECT id, nome, cognome FROM persone
        WHERE (cognome, nome, id) > {attuale}
        ORDER BY cognome, nome, id LIMIT 1""", (persona_id,))
    return (prima[0] if prima else None), (dopo[0] if dopo else None)
