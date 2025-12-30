"""
Script per poblar la base de dades amb països i traduccions.
Versió MVP: 10 països × 4 idiomes

Executar: python seed_paisos_traduccions.py
"""

from app import app, db
from models.ubicacions import Pais, TraduccioPais

# Dades MVP: 10 països amb traduccions en ca, es, en i idioma local (si escau)
PAISOS_SEED = [
    {
        'codi_iso': 'ES',
        'nom_oficial_en': 'Spain',
        'traduccions': {
            'ca': 'Espanya',
            'es': 'España',
            'en': 'Spain',
            'eu': 'Espainia',
        }
    },
    {
        'codi_iso': 'FR',
        'nom_oficial_en': 'France',
        'traduccions': {
            'ca': 'França',
            'es': 'Francia',
            'en': 'France',
            'fr': 'France',
        }
    },
    {
        'codi_iso': 'DE',
        'nom_oficial_en': 'Germany',
        'traduccions': {
            'ca': 'Alemanya',
            'es': 'Alemania',
            'en': 'Germany',
            'de': 'Deutschland',
        }
    },
    {
        'codi_iso': 'IT',
        'nom_oficial_en': 'Italy',
        'traduccions': {
            'ca': 'Itàlia',
            'es': 'Italia',
            'en': 'Italy',
            'it': 'Italia',
        }
    },
    {
        'codi_iso': 'GR',
        'nom_oficial_en': 'Greece',
        'traduccions': {
            'ca': 'Grècia',
            'es': 'Grecia',
            'en': 'Greece',
            'el': 'Ελλάδα',  # Grec
        }
    },
    {
        'codi_iso': 'JP',
        'nom_oficial_en': 'Japan',
        'traduccions': {
            'ca': 'Japó',
            'es': 'Japón',
            'en': 'Japan',
            'ja': '日本',  # Japonès
        }
    },
    {
        'codi_iso': 'RU',
        'nom_oficial_en': 'Russian Federation',
        'traduccions': {
            'ca': 'Rússia',
            'es': 'Rusia',
            'en': 'Russia',
            'ru': 'Россия',  # Rus
        }
    },
    {
        'codi_iso': 'CN',
        'nom_oficial_en': 'China',
        'traduccions': {
            'ca': 'Xina',
            'es': 'China',
            'en': 'China',
            'zh': '中国',  # Xinès simplificat
        }
    },
    {
        'codi_iso': 'BR',
        'nom_oficial_en': 'Brazil',
        'traduccions': {
            'ca': 'Brasil',
            'es': 'Brasil',
            'en': 'Brazil',
            'pt': 'Brasil',
        }
    },
    {
        'codi_iso': 'US',
        'nom_oficial_en': 'United States',
        'traduccions': {
            'ca': 'Estats Units',
            'es': 'Estados Unidos',
            'en': 'United States',
        }
    },
]

def seed_paisos():
    """Pobla la base de dades amb països i traduccions"""
    
    with app.app_context():
        print("🌍 Iniciant seed de països i traduccions...")
        
        for pais_data in PAISOS_SEED:
            # Comprovar si ja existeix
            pais_existent = Pais.query.filter_by(codi_iso=pais_data['codi_iso']).first()
            
            if pais_existent:
                print(f"  ⚠️  {pais_data['codi_iso']} ja existeix, saltant...")
                continue
            
            # Crear país
            nou_pais = Pais(
                codi_iso=pais_data['codi_iso'],
                nom_oficial_en=pais_data['nom_oficial_en'],
                revisat_per_admin=True  # Seed = revisat
            )
            db.session.add(nou_pais)
            db.session.flush()  # Per obtenir l'ID
            
            # Crear traduccions
            for idioma, nom in pais_data['traduccions'].items():
                traduccio = TraduccioPais(
                    pais_id=nou_pais.id,
                    idioma=idioma,
                    nom=nom
                )
                db.session.add(traduccio)
            
            print(f"  ✅ Creat: {pais_data['codi_iso']} amb {len(pais_data['traduccions'])} traduccions")
        
        db.session.commit()
        print(f"\n🎉 Seed completat! {len(PAISOS_SEED)} països afegits.\n")
        
        # Mostrar resum
        print("📊 Resum:")
        total_paisos = Pais.query.count()
        total_traduccions = TraduccioPais.query.count()
        print(f"  • Total països: {total_paisos}")
        print(f"  • Total traduccions: {total_traduccions}")
        print(f"  • Mitjana traduccions/país: {total_traduccions/total_paisos:.1f}")

if __name__ == '__main__':
    seed_paisos()