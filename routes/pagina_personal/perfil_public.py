from flask import Blueprint, render_template, url_for
from models import Usuari, Entrada, PerfilBiografic
from flask_login import current_user

perfil_public_bp = Blueprint("perfil_public", __name__)

@perfil_public_bp.route("/perfil/<usuari_login>")
def perfil_public(usuari_login):
    usuari = Usuari.query.filter_by(nom_login=usuari_login).first_or_404()

    # Perfil biogràfic i relacions (llistes segures per a Jinja)
    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()
    experiencies = list(perfil.experiencies) if perfil and perfil.experiencies else []
    estudis = list(perfil.estudis) if perfil and perfil.estudis else []
    carrecs = list(perfil.carrecs_publics) if perfil and perfil.carrecs_publics else []
    obres = list(perfil.obres) if perfil and perfil.obres else []

    # Entrades (mantinc la teva lògica actual)
    entrades = (Entrada.query
                .filter_by(usuari_id=usuari.id)
                .order_by(Entrada.data_creacio.desc())
                .all())

    # Miniatures
    for e in entrades:
        e.usuari_login = usuari.nom_login
        if getattr(e, "nom_fitxer", None):
            e.miniatura = url_for(
                "serveis_media.serveix_fitxer",
                usuari=usuari.nom_login,
                entrada_id=str(e.id),
                nom_fitxer=e.nom_fitxer
            )
        else:
            e.miniatura = "/static/icons/default.png"

    return render_template(
        "pagina_personal/perfil_public.html",
        usuari=usuari,
        perfil=perfil,
        entrades=entrades,
        experiencies=experiencies,
        estudis=estudis,
        carrecs=carrecs,
        obres=obres,
    )
