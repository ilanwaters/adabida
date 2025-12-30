from flask import Blueprint, render_template
from datetime import date
aportacions_bp = Blueprint("aportacions", __name__)

@aportacions_bp.route("/aportacions")
def aportacions():
    """
    Pàgina d'aportacions voluntàries.
    Explica el model de finançament ètic d'Adabida.
    """
    return render_template("aportacions.html")

@aportacions_bp.route("/fes-aportacio")
def nova_aportacio():
    """
    Formulari per fer aportacions (versió pública amb 2 columnes)
    """
    today = date.today().strftime('%Y-%m-%d')
    return render_template("nova_aportacio_inici.html", today=today)