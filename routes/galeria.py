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


