import json
import sys
from app import app, db
from models.ubicacions import Pais, Regio, Municipi

# Obtenir fitxer dels arguments
fitxer = sys.argv[1] if len(sys.argv) > 1 else 'data/espanya.json'

with app.app_context():
    with open(fitxer, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pais_data = data['pais']
    
    # Comprovar si ja existeix
    pais = Pais.query.filter_by(codi_iso=pais_data['codi_iso']).first()
    if not pais:
        pais = Pais(
            codi_iso=pais_data['codi_iso'],
            nom_oficial_en=pais_data['nom']
        )
        db.session.add(pais)
        db.session.flush()
        print(f"✅ País creat: {pais_data['nom']}")
    else:
        print(f"ℹ️  País ja existeix: {pais_data['nom']}")
    
    for regio_data in data['regions']:
        regio = Regio.query.filter_by(nom=regio_data['nom'], pais_id=pais.id).first()
        if not regio:
            regio = Regio(
                nom=regio_data['nom'],
                pais_id=pais.id
            )
            db.session.add(regio)
            db.session.flush()
            print(f"  📍 Regió creada: {regio_data['nom']}")
        
        for muni in regio_data['municipis']:
            municipi = Municipi.query.filter_by(nom=muni, regio_id=regio.id).first()
            if not municipi:
                municipi = Municipi(
                    nom=muni,
                    regio_id=regio.id
                )
                db.session.add(municipi)
    
    db.session.commit()
    print("✅ Importat correctament!")