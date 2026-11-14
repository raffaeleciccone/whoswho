"""Tiene allineato kit-ricostruzione/ con i documenti del progetto.

    python strumenti/aggiorna_kit.py              # copia i documenti attuali nel kit
    python strumenti/aggiorna_kit.py --controlla  # controlla soltanto: esce con errore se il kit è vecchio

Il kit contiene COPIE (così i compagni scaricano una cartella sola): vanno rigenerate ogni volta
che cambiano SPEC, PIANO, AGENTS, CLAUDE, README, HANDOFF, la bozza, lo strumento di misura o i dati di esempio.
"""
import filecmp
import shutil
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
KIT = RADICE / "kit-ricostruzione"

# sorgente nel progetto -> destinazione nel kit
COPIE = {
    "SPEC.md": "progetto/SPEC.md",
    "PIANO.md": "progetto/PIANO.md",
    "AGENTS.md": "progetto/AGENTS.md",
    "CLAUDE.md": "progetto/CLAUDE.md",
    "README.md": "progetto/README.md",
    "HANDOFF.md": "progetto/HANDOFF.md",
    "design/bozza.html": "progetto/design/bozza.html",
    "strumenti/misura_c34.py": "misura_c34.py",
    "dati/esempio.json": "dati-di-prova/esempio.json",
}


def main():
    controlla = "--controlla" in sys.argv
    vecchi = []
    for sorgente, destinazione in COPIE.items():
        s, d = RADICE / sorgente, KIT / destinazione
        if d.exists() and filecmp.cmp(s, d, shallow=False):
            continue
        vecchi.append(destinazione)
        if not controlla:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(s, d)

    # nel kit, la cartella progetto/ deve contenere SOLO i documenti
    attesi = {KIT / d for d in COPIE.values() if d.startswith("progetto/")}
    estranei = [p for p in (KIT / "progetto").rglob("*") if p.is_file() and p not in attesi] if (KIT / "progetto").exists() else []

    if controlla:
        if vecchi or estranei:
            for v in vecchi:
                print(f"VECCHIO   kit-ricostruzione/{v}")
            for e in estranei:
                print(f"ESTRANEO  {e.relative_to(RADICE)}")
            sys.exit("Il kit non e' allineato: esegui  python strumenti/aggiorna_kit.py")
        print("Kit allineato con i documenti del progetto.")
    else:
        print("Aggiornati:", ", ".join(vecchi) if vecchi else "niente, era già allineato")
        if estranei:
            print("ATTENZIONE, file in più in progetto/ (da togliere a mano):", *estranei, sep="\n  ")


if __name__ == "__main__":
    main()
