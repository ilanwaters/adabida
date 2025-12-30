from app import app, db
from models import Usuari
from werkzeug.security import generate_password_hash

# Configuració
NOM_LOGIN = "ilanilan"  # ← CANVIA AIXÒ pel teu nom d'usuari
NOVA_CONTRASENYA = "Ilan.1234"  # ← CANVIA AIXÒ per la nova contrasenya

with app.app_context():
    usuari = Usuari.query.filter_by(nom_login=NOM_LOGIN).first()
    
    if usuari:
        usuari.contrasenya_hash = generate_password_hash(NOVA_CONTRASENYA)
        db.session.commit()
        print(f"✅ Contrasenya de '{NOM_LOGIN}' canviada a '{NOVA_CONTRASENYA}'")
    else:
        print(f"❌ Usuari '{NOM_LOGIN}' no trobat")
        print("\nUsuaris disponibles:")
        for u in Usuari.query.all():
            print(f"  - {u.nom_login}")