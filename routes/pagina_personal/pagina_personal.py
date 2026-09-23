from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request, abort
from models import db, Usuari, Entrada, Experiencia, Estudi, Obra, CarrecPublic, MembreOrganitzacio, Organitzacio
from flask_babel import _
import os
from utils.text_biografic import generar_biografia_entrevista
from flask_login import current_user, login_required
from models import PerfilBiografic, ImatgeGaleria, Missatge
from sqlalchemy import or_
from utils import generar_miniatura_entrada
import re
from sqlalchemy import cast, Integer
import pycountry
from datetime import datetime
from models import Pais, Regio, Municipi, Conversa
from datetime import datetime, date

pagina_personal_bp = Blueprint("pagina_personal", __name__)

import pycountry

# Mapeo manual per banderes no-oficials
BANDERES_CUSTOM = {
    'CAT': 'Catalunya',
    'EUS': 'Euskadi', 
    'KUR': 'Kurdistan',
    'PAL': 'Palestina'
}

def obtenir_banderes_disponibles(app):
    """Obté totes les banderes disponibles a /static/banderes/"""
    banderes_dir = os.path.join(app.static_folder, 'banderes')
    banderes = []
    
    if not os.path.exists(banderes_dir):
        return banderes
    
    for fitxer in sorted(os.listdir(banderes_dir)):
        if fitxer.endswith('.svg'):
            codi = fitxer.replace('.svg', '')
            
            # Mirar si és custom
            if codi in BANDERES_CUSTOM:
                nom = BANDERES_CUSTOM[codi]
            else:
                # Buscar amb pycountry
                try:
                    pais = pycountry.countries.get(alpha_2=codi.upper())
                    nom = pais.name if pais else codi
                except:
                    nom = codi
            
            banderes.append({'codi': codi, 'nom': nom})
    
    return banderes

@pagina_personal_bp.route("/pagina_personal")
def pagina_personal():

    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get(usuari_id)
    if not usuari:
        flash(_("Usuari inexistent"))
        return redirect(url_for("login.login"))
    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()
    experiencies = Experiencia.query.filter_by(perfil_id=perfil.id).order_by(Experiencia.ordre).all() if perfil else []
    estudis = Estudi.query.filter_by(perfil_id=perfil.id).order_by(Estudi.ordre).all() if perfil else []
    obres = Obra.query.filter_by(perfil_id=perfil.id).order_by(Obra.any.desc()).all() if perfil else []
    carrecs = CarrecPublic.query.filter_by(perfil_id=perfil.id).order_by(CarrecPublic.any_inici.desc()).all() if perfil else []
    missatges = (
        Missatge.query
            .filter(
            or_(
                Missatge.receptor_id == usuari.id,
                Missatge.emissor_id == usuari.id
            )
        )
        .order_by(Missatge.data_env.desc())
        .all()
    )
    for m in missatges:
        print("-", m.assumpte, "de", m.emissor_id)

    if not perfil:
        flash(_("Encara no has creat la teva fitxa biogràfica"))
        text_biografic = ""
    else:
        text_biografic = generar_biografia_entrevista(perfil.id)


# Obtenir entrades
    entrada_ids_amb_conversa = [c.entrada_id for c in Conversa.query.filter(Conversa.entrada_id.isnot(None)).all()]
    entrades_raw = Entrada.query.filter_by(usuari_id=usuari.id, es_publica=True).filter(~Entrada.id.in_(entrada_ids_amb_conversa)).all()
    entrades = []
    for entrada in entrades_raw:
        miniatura = generar_miniatura_entrada(entrada, usuari.nom_login)
        entrades.append({
            "id": entrada.id,
            "tipus": "entrada",
            "titol": entrada.titol,
            "tema": entrada.tema,
            "any": entrada.any_text,
            "lloc": None,  # TODO: construir lloc igual que a repositori
            "resum": entrada.contingut[:120] + "..." if entrada.contingut else "",
            "data": entrada.data_creacio.strftime("%d/%m/%Y") if entrada.data_creacio else "",
            "data_ordenacio": entrada.data_creacio or datetime.min,
            "miniatura": miniatura,
            "usuari": entrada.usuari
        })

    # Obtenir converses
    converses_raw = Conversa.query.filter_by(usuari_id=usuari.id).all()
    converses = []
    for conversa in converses_raw:
        conv_dict = preparar_conversa_per_vista(conversa, usuari.nom_login)
        conv_dict["data_ordenacio"] = conversa.data_conversa or conversa.created_at
        converses.append(conv_dict)

# Barrejar i ordenar per data

    def normalitza_data(d):
        if isinstance(d, datetime):
            return d
        elif isinstance(d, date):
            return datetime.combine(d, datetime.min.time())
        return datetime.min

    entrades = sorted(entrades + converses, key=lambda x: normalitza_data(x["data_ordenacio"]), reverse=True)

    # ✅ Obtenim la pestanya activa des de l'URL (per exemple: ?pestanya=entrades)
    pestanya_activa = request.args.get("pestanya", "biografia")  # Per defecte: biografia
    
    imatges_destacades = (
        ImatgeGaleria.query
        .filter(ImatgeGaleria.destinacio.in_(["galeria", "inici"]))
        .order_by(ImatgeGaleria.data_publicacio.desc())
        .all()
    )
    for img in imatges_destacades:
        print("— Fitxer:", img.nom_fitxer)
        print("— Data:", img.data_publicacio)
        print("— Entrada ID:", img.entrada_id)
        print("— Usuari:", img.entrada.usuari.nom_login if img.entrada and img.entrada.usuari else "❌ cap usuari")

    familia = (
        perfil and (
            perfil.pare_nom or perfil.mare_nom or
            perfil.pare_primer_cognom or perfil.mare_primer_cognom or
            perfil.pare_data_naixement or perfil.mare_data_naixement
        )
    )
    # Al final de la funció, abans del return render_template
    organitzacions_admin = []
    organitzacions_vistes = set()

    if usuari:  # Ja sabem que usuari existeix
        print(f"=== DEBUG ORGANITZACIONS USUARI {usuari.id} ===")
        # Necessitem carregar les membresies de l'usuari
        membresies = MembreOrganitzacio.query.filter_by(usuari_id=usuari.id).all()
        print(f"Total membresies: {len(membresies)}")
        for membre in membresies:
            print(f"Membre ID:{membre.id} | Org:{membre.organitzacio.nom} | Rol:{membre.rol} | OrgID:{membre.organitzacio.id}")
            if membre.rol == 'admin' and membre.organitzacio.id not in organitzacions_vistes:
                organitzacions_admin.append(membre)
                organitzacions_vistes.add(membre.organitzacio.id)
            
        print(f"Organitzacions admin úniques: {len(organitzacions_admin)}")
        print("=== FI DEBUG ===")
    else:
        membresies = []

    return render_template(
        "pagina_personal/pagina_personal.html",
        usuari=usuari,
        usuari_id=usuari.id,
        perfil=perfil,
        entrades=entrades,
        text_biografic=text_biografic,
        mode="crear",
        entrada=None,
        pestanya_activa=pestanya_activa,
        imatges_destacades=imatges_destacades,
        experiencies=experiencies,
        estudis=estudis,
        obres=obres,
        carrecs=carrecs,
        familia=familia,
        missatges=missatges,
        organitzacions_admin=organitzacions_admin,
        usuari_organitzacions=[m.organitzacio for m in membresies]
    )

@pagina_personal_bp.route("/eliminar_entrada/<int:entrada_id>", methods=["POST"])
def eliminar_entrada(entrada_id):
    entrada = Entrada.query.get(entrada_id)
    if not entrada:
        return "No trobada", 404

    db.session.delete(entrada)
    db.session.commit()
    return "", 204

@pagina_personal_bp.route("/pagina_personal/<int:perfil_id>")
def mostra_pagina_personal(perfil_id):
    usuari = Usuari.query.get(perfil_id)
    if not usuari:
        flash(_("Usuari inexistent"))
        return redirect(url_for("login.login"))

    # 🔍 Obtenim perfil i text biogràfic
    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()
    if not perfil:
        flash(_("Aquest perfil no té fitxa biogràfica"))
        return redirect(url_for("login.login"))

    text_biografic = generar_biografia_entrevista(perfil.id)

    entrades_raw = Entrada.query.filter_by(usuari_id=usuari.id).order_by(Entrada.data_creacio.desc()).all()
    entrades = []
    for entrada in entrades_raw:
        miniatura = generar_miniatura_entrada(entrada, usuari.nom_login)

        entrades.append({
            "id": entrada.id,
            "titol": entrada.titol,
            "any": entrada.any_text,
            "resum": entrada.contingut[:120] + "...",
            "data": entrada.data_creacio.strftime("%d/%m/%Y") if entrada.data_creacio else "",
            "miniatura": miniatura
        })

    missatges = Missatge.query.filter_by(receptor_id=usuari.id).order_by(Missatge.data_env.desc()).all()

    return render_template("pagina_personal.html", 
                       usuari=usuari, 
                       usuari_id=usuari.id, 
                       perfil=perfil,
                       entrades=entrades,
                       text_biografic=text_biografic,
                       mode="crear",
                       entrada=None,
                       pestanya_activa="biografia",  # o "entrades", com vulguis
                       imatges_destacades=[],
                       experiencies=[],
                       estudis=[],
                       obres=[],
                       carrecs=[],
                       familia=False,
                       missatges=missatges)


@pagina_personal_bp.route('/entrades')
def entrades():
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get(usuari_id)
    if not usuari:
        flash(_("Usuari inexistent"))
        return redirect(url_for("login.login"))

    # Obtenir entrades
    from models import Conversa
    entrada_ids_amb_conversa = [c.entrada_id for c in Conversa.query.filter(Conversa.entrada_id.isnot(None), Conversa.tipus_conversa == 'entrevista_adabida').all()]
    entrades_raw = Entrada.query.filter_by(usuari_id=usuari.id, es_publica=True).filter(~Entrada.id.in_(entrada_ids_amb_conversa)).all()
    entrades = []
    for entrada in entrades_raw:
        miniatura = generar_miniatura_entrada(entrada, usuari.nom_login)
        
        # Construir lloc
        parts_lloc = []
        if entrada.municipi:
            try:
                if entrada.municipi.isdigit():
                    mun = Municipi.query.get(int(entrada.municipi))
                    parts_lloc.append(mun.nom if mun else entrada.municipi)
                else:
                    parts_lloc.append(entrada.municipi)
            except:
                parts_lloc.append(entrada.municipi)
        
        if entrada.regio:
            try:
                if entrada.regio.isdigit():
                    reg = Regio.query.get(int(entrada.regio))
                    parts_lloc.append(reg.nom if reg else entrada.regio)
                else:
                    parts_lloc.append(entrada.regio)
            except:
                parts_lloc.append(entrada.regio)
        
        if entrada.pais:
            try:
                if entrada.pais.isdigit():
                    pai = Pais.query.get(int(entrada.pais))
                    parts_lloc.append(pai.nom if pai else entrada.pais)
                else:
                    parts_lloc.append(entrada.pais)
            except:
                parts_lloc.append(entrada.pais)
        
        lloc = ", ".join(parts_lloc) if parts_lloc else None
        
        # Netejar HTML
        resum = ""
        if entrada.contingut:
            contingut_net = re.sub(r'<[^>]+>', '', entrada.contingut)
            contingut_net = contingut_net.replace('&nbsp;', ' ').replace('&amp;', '&')
            resum = contingut_net[:120] + "..." if len(contingut_net) > 120 else contingut_net

        entrades.append({
            "id": entrada.id,
            "tipus": "entrada",
            "titol": entrada.titol,
            "tema": entrada.tema,
            "any": entrada.any_text,
            "lloc": lloc,
            "resum": resum,
            "data": entrada.data_creacio.strftime("%d/%m/%Y") if entrada.data_creacio else "",
            "data_ordenacio": entrada.data_creacio or datetime.min,
            "miniatura": miniatura,
            "usuari": entrada.usuari,
            "usuari_id": entrada.usuari_id
        })
    # Obtenir converses
    converses_raw = Conversa.query.join(Entrada, Conversa.entrada_id == Entrada.id).filter(Conversa.usuari_id == usuari.id, Conversa.tipus_conversa == 'entrevista_adabida', Entrada.es_publica == True).all()
    converses = []
    for conversa in converses_raw:
        conv_dict = preparar_conversa_per_vista(conversa, usuari.nom_login)
        conv_dict["data_ordenacio"] = conversa.data_conversa or conversa.created_at
        converses.append(conv_dict)

    # Barrejar i ordenar per data
    def normalitza_data(d):
        if isinstance(d, datetime):
            return d
        elif isinstance(d, date):
            return datetime.combine(d, datetime.min.time())
        return datetime.min

    entrades = sorted(entrades + converses, key=lambda x: normalitza_data(x["data_ordenacio"]), reverse=True)

    return render_template('pagina_personal/entrades.html', usuari=usuari, entrades=entrades)

@pagina_personal_bp.route('/nova_entrada')
def nova_entrada():
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get(usuari_id)
    if not usuari:
        flash(_("Usuari inexistent"))
        return redirect(url_for("login.login"))

    return render_template('pagina_personal/nova_entrada_distribuidor.html', usuari=usuari)
    
@pagina_personal_bp.route('/perfil')
def perfil():
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get(usuari_id)
    if not usuari:
        flash(_("Usuari inexistent"))
        return redirect(url_for("login.login"))

    # Carregar perfil
    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()
    
    # Carregar dades relacionades
    experiencies = Experiencia.query.filter_by(perfil_id=perfil.id).order_by(Experiencia.ordre).all() if perfil else []
    estudis = Estudi.query.filter_by(perfil_id=perfil.id).order_by(Estudi.ordre).all() if perfil else []
    obres = Obra.query.filter_by(perfil_id=perfil.id).order_by(Obra.any.desc()).all() if perfil else []
    carrecs = CarrecPublic.query.filter_by(perfil_id=perfil.id).order_by(CarrecPublic.any_inici.desc()).all() if perfil else []
    
    # Carregar missatges
    missatges = (
        Missatge.query
        .filter(or_(Missatge.receptor_id == usuari.id, Missatge.emissor_id == usuari.id))
        .order_by(Missatge.data_env.desc())
        .all()
    )
    
    # Carregar organitzacions admin
    organitzacions_admin = []
    organitzacions_vistes = set()
    if usuari:
        membresies = MembreOrganitzacio.query.filter_by(usuari_id=usuari.id).all()
        for membre in membresies:
            if membre.rol == 'admin' and membre.organitzacio.id not in organitzacions_vistes:
                organitzacions_admin.append(membre)
                organitzacions_vistes.add(membre.organitzacio.id)

    # Variable familia
    familia = (
        perfil and (
            perfil.pare_nom or perfil.mare_nom or
            perfil.pare_primer_cognom or perfil.mare_primer_cognom or
            perfil.pare_data_naixement or perfil.mare_data_naixement
        )
    )

    # Carregar entrades de l'usuari (copiat de pagina_personal original)
    entrada_ids_amb_conversa = [c.entrada_id for c in Conversa.query.filter(Conversa.entrada_id.isnot(None)).all()]
    entrades_raw = Entrada.query.filter_by(usuari_id=usuari.id).filter(~Entrada.id.in_(entrada_ids_amb_conversa)).order_by(Entrada.data_creacio.desc()).all()
    entrades = []
    for entrada in entrades_raw:
        miniatura = generar_miniatura_entrada(entrada, usuari.nom_login)

        entrades.append({
            "id": entrada.id,
            "titol": entrada.titol,
            "tema": entrada.tema,
            "any": entrada.any_text,
            "contingut": entrada.contingut,
            "data": entrada.data_creacio.strftime("%d/%m/%Y") if entrada.data_creacio else "",
            "miniatura": miniatura
        })
    from flask import current_app
    banderes = obtenir_banderes_disponibles(current_app)

    return render_template('pagina_personal/perfil.html',
                          usuari=usuari,
                          perfil=perfil,
                          missatges=missatges,
                          organitzacions_admin=organitzacions_admin,
                          experiencies=experiencies,
                          estudis=estudis,
                          obres=obres,
                          carrecs=carrecs,
                          familia=familia,
                          entrades=entrades,
                          banderes=banderes)

@pagina_personal_bp.route('/guardar_bandera', methods=['POST'])
def guardar_bandera():
    """Guarda la bandera preferida de l'usuari"""
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        return jsonify({'success': False, 'error': 'No autenticat'}), 401
    
    usuari = Usuari.query.get(usuari_id)
    if not usuari:
        return jsonify({'success': False, 'error': 'Usuari no trobat'}), 404
    
    data = request.get_json()
    bandera = data.get('bandera')
    
    if not bandera:
        return jsonify({'success': False, 'error': 'Bandera no especificada'}), 400
    
    # Guardar a BD
    usuari.bandera_preferida = bandera
    db.session.commit()
    
    return jsonify({'success': True, 'bandera': bandera})

def preparar_conversa_per_vista(conversa, usuari_nom_login):
    """Converteix una Conversa en format dict per renderitzar com caixa"""
    from utils import generar_miniatura_entrada
    
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
        "usuari_id": conversa.usuari_id,
        "entrada_id": conversa.entrada_id,
        "participant_nom": participant_nom,
        "tema": conversa.tema,
        "any": any,
        "lloc": lloc,
        "durada_minuts": conversa.durada_minuts,
        "resum": resum,
        "data": conversa.data_conversa.strftime("%d/%m/%Y") if conversa.data_conversa else conversa.created_at.strftime("%d/%m/%Y"),
        "miniatura": Entrada.query.get(conversa.entrada_id).miniatura if conversa.entrada_id else "/static/icons/entrevista.svg",
        "usuari": conversa.usuari
    }


@pagina_personal_bp.route('/pagina_personal/pujar-imatge-card', methods=['POST'])
def pujar_imatge_card():
    """Pujar imatge personalitzada per un card de l'espai personal"""
    try:
        card_type = request.form.get('card_type')
        imatge = request.files.get('imatge')
        if not card_type or not imatge:
            return jsonify({'success': False, 'error': 'Falten dades'}), 400

        camps_permesos = ['biografia', 'entrades', 'nova_entrada', 'perfil', 'organitzacions', 'familia', 'conversa']
        if card_type not in camps_permesos:
            return jsonify({'success': False, 'error': 'Tipus de card invàlid'}), 400

        from werkzeug.utils import secure_filename
        filename = secure_filename(imatge.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'

        nom_final = f"usuari_{current_user.id}_card_{card_type}.{ext}"

        carpeta = os.path.join('static', 'cards_personal')
        os.makedirs(carpeta, exist_ok=True)

        ruta_completa = os.path.join(carpeta, nom_final)
        imatge.save(ruta_completa)

        camp_bd = f'imatge_card_{card_type}'
        setattr(current_user, camp_bd, nom_final)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Imatge guardada correctament'})
    except Exception as e:
        db.session.rollback()
        print(f"Error pujant imatge card: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500