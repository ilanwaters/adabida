# utils/vinculador.py

from models import db, ImatgeGaleria, Entrada

def vincular_imatges_galeria(verbose=True):
    """
    Vincula automàticament imatges de galeria amb entrades, si tenen el mateix nom_fitxer.
    """
    imatges = ImatgeGaleria.query.filter_by(entrada_id=None).all()
    vinculades = 0

    for img in imatges:
        entrada = Entrada.query.filter_by(nom_fitxer=img.nom_fitxer).first()
        if entrada:
            img.entrada_id = entrada.id
            vinculades += 1
            if verbose:
                print(f"🔗 Vinculat: {img.nom_fitxer} → entrada {entrada.id}")

    db.session.commit()

    if verbose:
        print(f"✅ Vinculació completada: {vinculades} imatges assignades.")
    return vinculades
