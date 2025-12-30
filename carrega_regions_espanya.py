import json
from app import app, db
from models.ubicacions import Pais, Regio, Municipi

with app.app_context():
    # Buscar Espanya (ja existeix)
    pais = Pais.query.filter_by(codi_iso='ES').first()
    
    if not pais:
        print("❌ País Espanya no trobat")
        exit(1)
    
    print(f"✅ País trobat: {pais.nom_oficial_en} (ID: {pais.id})")
    
    # Carregar JSON
    with open('static/data/ubicacions_espanya.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Carregar regions i municipis
    for regio_data in data['regions']:
        # Comprovar si ja existeix
        regio_exist = Regio.query.filter_by(nom=regio_data['nom'], pais_id=pais.id).first()
        if regio_exist:
            print(f"⚠️  Regió ja existeix: {regio_data['nom']}")
            continue
            
        regio = Regio(
            nom=regio_data['nom'],
            pais_id=pais.id
        )
        db.session.add(regio)
        db.session.flush()
        
        for muni in regio_data['municipis']:
            municipi = Municipi(
                nom=muni,
                regio_id=regio.id
            )
            db.session.add(municipi)
        
        print(f"✅ Regió: {regio_data['nom']} amb {len(regio_data['municipis'])} municipis")
    
    db.session.commit()
    print("\n🎉 Importació completada!")
