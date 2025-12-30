# routes/organitzacions/admin.py
# Funcions d'administració d'organitzacions migrades des de organitzacions.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from flask_babel import gettext as _
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_, or_
from models import db, Organitzacio, MembreOrganitzacio, Usuari, Entrada, SolicitudOrganitzacio, MissatgeOrganitzacio, Missatge
from datetime import datetime

admin_organitzacions_bp = Blueprint('organitzacions_admin', __name__, url_prefix='/organitzacions')

@admin_organitzacions_bp.route('/admin/<int:id>')
@login_required
def admin(id):
    """Panell d'administració de l'organització"""
    print(f"=== ACCEDINT A ADMIN ORGANITZACIÓ ID: {id} ===")
    
    # Buscar l'organització AMB els seus membres
    organitzacio = Organitzacio.query.options(
        db.joinedload(Organitzacio.membres).joinedload(MembreOrganitzacio.usuari)
    ).get_or_404(id)

    # Verificar que l'usuari és membre amb permisos d'admin
    membre = MembreOrganitzacio.query.filter_by(
        usuari_id=current_user.id,
        organitzacio_id=id,
        rol='admin'
    ).first()
    
    if not membre:
        flash('No tens permisos per administrar aquesta organització', 'error')
        return redirect(url_for('pagina_personal.pagina_personal'))
    
    entrades_compartides = Entrada.query.filter_by(
        organitzacio_compartida_id=id
    ).order_by(Entrada.data_creacio.desc()).all()

    solicituds_pendents = SolicitudOrganitzacio.query.filter_by(
        organitzacio_id=id,
        estat='pendent'
    ).order_by(SolicitudOrganitzacio.data_solicitud.desc()).all()

    missatges_organitzacio = MissatgeOrganitzacio.query.filter_by(
        organitzacio_id=id,
        tipus='rebut'
    ).order_by(MissatgeOrganitzacio.data_env.desc()).all()

    missatges_enviats_org = MissatgeOrganitzacio.query.filter_by(
        organitzacio_id=id,
        tipus='enviat'
    ).order_by(MissatgeOrganitzacio.data_env.desc()).all()
    
    return render_template('organitzacions/organitzacio_admin.html', 
                         organitzacio=organitzacio,
                         entrades_compartides=entrades_compartides,
                         solicituds_pendents=solicituds_pendents,
                         missatges_organitzacio=missatges_organitzacio,
                         missatges_enviats_org=missatges_enviats_org)

@admin_organitzacions_bp.route('/actualitzar/<int:id>', methods=['POST'])
@login_required
def actualitzar(id):
    """Actualitzar dades de l'organització"""
    try:
        organitzacio = Organitzacio.query.get_or_404(id)
        
        # Verificar permisos d'admin
        membre = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=id,
            rol='admin'
        ).first()
        
        if not membre:
            flash('No tens permisos per administrar aquesta organització', 'error')
            return redirect(url_for('pagina_personal.pagina_personal'))
        
        # Actualitzar camps del formulari
        organitzacio.nom = request.form.get('nom', organitzacio.nom)
        organitzacio.tipus = request.form.get('tipus', organitzacio.tipus)
        organitzacio.descripcio = request.form.get('descripcio', organitzacio.descripcio)
        
        db.session.commit()
        flash('Dades de l\'organització actualitzades correctament', 'success')
        
        return redirect(url_for('organitzacions_admin.admin', id=id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error actualitzant l\'organització: {str(e)}', 'error')
        return redirect(url_for('organitzacions_admin.admin', id=id))

@admin_organitzacions_bp.route('/canviar_rol', methods=['POST'])
@login_required 
def canviar_rol():
    """Canviar rol d'un membre"""
    try:
        data = request.get_json()
        membre_id = data.get('membre_id')
        nou_rol = data.get('nou_rol')
        
        membre = MembreOrganitzacio.query.get_or_404(membre_id)
        
        # Verificar que som admin de l'organització
        admin = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=membre.organitzacio_id,
            rol='admin'
        ).first()
        
        if not admin:
            return jsonify({'success': False, 'error': 'No tens permisos'})
        
        if nou_rol not in ['admin', 'entrevistador', 'adherit']:
            return jsonify({'success': False, 'error': 'Rol no vàlid'})
        
        membre.rol = nou_rol
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Rol canviat a {nou_rol}'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@admin_organitzacions_bp.route('/expulsar_membre', methods=['POST'])
@login_required
def expulsar_membre():
    """Expulsar membre de l'organització"""
    try:
        data = request.get_json()
        membre_id = data.get('membre_id')
        
        membre = MembreOrganitzacio.query.get_or_404(membre_id)
        
        # Verificar permisos
        admin = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=membre.organitzacio_id,
            rol='admin'
        ).first()
        
        if not admin:
            return jsonify({'success': False, 'error': 'No tens permisos'})
        
        # No permetre expulsar-se a un mateix
        if membre.usuari_id == current_user.id:
            return jsonify({'success': False, 'error': 'No et pots expulsar a tu mateix'})
        
        db.session.delete(membre)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Membre expulsat'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@admin_organitzacions_bp.route('/processar_solicitud', methods=['POST'])
@login_required
def processar_solicitud():
    """Acceptar o rebutjar sol·licitud"""
    try:
        data = request.get_json()
        solicitud_id = data.get('solicitud_id')
        accio = data.get('accio')  # 'acceptar' o 'rebutjar'
        
        solicitud = SolicitudOrganitzacio.query.get_or_404(solicitud_id)
        
        # Verificar permisos d'admin
        admin = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=solicitud.organitzacio_id,
            rol='admin'
        ).first()
        
        if not admin:
            return jsonify({'success': False, 'error': 'No tens permisos'})
        
        if accio == 'acceptar':
            # Crear membre nou
            nou_membre = MembreOrganitzacio(
                usuari_id=solicitud.usuari_id,
                organitzacio_id=solicitud.organitzacio_id,
                rol='adherit',  # Rol per defecte
                data_adhesio=datetime.utcnow()
            )
            db.session.add(nou_membre)
            
            # Actualitzar sol·licitud
            solicitud.estat = 'acceptada'
            solicitud.data_resposta = datetime.utcnow()
            solicitud.processat_per_id = current_user.id
            
            db.session.commit()
            print(f"SOL·LICITUD ACCEPTADA: {solicitud.usuari.nom} -> {solicitud.organitzacio.nom}")
            
            return jsonify({'success': True, 'message': 'Sol·licitud acceptada i usuari afegit'})
            
        elif accio == 'rebutjar':
            solicitud.estat = 'rebutjada'
            solicitud.data_resposta = datetime.utcnow()
            solicitud.processat_per_id = current_user.id
            
            db.session.commit()
            print(f"SOL·LICITUD REBUTJADA: {solicitud.usuari.nom} -> {solicitud.organitzacio.nom}")
            
            return jsonify({'success': True, 'message': 'Sol·licitud rebutjada'})
            
    except Exception as e:
        db.session.rollback()
        print(f"ERROR PROCESSANT SOL·LICITUD: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@admin_organitzacions_bp.route('/esborrar/<int:id>', methods=['POST'])
@login_required
def esborrar(id):
    """Esborrar organització completament"""
    print(f"=== INTENT ESBORRAR ORGANITZACIO ID: {id} ===")
    
    try:
        organitzacio = Organitzacio.query.get_or_404(id)
        print(f"Organització trobada: {organitzacio.nom}")
        
        # Verificar que som admin
        membre = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=id,
            rol='admin'
        ).first()
        
        if not membre:
            print("ERROR: No tens permisos")
            return jsonify({'success': False, 'error': 'No tens permisos'})
        
        print("Permisos OK - Esborrant organització...")
        
        # Esborrar organització (cascade esborrarà membres automàticament)
        nom_org = organitzacio.nom
        db.session.delete(organitzacio)
        db.session.commit()
        
        print(f"✅ Organització {nom_org} esborrada!")
        return jsonify({'success': True, 'message': f'Organització "{nom_org}" esborrada'})
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# ========================
# FUNCIONS MISSATGERIA ORGANITZACIÓ
# ========================

@admin_organitzacions_bp.route('/api/missatge/<int:missatge_id>')
@login_required
def api_missatge_organitzacio(missatge_id):
    """Obtenir dades d'un missatge d'organització"""
    try:
        missatge = MissatgeOrganitzacio.query.options(
            db.joinedload(MissatgeOrganitzacio.emissor),
            db.joinedload(MissatgeOrganitzacio.organitzacio)
        ).get_or_404(missatge_id)
        
        # Verificar que l'usuari té permisos (admin de l'organització)
        admin = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=missatge.organitzacio_id,
            rol='admin'
        ).first()
        
        if not admin:
            return jsonify({'success': False, 'error': 'No tens permisos'})
        
        return jsonify({
            'success': True,
            'missatge': {
                'id': missatge.id,
                'assumpte': missatge.assumpte,
                'contingut': missatge.contingut,
                'emissor_nom': f"{missatge.emissor.nom} {missatge.emissor.primer_cognom}".strip(),
                'emissor_login': missatge.emissor.nom_login,
                'data_env': missatge.data_env.strftime('%d/%m/%Y %H:%M'),
                'llegit': missatge.llegit
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@admin_organitzacions_bp.route('/marcar_llegit/<int:missatge_id>', methods=['POST'])
@login_required
def marcar_llegit_organitzacio(missatge_id):
    """Marcar missatge com llegit"""
    try:
        missatge = MissatgeOrganitzacio.query.get_or_404(missatge_id)
        
        # Verificar permisos
        admin = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=missatge.organitzacio_id,
            rol='admin'
        ).first()
        
        if not admin:
            return jsonify({'success': False, 'error': 'No tens permisos'})
        
        missatge.llegit = True
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@admin_organitzacions_bp.route('/enviar_missatge', methods=['POST'])
@login_required
def enviar_missatge_organitzacio():
    """Enviar missatge com a organització"""
    try:
        data = request.get_json()
        org_id = data.get('organitzacio_id')
        receptor_login = data.get('receptor_login')
        assumpte = data.get('assumpte')
        contingut = data.get('contingut')
        
        # Verificar permisos d'admin
        admin = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=org_id,
            rol='admin'
        ).first()
        
        if not admin:
            return jsonify({'success': False, 'error': 'No tens permisos'})
        
        # Trobar usuari destinatari
        receptor = Usuari.query.filter_by(nom_login=receptor_login).first()
        if not receptor:
            return jsonify({'success': False, 'error': 'Usuari no trobat'})
        
        # Crear missatge individual (a la bústia personal de l'usuari)
        missatge_individual = Missatge(
            emissor_id=current_user.id,  # L'admin que envia
            receptor_id=receptor.id,
            assumpte=f"[{admin.organitzacio.nom}] {assumpte}",
            contingut=f"Missatge de l'organització {admin.organitzacio.nom}:\n\n{contingut}"
        )
        db.session.add(missatge_individual)
        
        # Crear còpia a la bústia de l'organització
        missatge_org = MissatgeOrganitzacio(
            organitzacio_id=org_id,
            emissor_id=receptor.id,  # Per identificar qui ha rebut el missatge
            receptor_id=current_user.id,  # L'admin que l'ha enviat
            assumpte=assumpte,
            contingut=contingut,
            tipus='enviat'  # Per distingir enviats vs rebuts
        )
        db.session.add(missatge_org)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Missatge enviat correctament'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@admin_organitzacions_bp.route('/eliminar_missatge/<int:missatge_id>', methods=['POST'])
@login_required
def eliminar_missatge_organitzacio(missatge_id):
    """Eliminar missatge rebut per l'organització"""
    try:
        missatge = MissatgeOrganitzacio.query.get_or_404(missatge_id)
        
        # Verificar permisos
        admin = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=missatge.organitzacio_id,
            rol='admin'
        ).first()
        
        if not admin:
            return jsonify({'success': False, 'error': 'No tens permisos'})
        
        db.session.delete(missatge)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})
        
@admin_organitzacions_bp.route('/eliminar_missatge_enviat/<int:missatge_id>', methods=['POST'])
@login_required
def eliminar_missatge_enviat_organitzacio(missatge_id):
    """Eliminar missatge enviat per l'organització"""
    try:
        missatge = MissatgeOrganitzacio.query.get_or_404(missatge_id)
        
        # Verificar permisos
        admin = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=missatge.organitzacio_id,
            rol='admin'
        ).first()
        
        if not admin:
            return jsonify({'success': False, 'error': 'No tens permisos'})
        
        db.session.delete(missatge)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@admin_organitzacions_bp.route('/<slug>/pujar-imatge-card', methods=['POST'])
@login_required
def pujar_imatge_card(slug):
    """Pujar imatge personalitzada per un card"""
    import os
    try:
        organitzacio = Organitzacio.query.filter_by(url_publica=slug).first_or_404()
        
        # Verificar que és admin
        es_membre = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=organitzacio.id
        ).first()
        
        if not es_membre or es_membre.rol != 'admin':
            return jsonify({'success': False, 'error': 'No tens permisos'}), 403
        
        # Obtenir dades
        card_type = request.form.get('card_type')
        imatge = request.files.get('imatge')
        
        if not card_type or not imatge:
            return jsonify({'success': False, 'error': 'Falten dades'}), 400
        
        # Validar tipus card
        camps_permesos = ['home', 'historia', 'entrades', 'membres', 'imatges']
        if card_type not in camps_permesos:
            return jsonify({'success': False, 'error': 'Tipus de card invàlid'}), 400
        
        # Guardar imatge
        from werkzeug.utils import secure_filename
        filename = secure_filename(imatge.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
        
        # Nom final: org_{id}_card_{tipus}.{ext}
        nom_final = f"org_{organitzacio.id}_card_{card_type}.{ext}"
        
        # Crear carpeta si no existeix
        carpeta = os.path.join('static', 'cards_organitzacio')
        os.makedirs(carpeta, exist_ok=True)
        
        # Guardar fitxer
        ruta_completa = os.path.join(carpeta, nom_final)
        imatge.save(ruta_completa)
        
        # Actualitzar BD
        camp_bd = f'imatge_card_{card_type}'
        setattr(organitzacio, camp_bd, nom_final)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Imatge guardada correctament'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error pujant imatge card organització: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500