import os

PAISOS_CANONICS = {
    "espanya": "spain",
    "españa": "spain",
    "spain": "spain",
    "catalunya": "spain",
    "italia": "italy",
    "italy": "italy",
    "alemanya": "germany",
    "germany": "germany",
    "frança": "france",
    "france": "france",
    "francia": "france",
    "portugal": "portugal",
    "brasil": "brazil",
    "brasilien": "brazil",
    "brazil": "brazil",
    "ucraina": "ukraine",
    "ukraine": "ukraine",
    "ucrania": "ukraine",
    "andorra": "andorra",
    "marroc": "morocco",
    "morocco": "morocco",
    "argèlia": "algeria",
    "algeria": "algeria",
    "veneçuela": "venezuela",
    "venezuela": "venezuela",
    "colòmbia": "colombia",
    "colombia": "colombia",
    "equador": "ecuador",
    "ecuador": "ecuador",
    "estats units": "usa",
    "estados unidos": "usa",
    "united states": "usa",
    "usa": "usa",
    "mexic": "mexico",
    "méxico": "mexico",
    "mexico": "mexico",
    "xile": "chile",
    "chile": "chile",
    "perú": "peru",
    "peru": "peru",
}

CODIS_NUMERICS_PAIS = {
    "spain": "01",
    "italy": "02",
    "germany": "03",
    "france": "04",
    "portugal": "05",
    "brazil": "06",
    "ukraine": "07",
    "andorra": "08",
    "morocco": "09",
    "algeria": "10",
    "venezuela": "11",
    "colombia": "12",
    "ecuador": "13",
    "usa": "14",
    "mexico": "15",
    "chile": "16",
    "peru": "17",
    "desconegut": "99"
}

# ✍️ Si es vol guardar en fitxer els països no normalitzats:
REGISTRAR_DESCONEGUTS = True
FITXER_LOG = os.path.join("logs", "paisos_no_normalitzats.txt")

def normalitza_pais(nom_pais):
    if not nom_pais:
        return "desconegut"
    nom = nom_pais.strip().lower()

    if nom in PAISOS_CANONICS:
        return PAISOS_CANONICS[nom]

    nom_final = nom.replace(" ", "_")

    print(f"⚠️ [avís] País no reconegut: '{nom}' → '{nom_final}'")

    if REGISTRAR_DESCONEGUTS:
        os.makedirs("logs", exist_ok=True)
        with open(FITXER_LOG, "a", encoding="utf-8") as f:
            f.write(f"{nom}\n")

    return nom_final  # ← aquest return estava buit

    
def codi_numeric_pais(nom_pais):
    pais_normalitzat = normalitza_pais(nom_pais)
    return CODIS_NUMERICS_PAIS.get(pais_normalitzat, "99")

    
