from app import app
from models import db, MembreOrganitzacio

print("=== NETEJANT DUPLICATS MEMBRES ORGANITZACIÓ ===")

with app.app_context():
    # Buscar tots els membres
    tots_membres = MembreOrganitzacio.query.all()
    print(f"Total membres trobats: {len(tots_membres)}")
    
    # Detectar duplicats
    membres_únics = {}
    duplicats_a_esborrar = []
    
    for membre in tots_membres:
        # Clau única: usuari + organització + rol
        clau = (membre.usuari_id, membre.organitzacio_id, membre.rol)
        
        if clau in membres_únics:
            # És un duplicat - mantenir el més antic (ID més petit)
            membre_existent = membres_únics[clau]
            if membre.id < membre_existent.id:
                # El nou és més antic - esborrar l'existent i guardar el nou
                duplicats_a_esborrar.append(membre_existent)
                membres_únics[clau] = membre
            else:
                # L'existent és més antic - esborrar el nou
                duplicats_a_esborrar.append(membre)
        else:
            # És únic - guardar-lo
            membres_únics[clau] = membre
    
    print(f"Duplicats detectats: {len(duplicats_a_esborrar)}")
    
    if len(duplicats_a_esborrar) > 0:
        print("Esborrant duplicats...")
        
        for duplicat in duplicats_a_esborrar:
            print(f"- Esborrant membre ID {duplicat.id}: usuari {duplicat.usuari_id} -> org {duplicat.organitzacio_id}")
            db.session.delete(duplicat)
        
        # Confirmar canvis
        db.session.commit()
        print(f"✅ {len(duplicats_a_esborrar)} duplicats esborrats correctament!")
        
        # Verificar resultat
        membres_finals = MembreOrganitzacio.query.all()
        print(f"Membres restants: {len(membres_finals)}")
        
    else:
        print("✅ No s'han trobat duplicats!")

print("=== NETEJA COMPLETADA ===")