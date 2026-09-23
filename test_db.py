
# test_db.py

from app import app
from models import db, ImatgeGaleria, Entrada

with app.app_context():
    img = ImatgeGaleria.query.get(58)
    print("📷 ID:", img.id)
    print("📷 Nom fitxer:", img.nom_fitxer)
    print("🔗 Entrada ID:", img.entrada_id)

    entrada = Entrada.query.get(img.entrada_id)
    print("✅ Entrada trobada?", entrada is not None)

    if entrada:
        print("👤 Usuari rel:", entrada.usuari_rel)
        print("👤 Nom login:", entrada.usuari_rel.nom_login if entrada.usuari_rel else "⚠️ None")
