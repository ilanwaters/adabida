# routes/pagina_personal/personal_biografia.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Entrada
from werkzeug.utils import secure_filename
import os
import uuid

# Crear blueprint
personal_biografia_bp = Blueprint('personal_biografia', __name__, url_prefix='/perfil')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@personal_biografia_bp.route('/biografia')
@login_required
def biografia():
    """Pàgina de biografia personal"""
    return render_template('pagina_personal/personal_biografia.html')

@personal_biografia_bp.route('/biografia/guardar', methods=['POST'])
@login_required
def guardar_biografia():
    """Guardar biografia de l'usuari"""
    try:
        data = request.get_json()
        biografia_html = data.get('biografia', '')
        
        current_user.biografia = biografia_html
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Biografia guardada correctament'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error guardant biografia: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@personal_biografia_bp.route('/biografia/pujar-imatge', methods=['POST'])
@login_required
def pujar_imatge_biografia():
    """Pujar imatge per a la biografia"""
    # TODO: Decidir on guardar les imatges (NO static!)
    return jsonify({'error': 'Funcionalitat pendent'}), 501

@personal_biografia_bp.route('/biografia/llistar-entrades')
@login_required
def llistar_entrades_biografia():
    """Llistar entrades de l'usuari per enllaçar a la biografia"""
    try:
        entrades = Entrada.query.filter_by(
            usuari_id=current_user.id
        ).order_by(Entrada.data_creacio.desc()).all()
        
        entrades_json = []
        for entrada in entrades:
            entrades_json.append({
                'id': entrada.id,
                'titol': entrada.titol,
                'data': entrada.data_creacio.strftime('%d/%m/%Y')
            })
        
        return jsonify({
            'success': True,
            'entrades': entrades_json
        })
        
    except Exception as e:
        print(f"Error llistant entrades: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500