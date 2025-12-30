import os
from datetime import datetime
from unidecode import unidecode

# Ruta base del projecte
RUTA_BASE = "umberto"

def generar_nom_fitxer(usuari, tipus='fitxer', extensio='jpg', contador=1):
    """
    Retorna un nom com:
    sanchezfernandezilda19440308001010725_imatge1.jpg
    """
    identificador = usuari.identificador_abadia
    nom = f"{identificador}_{tipus}{contador}.{extensio}"
    return nom

def crear_carpeta_usuari(usuari, tipus='usuaris'):
    """
    Crea la ruta:
    umberto/[tipus]/[pais]/[any]/[mes]/[lletra]/[identificador]/
    i la retorna.
    """
    # País normalitzat
    pais = unidecode((usuari.pais_residencia or 'desconegut').lower())

    # Data de creació
    data_creacio = getattr(usuari, 'data_registre', None) or datetime.utcnow()
    any_str = str(data_creacio.year)
    mes_str = f"{data_creacio.month:02d}"

    # Inicial
    inicial = usuari.identificador_abadia[0].lower()

    # Identificador
    ident = usuari.identificador_abadia

    # Ruta completa
    ruta = os.path.join(RUTA_BASE, tipus, pais, any_str, mes_str, inicial, ident)
    os.makedirs(ruta, exist_ok=True)

    return ruta
