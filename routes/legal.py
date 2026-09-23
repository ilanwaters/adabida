from flask import Blueprint, render_template, current_app
from flask_babel import get_locale
import os

legal_bp = Blueprint('legal', __name__, url_prefix='/legal')


def render_legal_template(base_name):
    """
    Renderitza un template legal amb detecció d'idioma i fallback a anglès/català
    
    Args:
        base_name: Nom base del template (ex: 'avis_legal', 'politica_cookies')
    """
    idioma = str(get_locale())
    template_path = f'legal/{base_name}_{idioma}.html'
    
    # Comprovar si existeix el template
    full_path = os.path.join(current_app.root_path, 'templates', template_path)
    if not os.path.exists(full_path):
        # Fallback 1: Anglès
        template_path = f'legal/{base_name}_en.html'
        full_path = os.path.join(current_app.root_path, 'templates', template_path)
        
        if not os.path.exists(full_path):
            # Fallback 2: Català (sempre existeix)
            template_path = f'legal/{base_name}_ca.html'
    
    return render_template(template_path)


@legal_bp.route('/avis-legal')
def avis_legal():
    """Mostra l'avís legal"""
    return render_legal_template('avis_legal')


@legal_bp.route('/politica-privadesa')
def politica_privadesa():
    """Mostra la política de privacitat"""
    return render_legal_template('politica_privadesa')


@legal_bp.route('/politica-cookies')
def politica_cookies():
    """Mostra la política de cookies"""
    return render_legal_template('politica_cookies')


@legal_bp.route('/termes-condicions')
def termes_condicions():
    """Mostra els termes i condicions d'ús"""
    return render_legal_template('termes_condicions')