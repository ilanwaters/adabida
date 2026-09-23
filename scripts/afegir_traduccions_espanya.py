import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Pais, Regio, TraducioUbicacio

def afegir_traduccions_espanya():
    """Afegeix traduccions en català per Espanya"""
    
    with app.app_context():
        # Buscar Espanya
        espanya = Pais.query.filter_by(codi_iso='ES').first()
        
        if not espanya:
            print("❌ No s'ha trobat Espanya a la BD")
            return
        
        print(f"✅ Trobat país: {espanya.nom} (ID: {espanya.id})")
        
        # Traducció del país
        traduccions_pais = [
            ('ca', 'Espanya'),
            ('es', 'España'),
            ('en', 'Spain'),
            ('eu', 'Espainia'),
            ('gl', 'España')
        ]
        
        for idioma, nom in traduccions_pais:
            existe = TraducioUbicacio.query.filter_by(
                tipus='pais',
                element_id=espanya.id,
                idioma=idioma
            ).first()
            
            if not existe:
                traduccio = TraducioUbicacio(
                    tipus='pais',
                    element_id=espanya.id,
                    idioma=idioma,
                    nom=nom
                )
                db.session.add(traduccio)
                print(f"  📝 Afegida traducció [{idioma}]: {nom}")
        
        # Traduccions de regions/províncies
        traduccions_regions = {
            'A Coruña': {'ca': 'La Corunya', 'es': 'A Coruña', 'en': 'A Coruña', 'gl': 'A Coruña'},
            'Álava': {'ca': 'Àlaba', 'es': 'Álava', 'en': 'Álava', 'eu': 'Araba'},
            'Albacete': {'ca': 'Albacete', 'es': 'Albacete', 'en': 'Albacete'},
            'Alicante': {'ca': 'Alacant', 'es': 'Alicante', 'en': 'Alicante'},
            'Almería': {'ca': 'Almeria', 'es': 'Almería', 'en': 'Almería'},
            'Asturias': {'ca': 'Astúries', 'es': 'Asturias', 'en': 'Asturias', 'ast': 'Asturies'},
            'Ávila': {'ca': 'Àvila', 'es': 'Ávila', 'en': 'Ávila'},
            'Badajoz': {'ca': 'Badajoz', 'es': 'Badajoz', 'en': 'Badajoz'},
            'Barcelona': {'ca': 'Barcelona', 'es': 'Barcelona', 'en': 'Barcelona'},
            'Vizcaya': {'ca': 'Biscaia', 'es': 'Vizcaya', 'en': 'Biscay', 'eu': 'Bizkaia'},
            'Burgos': {'ca': 'Burgos', 'es': 'Burgos', 'en': 'Burgos'},
            'Cáceres': {'ca': 'Càceres', 'es': 'Cáceres', 'en': 'Cáceres'},
            'Cádiz': {'ca': 'Cadis', 'es': 'Cádiz', 'en': 'Cádiz'},
            'Cantabria': {'ca': 'Cantàbria', 'es': 'Cantabria', 'en': 'Cantabria'},
            'Castellón': {'ca': 'Castelló', 'es': 'Castellón', 'en': 'Castellón'},
            'Ciudad Real': {'ca': 'Ciudad Real', 'es': 'Ciudad Real', 'en': 'Ciudad Real'},
            'Córdoba': {'ca': 'Còrdova', 'es': 'Córdoba', 'en': 'Córdoba'},
            'Cuenca': {'ca': 'Conca', 'es': 'Cuenca', 'en': 'Cuenca'},
            'Guipúzcoa': {'ca': 'Guipúscoa', 'es': 'Guipúzcoa', 'en': 'Gipuzkoa', 'eu': 'Gipuzkoa'},
            'Girona': {'ca': 'Girona', 'es': 'Gerona', 'en': 'Girona'},
            'Granada': {'ca': 'Granada', 'es': 'Granada', 'en': 'Granada'},
            'Guadalajara': {'ca': 'Guadalajara', 'es': 'Guadalajara', 'en': 'Guadalajara'},
            'Huelva': {'ca': 'Huelva', 'es': 'Huelva', 'en': 'Huelva'},
            'Huesca': {'ca': 'Osca', 'es': 'Huesca', 'en': 'Huesca'},
            'Illes Balears': {'ca': 'Illes Balears', 'es': 'Islas Baleares', 'en': 'Balearic Islands'},
            'Jaén': {'ca': 'Jaén', 'es': 'Jaén', 'en': 'Jaén'},
            'León': {'ca': 'Lleó', 'es': 'León', 'en': 'León'},
            'Lleida': {'ca': 'Lleida', 'es': 'Lérida', 'en': 'Lleida'},
            'Lugo': {'ca': 'Lugo', 'es': 'Lugo', 'en': 'Lugo', 'gl': 'Lugo'},
            'Madrid': {'ca': 'Madrid', 'es': 'Madrid', 'en': 'Madrid'},
            'Málaga': {'ca': 'Màlaga', 'es': 'Málaga', 'en': 'Málaga'},
            'Murcia': {'ca': 'Múrcia', 'es': 'Murcia', 'en': 'Murcia'},
            'Navarra': {'ca': 'Navarra', 'es': 'Navarra', 'en': 'Navarre', 'eu': 'Nafarroa'},
            'Ourense': {'ca': 'Ourense', 'es': 'Orense', 'en': 'Ourense', 'gl': 'Ourense'},
            'Palencia': {'ca': 'Palència', 'es': 'Palencia', 'en': 'Palencia'},
            'Las Palmas': {'ca': 'Las Palmas', 'es': 'Las Palmas', 'en': 'Las Palmas'},
            'Pontevedra': {'ca': 'Pontevedra', 'es': 'Pontevedra', 'en': 'Pontevedra', 'gl': 'Pontevedra'},
            'La Rioja': {'ca': 'La Rioja', 'es': 'La Rioja', 'en': 'La Rioja'},
            'Salamanca': {'ca': 'Salamanca', 'es': 'Salamanca', 'en': 'Salamanca'},
            'Santa Cruz de Tenerife': {'ca': 'Santa Cruz de Tenerife', 'es': 'Santa Cruz de Tenerife', 'en': 'Santa Cruz de Tenerife'},
            'Segovia': {'ca': 'Segòvia', 'es': 'Segovia', 'en': 'Segovia'},
            'Sevilla': {'ca': 'Sevilla', 'es': 'Sevilla', 'en': 'Seville'},
            'Soria': {'ca': 'Sòria', 'es': 'Soria', 'en': 'Soria'},
            'Tarragona': {'ca': 'Tarragona', 'es': 'Tarragona', 'en': 'Tarragona'},
            'Teruel': {'ca': 'Terol', 'es': 'Teruel', 'en': 'Teruel'},
            'Toledo': {'ca': 'Toledo', 'es': 'Toledo', 'en': 'Toledo'},
            'Valencia': {'ca': 'València', 'es': 'Valencia', 'en': 'Valencia'},
            'Valladolid': {'ca': 'Valladolid', 'es': 'Valladolid', 'en': 'Valladolid'},
            'Zamora': {'ca': 'Zamora', 'es': 'Zamora', 'en': 'Zamora'},
            'Zaragoza': {'ca': 'Saragossa', 'es': 'Zaragoza', 'en': 'Zaragoza'},
            'Ceuta': {'ca': 'Ceuta', 'es': 'Ceuta', 'en': 'Ceuta'},
            'Melilla': {'ca': 'Melilla', 'es': 'Melilla', 'en': 'Melilla'}
        }
        
        for nom_original, traduccions in traduccions_regions.items():
            regio = Regio.query.filter_by(nom=nom_original, pais_id=espanya.id).first()
            
            if regio:
                for idioma, nom_traduit in traduccions.items():
                    existe = TraducioUbicacio.query.filter_by(
                        tipus='regio',
                        element_id=regio.id,
                        idioma=idioma
                    ).first()
                    
                    if not existe:
                        traduccio = TraducioUbicacio(
                            tipus='regio',
                            element_id=regio.id,
                            idioma=idioma,
                            nom=nom_traduit
                        )
                        db.session.add(traduccio)
                        print(f"    📍 {nom_original} [{idioma}]: {nom_traduit}")
        
        db.session.commit()
        print("\n🎉 Traduccions afegides correctament!")
        
        # Estadístiques
        total = TraducioUbicacio.query.count()
        print(f"📊 Total traduccions a la BD: {total}")

if __name__ == '__main__':
    print("🌍 Afegint traduccions per Espanya...\n")
    afegir_traduccions_espanya()