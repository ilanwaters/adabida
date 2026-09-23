from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models import db, Usuari, PerfilBiografic

questionari_bp = Blueprint("questionari", __name__)

@questionari_bp.route("/questionari", methods=["GET", "POST"])
def questionari():
    usuari_login = session.get("usuari")
    if not usuari_login:
        flash("Sessió no vàlida")
        return redirect(url_for("login.login"))

    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        flash("Usuari no trobat")
        return redirect(url_for("login.login"))

    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()

    if request.method == "POST":
        print("🚀 POST rebut")
        # Recollir dades del formulari
        dades = {
            'pare_nom': request.form.get("pare_nom"),
            'mare_nom': request.form.get("mare_nom"),
            'germans': request.form.get("germans"),
            'parella': request.form.get("parella"),
            'fills': request.form.get("fills"),
            'lloc_neixement': request.form.get("lloc_neixement"),
            'data_neixement': request.form.get("data_neixement"),
            'llocs_residencia': request.form.get("llocs_residencia"),
            'salut': request.form.get("salut"),
            'moments': request.form.get("moments"),
            'aficions': request.form.get("aficions"),
            'valors': request.form.get("valors")
        }

        if perfil:
            # Actualitzar
            for camp, valor in dades.items():
                setattr(perfil, camp, valor)
        else:
            # Crear nou
            perfil = PerfilBiografic(usuari_id=usuari.id, **dades)
            db.session.add(perfil)

        db.session.commit()
        flash("Qüestionari desat correctament")
        return redirect(url_for("pagina_personal.pagina_personal"))

    return render_template("questionari.html", perfil=perfil, usuari_id=usuari.id)
