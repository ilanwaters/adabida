from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Usuari, PerfilBiografic
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_babel import _ as traduir
from utils.paisos import normalitza_pais
from utils.email import enviar_email_verificacio
import os
from datetime import datetime
from genera_identificadors import genera_identificador, extreu_dades_identificador
import re


registre_individual_routes = Blueprint("registre_individual", __name__)

@registre_individual_routes.route("/avis-legal")
def avis_legal():
    return render_template("abadia_principal/avis_legal.html")

@registre_individual_routes.route("/registre_individual", methods=["GET", "POST"])
 

@registre_individual_routes.route("/registre_individual", methods=["GET", "POST"])
def registre_individual():
    if request.method == "POST":
        nom = request.form["nom"]
        primer_cognom = request.form["primer_cognom"]
        segon_cognom = request.form["segon_cognom"]
        data = request.form["data"]
        municipi_naixement = request.form.get("municipi")
        regio_naixement = request.form.get("regio")
        pais_naixement = request.form["pais"]
        idioma = request.form["idioma"]
        pais_residencia_raw = request.form["pais_residencia"]
        pais_residencia = normalitza_pais(pais_residencia_raw)
        email = request.form["direccion_email"]
        nom_login = request.form["nom_login"]
        contrasenya = request.form.get("contrasenya", "")
        confirmar = request.form.get("confirmar_contrasenya", "")

        if Usuari.query.filter_by(nom_login=nom_login).first():
            flash(traduir("Aquest nom d’usuari ja està registrat"))
            return render_template("registre_individual.html", dades=request.form)

        if Usuari.query.filter_by(email=email).first():
            flash(traduir("Aquest correu electrònic ja està registrat"))
            return render_template("registre_individual.html", dades=request.form)

        if contrasenya != confirmar:
            return render_template("registre_individual.html", dades=request.form,
                                   error_contrasenya=traduir("Les contrasenyes no coincideixen"))

        if len(contrasenya) < 8 or not re.search(r"[A-Za-z]", contrasenya) or not re.search(r"\d", contrasenya):
            return render_template(
                "registre_individual.html",
                dades=request.form,
                error_contrasenya=traduir("La contrasenya ha de tenir com a mínim 8 caràcters, incloent lletres i números.")
            )

        nou = Usuari(
            nom_login=nom_login,
            email=email,
            nom=nom,
            primer_cognom=primer_cognom,
            segon_cognom=segon_cognom,
            data_naixement=datetime.strptime(data, "%Y-%m-%d").date(),
            municipi_naixement=municipi_naixement,
            regio_naixement=regio_naixement,
            pais_naixement=pais_naixement,
            idioma=idioma,
            pais_residencia=pais_residencia,
            contrasenya_hash=generate_password_hash(contrasenya),
            email_verificat=False
        )
        nou.identificador_abadia = genera_identificador(nou)
        nou.generar_token_verificacio()

        try:
            db.session.add(nou)
            db.session.flush()  
          
            perfil = PerfilBiografic(
                usuari_id=nou.id,
                codi_identificacio=nou.identificador_abadia,

              
                pais_naixement=pais_naixement,
                regio_naixement=regio_naixement,
                municipi_naixement=municipi_naixement,
                data_naixement=datetime.strptime(data, "%Y-%m-%d").date() if data else None,

        
                pare_nom=request.form.get("pare_nom"),
                pare_primer_cognom=request.form.get("pare_primer_cognom"),
                pare_segon_cognom=request.form.get("pare_segon_cognom"),
                pare_data_naixement=request.form.get("pare_data_naixement") or None,
                pare_data_defuncio=request.form.get("pare_data_defuncio") or None,
                pare_municipi_naixement=request.form.get("municipi_naixement_pare"),
                pare_regio_naixement=request.form.get("regio_naixement_pare"),
                pare_pais_naixement=request.form.get("pais_naixement_pare"),
                pare_municipi_defuncio=request.form.get("municipi_defuncio_pare"),
                pare_regio_defuncio=request.form.get("regio_defuncio_pare"),
                pare_pais_defuncio=request.form.get("pais_defuncio_pare"),
                mare_nom=request.form.get("mare_nom"),
                mare_primer_cognom=request.form.get("mare_primer_cognom"),
                mare_segon_cognom=request.form.get("mare_segon_cognom"),
                mare_data_naixement=request.form.get("mare_data_naixement") or None,
                mare_data_defuncio=request.form.get("mare_data_defuncio") or None,
                mare_municipi_naixement=request.form.get("municipi_naixement_mare"),
                mare_regio_naixement=request.form.get("regio_naixement_mare"),
                mare_pais_naixement=request.form.get("pais_naixement_mare"),
                mare_municipi_defuncio=request.form.get("municipi_defuncio_mare"),
                mare_regio_defuncio=request.form.get("regio_defuncio_mare"),
                mare_pais_defuncio=request.form.get("pais_defuncio_mare"),
            )
            db.session.add(perfil)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print("❌ ERROR AL GUARDAR:", e)
            flash(traduir("Error en desar el perfil."))
            return redirect(url_for("registre_individual.registre_individual"))

        _, any_str, mes_str = extreu_dades_identificador(nou.identificador_abadia)
        carpeta_usuari = os.path.join("umberto", "usuaris", pais_residencia, any_str, mes_str, nom_login)
        os.makedirs(carpeta_usuari, exist_ok=True)
        carpeta_docs = os.path.join(carpeta_usuari, "Documentacio personal")
        os.makedirs(carpeta_docs, exist_ok=True)

        carpeta_temp = os.path.join("umberto", "media", "temp", pais_residencia, any_str, mes_str, nom_login)
        os.makedirs(carpeta_temp, exist_ok=True)

        documents = request.files.getlist("documents")
        for i, arxiu in enumerate(documents):
            if arxiu.filename:
                nom_arxiu = secure_filename(f"{nom_login}_doc{i+1}_{arxiu.filename}")
                ruta_final = os.path.join(carpeta_docs, nom_arxiu)
                arxiu.save(ruta_final)
                print(f"✅ Document desat: {ruta_final}")

        # Enviar email de verificació
        if enviar_email_verificacio(nou):
            db.session.commit()
            return render_template("auth/registre_complet.html", email=email)
        else:
            db.session.rollback()
            flash(traduir("Perfil creat, però hi ha hagut un problema enviant l'email de verificació."), "warning")
            return redirect(url_for("auth.reenviar_verificacio"))

    return render_template("registre_individual.html", dades={})
