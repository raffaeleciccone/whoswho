r"""Misura del criterio C34 (SPEC sez. 5, PIANO sez. 4c). Serve l'app accesa e Google Chrome (o Edge).

    python strumenti/misura_c34.py                          # questo progetto
    python strumenti/misura_c34.py C:\percorso\progetto     # un'altra copia (es. ricostruita in classe)
    python strumenti/misura_c34.py C:\percorso\progetto 8001  # ... con la porta del sito

La cartella indicata deve avere il suo docker-compose.yml e il comando
`python -m whoswho.avvio scheda-tipica` (PIANO sez. 4c): se manca, anche questo è un risultato.

1. chiede al container "app" l'HTML della scheda della persona tipica (database dei test);
2. la apre in Chrome senza finestra, con il foglio di stile vero servito da nginx (localhost:8000);
3. portatile: a 1366 px di larghezza il fondo dei 4 riquadri deve stare entro 650 px;
4. telefono: dentro una cornice larga 390 px la pagina non deve essere più larga dello schermo.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_QUI = Path(__file__).resolve().parent
if len(sys.argv) > 1:
    RADICE = Path(sys.argv[1]).resolve()
elif (_QUI / "progetto").is_dir():      # lanciato dal kit-ricostruzione: misura la cartella progetto/
    RADICE = _QUI / "progetto"
else:                                   # lanciato da strumenti/ del progetto originale
    RADICE = _QUI.parent


def _porta():
    """HOST_APP_PORT da variabile d'ambiente, poi dal file .env, altrimenti 8000."""
    if len(sys.argv) > 2:
        return sys.argv[2]
    if os.environ.get("HOST_APP_PORT"):
        return os.environ["HOST_APP_PORT"]
    env = RADICE / ".env"
    if env.exists():
        m = re.search(r"^HOST_APP_PORT=(\d+)", env.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1)
    return "8000"


PORTA = _porta()
LIMITE_ALTEZZA = 650

CANDIDATI = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]


def trova_chrome():
    for c in CANDIDATI:
        if Path(c).exists() or shutil.which(c):
            return c
    sys.exit("Chrome/Edge non trovato: installalo o aggiungi il percorso in CANDIDATI.")


def titolo(chrome, file, larghezza, altezza):
    uscita = subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
         f"--window-size={larghezza},{altezza}", "--virtual-time-budget=4000", "--dump-dom", file.as_uri()],
        capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    m = re.search(r"<title>([^<]*)</title>", uscita)
    return m.group(1) if m else ""


def main():
    # senza docker-compose.yml qui, Docker cercherebbe nelle cartelle superiori e misurerebbe
    # un altro progetto (per esempio l'originale, se il kit è dentro il repository)
    if not (RADICE / "docker-compose.yml").exists():
        sys.exit(f"In {RADICE} non c'è ancora un programma (manca docker-compose.yml): niente da misurare.")
    html = subprocess.run(["docker", "compose", "run", "--rm", "-T", "app", "python", "-m", "whoswho.avvio", "scheda-tipica"],
                          cwd=RADICE, capture_output=True, text=True, encoding="utf-8").stdout
    if "<html" not in html:
        sys.exit("Non ho ricevuto la scheda dal container app: l'app è accesa?")
    # senza il foglio di stile la misura non ha senso: controllo che il sito risponda
    import urllib.request
    try:
        urllib.request.urlopen(f"http://localhost:{PORTA}/static/stile.css", timeout=5).read(1)
    except Exception:
        sys.exit(f"Il sito non risponde su http://localhost:{PORTA} (foglio di stile non trovato): "
                 "avvialo con 'docker compose up -d' o indica la porta giusta.")
    html = html.replace("<head>", f'<head><base href="http://localhost:{PORTA}/">', 1)
    misura = ('<script>window.addEventListener("load",function(){'
              'var q=document.querySelector(".quattro").getBoundingClientRect();'
              'document.title="FINE="+Math.round(q.bottom)+" LARGH="+document.documentElement.scrollWidth'
              '+"/"+document.documentElement.clientWidth;});</script></body>')
    cartella = Path(tempfile.mkdtemp(prefix="misura_c34_"))
    scheda = cartella / "scheda.html"
    scheda.write_text(html.replace("</body>", misura), encoding="utf-8")
    telefono = cartella / "telefono.html"
    telefono.write_text('<!doctype html><title>x</title><iframe id="f" src="scheda.html" style="width:390px;height:900px;border:0"></iframe>'
                        '<script>document.getElementById("f").onload=function(){var t=this.contentDocument.title;'
                        'setTimeout(function(){document.title=document.getElementById("f").contentDocument.title;},500);};</script>',
                        encoding="utf-8")
    chrome = trova_chrome()

    ok = True
    t = titolo(chrome, scheda, 1366, 650)
    fine = int(re.search(r"FINE=(\d+)", t).group(1))
    esito = fine <= LIMITE_ALTEZZA
    ok &= esito
    print(f"Portatile 1366x768: la scheda finisce a {fine} px (limite {LIMITE_ALTEZZA})  {'OK' if esito else 'NO'}")

    t = titolo(chrome, telefono, 800, 1000)
    larga, schermo = map(int, re.search(r"LARGH=(\d+)/(\d+)", t).groups())
    esito = larga <= schermo
    ok &= esito
    print(f"Telefono 390 px: pagina larga {larga} px su {schermo} px di schermo  {'OK' if esito else 'NO'}")

    print("C34:", "RISPETTATO" if ok else "NON RISPETTATO")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
