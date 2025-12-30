from flask import Blueprint, render_template, url_for
from models import ImatgeGaleria, Exposicio, ImatgeExposicio
import os
from sqlalchemy.orm import joinedload
from models import Entrada, Exposicio

galeria_bp = Blueprint("galeria", __name__)

@galeria_bp.route("/galeria")
def galeria():
    base_path = os.path.join("umberto", "media", "galeria")
    imatges_destacades = []
    exposicions = Exposicio.query.order_by(Exposicio.id.desc()).all()
    
    imatges = (
        ImatgeGaleria.query
        .options(joinedload(ImatgeGaleria.entrada).joinedload(Entrada.usuari))
        .filter(ImatgeGaleria.destinacio.in_(["galeria", "inici"]))
        .order_by(ImatgeGaleria.data_publicacio.desc())
        .all()
    )
    
    for img in imatges:
        any_mes = img.data_publicacio.strftime('%Y/%m')
        ruta_fitxer = os.path.join(base_path, any_mes, img.nom_fitxer)
        
        if os.path.exists(ruta_fitxer):
            if not img.nom_fitxer.startswith("expo_"):
                imatges_destacades.append(img)
    
    for exposicio in exposicions:
        exposicio.carpeta = exposicio.carpeta.replace("\\", "/")
    
    return render_template("galeria.html", 
                         imatges_destacades=imatges_destacades,
                         exposicions=exposicions)

@galeria_bp.route("/galeria/exposicio/<int:id>")
def exposicio_imatges(id):
    exposicio = Exposicio.query.get_or_404(id)
    relacions = ImatgeExposicio.query.filter_by(exposicio_id=id).all()
    imatges = []

    for rel in relacions:
        imatge = ImatgeGaleria.query.get(rel.imatge_id)
        if imatge:
           ruta = f"expo/{exposicio.carpeta}/{imatge.nom_fitxer}"
           url = url_for("serveis_media.serveix_media", filepath=ruta)
           print("📸 Ruta imatge:", ruta)
           print("🌐 URL generada:", url)
           imatges.append({ "url": url })


    return render_template("galeria.html",
                           titol_exposicio=exposicio.titol,
                           imatges=imatges)
