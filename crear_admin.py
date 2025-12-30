from app import app, db
from models.usuari import Usuari
from werkzeug.security import generate_password_hash

with app.app_context():
    # Dades admin
    nom_login = input("Nom login admin: ")
    email = input("Email admin: ")
    password = input("Password admin: ")
    
    # Crear admin
    admin = Usuari(
        nom_login=nom_login,
        email=email,
        contrasenya_hash=generate_password_hash(password),
        nom="Administrador",
        primer_cognom="Adabida",
        es_admin=True,
        email_verificat=True,
        idioma='ca'
    )
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"\n✅ Usuari admin '{nom_login}' creat correctament!")
