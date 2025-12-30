from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Usuari
from flask_babel import _
from flask_login import login_user, logout_user



login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"], endpoint="login")
def login_page():
    if request.method == "POST":
        nom_login = request.form.get("usuari")
        contrasenya = request.form.get("contrasenya")
        usuari = Usuari.query.filter_by(nom_login=nom_login).first()
        
        if not usuari or not usuari.check_contrasenya(contrasenya):
            flash(_("Credencials incorrectes"), "error-login")
            session["mostrar_login"] = True
            return redirect(url_for("inici.inici_pagina"))
        
        if not usuari.email_verificat:
            flash(_("⚠️ Si us plau, verifica el teu email abans de fer login. Revisa la teva safata d'entrada."), "warning")
            session["mostrar_login"] = True
            return redirect(url_for("auth.reenviar_verificacio"))
        
        print("✅ Login correcte:", usuari.nom_login)
        login_user(usuari) 
        session["usuari"] = usuari.nom_login
        session["usuari_id"] = usuari.id  
        session["nom_login"] = usuari.nom_login  
        session["es_admin"] = usuari.es_admin

        # ✅ Redirigeix segons si és administrador o no
        if usuari.es_admin:
            return redirect(url_for("admin.pagina_admin"))
        else:
            print("➡️ Redirigint cap a PÀGINA PERSONAL...")
            return redirect(url_for("pagina_personal.pagina_personal"))

    # GET — mostra la modal si hi ha paràmetre error=1
    mostrar_login = session.pop("mostrar_login", False)
    return render_template("inici.html", mostrar_login=mostrar_login)

@login_bp.route("/logout")
def logout():
    logout_user()  # ⬅️ Tanca la sessió Flask-Login
    session.clear()
    flash(_("Sessió tancada correctament."))
    return redirect(url_for("inici.inici_pagina"))

