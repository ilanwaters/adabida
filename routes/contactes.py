from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Usuari, Contacte

contactes_bp = Blueprint('contactes', __name__)

@contactes_bp.route('/afegir_contacte', methods=['POST'])
@login_required
def afegir_contacte():
    data = request.get_json()
    contacte_id = data.get('contacte_id')
    nom_personalitzat = data.get('nom_personalitzat', '')
    
    usuari_contacte = Usuari.query.get(contacte_id)
    if usuari_contacte and current_user.afegir_contacte(usuari_contacte, nom_personalitzat):
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'No s\'ha pogut afegir el contacte'})

@contactes_bp.route('/eliminar_contacte', methods=['POST'])
@login_required
def eliminar_contacte():
    data = request.get_json()
    contacte_id = data.get('contacte_id')
    
    usuari_contacte = Usuari.query.get(contacte_id)
    if usuari_contacte and current_user.eliminar_contacte(usuari_contacte):
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'No s\'ha pogut eliminar el contacte'})

@contactes_bp.route('/llistar_contactes')
@login_required
def llistar_contactes():
    contactes = current_user.obtenir_contactes()
    return jsonify([{
        'id': usuari.id,
        'nom': usuari.nom_complet,
        'nom_login': usuari.nom_login,
        'nom_personalitzat': contacte.nom_personalitzat
    } for contacte, usuari in contactes])