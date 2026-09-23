import os
from flask import Blueprint, request, session, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from models import db, Usuari
from utils.paisos import normalitza_pais
from genera_identificadors import extreu_dades_identificador
from .nova_entrada_personal import detectar_tipus_media

pujar_temp_bp = Blueprint("pujar_temp_bp", __name__)

@pujar_temp_bp.route("/pujar_arxiu_temp", methods=["POST"])
def pujar_arxiu_temp():
    usuari_login = session.get("usuari")
    if not usuari_login:
        return jsonify({"error": "Sessió no vàlida"}), 401

    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        return jsonify({"error": "Usuari inexistent"}), 404

    arxiu = request.files.get("arxiu")
    mime = arxiu.mimetype

    if not arxiu or arxiu.filename == "":
        return jsonify({"error": "Cap arxiu rebut"}), 400

    nom_seg = secure_filename(arxiu.filename)

    _, any_str, mes_str = extreu_dades_identificador(usuari.identificador_abadia)
    pais = normalitza_pais(usuari.pais_residencia)

    carpeta_temp = os.path.join("umberto", "media", "temp", pais, any_str, mes_str, usuari.nom_login)

    os.makedirs(carpeta_temp, exist_ok=True)

    ruta_final = os.path.join(carpeta_temp, nom_seg)
    arxiu.save(ruta_final)

    # ✅ DETECCIÓ SINCRONITZADA AMB NOVA_ENTRADA_PERSONAL
    if nom_seg.lower().endswith('.webm'):
        tipus_detectat = detectar_tipus_media(ruta_final)
        tipus_final = "video" if tipus_detectat == "video" else "audio"
        print(f"🔍 TEMP: {nom_seg} → detectat com '{tipus_detectat}' → retornat com '{tipus_final}'")
    else:
        is_video = mime.startswith("video/")
        is_audio = mime.startswith("audio/")
        tipus_final = "video" if is_video else "audio" if is_audio else "altre"

    return jsonify({
        "success": True,
        "missatge": "Arxiu pujat correctament",
        "mime": mime,
        "tipus": tipus_final,
        "nom": nom_seg,
        "url": f"/media/temp/{pais}/{any_str}/{mes_str}/{usuari.nom_login}/{nom_seg}"
    }), 200

@pujar_temp_bp.route("/eliminar_arxiu_temp", methods=["POST"])
def eliminar_arxiu_temp():
    usuari_login = session.get("usuari")
    if not usuari_login:
        return jsonify({"error": "Sessió no vàlida"}), 401

    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        return jsonify({"error": "Usuari inexistent"}), 404

    dades = request.get_json()
    nom_fitxer = dades.get("nom_fitxer")

    if not nom_fitxer:
        return jsonify({"error": "Falta nom_fitxer"}), 400

    _, any_str, mes_str = extreu_dades_identificador(usuari.identificador_abadia)
    pais = normalitza_pais(usuari.pais_residencia)

    carpeta_temp = os.path.join("umberto", "media", "temp", pais, any_str, mes_str, usuari.nom_login)
    ruta_fitxer = os.path.join(carpeta_temp, secure_filename(nom_fitxer))

    if os.path.exists(ruta_fitxer):
        os.remove(ruta_fitxer)
        return jsonify({"success": True, "missatge": "Fitxer eliminat"})
    else:
        return jsonify({"error": "Fitxer no trobat"}), 404


