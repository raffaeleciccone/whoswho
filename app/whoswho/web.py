"""Pagina web: ricerche (F1, F3, F4, F5), scheda (F2, F6), collegamenti a mano (F7), navigazione (F8)."""
from flask import Flask, abort, flash, g, redirect, render_template, request, url_for

from . import db, ricerche

TIPI = {
    "nome": "Nome",
    "azienda": "Azienda",
    "skill": "Skill",
}


def crea_app(database: str | None = None) -> Flask:
    app = Flask(__name__)
    app.secret_key = "whoswho-locale"  # serve solo per i messaggi flash, app locale senza login

    def conn():
        if "conn" not in g:
            g.conn = db.connetti(database)
        return g.conn

    @app.teardown_appcontext
    def chiudi(_):
        c = g.pop("conn", None)
        if c is not None:
            c.close()

    @app.template_filter("data_it")
    def data_it(d):
        return d.strftime("%d/%m/%Y") if d else ""

    @app.template_filter("mese_anno")
    def mese_anno(d):
        return d.strftime("%m/%Y") if d else "?"

    @app.context_processor
    def per_la_barra():
        """Dati che servono alla barra in alto, presente su ogni pagina (F8, C14)."""
        return {"tipi": TIPI, "skill_note": ricerche.elenco_skill(conn())}

    @app.get("/")
    def home():
        return render_template("home.html", eventi=ricerche.elenco_eventi(conn())[:5])

    @app.get("/persone")
    def persone():
        return render_template("persone.html", persone=ricerche.elenco_persone(conn()))

    @app.get("/eventi")
    def eventi():
        return render_template("eventi.html", eventi=ricerche.elenco_eventi(conn()))

    @app.get("/cerca")
    def cerca():
        tipo = request.args.get("tipo", "nome")
        q = request.args.get("q", "")
        if tipo == "evento":
            try:
                evento_id = int(request.args.get("evento", ""))
            except ValueError:
                return redirect(url_for("home"))
            ev = ricerche.evento(conn(), evento_id)
            if ev is None:
                abort(404)
            risultati = ricerche.cerca_per_evento(conn(), evento_id)
            titolo = f"Incontrate a: {ev['nome']}"
        else:
            funzione = {
                "nome": ricerche.cerca_per_nome,
                "azienda": ricerche.cerca_per_azienda,
                "skill": ricerche.cerca_per_skill,
            }.get(tipo)
            if funzione is None:
                abort(400)
            if not q.strip():  # C28: ricerca vuota
                return render_template("risultati.html", risultati=[], titolo="Cerca", vuota=True)
            risultati = funzione(conn(), q)
            titolo = f"{TIPI[tipo]}: “{q.strip()}”"
        return render_template("risultati.html", risultati=risultati, titolo=titolo)

    @app.get("/persona/<int:persona_id>")
    def persona(persona_id):
        s = ricerche.scheda(conn(), persona_id)
        if s is None:
            abort(404)
        altre = [p for p in ricerche.elenco_persone(conn()) if p["id"] != persona_id]
        precedente, successiva = ricerche.precedente_successiva(conn(), persona_id)
        return render_template("persona.html", p=s, altre=altre,
                               precedente=precedente, successiva=successiva)

    @app.post("/persona/<int:persona_id>/collegamenti")
    def aggiungi_collegamento(persona_id):
        try:
            altra = int(request.form.get("altra_persona", ""))
        except ValueError:
            flash("Scegli la persona della relazione.", "errore")
            return redirect(url_for("persona", persona_id=persona_id))
        try:
            ricerche.aggiungi_collegamento(conn(), persona_id, altra, request.form.get("descrizione", ""))
            flash("Relazione aggiunta.")
        except ValueError as e:
            flash(str(e), "errore")
        return redirect(url_for("persona", persona_id=persona_id))

    @app.post("/persona/<int:persona_id>/collegamenti/<int:collegamento_id>/elimina")
    def elimina_collegamento(persona_id, collegamento_id):
        ricerche.elimina_collegamento(conn(), collegamento_id)
        flash("Relazione eliminata.")
        return redirect(url_for("persona", persona_id=persona_id))

    return app
