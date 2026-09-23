from app import db
from models import Usuari
from genera_identificadors import genera_identificador

print("📦 CONNECTANT A LA BASE DE DADES...")
usuaris = Usuari.query.all()
print(f"🔍 Trobats {len(usuaris)} usuaris")

for usuari in usuaris:
    if not usuari.identificador_abadia:
        id_abadia = genera_identificador(usuari)
        usuari.identificador_abadia = id_abadia
        print(f"✔️ Assignat: {id_abadia} a {usuari.nom_login}")
    else:
        print(f"🔹 Ja tenia identificador: {usuari.nom_login} → {usuari.identificador_abadia}")

db.session.commit()
