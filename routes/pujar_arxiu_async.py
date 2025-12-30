from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime

pujar_arxiu_bp = Blueprint("pujar_arxiu_async", __name__)

@pujar_arxiu_bp.route("/pujar_arxiu_async", methods=["POST"])
def pujar_arxiu_async():
    usuari_login = session.get("usuari")
    if not usuari_login:
        return jsonify({"error": "Sessió no vàlida"}), 401

    f = request.files.get("arxiu")
    if not f or not f.filename:
        return jsonify({"error": "Fitxer invàlid"}), 400

    nom_seg = secure_filename(f.filename)
    extensio = nom_seg.rsplit('.', 1)[-1].lower()

    # Carpeta temporal per l’usuari
    carpeta_temp = os.path.join("umberto", usuari_login, "temp_arxius")
    os.makedirs(carpeta_temp, exist_ok=True)

    ruta_dest = os.path.join(carpeta_temp, nom_seg)
    f.save(ruta_dest)

    return jsonify({
        "nom_fitxer": nom_seg,
        "tipus": extensio,
        "ruta_relativa": f"/{ruta_dest.replace(os.sep, '/')}"
    })
