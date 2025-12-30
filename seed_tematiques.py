from app import app, db
from models import Pais, CategoriaTema, Tema

def seed_tematiques():
    with app.app_context():
        # Comprovar si ja existeix
        espanya = Pais.query.filter_by(codi_iso='ES').first()
        if espanya:
            print('España ja existeix, afegint temes...')
        else:
            # Crear España
            espanya = Pais(nom='España', codi_iso='ES')
            db.session.add(espanya)
            db.session.flush()
            print('España creada')
        
        # Categoria 1: Política
        cat_politica = CategoriaTema(pais_id=espanya.id, nom='Política', ordre=1)
        db.session.add(cat_politica)
        db.session.flush()
        
        temes_politica = [
            'Guerra Civil', 'Dictadures', 'Transició', 'Democràcia'
        ]
        for i, nom in enumerate(temes_politica):
            tema = Tema(categoria_id=cat_politica.id, nom=nom, ordre=i)
            db.session.add(tema)
        
        # Categoria 2: Conflictes armats
        cat_conflictes = CategoriaTema(pais_id=espanya.id, nom='Conflictes armats', ordre=2)
        db.session.add(cat_conflictes)
        db.session.flush()
        
        temes_conflictes = [
            'ETA', 'GRAPO', 'IRA', 'Guerres balcàniques'
        ]
        for i, nom in enumerate(temes_conflictes):
            tema = Tema(categoria_id=cat_conflictes.id, nom=nom, ordre=i)
            db.session.add(tema)
        
        # Categoria 3: Societat
        cat_societat = CategoriaTema(pais_id=espanya.id, nom='Societat', ordre=3)
        db.session.add(cat_societat)
        db.session.flush()
        
        temes_societat = [
            'Pandèmia de SIDA', 'Feminisme', 'LGTBI+', 'Drets civils',
            'Exilis', 'Migració', 'Moviments socials', 'Cultura',
            'Greenpeace', 'Oficis tradicionals', 'Tradicions familiars'
        ]
        for i, nom in enumerate(temes_societat):
            tema = Tema(categoria_id=cat_societat.id, nom=nom, ordre=i)
            db.session.add(tema)
        
        # Categoria GLOBAL: Cultura Popular (sense país específic)
        cat_cultura_popular = CategoriaTema(pais_id=None, nom='Cultura Popular', ordre=99)
        db.session.add(cat_cultura_popular)
        db.session.flush()

        temes_cultura_popular = [
            'Cançons i contes populars',
            'Receptes de cuina tradicional', 
            'Refranys i dites'
        ]
        for i, nom in enumerate(temes_cultura_popular):
            tema = Tema(categoria_id=cat_cultura_popular.id, nom=nom, ordre=i, aplicar_a_tots_paisos=True)
            db.session.add(tema)
            
        db.session.commit()
        print(f'✓ Temes afegits: {len(temes_politica) + len(temes_conflictes) + len(temes_societat)}')

        for i, nom in enumerate(temes_societat):
            tema = Tema(categoria_id=cat_societat.id, nom=nom, ordre=i)
            db.session.add(tema)
        
        # Afegir altres països buits (sense temes)
        paisos_buits = [
            ('Alemanya', 'DE'),
            ('Argentina', 'AR'),
            ('Perú', 'PE'),
            ('Xile', 'CL'),
            ('Mèxic', 'MX')
        ]
        
        for nom, codi in paisos_buits:
            pais_existeix = Pais.query.filter_by(codi_iso=codi).first()
            if not pais_existeix:
                nou_pais = Pais(nom=nom, codi_iso=codi)
                db.session.add(nou_pais)
                print(f'País {nom} ({codi}) creat')
        
        db.session.commit()
        print(f'✓ Temes afegits: {len(temes_politica) + len(temes_conflictes) + len(temes_societat)}')

if __name__ == '__main__':
    seed_tematiques()