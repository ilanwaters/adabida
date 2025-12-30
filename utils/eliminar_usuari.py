import shutil
import os

def elimina_fitxers_usuari(nom_login):
    base_path = os.path.join("umberto")
    carpetes = ["media", "usuaris", "documentacio"]

    for carpeta in carpetes:
        ruta = os.path.join(base_path, carpeta)
        if not os.path.exists(ruta):
            continue

        # Navegar dins carpeta/codi_pais/any/mes/
        for arrel, dirs, files in os.walk(ruta):
            for nom_dir in dirs:
                if nom_login in nom_dir:
                    ruta_completa = os.path.join(arrel, nom_dir)
                    print("🧨 Eliminant carpeta:", ruta_completa)
                    shutil.rmtree(ruta_completa, ignore_errors=True)
