from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import Usuari

api_cercar_usuaris_bp = Blueprint('api_cercar_usuaris', __name__)


@api_cercar_usuaris_bp.route('/api/cercar_usuaris')
@login_required
def cercar_usuaris():
    """Cercar usuaris per nom o login, per a missatgeria (organitzacions/famílies)"""
    query = request.args.get('q', '').strip()

    if len(query) < 2:
        return jsonify({'success': True, 'usuaris': []})

    usuaris = Usuari.query.filter(
        (Usuari.nom_login.ilike(f'%{query}%')) |
        (Usuari.nom.ilike(f'%{query}%')) |
        (Usuari.primer_cognom.ilike(f'%{query}%'))
    ).limit(10).all()

    resultats = []
    for u in usuaris:
        nom_complet = f"{u.nom} {u.primer_cognom}".strip()
        resultats.append({
            'nom_login': u.nom_login,
            'nom_complet': nom_complet
        })

    return jsonify({'success': True, 'usuaris': resultats})
