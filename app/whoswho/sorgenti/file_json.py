"""Sorgente: file JSON già nel formato della porta d'ingresso (es. dati/esempio.json)."""
import json
from pathlib import Path


def leggi(percorso: str | Path) -> list[dict]:
    dati = json.loads(Path(percorso).read_text(encoding="utf-8"))
    if isinstance(dati, dict) and "persone" in dati:
        dati = dati["persone"]
    if not isinstance(dati, list):
        raise ValueError("Il file deve contenere una lista di persone")
    return dati
