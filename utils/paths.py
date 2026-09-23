# utils/paths.py
import os
from datetime import datetime
from flask import current_app
from utils.paisos import normalitza_pais

def storage_root():
    """Arrel on es desa tot el material (definit a config.py com STORAGE_ROOT)."""
    return current_app.config["STORAGE_ROOT"]

def carpeta_temp(usuari):
    """Carpeta temporal on es guarden fitxers mentre es crea l'entrada."""
    avui = datetime.now()
    any_actual = avui.strftime("%Y")
    mes_actual = avui.strftime("%m")
    pais = normalitza_pais(usuari.pais_residencia)
    return os.path.join(storage_root(), "media", "temp", pais, any_actual, mes_actual, usuari.nom_login)

def carpeta_entrada(usuari, entrada_id):
    """Carpeta definitiva d'una entrada concreta."""
    avui = datetime.now()
    any_actual = avui.strftime("%Y")
    mes_actual = avui.strftime("%m")
    pais = normalitza_pais(usuari.pais_residencia)
    return os.path.join(storage_root(), "usuaris", pais, any_actual, mes_actual, usuari.nom_login, "entrades", str(entrada_id))

def carpeta_converses(usuari, entrada_id):
    """Carpeta on es desaran les converses (àudios/vídeos) dins d'una entrada."""
    return os.path.join(carpeta_entrada(usuari, entrada_id), "converses")

def carpeta_miniatures(usuari, entrada_id):
    """Carpeta de miniatures d'una entrada."""
    return os.path.join(carpeta_entrada(usuari, entrada_id), "mini")

def carpeta_pendents(usuari):
    """Carpeta on es copien arxius pendents de revisió a la galeria."""
    avui = datetime.now()
    any_actual = avui.strftime("%Y")
    mes_actual = avui.strftime("%m")
    pais = normalitza_pais(usuari.pais_residencia)
    return os.path.join(storage_root(), "media", "pendents", any_actual, pais, mes_actual)
