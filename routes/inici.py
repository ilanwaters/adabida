from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_babel import _
from models import EntradaBlog, db, ImatgeGaleria
from sqlalchemy import func
import os
import datetime
import random
from sqlalchemy.orm import joinedload
from models import Entrada, Exposicio, Conversa
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
    
    # Query amb ordre aleatori real a nivell de base de dades
    entrades = (
        Entrada.query
        .options(joinedload(Entrada.usuari))
        .order_by(func.random())
        .limit(limit)
        .all()
    )
    return entrades

def preparar_conversa_per_vista(conversa, usuari_nom_login):
    """Converteix una Conversa en format dict per renderitzar com caixa"""
    # Obtenir nom del participant principal
    participant_nom = "Desconegut"
    if conversa.participants:
        primer = conversa.participants[0]
        participant_nom = f"{primer.nom} {primer.primer_cognom or ''} {primer.segon_cognom or ''}".strip()
    
    # Construir lloc
    parts_lloc = [conversa.lloc_municipi, conversa.lloc_regio, conversa.lloc_pais]
    lloc = ", ".join([p for p in parts_lloc if p]) or None
    
    # Extreure any
    any = conversa.data_conversa.year if conversa.data_conversa else None
    
    # Resum del contingut
    resum = ""
    if conversa.contingut:
        import re
        contingut_net = re.sub(r'<[^>]+>', '', conversa.contingut)
        contingut_net = contingut_net.replace('&nbsp;', ' ').replace('&amp;', '&')
        resum = contingut_net[:120] + "..." if len(contingut_net) > 120 else contingut_net
    
    return {
        "id": conversa.id,
        "tipus": "conversa",
        "participant_nom": participant_nom,
        "tema": conversa.tema,
        "any": any,
        "lloc": lloc,
        "durada_minuts": conversa.durada_minuts,
        "resum": resum,
        "data": conversa.data_conversa.strftime("%d/%m/%Y") if conversa.data_conversa else conversa.created_at.strftime("%d/%m/%Y"),
        "miniatura": "/static/icons/entrevista.svg",
        "usuari": conversa.usuari
    }

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

    # Obtenir converses aleatòries
    min_id_conv = db.session.query(func.min(Conversa.id)).scalar()
    max_id_conv = db.session.query(func.max(Conversa.id)).scalar()

    converses_aleatories = []
    if min_id_conv and max_id_conv:
        ids_aleatoris_conv = random.sample(range(min_id_conv, max_id_conv + 1), min(5 * 3, max_id_conv - min_id_conv + 1))
        converses_raw = (
            Conversa.query
            .options(joinedload(Conversa.usuari))
            .filter(Conversa.id.in_(ids_aleatoris_conv))
            .limit(5)
            .all()
        )
        
        for conversa in converses_raw:
            conv_dict = preparar_conversa_per_vista(conversa, conversa.usuari.nom_login if conversa.usuari else 'anonim')
            converses_aleatories.append(conv_dict)

    # Barrejar entrades + converses
    contingut_aleatori = entrades_aleatories[:5] + converses_aleatories[:5]
    random.shuffle(contingut_aleatori)   
        
    return render_template(
        "inici.html",
        imatges_destacades=imatges_destacades,
        exposicions=exposicions,
        exposicions_extra=exposicions_extra,
        mostrar_login=mostrar_login,
        entrades_blog=entrades_blog,
        mesos_disponibles=mesos_disponibles,
        datetime=datetime.datetime,
        entrades_aleatories=contingut_aleatori
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
            'data': e.data_creacio.strftime('%d/%m/%Y') if e.data_creacio else '',
            'miniatura': e.miniatura or '/static/icons/sense_imatge.png',
            'imatge_gran': e.imatge_gran,
            'usuari': {
                'nom': e.usuari.nom if e.usuari else 'Anònim',
                'nom_login': e.usuari.nom_login if e.usuari else 'anonim',
                'bandera': e.usuari.bandera_preferida if e.usuari else None
            },
            'ubicacio': {
                'municipi': e.municipi,
                'regio': e.regio,
                'pais': e.pais
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