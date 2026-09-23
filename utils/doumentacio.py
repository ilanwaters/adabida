from datetime import datetime
from utils.temps import ara_utc
import os

def genera_ruta_documentacio(perfil):
    """
    Ruta per guardar documentació pendent de validació per l’administrador.
    Ex: documentacio_pendent/espanya/2025/juliol/
    """
    ara = ara_utc()
    any_str = str(ara.year)
    mes_str = ara.strftime('%B').lower()
    pais = getattr(perfil.usuari, "pais_residencia", "sense_pais").lower().replace(" ", "_")

    carpeta = os.path.join(
        "documentacio_pendent",
        pais,
        any_str,
        mes_str
    )
    os.makedirs(carpeta, exist_ok=True)
    return carpeta
