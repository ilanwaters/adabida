"""
Script per generar URLs (slugs) pels espais familiars existents que no en tenen
Executar: python generar_urls_families.py
"""

from app import app, db
from models import EspaiFamiliar
import re

def generar_slug(nom, municipi=None):
    """Genera un slug net a partir del nom i opcionalment municipi"""
    slug_base = nom.lower().strip()
    
    if municipi:
        slug_base = f"{slug_base}-{municipi.lower().strip()}"
    
    # Netejar: només lletres, números i guions
    slug_base = re.sub(r'[^a-z0-9-]', '-', slug_base)
    slug_base = re.sub(r'-+', '-', slug_base)  # Múltiples guions → un sol
    slug_base = slug_base.strip('-')  # Treure guions dels extrems
    
    return slug_base

def main():
    with app.app_context():
        # Obtenir tots els espais sense URL
        espais_sense_url = EspaiFamiliar.query.filter(
            (EspaiFamiliar.url == None) | (EspaiFamiliar.url == '')
        ).all()
        
        print(f"📋 Trobats {len(espais_sense_url)} espais familiars sense URL")
        
        if not espais_sense_url:
            print("✅ Tots els espais ja tenen URL!")
            return
        
        urls_existents = set()
        # Carregar URLs existents per evitar duplicats
        for e in EspaiFamiliar.query.filter(EspaiFamiliar.url != None).all():
            urls_existents.add(e.url)
        
        actualitzats = 0
        
        for espai in espais_sense_url:
            # Intentar obtenir primer municipi d'origen
            municipi = None
            if espai.ubicacions_origen and len(espai.ubicacions_origen) > 0:
                municipi = espai.ubicacions_origen[0].municipi
            
            # Generar slug base
            slug_base = generar_slug(espai.nom, municipi)
            
            # Comprovar si ja existeix i afegir número si cal
            slug_final = slug_base
            contador = 1
            while slug_final in urls_existents:
                slug_final = f"{slug_base}-{contador}"
                contador += 1
            
            # Assignar URL
            espai.url = slug_final
            urls_existents.add(slug_final)
            
            print(f"  ✓ {espai.nom} → {slug_final}")
            actualitzats += 1
        
        # Guardar canvis
        try:
            db.session.commit()
            print(f"\n✅ {actualitzats} espais familiars actualitzats correctament!")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error guardant canvis: {e}")

if __name__ == '__main__':
    main()
