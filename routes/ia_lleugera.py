from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from utils.temps import ara_utc
from models import db, Usuari, TemaEntrevista, Entrevista, Missatge
from models import PerfilBiografic 
ia_lleugera_bp = Blueprint("ia_lleugera", __name__)

@ia_lleugera_bp.route("/entrevista_ia/<int:perfil_id>", methods=["GET", "POST"])
def entrevista_ia(perfil_id):
    usuari_actual = session.get("usuari")
    if not usuari_actual:
        return redirect(url_for("login.login"))

    perfil = PerfilBiografic.query.filter_by(id=perfil_id).first_or_404()
    session["perfil_id"] = perfil.id  # Ens assegurem que està disponible

    tema_nom = request.args.get("tema", "").strip()
    entrevista = None
    missatges = []

    # ─── Si NO hi ha cap tema seleccionat ─────────────────────
    if not tema_nom:
        if request.method == "POST":
            nou_tema = request.form.get("missatge", "").strip()
            if nou_tema:
                tema = TemaEntrevista.query.filter_by(nom=nou_tema).first()
                if not tema:
                    tema = TemaEntrevista(nom=nou_tema, creat_per=usuari_actual)
                    db.session.add(tema)
                    db.session.commit()
                entrevistes_existents = Entrevista.query.filter_by(perfil_id=perfil.id, tema=tema).all()
                if entrevistes_existents:
                    return render_template("tria_tema_confirmar.html",
                                            tema=tema,
                                            entrevistes=entrevistes_existents,
                                            perfil=perfil)


                # Comptar entrevistes anteriors per aquest tema i perfil
                num_anteriors = Entrevista.query.filter_by(perfil_id=perfil.id, tema=tema).count()

                nova_entrevista = Entrevista(
                    perfil_id=perfil.id,
                    tema=tema,
                    numero=num_anteriors + 1
                )
                db.session.add(nova_entrevista)
                db.session.commit()

                return redirect(url_for("ia_lleugera.entrevista_ia", perfil_id=perfil.id, tema=tema.nom))

        return render_template("tria_tema.html", perfil=perfil)

    # ─── Si hi ha un tema seleccionat ─────────────────────────
    tema = TemaEntrevista.query.filter_by(nom=tema_nom).first()
    if not tema:
        tema = TemaEntrevista(nom=tema_nom, creat_per=usuari_actual)
        db.session.add(tema)
        db.session.commit()

    entrevista = Entrevista.query.filter_by(perfil_id=perfil.id, tema=tema).first()
    if not entrevista:
        entrevista = Entrevista(perfil_id=perfil.id, tema=tema, numero=1)
        db.session.add(entrevista)
        db.session.commit()

    if request.method == "POST":
        nou_text = request.form.get("missatge", "").strip()
        if nou_text:
            missatge_usuari = Missatge(
                entrevista_id=entrevista.id,
                autor="usuari",
                text=nou_text,
                timestamp=ara_utc()
            )
            resposta_echo = Missatge(
                entrevista_id=entrevista.id,
                autor="echo",
                text="(Simulació) M'ho pots explicar una mica més?",
                timestamp=ara_utc()
            )
            db.session.add_all([missatge_usuari, resposta_echo])
            db.session.commit()

            from models import RespostaEntrevista  # només cal si no el tens ja

            resposta_bio = RespostaEntrevista(
                entrevista_id=entrevista.id,
                perfil_id=perfil.id, 
                pregunta=nou_text,
                resposta="(Simulació) M'ho pots explicar una mica més?",
                tema=tema.nom
            )
            db.session.add(resposta_bio)
            db.session.commit()


            return redirect(url_for("ia_lleugera.entrevista_ia", perfil_id=perfil.id, tema=tema.nom))

    missatges = Missatge.query.filter_by(entrevista_id=entrevista.id).order_by(Missatge.timestamp.asc()).all()

    temes_globals = TemaEntrevista.query.filter_by(creat_per="admin").all()
    temes_personals = TemaEntrevista.query.filter_by(creat_per=usuari_actual).all()

    # ─── Agrupar entrevistes del perfil per tema ──────────────
    entrevistes_per_tema = {}
    totes_entrevistes = Entrevista.query.filter_by(perfil_id=perfil.id).all()
    for ent in totes_entrevistes:
        nom = ent.tema.nom
        if nom not in entrevistes_per_tema:
            entrevistes_per_tema[nom] = []
        entrevistes_per_tema[nom].append(ent)

    return render_template(
        "ia_entrevista.html",
        missatges=missatges,
        perfil=perfil,
        usuari=perfil,
        temes_globals=temes_globals,
        temes_personals=temes_personals,
        tema_seleccionat=tema.nom,
        pestanya_activa="entrevista",
        entrevistes_per_tema=entrevistes_per_tema
    )



@ia_lleugera_bp.route("/llistar_temes")
def llistar_temes():
    usuari_actual = session.get("nom_login")
    if not usuari_actual:
        return "Cal iniciar sessió", 401

    # Temes globals (creats per 'admin')
    temes_globals = TemaEntrevista.query.filter_by(creat_per="admin").all()

    # Temes personals (creats per l’usuari actual)
    temes_personals = TemaEntrevista.query.filter_by(creat_per=usuari_actual).all()

    resposta = "<h1>📚 Llista de temes</h1>"

    resposta += f"<h2>🌍 Temes globals (admin)</h2><ul>"
    for t in temes_globals:
        resposta += f"<li>{t.nom}</li>"
    resposta += "</ul>"

    resposta += f"<h2>👤 Temes personals ({usuari_actual})</h2><ul>"
    for t in temes_personals:
        resposta += f"<li>{t.nom}</li>"
    resposta += "</ul>"

    return resposta

@ia_lleugera_bp.route("/temes", methods=["GET", "POST"])
def gestio_temes():
    if request.method == "POST":
        nou_tema = request.form.get("nou_tema", "").strip()
        if nou_tema:
            existent = TemaEntrevista.query.filter_by(nom=nou_tema).first()
            if not existent:
                tema = TemaEntrevista(nom=nou_tema)
                db.session.add(tema)
                db.session.commit()
    temes = TemaEntrevista.query.order_by(TemaEntrevista.nom.asc()).all()
    return render_template("gestio_temes.html", temes=temes)

ia_bp = ia_lleugera_bp
 
@ia_lleugera_bp.route("/api/afegir_tema", methods=["POST"])
def api_afegir_tema():
    usuari_actual = session.get("usuari")
    if not usuari_actual:
        return jsonify({"success": False, "error": "No autenticat"}), 401

    dades = request.get_json()
    nom_tema = dades.get("tema", "").strip()

    if not nom_tema:
        return jsonify({"success": False, "error": "Tema buit"}), 400

    existent = TemaEntrevista.query.filter_by(nom=nom_tema, creat_per=usuari_actual).first()
    if existent:
        return jsonify({"success": False, "error": "El tema ja existeix"}), 409

    nou_tema = TemaEntrevista(nom=nom_tema, creat_per=usuari_actual)
    db.session.add(nou_tema)
    db.session.commit()

    return jsonify({"success": True, "tema": nom_tema})

@ia_lleugera_bp.route("/nova_entrevista", methods=["POST"])
def nova_entrevista():
    usuari_actual = session.get("usuari")
    perfil_id = session.get("perfil_id")
    perfil = PerfilBiografic.query.get_or_404(perfil_id)


    tema_id = request.form.get("tema_id")
    tema = TemaEntrevista.query.get_or_404(tema_id)

    num_anteriors = Entrevista.query.filter_by(perfil_id=perfil.id, tema=tema).count()
    nova = Entrevista(perfil_id=perfil.id, tema=tema, numero=num_anteriors + 1)
    db.session.add(nova)
    db.session.commit()

    return redirect(url_for("ia_lleugera.entrevista_ia", perfil_id=perfil.id, tema=tema.nom))

