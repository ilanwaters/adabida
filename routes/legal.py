from flask import Blueprint, render_template

legal_bp = Blueprint('legal', __name__, url_prefix='/legal')


@legal_bp.route('/avis-legal')
def avis_legal():
    """Mostra l'avís legal"""
    return render_template('legal/avis_legal_ca.html')


@legal_bp.route('/politica-privadesa')
def politica_privadesa():
    """Mostra la política de privacitat"""
    # De moment redirigeix a avís legal, després crearàs el template
    return render_template('legal/politica_privadesa_ca.html')


@legal_bp.route('/termes-condicions')
def termes_condicions():
    """Mostra els termes i condicions d'ús"""
    # De moment redirigeix a avís legal, després crearàs el template
    return render_template('legal/termes_condicions_ca.html')