from flask import Blueprint
from models import db, Usuari

reset_bp = Blueprint("reset", __name__)

@reset_bp.route("/reset_admin")
def reset_admin():
    usuari = Usuari.query.filter_by(nom_login="admin").first()
    if not usuari:
        return "❌ Usuari admin no trobat."

    usuari.set_contrasenya("1234")
    db.session.commit()
    return "✅ Contrasenya de l'usuari admin actualitzada a '1234'."
