from flask import Blueprint, jsonify, request, session, abort, render_template, url_for
from models import db, Usuari, EntradaGuardada, Entrada, Conversa
from routes.inici import preparar_conversa_per_vista


api_guardades_bp = Blueprint("api_guardades", __name__)

@api_guardades_bp.route("/api/guardades/<usuari_login>")
def llista_entrades_guardades(usuari_login):
    print(f"📥 Rebuda petició per: {usuari_login}")
    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        print("❌ Usuari no trobat")
        return "", 404

    guardades = EntradaGuardada.query.filter_by(usuari_id=usuari.id).all()
    entrades = []

    for g in guardades:
        entrada = Entrada.query.get(g.entrada_id)
        if not entrada:
            print(f"⚠️ Entrada amb ID {g.entrada_id} no trobada")
            continue

        conversa = Conversa.query.filter_by(entrada_id=entrada.id).first()
        if conversa:
            item = preparar_conversa_per_vista(conversa, entrada.usuari.nom_login)
            item["usuari_login"] = entrada.usuari.nom_login
        else:
            entrada.usuari_login = entrada.usuari.nom_login
            entrada.tipus = "entrada"
            item = entrada

        entrades.append(item)

    return render_template("fragments/targetes_guardades.html", entrades=entrades)


@api_guardades_bp.route("/api/guardar_entrada/<int:entrada_id>", methods=["POST"])
def guardar_entrada(entrada_id):
    if 'usuari' not in session:
        abort(401)

    usuari = Usuari.query.filter_by(nom_login=session['usuari']).first()
    if not usuari:
        abort(401)

    # Evita duplicats
    existent = EntradaGuardada.query.filter_by(usuari_id=usuari.id, entrada_id=entrada_id).first()
    if existent:
        return jsonify({"missatge": "Ja estava guardada"}), 200

    nova = EntradaGuardada(usuari_id=usuari.id, entrada_id=entrada_id)
    db.session.add(nova)
    db.session.commit()

    return jsonify({"missatge": "Entrada guardada"}), 200

@api_guardades_bp.route("/api/eliminar_entrada_guardada/<int:entrada_id>", methods=["POST"])
def eliminar_entrada_guardada(entrada_id):
    if 'usuari' not in session:
        abort(401)

    usuari = Usuari.query.filter_by(nom_login=session['usuari']).first()
    if not usuari:
        abort(401)

    guardada = EntradaGuardada.query.filter_by(usuari_id=usuari.id, entrada_id=entrada_id).first()
    if guardada:
        db.session.delete(guardada)
        db.session.commit()
        return jsonify({"missatge": "Eliminada"}), 200

    return jsonify({"missatge": "No trobada"}), 404

@api_guardades_bp.route("/api/esborranys/<usuari_login>")
def llista_esborranys(usuari_login):
    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        return "", 404

    entrades_raw = Entrada.query.filter_by(usuari_id=usuari.id, es_publica=False).all()
    entrades = []

    from utils.media_helpers import generar_miniatura_entrada
    for entrada in entrades_raw:
        conversa = Conversa.query.filter_by(entrada_id=entrada.id, tipus_conversa='entrevista_adabida').first()
        if conversa:
            item = preparar_conversa_per_vista(conversa, usuari.nom_login)
            item["usuari_login"] = usuari.nom_login
        else:
            entrada.usuari_login = usuari.nom_login
            entrada.tipus = "entrada"
            entrada.miniatura_calculada = generar_miniatura_entrada(entrada, usuari.nom_login)
            item = entrada
        entrades.append(item)

    return render_template("fragments/targetes_guardades.html", entrades=entrades)