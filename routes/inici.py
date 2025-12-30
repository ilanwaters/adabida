from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_babel import _
from models import EntradaBlog, db, ImatgeGaleria
from sqlalchemy import func
import os
import datetime
import random
from sqlalchemy.orm import joinedload
from models import Entrada, Exposicio
from flask_login import current_user

inici_bp = Blueprint("inici", __name__)

def obtenir_entrades_aleatories(limit=10):
    """
    Obté entrades aleatòries de manera eficient.
    Genera IDs aleatoris i fa query directa.
    """
    # Obtenir min i max ID
    min_id = db.session.query(func.min(Entrada.id)).scalar()
    max_id = db.session.query(func.max(Entrada.id)).scalar()
    
    if not min_id or not max_id:
        return []
    
    # Generar IDs aleatoris (generem més per si alguns no existeixen)
    ids_aleatoris = random.sample(range(min_id, max_id + 1), min(limit * 3, max_id - min_id + 1))
    
    # Query directa amb IDs
    entrades = (
        Entrada.query
        .options(joinedload(Entrada.usuari))
        .filter(Entrada.id.in_(ids_aleatoris))
        .limit(limit)
        .all()
    )
    
    return entrades

@inici_bp.route("/")
def inici_pagina():
    print("💬 Sessió activa?", session.get("usuari_id"))
    if current_user.is_authenticated and "usuari_id" not in session:
        session["usuari_id"] = current_user.id
        session["nom_login"] = current_user.nom_login
    base_path = os.path.join("umberto", "media", "galeria")
    imatges_destacades = []
    exposicions = Exposicio.query.order_by(Exposicio.id.desc()).all()
    exposicions_extra = []

    imatges = (
        ImatgeGaleria.query
        .options(joinedload(ImatgeGaleria.entrada).joinedload(Entrada.usuari))
        .filter(ImatgeGaleria.destinacio.in_(["galeria", "inici"]))
        .order_by(ImatgeGaleria.data_publicacio.desc())
        .all()
    )

    for img in imatges:
        any_mes = img.data_publicacio.strftime('%Y/%m')
        ruta_fitxer = os.path.join(base_path, any_mes, img.nom_fitxer)

        if os.path.exists(ruta_fitxer):
            if img.nom_fitxer.startswith("expo_"):
                exposicions_extra.append({
                    "titol": img.nom_fitxer.replace("expo_", "").split(".")[0].capitalize(),
                    "descripcio": "Col·lecció especial",
                    "carpeta": f"galeria/{any_mes}/{img.nom_fitxer}".replace("\\", "/")
                })
            else:
                imatges_destacades.append(img)

    mostrar_login = session.pop("mostrar_login", False)

    entrades_blog = (
        EntradaBlog.query
        .order_by(EntradaBlog.data_creacio.desc())
        .limit(10)
        .all()
    )

    any_ = func.extract('year', EntradaBlog.data_creacio).label("any")
    mes = func.extract('month', EntradaBlog.data_creacio).label("mes")
    mesos_disponibles = (
        db.session.query(any_, mes)
        .group_by(any_, mes)
        .order_by(any_.desc(), mes.desc())
        .all()
    )

    for exposicio in exposicions:
        exposicio.carpeta = exposicio.carpeta.replace("\\", "/")
    
    # Obtenir entrades aleatòries
    entrades_aleatories = obtenir_entrades_aleatories(10)

    for entrada in entrades_aleatories:
        print(f"DEBUG Entrada {entrada.id}: miniatura={entrada.miniatura}, imatge_gran={entrada.imatge_gran}")  
        
    return render_template(
        "inici.html",
        imatges_destacades=imatges_destacades,
        exposicions=exposicions,
        exposicions_extra=exposicions_extra,
        mostrar_login=mostrar_login,
        entrades_blog=entrades_blog,
        mesos_disponibles=mesos_disponibles,
        datetime=datetime.datetime,
        entrades_aleatories=entrades_aleatories
    )



@inici_bp.route("/manifest")
def manifest():
    return render_template("manifest_etic.html")

@inici_bp.route("/set_language/<idioma>")
def set_language(idioma: str):
    idiomes_permesos = ["ca", "es", "en", "fr", "de", "ru", "eu", "uk"]
    if idioma in idiomes_permesos:
        session["idioma"] = idioma
    return redirect(request.referrer or url_for("inici.inici_pagina"))

@inici_bp.route("/api/entrades-aleatories")
def api_entrades_aleatories():
    """
    API per obtenir noves entrades aleatòries (botó refresh)
    """
    limit = request.args.get('limit', 10, type=int)
    entrades = obtenir_entrades_aleatories(limit)
    
    return jsonify({
        'entrades': [{
            'id': e.id,
            'titol': e.titol,
            'subtitol': e.subtitol,
            'resum': e.resum,
            'data': e.data.strftime('%d/%m/%Y') if e.data else '',
            'miniatura': e.miniatura or '/static/icons/sense_imatge.png',  # ← AFEGEIX
            'imatge_gran': e.imatge_gran,  # ← AFEGEIX
            'usuari': {
                'nom': e.usuari.nom if e.usuari else 'Anònim',
                'nom_login': e.usuari.nom_login if e.usuari else 'anonim',  # ← AFEGEIX
                'bandera': e.usuari.bandera_preferida if e.usuari else None
            },
            'ubicacio': {
                'municipi': e.municipi_origen,
                'regio': e.regio_origen,
                'pais': e.pais_origen
            }
        } for e in entrades]
    })


@inici_bp.route('/benvinguts')
def benvinguts():
    idioma = session.get('idioma', 'ca')
    try:
        return render_template(f'benvinguts/benvinguts_{idioma}.html')
    except:
        return render_template('benvinguts/benvinguts_ca.html')