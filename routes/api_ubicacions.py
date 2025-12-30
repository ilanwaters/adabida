from flask import Blueprint, jsonify, request, session
from models import Pais, Regio, Municipi, TraducioUbicacio

api_ubicacions_bp = Blueprint('api_ubicacions', __name__)


def obtenir_traduccio(tipus, element_id, idioma='ca'):
    """Obté la traducció d'un element o retorna el nom original"""
    traduccio = TraducioUbicacio.query.filter_by(
        tipus=tipus,
        element_id=element_id,
        idioma=idioma
    ).first()
    
    return traduccio.nom if traduccio else None


@api_ubicacions_bp.route('/api/paisos', methods=['GET'])
def obtenir_paisos():
    """Retorna tots els països disponibles amb traduccions
    
    FORMAT UNIFICAT compatible amb temes i ubicacions:
    {
        "id": 1,
        "codi": "ES",           ← Nou (per compatibilitat temes)
        "codi_iso": "ES",       ← Mantingut (compatibilitat ubicacions)
        "nom": "Espanya"
    }
    """
    idioma = session.get('idioma', 'ca')
    paisos = Pais.query.order_by(Pais.nom_oficial_en).all()
    
    result = []
    for p in paisos:
        nom_traduit = obtenir_traduccio('pais', p.id, idioma) or p.obtenir_nom(idioma)
        result.append({
            'id': p.id,
            'nom': nom_traduit,
            'codi': p.codi_iso,      # ← NOU: per temes
            'codi_iso': p.codi_iso   # ← MANTINGUT: per ubicacions
        })
    
    return jsonify(result)


@api_ubicacions_bp.route('/api/regions/<int:pais_id>', methods=['GET'])
def obtenir_regions(pais_id):
    """Retorna totes les regions/províncies d'un país amb traduccions"""
    idioma = session.get('idioma', 'ca')
    regions = Regio.query.filter_by(pais_id=pais_id).order_by(Regio.nom).all()
    
    print(f"🔍 API /api/regions/{pais_id}")
    print(f"   Idioma sessió: {idioma}")
    print(f"   Regions trobades: {len(regions)}")
    if len(regions) > 0:
        print(f"   Primera regió: {regions[0].nom}")
    
    result = []
    for r in regions:
        nom_traduit = obtenir_traduccio('regio', r.id, idioma) or r.nom
        result.append({
            'id': r.id,
            'nom': nom_traduit
        })
    
    print(f"   Retornant {len(result)} regions")
    return jsonify(result)


@api_ubicacions_bp.route('/api/municipis/<int:regio_id>', methods=['GET'])
def obtenir_municipis(regio_id):
    """Retorna tots els municipis d'una regió"""
    municipis = Municipi.query.filter_by(regio_id=regio_id).order_by(Municipi.nom).all()
    return jsonify([
        {'id': m.id, 'nom': m.nom}
        for m in municipis
    ])


@api_ubicacions_bp.route('/api/afegir-municipi', methods=['POST'])
def afegir_municipi():
    """Crea un nou municipi enviat per l'usuari"""
    from models import db
    
    data = request.get_json()
    regio_id = data.get('regio_id')
    nom = data.get('nom', '').strip()
    
    if not regio_id or not nom:
        return jsonify({'success': False, 'error': 'Falten dades'}), 400
    
    regio = Regio.query.get(regio_id)
    if not regio:
        return jsonify({'success': False, 'error': 'Regió no vàlida'}), 400
    
    municipi_existent = Municipi.query.filter_by(
        nom=nom,
        regio_id=regio_id
    ).first()
    
    if municipi_existent:
        return jsonify({
            'success': True,
            'municipi_id': municipi_existent.id,
            'message': 'El municipi ja existia'
        })
    
    nou_municipi = Municipi(
        nom=nom,
        regio_id=regio_id
    )
    
    db.session.add(nou_municipi)
    db.session.commit()
    
    print(f"✅ Nou municipi creat: {nom} (ID: {nou_municipi.id}) a {regio.nom}")
    
    return jsonify({
        'success': True,
        'municipi_id': nou_municipi.id,
        'message': f'Municipi "{nom}" creat correctament'
    })