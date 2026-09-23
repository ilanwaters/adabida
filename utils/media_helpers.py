# utils/media_helpers.py

from flask import url_for

def generar_miniatura_entrada(entrada, usuari_login):
    """
    Genera la URL de la miniatura d'una entrada.
    Prioritza imatges reals, després icones segons tipus_media.
    
    Args:
        entrada: Objecte Entrada amb arxius_adjuntats
        usuari_login: String amb el nom de login de l'usuari
        
    Returns:
        String amb la URL de la miniatura
    """
    arxius = entrada.arxius_adjuntats
    
    # Si no hi ha cap arxiu, retornar icona per defecte
    if not arxius:
        return "/static/icons/sense_imatge.png"
    
    # 0. Prioritat màxima: portada triada explícitament per l'usuari
    for arxiu in arxius:
        if arxiu.es_portada:
            return url_for(
                "serveis_media.serveix_miniatura",
                usuari=usuari_login,
                entrada_id=str(entrada.id),
                nom_fitxer=arxiu.nom_fitxer
            )
    
    # 1. Prioritat: Buscar primera imatge real
    for arxiu in arxius:
        if arxiu.tipus.lower() in ["jpg", "jpeg", "png", "gif", "webp"]:
            return url_for(
                "serveis_media.serveix_miniatura",
                usuari=usuari_login,
                entrada_id=str(entrada.id),
                nom_fitxer=arxiu.nom_fitxer
            )
    # 2. Si no hi ha imatge, usar icona segons tipus del primer arxiu
    primer_arxiu = arxius[0]
    
    # Gestió especial per webm amb tipus_media
    if primer_arxiu.tipus.lower() == "webm" and primer_arxiu.tipus_media:
        if primer_arxiu.tipus_media == "video":
            return "/static/icons/video_webm.png"
        elif primer_arxiu.tipus_media == "audio":
            return "/static/icons/audio_webm.png"
    
    # Gestió especial per PDF
    if primer_arxiu.tipus.lower() == "pdf":
        return "/static/icons/pdf.png"
    
    # Per qualsevol altre tipus, usar icona genèrica
    return f"/static/icons/{primer_arxiu.tipus.lower()}.png"