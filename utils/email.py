from flask_mail import Mail, Message
from flask import render_template, current_app
from threading import Thread

mail = Mail()

def enviar_email_async(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print(f"✅ Email enviat correctament a {msg.recipients}")
        except Exception as e:
            print(f"❌ Error enviant email: {str(e)}")

def enviar_email(destinatari, assumpte, template_html, **kwargs):
    try:
        msg = Message(
            subject=assumpte,
            recipients=[destinatari],
            html=render_template(template_html, **kwargs),
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        app = current_app._get_current_object()
        Thread(target=enviar_email_async, args=(app, msg)).start()
        
        return True
    except Exception as e:
        print(f"❌ Error preparant email: {str(e)}")
        return False

def enviar_email_verificacio(usuari):
    token = usuari.generar_token_verificacio()
    url_verificacio = f"{current_app.config['BASE_URL']}/verificar-email/{token}"
    
    return enviar_email(
        destinatari=usuari.email,
        assumpte="Verifica el teu compte d'Adabida",
        template_html='emails/verificacio_email.html',
        usuari=usuari,
        url_verificacio=url_verificacio
    )

def enviar_email_reset_password(usuari):
    token = usuari.generar_token_reset_password()
    url_reset = f"{current_app.config['BASE_URL']}/reset-password/{token}"
    
    return enviar_email(
        destinatari=usuari.email,
        assumpte="Recupera la teva contrasenya d'Adabida",
        template_html='emails/reset_password.html',
        usuari=usuari,
        url_reset=url_reset
    )

def enviar_email_confirmacio_canvi_password(usuari):
    return enviar_email(
        destinatari=usuari.email,
        assumpte="Contrasenya canviada correctament",
        template_html='emails/confirmacio_canvi_password.html',
        usuari=usuari
    )