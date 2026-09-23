from flask import Blueprint, jsonify
from flask_babel import get_locale
from models.categoria import Categoria
from models.tematiques import Pais

barra_lateral_api_bp = Blueprint('barra_lateral_api', __name__, url_prefix='/api/barra-lateral')

@barra_lateral_api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Retorna totes les categories actives ordenades"""
    idioma = str(get_locale())  # ← AFEGIR
    categories = Categoria.query.filter_by(activa=True).order_by(Categoria.ordre).all()
    
    return jsonify([{
        'id': c.id,
        'nom': c.obtenir_nom(idioma),  # ← CANVIAT (abans c.nom)
        'icona': c.icona
    } for c in categories])


@barra_lateral_api_bp.route('/paisos', methods=['GET'])
def get_paisos():
    """Retorna tots els països en l'idioma actual de l'usuari"""
    idioma = str(get_locale())  # 'ca', 'es', 'en', etc.
    paisos = Pais.query.all()
    
    resultat = []
    for p in paisos:
        resultat.append({
            'id': p.id,
            'codi': p.codi_iso,
            'nom': p.obtenir_nom(idioma)
        })
    
    # Ordenar per nom traduït
    resultat.sort(key=lambda x: x['nom'])
    
    return jsonify(resultat)