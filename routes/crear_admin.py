from flask import Blueprint
from models import db, Usuari

crear_admin_bp = Blueprint("crear_admin", __name__)

@crear_admin_bp.route("/crear_admin")
def crear_admin():
    existent = Usuari.query.filter_by(nom_login="admin").first()
    if existent:
        return "⚠️ Ja existeix un usuari amb nom 'admin'."

    nou = Usuari(
        nom_login="admin",
        email="admin@abadia.org",
        nom="Administrador",
        primer_cognom="Abadia",
        segon_cognom="Central",
        data_naixement="1900-01-01",
        lloc_naixement="Lloc desconegut",
        pais_naixement="Desconegut",
        idioma="ca",
        pais_residencia="Desconegut",
        es_admin=True
    )
    nou.set_contrasenya("admin123")
    db.session.add(nou)
    db.session.commit()
    return "✅ Usuari admin creat amb contrasenya 'admin123'."
