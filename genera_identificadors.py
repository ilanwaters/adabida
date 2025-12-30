import unicodedata
from datetime import datetime
from collections import defaultdict
import re
from utils.paisos import codi_numeric_pais
from models import Exposicio

# Mapa temporal per comptar coincidències dins de l’execució
coincidencies = defaultdict(int)

def neteja_text(text):
    text = text.lower().replace(" ", "")
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
    return text

def genera_identificador(usuari):
    nom_net = neteja_text(usuari.nom)
    cognom1_net = neteja_text(usuari.primer_cognom)
    cognom2_net = neteja_text(usuari.segon_cognom)
    base_nom = cognom1_net + cognom2_net + nom_net

    try:
        naix = datetime.strptime(str(usuari.data_naixement), "%Y-%m-%d")
        naix_str = naix.strftime("%Y%m%d")
    except Exception:
        naix_str = "00000000"

    clau = (base_nom, naix_str)
    coincidencies[clau] += 1
    num = f"{coincidencies[clau]:03d}"

    pais = "01"  # codificació temporal per Espanya
    avui = datetime.now().strftime("%m%y")  # mes i any actuals

    return f"{base_nom}{naix_str}{num}{pais}{avui}"

def extreu_dades_identificador(identificador):
    """
    Extreu país, any i mes a partir de l'identificador Abadia.
    Ex: "sanchezilda19440308001010725" → retorna ("01", "2025", "07")
    """
    try:
        codi_pais = identificador[-6:-4]
        data_creacio = identificador[-4:]
        any_str = f"20{data_creacio[2:]}"
        mes_str = data_creacio[:2]
        return codi_pais, any_str, mes_str
    except Exception as e:
        print("❌ Error extraient dades de l’identificador:", e)
        return "00", "1900", "01"  # valors de fallback


def genera_codi_expo(pais: str, titol: str) -> str:
    now = datetime.now()
    any_mes = now.strftime("%Y%m")
    codi_pais = codi_numeric_pais(pais)
    slug_base = re.sub(r'\W+', '', titol.lower())[:20]
    
    # Prova codi original
    base = f"{codi_pais}-{any_mes}{slug_base}"
    codi_final = base
    i = 1

    # Si ja existeix, afegeix sufix numèric incremental
    while Exposicio.query.filter_by(codi=codi_final).first():
        codi_final = f"{base}-{i}"
        i += 1

    return codi_final
