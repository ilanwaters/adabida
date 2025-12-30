# BLUEPRINT CONVERSES I DIÀLEGS
# Fitxer: routes/converses.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename
import uuid

from models import db, Conversa, ConversaParticipant, Organitzacio, MembreOrganitzacio

converses_bp = Blueprint('converses', __name__, url_prefix='/converses')

@converses_bp.route('/')
@login_required
def llistat():
    """Llistat de converses de l'usuari actual"""
    converses = Conversa.query.filter_by(usuari_id=current_user.id).order_by(
        Conversa.data_conversa.desc(), 
        Conversa.created_at.desc()
    ).all()
    
    return render_template('converses/llistat_converses.html', converses=converses)


@converses_bp.route('/nova', methods=['GET', 'POST'])
@login_required  
def nova_conversa():
    """Crear nova conversa/diàleg"""
    
    if request.method == 'GET':
        # Obtenir organitzacions de l'usuari per dropdown
        organitzacions = []
        membres = MembreOrganitzacio.query.filter_by(usuari_id=current_user.id).all()
        for membre in membres:
            organitzacions.append(membre.organitzacio)
        
        return render_template('converses/nova_conversa.html', organitzacions=organitzacions)
    
    # POST - Processar formulari
    try:
        # Crear conversa principal
        conversa = Conversa(
            usuari_id=current_user.id,
            lloc_municipi=request.form.get('lloc_municipi', '').strip(),
            lloc_regio=request.form.get('lloc_regio', '').strip(), 
            lloc_pais=request.form.get('lloc_pais', '').strip(),
            durada_minuts=int(request.form.get('durada_minuts', 0)) or None,
            observacions_generals=request.form.get('observacions_generals', '').strip()
        )
        
        # Processar data conversa
        data_str = request.form.get('data_conversa')
        if data_str:
            conversa.data_conversa = datetime.strptime(data_str, '%Y-%m-%d').date()
        
        # Organització (opcional)
        organitzacio_id = request.form.get('organitzacio_id')
        if organitzacio_id and organitzacio_id != '':
            conversa.organitzacio_id = int(organitzacio_id)
        
        # Processar arxiu multimèdia
        arxiu = request.files.get('arxiu')
        if arxiu and arxiu.filename:
            nom_arxiu = _guardar_arxiu_conversa(arxiu, conversa)
            conversa.arxiu_nom = nom_arxiu
            conversa.arxiu_tipus = _detectar_tipus_arxiu(arxiu.filename)
            conversa.arxiu_tamany = _obtenir_tamany_arxiu(arxiu)
        
        db.session.add(conversa)
        db.session.flush()  # Per obtenir l'ID
        
        # Processar participants
        participants_data = _processar_participants(request.form)
        for i, participant_data in enumerate(participants_data):
            if participant_data['nom'].strip():  # Només si té nom
                participant = ConversaParticipant(
                    conversa_id=conversa.id,
                    nom=participant_data['nom'].strip(),
                    lloc_municipi=participant_data.get('municipi', '').strip(),
                    lloc_regio=participant_data.get('regio', '').strip(),
                    lloc_pais=participant_data.get('pais', '').strip(),
                    observacions=participant_data.get('observacions', '').strip(),
                    ordre=i + 1
                )
                
                # Processar data naixement
                if participant_data.get('data_naixement'):
                    try:
                        participant.data_naixement = datetime.strptime(
                            participant_data['data_naixement'], '%Y-%m-%d'
                        ).date()
                    except ValueError:
                        pass  # Ignorar dates malformades
                
                db.session.add(participant)
        
        db.session.commit()
        flash('Conversa creada correctament!', 'success')
        return redirect(url_for('converses.llistat'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creant conversa: {e}")
        flash('Error creant la conversa. Torna-ho a provar.', 'error')
        return redirect(url_for('converses.nova_conversa'))


@converses_bp.route('/<int:id>')
@login_required
def detall_conversa(id):
    """Veure detalls d'una conversa"""
    conversa = Conversa.query.get_or_404(id)
    
    # Verificar permisos
    if conversa.usuari_id != current_user.id:
        # TODO: Verificar si l'usuari és admin d'organització compartida
        flash('No tens permisos per veure aquesta conversa.', 'error')
        return redirect(url_for('converses.llistat'))
    
    return render_template('converses/detall_conversa.html', conversa=conversa)


@converses_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_conversa(id):
    """Editar conversa existent"""
    conversa = Conversa.query.get_or_404(id)
    
    # Verificar permisos
    if conversa.usuari_id != current_user.id:
        flash('No tens permisos per editar aquesta conversa.', 'error')
        return redirect(url_for('converses.llistat'))
    
    if request.method == 'GET':
        organitzacions = []
        membres = MembreOrganitzacio.query.filter_by(usuari_id=current_user.id).all()
        for membre in membres:
            organitzacions.append(membre.organitzacio)
        
        return render_template('converses/editar_conversa.html', 
                             conversa=conversa, organitzacions=organitzacions)
    
    # POST - Actualitzar
    try:
        conversa.lloc_municipi = request.form.get('lloc_municipi', '').strip()
        conversa.lloc_regio = request.form.get('lloc_regio', '').strip()
        conversa.lloc_pais = request.form.get('lloc_pais', '').strip()
        conversa.durada_minuts = int(request.form.get('durada_minuts', 0)) or None
        conversa.observacions_generals = request.form.get('observacions_generals', '').strip()
        
        # Data
        data_str = request.form.get('data_conversa')
        if data_str:
            conversa.data_conversa = datetime.strptime(data_str, '%Y-%m-%d').date()
        
        # Organització
        organitzacio_id = request.form.get('organitzacio_id')
        conversa.organitzacio_id = int(organitzacio_id) if organitzacio_id else None
        
        conversa.updated_at = datetime.utcnow()
        
        # TODO: Actualitzar participants (més complex)
        
        db.session.commit()
        flash('Conversa actualitzada correctament!', 'success')
        return redirect(url_for('converses.detall_conversa', id=id))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error actualitzant conversa: {e}")
        flash('Error actualitzant la conversa.', 'error')
        return redirect(url_for('converses.editar_conversa', id=id))


@converses_bp.route('/<int:id>/esborrar', methods=['POST'])
@login_required
def esborrar_conversa(id):
    """Esborrar conversa"""
    conversa = Conversa.query.get_or_404(id)
    
    if conversa.usuari_id != current_user.id:
        flash('No tens permisos per esborrar aquesta conversa.', 'error')
        return redirect(url_for('converses.llistat'))
    
    try:
        # Esborrar arxiu físic si existeix
        if conversa.arxiu_nom:
            ruta_arxiu = os.path.join(current_app.config['UPLOAD_FOLDER'], conversa.ruta_arxiu)
            if os.path.exists(ruta_arxiu):
                os.remove(ruta_arxiu)
        
        db.session.delete(conversa)  # Els participants s'esborraran per cascade
        db.session.commit()
        flash('Conversa esborrada correctament.', 'success')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error esborrant conversa: {e}")
        flash('Error esborrant la conversa.', 'error')
    
    return redirect(url_for('converses.llistat'))


# FUNCIONS AUXILIARS
def _processar_participants(form_data):
    """Processar dades participants del formulari"""
    participants = []
    i = 0
    
    while f'participant_nom_{i}' in form_data:
        participant_data = {
            'nom': form_data.get(f'participant_nom_{i}', ''),
            'data_naixement': form_data.get(f'participant_data_naixement_{i}', ''),
            'municipi': form_data.get(f'participant_municipi_{i}', ''),
            'regio': form_data.get(f'participant_regio_{i}', ''),
            'pais': form_data.get(f'participant_pais_{i}', ''),
            'observacions': form_data.get(f'participant_observacions_{i}', '')
        }
        participants.append(participant_data)
        i += 1
    
    return participants


def _guardar_arxiu_conversa(arxiu, conversa):
    """Guardar arxiu conversa seguint estructura umberto/"""
    extensio = arxiu.filename.rsplit('.', 1)[1].lower()
    nom_unic = f"conversa_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{extensio}"
    
    # Crear directori si no existeix
    data_conversa = conversa.data_conversa or date.today()
    any = data_conversa.year
    mes = f"{data_conversa.month:02d}"
    pais = conversa.lloc_pais or 'desconegut'
    
    directori = os.path.join(current_app.config['UPLOAD_FOLDER'], 'umberto', pais, str(any), mes)
    os.makedirs(directori, exist_ok=True)
    
    # Guardar arxiu
    ruta_completa = os.path.join(directori, nom_unic)
    arxiu.save(ruta_completa)
    
    return nom_unic


def _detectar_tipus_arxiu(nom_arxiu):
    """Detectar tipus d'arxiu multimèdia"""
    extensio = nom_arxiu.rsplit('.', 1)[1].lower() if '.' in nom_arxiu else ''
    
    if extensio in ['mp3', 'wav', 'ogg', 'webm', 'm4a']:
        return 'audio'
    elif extensio in ['mp4', 'webm', 'avi', 'mov']:
        return 'video'
    else:
        return 'desconegut'


def _obtenir_tamany_arxiu(arxiu):
    """Obtenir tamany arxiu en bytes"""
    try:
        arxiu.seek(0, 2)  # Anar al final
        tamany = arxiu.tell()
        arxiu.seek(0)  # Tornar al principi
        return tamany
    except:
        return None

@converses_bp.route('/pestanya')
@login_required
def converses_pestanya():
    converses = Conversa.query.filter_by(usuari_id=current_user.id).order_by(
        Conversa.data_conversa.desc()
    ).limit(5).all()  # Només les 5 més recents
    return render_template('converses/converses_pestanya.html', converses=converses)

@converses_bp.route('/ajax')
@login_required
def converses_ajax():
    # Obtenir organitzacions de l'usuari
    usuari_organitzacions = []
    membres = MembreOrganitzacio.query.filter_by(usuari_id=current_user.id).all()
    for membre in membres:
        usuari_organitzacions.append(membre.organitzacio)
    
    return render_template('converses/formulari_simple.html', 
                         usuari_organitzacions=usuari_organitzacions)

# Afegir al final de routes/converses.py

@converses_bp.route('/nova_ajax', methods=['POST'])
@login_required
def nova_conversa_ajax():
    """Crear nova conversa via AJAX"""
    try:
        # Crear conversa principal
        conversa = Conversa(
            usuari_id=current_user.id,
            lloc_municipi=request.form.get('lloc_municipi', '').strip(),
            lloc_regio=request.form.get('lloc_regio', '').strip(), 
            lloc_pais=request.form.get('lloc_pais', '').strip(),
            durada_minuts=int(request.form.get('durada_minuts', 0)) or None,
            observacions_generals=request.form.get('observacions_generals', '').strip()
        )
        
        # Processar data conversa
        data_str = request.form.get('data_conversa')
        if data_str:
            conversa.data_conversa = datetime.strptime(data_str, '%Y-%m-%d').date()
        else:
            return jsonify({'error': 'Data conversa obligatòria'}), 400
        
        # Organització (opcional)
        organitzacio_id = request.form.get('organitzacio_id')
        if organitzacio_id and organitzacio_id != '':
            conversa.organitzacio_id = int(organitzacio_id)
        
        # Processar arxiu multimèdia
        arxiu = request.files.get('arxiu')
        if arxiu and arxiu.filename:
            nom_arxiu = _guardar_arxiu_conversa(arxiu, conversa)
            conversa.arxiu_nom = nom_arxiu
            conversa.arxiu_tipus = _detectar_tipus_arxiu(arxiu.filename)
            conversa.arxiu_tamany = _obtenir_tamany_arxiu(arxiu)
        
        db.session.add(conversa)
        db.session.flush()  # Per obtenir l'ID
        
        # Processar participants
        participants_data = _processar_participants_ajax(request.form)
        if not participants_data:
            return jsonify({'error': 'Cal almenys un participant'}), 400
            
        for i, participant_data in enumerate(participants_data):
            if participant_data['nom'].strip():  # Només si té nom
                participant = ConversaParticipant(
                    conversa_id=conversa.id,
                    nom=participant_data['nom'].strip(),
                    lloc_municipi=participant_data.get('municipi', '').strip(),
                    lloc_regio=participant_data.get('regio', '').strip(),
                    lloc_pais=participant_data.get('pais', '').strip(),
                    observacions=participant_data.get('observacions', '').strip(),
                    ordre=i + 1
                )
                
                # Processar data naixement
                if participant_data.get('data_naixement'):
                    try:
                        participant.data_naixement = datetime.strptime(
                            participant_data['data_naixement'], '%Y-%m-%d'
                        ).date()
                    except ValueError:
                        pass  # Ignorar dates malformades
                
                db.session.add(participant)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Conversa creada correctament',
            'conversa_id': conversa.id
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creant conversa via AJAX: {e}")
        return jsonify({'error': 'Error intern del servidor'}), 500


def _processar_participants_ajax(form_data):
    """Processar dades participants del formulari AJAX"""
    participants = []
    i = 0
    
    while f'participant_nom_{i}' in form_data:
        nom = form_data.get(f'participant_nom_{i}', '').strip()
        if nom:  # Només afegir si té nom
            participant_data = {
                'nom': nom,
                'data_naixement': form_data.get(f'participant_data_naixement_{i}', ''),
                'municipi': form_data.get(f'participant_municipi_{i}', ''),
                'regio': form_data.get(f'participant_regio_{i}', ''),
                'pais': form_data.get(f'participant_pais_{i}', ''),
                'observacions': form_data.get(f'participant_observacions_{i}', '')
            }
            participants.append(participant_data)
        i += 1
    
    return participants