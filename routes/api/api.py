from flask import Blueprint, jsonify, session, render_template, url_for
from models import db, Entrada, Usuari, EntradaGuardada


api_bp = Blueprint("api", __name__)

@api_bp.route("/api/entrada/<usuari_login>/<int:entrada_id>")
def obtenir_entrada(usuari_login, entrada_id):
    usuari = Usuari.query.filter_by(nom_login=usuari_login).first_or_404()
    entrada = Entrada.query.filter_by(id=entrada_id, usuari_id=usuari.id).first_or_404()

    # 🔍 Comprovem si l’usuari actual ja ha guardat aquesta entrada
    ja_guardada = False
    if 'usuari' in session:
        actual = Usuari.query.filter_by(nom_login=session['usuari']).first()
        if actual:
            ja_guardada = EntradaGuardada.query.filter_by(
                usuari_id=actual.id, entrada_id=entrada.id
            ).first() is not None

    es_propietari = session.get("usuari") == usuari.nom_login

    return jsonify({
        "id": entrada.id,
        "usuari_login": usuari.nom_login,
        "usuari_nom": f"{usuari.nom} {usuari.primer_cognom} {usuari.segon_cognom or ''}".strip(),
        "titol": entrada.titol,
        "tema": entrada.tema,
        "pais": entrada.pais,
        "regio": entrada.regio,
        "municipi": entrada.municipi,
        "pais_imatge": entrada.pais_imatge,
        "regio_imatge": entrada.regio_imatge,
        "municipi_imatge": entrada.municipi_imatge,
        "data_creacio": entrada.data_creacio.strftime('%d/%m/%Y') if entrada.data_creacio else None,
        "any": entrada.any_text,
        "contingut": entrada.contingut,
        "titol_imatge": entrada.titol_imatge,
        "any_imatge": entrada.any_imatge,
        "descripcio_imatge": entrada.descripcio_imatge,
        "referencia": entrada.referencia,
         "propietari": es_propietari,
        "ja_guardada": ja_guardada,
        "arxius": [
            {
                "nom_fitxer": f.nom_fitxer,
                "tipus": f.tipus,
                "tipus_media": f.tipus_media, 
                "ruta": f"/umberto/{usuari.nom_login}/{entrada.id}/{f.nom_fitxer}"
            }
            for f in entrada.arxius_adjuntats
        ]
    })

