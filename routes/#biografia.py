from flask import Blueprint, render_template
from models import db, Entrevista, RespostaEntrevista

biografia_bp = Blueprint("biografia", __name__)

@biografia_bp.route("/biografia/<int:perfil_id>")
def mostrar_biografia(perfil_id):
    """
    Genera un text de biografia a partir de les respostes de totes les entrevistes 
    associades a un perfil biogràfic.

    🔧 IMPORTANT:
    A partir de juliol 2025, el model RespostaEntrevista ja no té perfil_id directe.
    Ara cal accedir-hi a través de la taula Entrevista (que té perfil_id).
    """

   # Recuperem totes les respostes d’aquest perfil
    respostes = (
        RespostaEntrevista.query
        .filter_by(perfil_id=perfil_id)
        .order_by(RespostaEntrevista.tema, RespostaEntrevista.id)
        .all()
    )


    # Construcció del text de biografia
    text = "Aquest és un esborrany de biografia generat a partir de les respostes:\n\n"
    for r in respostes:
        text += f"{r.pregunta}\n→ {r.resposta}\n\n"

    return render_template("biografia_generada.html", text=text)
