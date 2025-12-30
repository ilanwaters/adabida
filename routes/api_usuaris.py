from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import Usuari

api_usuaris_bp = Blueprint('api_usuaris', __name__)

@api_usuaris_bp.route('/api/buscar-usuaris')
@login_required
def buscar_usuaris():
    """Buscar usuaris per vincular amb membres de família"""
    query = request.args.get('q', '').strip()
    
    if len(query) < 2:
        return jsonify([])
    
    # Buscar per nom o email
    usuaris = Usuari.query.filter(
        (Usuari.nom.ilike(f'%{query}%')) | 
        (Usuari.email.ilike(f'%{query}%'))
    ).limit(10).all()
    
    resultats = []
    for u in usuaris:
        resultats.append({
            'id': u.id,
            'nom': u.nom,
            'email': u.email,
            'text': f'{u.nom} ({u.email})'
        })
    
    return jsonify(resultats)