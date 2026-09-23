from flask import Blueprint, jsonify, session, render_template, url_for
from models import db, Entrada, Usuari, EntradaGuardada, Conversa
from models.tematiques import Tema, CategoriaTema

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/entrada/<usuari_login>/<int:entrada_id>")
def obtenir_entrada(usuari_login, entrada_id):
    usuari = Usuari.query.filter_by(nom_login=usuari_login).first_or_404()
    entrada = Entrada.query.filter_by(id=entrada_id, usuari_id=usuari.id).first_or_404()
    conversa = Conversa.query.filter_by(entrada_id=entrada.id).first()

    # 🔍 Comprovem si l’usuari actual ja ha guardat aquesta entrada
    ja_guardada = False
    if 'usuari' in session:
        actual = Usuari.query.filter_by(nom_login=session['usuari']).first()
        if actual:
            ja_guardada = EntradaGuardada.query.filter_by(
                usuari_id=actual.id, entrada_id=entrada.id
            ).first() is not None

    es_propietari = session.get("usuari") == usuari.nom_login

    return jsonify({
        "id": entrada.id,
        "usuari_login": usuari.nom_login,
        "usuari_nom": f"{usuari.nom} {usuari.primer_cognom} {usuari.segon_cognom or ''}".strip(),
        "titol": entrada.titol,
        "tema": entrada.tema,
        "pais": entrada.pais,
        "regio": entrada.regio,
        "municipi": entrada.municipi,
        "pais_imatge": entrada.pais_imatge,
        "regio_imatge": entrada.regio_imatge,
        "municipi_imatge": entrada.municipi_imatge,
        "data_creacio": entrada.data_creacio.strftime('%d/%m/%Y') if entrada.data_creacio else None,
        "data_modificacio": entrada.data_modificacio.strftime('%d/%m/%Y') if entrada.data_modificacio else None,
        "any": entrada.any_text,
        "contingut": entrada.contingut,
        "titol_imatge": entrada.titol_imatge,
        "any_imatge": entrada.any_imatge,
        "descripcio_imatge": entrada.descripcio_imatge,
        "referencia": entrada.referencia,
        "propietari": es_propietari,
        "ja_guardada": ja_guardada,
        "conversa": {
            "id": conversa.id,
            "data": conversa.data_conversa.strftime('%d/%m/%Y') if conversa.data_conversa else None,
            "durada_minuts": conversa.durada_minuts,
            "lloc_institucio": conversa.lloc_institucio,
            "lloc_municipi": conversa.lloc_municipi,
            "lloc_regio": conversa.lloc_regio,
            "lloc_pais": conversa.lloc_pais,
            "observacions_generals": conversa.observacions_generals,
            "participants": [
                {
                    "nom": p.nom,
                    "primer_cognom": p.primer_cognom,
                    "segon_cognom": p.segon_cognom,
                    "lloc_municipi": p.lloc_municipi,
                    "lloc_regio": p.lloc_regio,
                    "data_naixement": p.data_naixement.strftime('%d/%m/%Y') if p.data_naixement else None,
                }
                for p in conversa.participants
            ],
            "arxiu_nom": conversa.arxiu_nom,
            "arxiu_tipus": conversa.arxiu_tipus,
        } if conversa else None,
        "portada": next(
            (
                {
                    "nom_fitxer": f.nom_fitxer,
                    "tipus": f.tipus,
                    "tipus_media": f.tipus_media,
                }
                for f in entrada.arxius_adjuntats if f.es_portada
            ),
            None
        ),
        "arxius": [
            {
                "nom_fitxer": f.nom_fitxer,
                "tipus": f.tipus,
                "tipus_media": f.tipus_media,
                "ruta": f"/umberto/{usuari.nom_login}/{entrada.id}/{f.nom_fitxer}",
                "titol": f.titol,
                "any_arxiu": f.any_arxiu,
                "pais": f.pais,
                "regio": f.regio,
                "municipi": f.municipi,
                "descripcio": f.descripcio,
                "referencia": f.referencia,
                "es_conversa": f.es_conversa,
            }
            for f in entrada.arxius_adjuntats
            if not f.es_portada
        ]
    })


@api_bp.route("/api/tema/crear-multiple", methods=['POST'])
def crear_tema_multiple():
    from flask import request
    
    data = request.json
    nom_tema = data.get('nom')
    categories_ids = data.get('categories', [])
    
    if not nom_tema:
        return jsonify({'success': False, 'error': 'Nom obligatori'}), 400
    
    if not categories_ids:
        return jsonify({'success': False, 'error': 'Tria almenys una categoria'}), 400
    
    try:
        # Crear tema
        tema = Tema(nom=nom_tema, ordre=0)
        db.session.add(tema)
        db.session.flush()  # Per obtenir tema.id

        print(f"DEBUG: Rebut categories_ids: {categories_ids}")
        
        # Obtenir categories i vincular
        categories = CategoriaTema.query.filter(CategoriaTema.id.in_(categories_ids)).all()
        categories_ids = list(set(categories_ids))  
        
        if len(categories) != len(categories_ids):
            return jsonify({'success': False, 'error': 'Alguna categoria no existeix'}), 400
        
        # Vincular amb ORM
        tema.categories = categories
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'tema_id': tema.id,
            'nom': tema.nom
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error creant tema: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
@api_bp.route("/api/categoria/crear", methods=['POST'])
def crear_categoria():
    from flask import request
    from models.ubicacions import Pais
    
    data = request.json
    nom = data.get('nom')
    pais_codi = data.get('pais_codi', 'ES')
    
    if not nom:
        return jsonify({'success': False, 'error': 'Nom obligatori'}), 400
    
    # Obtenir país
    pais = Pais.query.filter_by(codi_iso=pais_codi).first()
    if not pais:
        pais = Pais.query.first()  # Fallback al primer país
    
    if not pais:
        return jsonify({'success': False, 'error': 'No hi ha països disponibles'}), 400
    
    # Crear categoria
    categoria = CategoriaTema(
        pais_id=pais.id,
        nom=nom,
        ordre=0
    )
    db.session.add(categoria)
    db.session.commit()
    db.session.refresh(categoria)
    
    return jsonify({
        'success': True,
        'id': categoria.id,
        'nom': categoria.nom
    })