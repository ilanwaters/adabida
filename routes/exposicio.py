
import os
from flask import Blueprint, render_template
from utils.paisos import normalitza_pais
from models import Exposicio,ImatgeGaleria
from sqlalchemy.orm import joinedload

exposicio_bp = Blueprint("exposicio", __name__)

@exposicio_bp.route("/exposicio/<codi_expo>")
def mostra_exposicio(codi_expo):
    expo = Exposicio.query.options(joinedload(Exposicio.entrada)).filter_by(codi=codi_expo).first()
    if not expo:
        return "Exposició no trobada", 404

    carpeta = os.path.join(
        "umberto", "media", "expo", 
        normalitza_pais(expo.pais), 
        str(expo.any), 
        f"{expo.mes:02}", 
        codi_expo
    )

    imatges = []
    if os.path.isdir(carpeta):
        for nom_fitxer in sorted(os.listdir(carpeta)):
            if nom_fitxer.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                ruta_relativa = os.path.join("media", "expo", normalitza_pais(expo.pais), str(expo.any), f"{expo.mes:02}", codi_expo, nom_fitxer)
                imatge_db = ImatgeGaleria.query.filter_by(nom_fitxer=nom_fitxer).first()

                if imatge_db and imatge_db.entrada and imatge_db.entrada.usuari:
                    entrada_id = imatge_db.entrada_id
                    usuari_login = imatge_db.entrada.usuari.nom_login
                else:
                    entrada_id = None
                    usuari_login = None

                entrada = imatge_db.entrada if imatge_db else None
                usuari = entrada.usuari if entrada and entrada.usuari else None

                imatges.append({
                    "url": f"/{ruta_relativa.replace(os.sep, '/')}",
                    "entrada_id": entrada_id,
                    "usuari_login": usuari_login,
                    "titol_entrada": entrada.titol if entrada else None,
                    "autor_nom": usuari.nom if usuari else None,
                    "data_creacio": entrada.data_creacio.strftime("%Y") if entrada and entrada.data_creacio else None
                })
        
    return render_template("exposicio_imatges.html", titol_exposicio=expo.titol, imatges=imatges)
