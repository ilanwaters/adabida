# routes/serveis_media.py

import os

from flask import Blueprint, send_from_directory
import mimetypes
mimetypes.add_type('video/webm', '.webm')  # o 'audio/webm' si només conté àudio

serveis_media_bp = Blueprint("serveis_media", __name__)

@serveis_media_bp.route("/media/<path:filepath>")
def serveix_media(filepath):
    media_root = os.path.join(os.getcwd(), "umberto", "media")
    ruta_completa = os.path.join(media_root, filepath)

    print("🧨 ESTIC DINS LA FUNCIÓ serveix_media() – filepath:", filepath)
    print("📂 RUTA COMPLETA A SERVIR:", ruta_completa)
    print("📦 FITXER EXISTEIX?", os.path.exists(ruta_completa))

    if not os.path.exists(ruta_completa):
        return f"Fitxer no trobat: {ruta_completa}", 404

    carpeta, nom_fitxer = os.path.split(filepath)
    return send_from_directory(os.path.join(media_root, carpeta), nom_fitxer)


@serveis_media_bp.route('/umberto/<usuari>/<entrada_id>/<nom_fitxer>')
def serveix_fitxer(usuari, entrada_id, nom_fitxer):
    base_dir = os.path.join("umberto", "usuaris")

    for arrel, carpetes, fitxers in os.walk(base_dir):
        if usuari in arrel and entrada_id in arrel and nom_fitxer in fitxers:
            ruta_carpeta = os.path.abspath(arrel)
            return send_from_directory(ruta_carpeta, nom_fitxer)

    return f"❌ Fitxer no trobat: {nom_fitxer}", 404

@serveis_media_bp.route('/umberto/<usuari>/<entrada_id>/mini/<nom_fitxer>')
def serveix_miniatura(usuari, entrada_id, nom_fitxer):
    base_dir = os.path.join("umberto", "usuaris")
    
    for arrel, carpetes, fitxers in os.walk(base_dir):
        if usuari in arrel and entrada_id in arrel and "mini" in arrel and nom_fitxer in fitxers:
            ruta_carpeta = os.path.abspath(arrel)
            return send_from_directory(ruta_carpeta, nom_fitxer)
    
    # Si no troba la miniatura, serveix la imatge original
    for arrel, carpetes, fitxers in os.walk(base_dir):
        if usuari in arrel and entrada_id in arrel and nom_fitxer in fitxers and "mini" not in arrel:
            ruta_carpeta = os.path.abspath(arrel)
            return send_from_directory(ruta_carpeta, nom_fitxer)
    
    return f"Miniatura no trobada: {nom_fitxer}", 404
