from flask import Blueprint, render_template, session, redirect, url_for, flash, request, abort, send_from_directory
from flask_babel import _
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from models import db
from models.usuari import Usuari
from models.entrades import Exposicio, ImatgeGaleria
from models.entrades import Entrada
from genera_identificadors import genera_codi_expo
from utils.paisos import normalitza_pais

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def pagina_admin():
    usuari_login = session.get("usuari")
    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()

    if not usuari or not usuari.es_admin:
        flash("Accés restringit")
        return redirect(url_for("inici.inici_pagina"))

    return render_template("admin/admin.html")

@admin_bp.route("/admin/nova_exposicio")
def nova_exposicio():
    return render_template("admin/nova_exposicio.html")

@admin_bp.route("/guardar_exposicio", methods=["POST"])
def guardar_exposicio():
    titol = request.form.get("titol")
    descripcio = request.form.get("descripcio")
    imatge = request.files.get("imatge")
    
    # De moment fixem el país a Espanya
    pais_raw = "espanya"
    pais_normalitzat = normalitza_pais(pais_raw)
    
    # Generar codi únic per l’expo
    codi_expo = genera_codi_expo(pais_normalitzat, titol)
    
    # Crear carpeta on guardar imatges
    now = datetime.now()
    any_str = now.strftime("%Y")
    mes_str = now.strftime("%m")
    carpeta_expo = os.path.join("umberto", "media", "expo", pais_normalitzat, any_str, mes_str, codi_expo)
    carpeta_expo = carpeta_expo.replace("\\", "/")

    os.makedirs(carpeta_expo, exist_ok=True)
    # Guardar imatge de portada
    if imatge:
        nom_imatge = secure_filename("portada.jpg")
        imatge.save(os.path.join(carpeta_expo, nom_imatge))

    # Desa a base de dades
    nova_expo = Exposicio(
        titol=titol,
        descripcio=descripcio,
        codi=codi_expo,
        pais=pais_normalitzat,
        any=int(any_str),
        mes=int(mes_str),
        carpeta=os.path.join("expo", pais_normalitzat, any_str, mes_str, codi_expo).replace("\\", "/")
    )
    db.session.add(nova_expo)
    db.session.commit()

    # Redirigir a la pàgina d’administració d’aquesta exposició
    return redirect(url_for('admin.control_expo', id=nova_expo.id))

@admin_bp.route("/admin/expo/<int:id>")
def control_expo(id):
    expo = Exposicio.query.get_or_404(id)
    return render_template("admin/control_expo.html", expo=expo)

@admin_bp.route("/admin/exposicions")
def admin_exposicions():
    exposicions = Exposicio.query.all()

    # Recollim els valors únics
    paisos = sorted(set([e.pais for e in exposicions]))
    anys = sorted(set([e.any for e in exposicions]), reverse=True)
    mesos = sorted(set([e.mes for e in exposicions]))

    return render_template(
        "admin/admin_expo.html",
        exposicions=exposicions,
        paisos=paisos,
        anys=anys,
        mesos=mesos
    )

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "umberto"))
@admin_bp.route("/admin/umberto/")
@admin_bp.route("/admin/umberto/<path:subpath>")
def navegador_umberto(subpath=""):
    ruta = os.path.join(BASE_PATH, subpath)

    if not os.path.exists(ruta) or not os.path.isdir(ruta):
        abort(404)

    contingut = os.listdir(ruta)
    carpetes = [f for f in contingut if os.path.isdir(os.path.join(ruta, f))]

    fitxers = []
    for f in contingut:
        ruta_fitxer = os.path.join(ruta, f)
        if os.path.isfile(ruta_fitxer):
            info = ImatgeGaleria.query.filter_by(nom_fitxer=f).first()

            usuari_login = ""
            entrada_id = ""

            if info and info.entrada_id:
                entrada = Entrada.query.get(info.entrada_id)
                if entrada and entrada.usuari:
                    usuari_login = entrada.usuari.nom_login
                    entrada_id = str(entrada.id)

            print("🧾 f.nom:", f)
            print("📁 f.ruta generada:", os.path.join(subpath, f))
            print("🧪 DEBUG FITXER:", f)
            print("    ➤ info:", info)
            print("    ➤ usuari_login:", usuari_login)
            print("    ➤ entrada_id:", entrada_id)
            print("    ➤ ruta_api:", f"/umberto/{usuari_login}/{entrada_id}/{f}" if usuari_login and entrada_id else None)

            fitxers.append({
                "nom": f,
                "ruta": os.path.join(subpath, f).replace("\\", "/"),
                "autor": info.usuari.nom_complet if info and info.usuari else "—",
                "data": info.data_publicacio.strftime("%Y-%m-%d") if info and info.data_publicacio else "—",
                "tipus": "imatge" if f.lower().endswith((".jpg", ".jpeg", ".png")) else "altre",
                "ruta_api": f"/umberto/{usuari_login}/{entrada_id}/{f}" if usuari_login and entrada_id else None
            })

    return render_template(
        "admin/admin_umberto.html",
        ruta_actual=subpath,
        carpetes=carpetes,
        fitxers=fitxers
    )
