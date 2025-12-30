from flask_login import login_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Usuari
from werkzeug.security import generate_password_hash
from utils.email import enviar_email_verificacio, enviar_email_reset_password, enviar_email_confirmacio_canvi_password
from flask_babel import _ as traduir

auth_bp = Blueprint("auth", __name__)

# ========== VERIFICACIÓ EMAIL ==========

@auth_bp.route("/verificar-email/<token>")
def verificar_email(token):
    usuari = Usuari.query.filter_by(token_verificacio=token).first()
    
    if not usuari:
        flash(traduir("Enllaç de verificació invàlid."), "error")
        return redirect(url_for('inici.inici_pagina'))
    
    if not usuari.verificar_token(token, tipus='verificacio'):
        flash(traduir("Aquest enllaç de verificació ha expirat."), "error")
        return redirect(url_for('auth.reenviar_verificacio'))
    
    usuari.email_verificat = True
    usuari.eliminar_token_verificacio()
    
    try:
        db.session.commit()
        db.session.refresh(usuari)
        login_user(usuari, remember=True)
        flash(traduir("Email verificat correctament!"), "success")
        return redirect(url_for('pagina_personal.pagina_personal'))
    except Exception as e:
        db.session.rollback()
        flash(traduir("Error verificant l'email."), "error")
        return redirect(url_for('inici.inici_pagina'))

@auth_bp.route("/reenviar-verificacio", methods=["GET", "POST"])
def reenviar_verificacio():
    if request.method == "POST":
        email = request.form.get("email")
        usuari = Usuari.query.filter_by(email=email).first()
        
        if not usuari:
            flash(traduir("Si aquest email està registrat, rebràs un nou enllaç de verificació."), "info")
            return redirect(url_for('inici.inici_pagina'))
        
        if usuari.email_verificat:
            flash(traduir("Aquest email ja està verificat."), "info")
            return redirect(url_for('login.login'))
        
        if enviar_email_verificacio(usuari):
            db.session.commit()
            flash(traduir("Hem enviat un nou enllaç de verificació al teu email."), "success")
        else:
            flash(traduir("Error enviant l'email."), "error")
        
        return redirect(url_for('inici.inici_pagina'))
    
    return render_template('auth/reenviar_verificacio.html')

# ========== RECUPERACIÓ CONTRASENYA ==========

@auth_bp.route("/recuperar-contrasenya", methods=["GET", "POST"])
def recuperar_contrasenya():
    if request.method == "POST":
        email = request.form.get("email")
        usuari = Usuari.query.filter_by(email=email).first()
        
        if not usuari:
            flash(traduir("Si aquest email està registrat, rebràs instruccions per recuperar la contrasenya."), "info")
            return redirect(url_for('inici.inici_pagina'))
        
        if enviar_email_reset_password(usuari):
            db.session.commit()
            return redirect(url_for('auth.recuperar_contrasenya', email_enviat=True, email=email))
        else:
            flash(traduir("Error enviant l'email."), "error")
        
        return redirect(url_for('inici.inici_pagina'))
    
    return render_template('auth/recuperar_contrasenya.html')
@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    usuari = Usuari.query.filter_by(token_reset_password=token).first()

    if not usuari:
        flash(traduir("Enllaç de recuperació invàlid."), "error")
        return redirect(url_for('inici.inici_pagina'))

    if not usuari.verificar_token(token, tipus='reset_password'):
        flash(traduir("Aquest enllaç de recuperació ha expirat."), "error")
        return redirect(url_for('auth.recuperar_contrasenya'))

    if request.method == "POST":
        nova_contrasenya = request.form.get("contrasenya")
        confirmar_contrasenya = request.form.get("confirmar_contrasenya")

        if not nova_contrasenya or len(nova_contrasenya) < 6:
            flash(traduir("La contrasenya ha de tenir mínim 6 caràcters."), "error")
            return render_template('auth/reset_password.html', token=token)

        if nova_contrasenya != confirmar_contrasenya:
            flash(traduir("Les contrasenyes no coincideixen."), "error")
            return render_template('auth/reset_password.html', token=token)

        usuari.set_contrasenya(nova_contrasenya)
        usuari.eliminar_token_reset_password()

        try:
            db.session.commit()
            enviar_email_confirmacio_canvi_password(usuari)
            flash(traduir("Contrasenya canviada correctament! Ja pots iniciar sessió."), "success")
            return redirect(url_for('login.login'))
        except Exception as e:
            db.session.rollback()
            flash(traduir("Error canviant la contrasenya."), "error")
            return render_template('auth/reset_password.html', token=token)

    return render_template('auth/reset_password.html', token=token)
