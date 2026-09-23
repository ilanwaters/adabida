"""
Plantilles de missatges multiidioma
Cada tipus de missatge té traducció en ca/es/en
"""

PLANTILLES_MISSATGES = {
    'vinculacio_familia': {
        'assumpte': {
            'ca': "T'han afegit a l'espai familiar {familia_nom}",
            'es': "Te han añadido al espacio familiar {familia_nom}",
            'en': "You've been added to the family space {familia_nom}"
        },
        'contingut': {
            'ca': """Hola!

L'administrador de la família '{familia_nom}' t'ha vinculat com a membre.

Configura la teva privacitat: /familia/membre/{membre_id}/configurar-privacitat

ℹ️ Nota: La llei de protecció de dades permet publicar el nom i data de naixement en context familiar.

Veure família: /familia/{familia_url}""",
            
            'es': """¡Hola!

El administrador de la familia '{familia_nom}' te ha vinculado como miembro.

Configura tu privacidad: /familia/membre/{membre_id}/configurar-privacitat

ℹ️ Nota: La ley de protección de datos permite publicar el nombre y fecha de nacimiento en contexto familiar.

Ver familia: /familia/{familia_url}""",
            
            'en': """Hello!

The administrator of '{familia_nom}' family has linked you as a member.

Configure your privacy: /familia/membre/{membre_id}/configurar-privacitat

ℹ️ Note: Data protection law allows publishing name and birth date in family context.

View family: /familia/{familia_url}"""
        }
    }
}

def obtenir_missatge_traduit(tipus, idioma, **dades):
    """
    Retorna assumpte i contingut traduits segons idioma
    """
    if tipus not in PLANTILLES_MISSATGES:
        return None, None
    
    plantilla = PLANTILLES_MISSATGES[tipus]
    idioma = idioma if idioma in ['ca', 'es', 'en'] else 'ca'  # Default català
    
    assumpte = plantilla['assumpte'][idioma].format(**dades)
    contingut = plantilla['contingut'][idioma].format(**dades)
    
    return assumpte, contingut
    