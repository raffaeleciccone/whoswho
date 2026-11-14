"""Porta d'ingresso: l'unico punto da cui i dati entrano nel database.

Qualsiasi sorgente (file di esempio, LinkedIn, sito eventi, CSV) produce una lista
di dizionari nel formato descritto in PIANO.md sezione 2 e chiama `importa_persone`.

Criteri della spec controllati qui:
- C12: importare due volte gli stessi dati non crea doppioni
- C13: una persona senza nome o cognome viene scartata e segnalata, le altre entrano
"""
from __future__ import annotations

import calendar
import re
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Resoconto:
    importate: int = 0
    scartate: list[str] = field(default_factory=list)
    avvisi: list[str] = field(default_factory=list)


def pulisci(testo) -> str:
    """Toglie spazi in testa/coda e spazi doppi. None -> ''."""
    if testo is None:
        return ""
    return re.sub(r"\s+", " ", str(testo)).strip()


def leggi_data(valore, avvisi: list[str], contesto: str, fine: bool = False) -> date | None:
    """Accetta 'AAAA-MM-GG', 'AAAA-MM' o 'AAAA'. Se non valida: None + avviso.

    Se mancano mese o giorno (SPEC C25): primo giorno del periodo, oppure
    l'ultimo se `fine=True` (data di fine di un'esperienza)."""
    v = pulisci(valore)
    if not v:
        return None
    try:
        if re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            return date.fromisoformat(v)
        if re.match(r"^\d{4}-\d{2}$", v):
            anno, mese = int(v[:4]), int(v[5:])
            giorno = calendar.monthrange(anno, mese)[1] if fine else 1
            return date(anno, mese, giorno)
        if re.match(r"^\d{4}$", v):
            return date(int(v), 12, 31) if fine else date(int(v), 1, 1)
    except ValueError:
        pass
    avvisi.append(f"{contesto}: data non valida '{v}', ignorata")
    return None


def normalizza_profilo(url: str) -> str:
    """Stesso profilo scritto in modi diversi -> stessa stringa (SPEC D4, C26; PIANO sez. 3).
    Contano solo sito e percorso: 'https://it.linkedin.com/in/Mario-Rossi/?x=1' -> 'linkedin.com/in/mario-rossi'."""
    u = url.strip().lower()
    u = re.sub(r"^[a-z]+://", "", u)          # http://, https://
    u = re.split(r"[?#]", u, maxsplit=1)[0]   # parametri e ancore
    sito, _, percorso = u.partition("/")
    sito = re.sub(r"^www\.", "", sito)
    if re.match(r"^[a-z]{2}\.", sito) and "." in sito[3:]:
        sito = sito[3:]                       # prefisso di lingua: it., uk., ...
    percorso = percorso.rstrip("/")
    return f"{sito}/{percorso}" if percorso else sito


def chiave_persona(nome: str, cognome: str, profilo_url: str) -> str:
    if profilo_url:
        return normalizza_profilo(profilo_url)
    return f"{nome} {cognome}".lower()


class PersonaAmbigua(Exception):
    """Il dato non ha profilo e il nome corrisponde a più persone con profili diversi (SPEC D5)."""


def trova_persona(cur, nome: str, cognome: str, profilo_url: str) -> int | None:
    """Regola "stessa persona" (SPEC D4/D5, PIANO sez. 3). Restituisce l'id, o None se è nuova."""
    if profilo_url:
        cur.execute("SELECT id FROM persone WHERE chiave = %s", (chiave_persona(nome, cognome, profilo_url),))
        trovata = cur.fetchone()
        if trovata:
            return trovata["id"]

    cur.execute("SELECT id, profilo_url FROM persone WHERE nome = %s AND cognome = %s ORDER BY id",
                (nome, cognome))
    omonimi = cur.fetchall()
    senza_profilo = [o for o in omonimi if not o["profilo_url"]]

    if profilo_url:
        # è l'omonimo senza profilo, se c'è; altrimenti un omonimo vero (persona nuova)
        return senza_profilo[0]["id"] if senza_profilo else None
    if not omonimi:
        return None
    if len(omonimi) == 1:
        return omonimi[0]["id"]
    if senza_profilo:
        return senza_profilo[0]["id"]
    raise PersonaAmbigua(f"{len(omonimi)} persone con questo nome e profili diversi, non so quale sia")


def _id_o_inserisci(cur, tabella: str, nome: str) -> int:
    cur.execute(f"INSERT IGNORE INTO {tabella} (nome) VALUES (%s)", (nome,))
    cur.execute(f"SELECT id FROM {tabella} WHERE nome = %s", (nome,))
    return cur.fetchone()["id"]


def _importa_una(cur, p: dict, res: Resoconto, etichetta: str) -> None:
    nome, cognome = pulisci(p.get("nome")), pulisci(p.get("cognome"))
    profilo_url = pulisci(p.get("profilo_url"))
    foto = pulisci(p.get("foto")) or None
    professione = pulisci(p.get("professione")) or None

    persona_id = trova_persona(cur, nome, cognome, profilo_url)
    if persona_id is None:
        cur.execute(
            """INSERT INTO persone (chiave, nome, cognome, foto, professione, profilo_url)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (chiave_persona(nome, cognome, profilo_url), nome, cognome, foto, professione, profilo_url or None),
        )
        persona_id = cur.lastrowid
    else:
        # D6: i campi presenti aggiornano, quelli vuoti non cancellano
        cur.execute(
            """UPDATE persone SET
                   nome = %s, cognome = %s,
                   foto = COALESCE(%s, foto),
                   professione = COALESCE(%s, professione),
                   profilo_url = COALESCE(%s, profilo_url),
                   chiave = COALESCE(%s, chiave)
               WHERE id = %s""",
            (nome, cognome, foto, professione, profilo_url or None,
             chiave_persona(nome, cognome, profilo_url) if profilo_url else None, persona_id),
        )

    for e in p.get("esperienze") or []:
        azienda = pulisci(e.get("azienda"))
        if not azienda:
            res.avvisi.append(f"{etichetta}: esperienza senza azienda, ignorata")
            continue
        fine = leggi_data(e.get("fine"), res.avvisi, etichetta, fine=True)
        if fine is None and pulisci(e.get("fine")):
            # C39: fine scritta ma non valida -> l'esperienza si ignora, altrimenti
            # "fine vuota" vorrebbe dire "ci lavora ancora" e creerebbe colleghi falsi
            res.avvisi.append(f"{etichetta}: lavoro in {azienda} ignorato (data di fine non valida)")
            continue
        azienda_id = _id_o_inserisci(cur, "aziende", azienda)
        ruolo = pulisci(e.get("ruolo"))
        inizio = leggi_data(e.get("inizio"), res.avvisi, etichetta)
        # "<=>" confronta anche i NULL: evita doppioni quando manca la data (C12)
        cur.execute(
            """SELECT id FROM esperienze
               WHERE persona_id = %s AND azienda_id = %s AND ruolo = %s AND inizio <=> %s""",
            (persona_id, azienda_id, ruolo, inizio),
        )
        trovata = cur.fetchone()
        if trovata:
            cur.execute("UPDATE esperienze SET fine = %s WHERE id = %s", (fine, trovata["id"]))
        else:
            cur.execute(
                "INSERT INTO esperienze (persona_id, azienda_id, ruolo, inizio, fine) VALUES (%s,%s,%s,%s,%s)",
                (persona_id, azienda_id, ruolo, inizio, fine),
            )

    for s in p.get("skill") or []:
        s = pulisci(s)
        if s:
            skill_id = _id_o_inserisci(cur, "skill", s)
            cur.execute("INSERT IGNORE INTO persona_skill VALUES (%s, %s)", (persona_id, skill_id))

    for ev in p.get("eventi") or []:
        nome_ev = pulisci(ev.get("nome"))
        if not nome_ev:
            res.avvisi.append(f"{etichetta}: evento senza nome, ignorato")
            continue
        data_ev = leggi_data(ev.get("data"), res.avvisi, etichetta)
        cur.execute("SELECT id FROM eventi WHERE nome = %s AND data <=> %s", (nome_ev, data_ev))
        trovato = cur.fetchone()
        if trovato:
            evento_id = trovato["id"]
        else:
            cur.execute(
                "INSERT INTO eventi (nome, data, luogo) VALUES (%s, %s, %s)",
                (nome_ev, data_ev, pulisci(ev.get("luogo")) or None),
            )
            evento_id = cur.lastrowid
        cur.execute(
            """INSERT INTO persona_evento (persona_id, evento_id, note) VALUES (%s, %s, %s) AS nuovo
               ON DUPLICATE KEY UPDATE note = COALESCE(nuovo.note, persona_evento.note)""",
            (persona_id, evento_id, pulisci(ev.get("note")) or None),
        )


def importa_persone(conn, persone: list[dict]) -> Resoconto:
    res = Resoconto()
    for i, p in enumerate(persone, start=1):
        nome, cognome = pulisci(p.get("nome")), pulisci(p.get("cognome"))
        etichetta = f"#{i} {nome} {cognome}".strip()
        if not nome or not cognome:
            res.scartate.append(f"#{i}: manca nome o cognome")  # C13
            continue
        try:
            with conn.cursor() as cur:
                _importa_una(cur, p, res, etichetta)
            conn.commit()
            res.importate += 1
        except PersonaAmbigua as errore:  # C20
            conn.rollback()
            res.scartate.append(f"{etichetta}: ambigua, {errore}")
        except Exception as errore:  # una persona rotta non blocca le altre (C13)
            conn.rollback()
            res.scartate.append(f"{etichetta}: errore {errore}")
    return res
