from flask import Blueprint, jsonify, request
from models import db
from models.ubicacions import Pais
from models.tematiques import CategoriaTema, Tema
from difflib import get_close_matches
from flask_babel import get_locale

tematiques_api_bp = Blueprint('tematiques_api', __name__, url_prefix='/api')


@tematiques_api_bp.route('/pais/crear', methods=['POST'])
def crear_pais():
    data = request.get_json()
    nom = data.get('nom', '').strip()
    
    if not nom:
        return jsonify({'error': 'Nom del país obligatori'}), 400
    
    # Normalitzar (capitalitzar primera lletra)
    nom = nom.capitalize()
    
    # Generar codi ISO (2 primeres lletres)
    codi = nom[:2].upper()
    
    # 1. COMPROVAR EXACTE (per codi)
    pais_existent = Pais.query.filter_by(codi_iso=codi).first()
    if pais_existent:
        return jsonify({
            'error': f'Ja existeix un país amb el codi {codi} ({pais_existent.nom})',
            'exists': True
        }), 409
    
    # 2. COMPROVAR SIMILAR (per nom)
    paisos_existents = Pais.query.all()
    noms_existents = [p.nom for p in paisos_existents]
    
    # Buscar noms similars
    similars = get_close_matches(nom, noms_existents, n=1, cutoff=0.6)
    
    if similars:
        return jsonify({
            'error': f'Ja existeix "{similars[0]}". Volies dir aquest?',
            'suggestion': similars[0],
            'similar': True
        }), 409
    
    # 3. TOT BÉ - CREAR PAÍS
    nou_pais = Pais(nom_oficial_en=nom, codi_iso=codi, revisat_per_admin=False)
    db.session.add(nou_pais)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'codi': codi,
        'nom': nom,
        'id': nou_pais.id
    })

@tematiques_api_bp.route('/temes-pais/<codi>', methods=['GET'])
def get_temes_pais(codi):
    from models.tematiques import TemaExclusio  # ← AFEGIR
    
    idioma = str(get_locale())
    print(f"DEBUG: get_locale() retorna = '{idioma}'") 
    
    if codi == 'GLOBAL':
        temes_globals = Tema.query.filter_by(aplicar_a_tots_paisos=True).all()
        return jsonify({
            'temes_globals': [{'nom': t.obtenir_nom(idioma)} for t in temes_globals],
            'temes_pais': []
        })
    
    pais = Pais.query.filter_by(codi_iso=codi).first()
    if not pais:
        return jsonify({'error': 'País no trobat'}), 404
    
    # Obtenir IDs de temes exclosos d'aquest país
    exclusions_ids = [e.tema_id for e in TemaExclusio.query.filter_by(pais_id=pais.id).all()]
    
    # Temes globals NO exclosos
    if exclusions_ids:
        temes_globals = Tema.query.filter_by(aplicar_a_tots_paisos=True).filter(
            ~Tema.id.in_(exclusions_ids)
        ).all()
    else:
        temes_globals = Tema.query.filter_by(aplicar_a_tots_paisos=True).all()
    
    # Temes específics del país
    categories_pais = CategoriaTema.query.filter_by(pais_id=pais.id).all()
    temes_pais = []
    for cat in categories_pais:
        temes_pais.extend(Tema.query.filter_by(categoria_id=cat.id, aplicar_a_tots_paisos=False).all())
    
    return jsonify({
        'codi': pais.codi_iso,
        'pais': pais.nom_oficial_en,
        'temes_globals': [{'nom': t.obtenir_nom(idioma)} for t in temes_globals],
        'temes_pais': [{'nom': t.obtenir_nom(idioma)} for t in temes_pais]
    })

# routes/api/tematiques.py - AFEGIR aquestes rutes

@tematiques_api_bp.route('/categories-pais/<codi>', methods=['GET'])
def get_categories_pais(codi):
    """Retorna categories d'un país per al selector del modal"""
    try:
        pais = Pais.query.filter_by(codi_iso=codi).first()
        if not pais:
            return jsonify({'error': 'País no trobat'}), 404
        
        categories = CategoriaTema.query.filter_by(pais_id=pais.id).order_by(CategoriaTema.nom).all()
        
        return jsonify({
            'categories': [{
                'id': c.id,
                'nom': c.nom
            } for c in categories]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tematiques_api_bp.route('/categoria/crear', methods=['POST'])
def crear_categoria():
    """Crea una categoria nova per a un país"""
    try:
        data = request.get_json()
        nom = data.get('nom', '').strip()
        pais_codi = data.get('pais_codi', '').strip()
        
        if not nom:
            return jsonify({'error': 'Nom de categoria obligatori'}), 400
        
        if not pais_codi:
            return jsonify({'error': 'País obligatori'}), 400
        
        # Trobar país
        pais = Pais.query.filter_by(codi_iso=pais_codi).first()
        if not pais:
            return jsonify({'error': 'País no trobat'}), 404
        
        # Comprovar si ja existeix
        categoria_existent = CategoriaTema.query.filter_by(
            pais_id=pais.id,
            nom=nom
        ).first()
        
        if categoria_existent:
            return jsonify({
                'success': True,
                'id': categoria_existent.id,
                'message': 'Categoria ja existia'
            })
        
        # Crear categoria nova
        nova_categoria = CategoriaTema(
            pais_id=pais.id,
            nom=nom,
            ordre=0
        )
        
        db.session.add(nova_categoria)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'id': nova_categoria.id,
            'nom': nova_categoria.nom
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@tematiques_api_bp.route('/tema/crear', methods=['POST'])
def crear_tema():
    """Crea un tema nou dins d'una categoria"""
    try:
        data = request.get_json()
        nom = data.get('nom', '').strip()
        categoria_id = data.get('categoria_id')
        
        if not nom:
            return jsonify({'error': 'Nom del tema obligatori'}), 400
        
        if not categoria_id:
            return jsonify({'error': 'Categoria obligatòria'}), 400
        
        # Comprovar que la categoria existeix
        categoria = CategoriaTema.query.get(categoria_id)
        if not categoria:
            return jsonify({'error': 'Categoria no trobada'}), 404
        
        # Comprovar si el tema ja existeix en aquesta categoria
        tema_existent = Tema.query.filter_by(
            categoria_id=categoria_id,
            nom=nom
        ).first()
        
        if tema_existent:
            return jsonify({
                'success': True,
                'id': tema_existent.id,
                'message': 'Tema ja existia'
            })
        
        # Crear tema nou
        nou_tema = Tema(
            categoria_id=categoria_id,
            nom=nom,
            ordre=0,
            aplicar_a_tots_paisos=False
        )
        
        db.session.add(nou_tema)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'id': nou_tema.id,
            'nom': nou_tema.nom
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@tematiques_api_bp.route('/temes-categoria/<int:categoria_id>', methods=['GET'])
def temes_categoria(categoria_id):
    """Retorna tots els temes d'una categoria"""
    try:
        from models.tematiques import Tema
        
        temes = Tema.query.filter_by(
            categoria_id=categoria_id
            # ← ELIMINA: actiu=True
        ).order_by(Tema.ordre, Tema.nom).all()
        
        return jsonify({
            'temes': [{
                'id': t.id,
                'nom': t.nom,
                'ordre': t.ordre
            } for t in temes]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500