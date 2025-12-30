from app import app, db
from models import Usuari

def canviar_contrasenya():
    with app.app_context():
        admin = Usuari.query.filter_by(nom_login='admin').first()
        
        if not admin:
            print("❌ No s'ha trobat l'usuari 'admin'")
            print("\nUsuaris disponibles:")
            for u in Usuari.query.all():
                print(f"  - {u.nom_login}")
            return
        
        nova_contrasenya = 'admin123'
        admin.set_contrasenya(nova_contrasenya)  # Usa el mètode que ja fa el hash
        db.session.commit()
        
        print(f"✅ Contrasenya de '{admin.nom_login}' canviada a: {nova_contrasenya}")

if __name__ == '__main__':
    canviar_contrasenya()