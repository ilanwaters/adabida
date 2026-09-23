import sys
import os
from datetime import datetime
import importlib.util

# 📦 Carreguem el mòdul manualment (no falla mai)
ruta_fitxer = os.path.join("utils", "identificador_arxius.py")
spec = importlib.util.spec_from_file_location("identificador_arxius", ruta_fitxer)
identificadors_arxius = importlib.util.module_from_spec(spec)
spec.loader.exec_module(identificadors_arxius)

# 📦 Carreguem l'app i la base de dades
from app import app, db
from models import Usuari

# 🔁 Executem dins context Flask
with app.app_context():
    # 🔍 Busquem un usuari pel seu login
    usuari = Usuari.query.filter_by(nom_login='ilan_sanchez').first()

    if usuari:
        print(f"✅ Usuari trobat: {usuari.nom_login}")

        # 🗂️ Crear carpeta
        ruta = identificador_arxius.crear_carpeta_usuari(usuari)
        print(f"📁 Carpeta creada: {ruta}")

        # 📝 Generar nom d’arxiu
        nom_fitxer = identificador_arxius.generar_nom_fitxer(usuari, tipus='imatge', extensio='jpg', contador=1)
        print(f"📝 Nom d’arxiu suggerit: {nom_fitxer}")

        # 📦 Ruta final
        ruta_final = os.path.join(ruta, nom_fitxer)
        print(f"📦 Ruta completa de destí: {ruta_final}")

        # 🧪 Prova de creació d’un fitxer buit (opcional)
        with open(ruta_final, 'w') as f:
            f.write("Fitxer de prova")
        print("✅ Fitxer creat correctament.")

    else:
        print("❌ No s’ha trobat cap usuari amb aquest login.")
