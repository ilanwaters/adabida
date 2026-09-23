# utils/text_biografic.py

def generar_text_biografic(perfil):
    """
    Genera un text biogràfic senzill a partir del perfil.
    """
    if not perfil:
        return "Encara no has completat el teu qüestionari biogràfic."

    text = f"Va néixer a {perfil.lloc_neixement} l'any {perfil.data_neixement}.\n"
    if perfil.pare_nom:
        text += f"El seu pare es deia {perfil.pare_nom}. "
    if perfil.mare_nom:
        text += f"La seva mare es deia {perfil.mare_nom}. "
    if perfil.fills:
        text += f"Té fills: {perfil.fills}. "
    if perfil.aficions:
        text += f"Li agrada {perfil.aficions.lower()}. "
    if perfil.moments:
        text += f"Un moment vital important: {perfil.moments.lower()}. "
    if perfil.salut:
        text += f"Ha partir de tal anya va tenir: {perfil.salut.lower()}. "
    if perfil.valors:
        text += f"Els valors que el defineixen són: {perfil.valors.lower()}. "

    return text.strip()

#from models import Entrevista, RespostaEntrevista

def generar_biografia_entrevista(perfil_id):
    """Funció desactivada - sistema d'entrevistes obsolet"""
    return 

    # Agafem totes les entrevistes del perfil
    entrevistes = Entrevista.query.filter_by(perfil_id=perfil_id).all()
    if not entrevistes:
        return "Encara no has iniciat cap entrevista."

    # Agafem totes les respostes de totes les entrevistes
    respostes = []
    for entrevista in entrevistes:
        respostes += (
            RespostaEntrevista.query
            .filter_by(entrevista_id=entrevista.id)
            .order_by(RespostaEntrevista.tema, RespostaEntrevista.id)
            .all()
        )

    if not respostes:
        return "Encara no has respost cap pregunta de l'entrevista."

    # Construïm el text
    text = ""
    for r in respostes:
        text += f"{r.pregunta}\n→ {r.resposta}\n\n"

    return text.strip()
