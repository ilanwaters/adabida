import json
import sys
import os

# Afegir el directori arrel al path per importar models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Pais, Regio, Municipi

def importar_desde_json(fitxer_json):
    """Importa dades geogràfiques des d'un fitxer JSON"""
    
    with open(fitxer_json, 'r', encoding='utf-8') as f:
        dades = json.load(f)
    
    with app.app_context():
        # 1. Crear el país
        pais_nom = dades['pais']['nom']
        pais_codi = dades['pais']['codi_iso']
        
        pais = Pais.query.filter_by(codi_iso=pais_codi).first()
        if not pais:
            pais = Pais(nom=pais_nom, codi_iso=pais_codi)
            db.session.add(pais)
            db.session.flush()  # Per obtenir l'ID
            print(f"✅ País creat: {pais_nom}")
        else:
            print(f"ℹ️  País ja existeix: {pais_nom}")
        
        # 2. Crear regions (províncies)
        for regio_data in dades['regions']:
            regio_nom = regio_data['nom']
            
            regio = Regio.query.filter_by(nom=regio_nom, pais_id=pais.id).first()
            if not regio:
                regio = Regio(nom=regio_nom, pais_id=pais.id)
                db.session.add(regio)
                db.session.flush()
                print(f"  📍 Regió creada: {regio_nom}")
            else:
                print(f"  ℹ️  Regió ja existeix: {regio_nom}")
            
            # 3. Crear municipis
            for municipi_nom in regio_data['municipis']:
                municipi = Municipi.query.filter_by(nom=municipi_nom, regio_id=regio.id).first()
                if not municipi:
                    municipi = Municipi(nom=municipi_nom, regio_id=regio.id)
                    db.session.add(municipi)
                    print(f"    🏘️  Municipi creat: {municipi_nom}")
        
        # Commit final
        db.session.commit()
        print(f"\n🎉 Importació completada!")
        
        # Estadístiques
        total_regions = Regio.query.filter_by(pais_id=pais.id).count()
        total_municipis = db.session.query(Municipi).join(Regio).filter(Regio.pais_id == pais.id).count()
        print(f"📊 Total regions: {total_regions}")
        print(f"📊 Total municipis: {total_municipis}")

if __name__ == '__main__':
    fitxer = 'data/espanya.json'
    
    if not os.path.exists(fitxer):
        print(f"❌ Error: No es troba el fitxer {fitxer}")
        sys.exit(1)
    
    print(f"🔄 Important dades de {fitxer}...\n")
    importar_desde_json(fitxer)