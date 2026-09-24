"""
Preparació de dades per a les pàgines públiques (personal, família, organització).
Les plantilles de pagina_publica/ només reben un objecte DadesPaginaPublica.
"""
from dataclasses import dataclass, field

from flask import url_for
from flask_babel import gettext as _

from models import PaginaPublica, BiografiaFamiliaSeccion, MembreFamilia


TEMES_DISPONIBLES = ('classic', 'sepia', 'modern', 'nocturn')
TEMA_PER_DEFECTE = 'classic'

BLOCS_PER_TIPUS = {
    PaginaPublica.TIPUS_FAMILIA: ('historia', 'membres', 'arbre'),
}


@dataclass
class Bloc:
    id: str
    etiqueta: str
    plantilla: str
    dades: dict = field(default_factory=dict)


@dataclass
class DadesPaginaPublica:
    titol: str
    tema: str
    lema: str = None
    imatge_portada_url: str = None
    blocs: list = field(default_factory=list)


# --------------------------------------------
# Configuració
# --------------------------------------------

def obtenir_config(tipus, entitat_id):
    return PaginaPublica.query.filter_by(tipus_entitat=tipus, entitat_id=entitat_id).first()


def _tema(config):
    if config and config.tema in TEMES_DISPONIBLES:
        return config.tema
    return TEMA_PER_DEFECTE


def _ids_blocs_actius(tipus, config):
    """Ordre i visibilitat dels blocs segons la config; si no n'hi ha, l'ordre per defecte."""
    disponibles = BLOCS_PER_TIPUS[tipus]
    guardats = (config.config or {}).get('blocs') if config else None
    if not guardats:
        return list(disponibles)
    return [b['id'] for b in guardats if b.get('visible', True) and b.get('id') in disponibles]


# --------------------------------------------
# Blocs de família
# --------------------------------------------

def _bloc_familia_historia(familia):
    seccions = BiografiaFamiliaSeccion.query.filter_by(
        familia_id=familia.id, visible=True
    ).order_by(BiografiaFamiliaSeccion.ordre).all()
    if not seccions:
        return None
    return Bloc('historia', _('Història'), 'pagina_publica/blocs/_historia.html',
                {'seccions': seccions})


def _bloc_familia_membres(familia):
    membres = MembreFamilia.query.filter_by(
        espai_familiar_id=familia.id, visible_public=True
    ).order_by(MembreFamilia.primer_cognom, MembreFamilia.nom).all()
    if not membres:
        return None

    targetes = []
    for m in membres:
        nom_complet = ' '.join(p for p in (m.nom, m.primer_cognom, m.segon_cognom) if p)
        # Privacitat: les dates només es mostren de persones difuntes
        anys = None
        if m.data_defuncio:
            naix = m.data_naixement.year if m.data_naixement else '?'
            anys = f'{naix} – {m.data_defuncio.year}'
        foto_url = url_for('static', filename=f'fotos_membres/{m.foto}') if m.foto else None
        targetes.append({'nom': nom_complet, 'anys': anys, 'foto_url': foto_url})

    return Bloc('membres', _('Membres'), 'pagina_publica/blocs/_membres.html',
                {'targetes': targetes})


def _bloc_familia_arbre(familia):
    return Bloc('arbre', _('Arbre genealògic'), 'pagina_publica/blocs/_en_construccio.html')


CONSTRUCTORS_FAMILIA = {
    'historia': _bloc_familia_historia,
    'membres': _bloc_familia_membres,
    'arbre': _bloc_familia_arbre,
}


def preparar_pagina_familia(familia):
    tipus = PaginaPublica.TIPUS_FAMILIA
    config = obtenir_config(tipus, familia.id)

    blocs = []
    for bloc_id in _ids_blocs_actius(tipus, config):
        bloc = CONSTRUCTORS_FAMILIA[bloc_id](familia)
        if bloc:
            blocs.append(bloc)

    return DadesPaginaPublica(
        titol=familia.nom,
        tema=_tema(config),
        lema=(config.lema if config and config.lema else familia.periode_referencia),
        imatge_portada_url=(config.imatge_portada if config and config.imatge_portada
                            else familia.imatge_card_home),
        blocs=blocs,
    )


# --------------------------------------------
# Configuració des del panell d'administració
# --------------------------------------------

from flask_babel import lazy_gettext as _l

from models import db

ETIQUETES_BLOCS = {
    'historia': _l('Història'),
    'membres': _l('Membres'),
    'arbre': _l('Arbre genealògic'),
}

ETIQUETES_TEMES = {
    'classic': _l('Clàssic'),
    'sepia': _l('Sèpia'),
    'modern': _l('Modern'),
    'nocturn': _l('Nocturn'),
}


def obtenir_o_crear_config(tipus, entitat_id):
    config = obtenir_config(tipus, entitat_id)
    if config is None:
        config = PaginaPublica(tipus_entitat=tipus, entitat_id=entitat_id, config={})
        db.session.add(config)
    return config


def blocs_per_formulari(tipus, config):
    """Tots els blocs disponibles, en l'ordre guardat, amb el seu estat de visibilitat."""
    disponibles = BLOCS_PER_TIPUS[tipus]
    guardats = (config.config or {}).get('blocs', []) if config else []

    resultat, vistos = [], set()
    for b in guardats:
        if b.get('id') in disponibles and b['id'] not in vistos:
            resultat.append({'id': b['id'], 'etiqueta': ETIQUETES_BLOCS[b['id']],
                             'visible': b.get('visible', True)})
            vistos.add(b['id'])
    # Blocs nous que encara no eren a la configuració guardada
    for bloc_id in disponibles:
        if bloc_id not in vistos:
            resultat.append({'id': bloc_id, 'etiqueta': ETIQUETES_BLOCS[bloc_id], 'visible': True})
    return resultat


def desar_config(config, tipus, tema, lema, ordre_blocs, blocs_visibles):
    """ordre_blocs: llista d'ids en l'ordre desitjat. blocs_visibles: conjunt d'ids marcats."""
    disponibles = BLOCS_PER_TIPUS[tipus]
    config.tema = tema if tema in TEMES_DISPONIBLES else TEMA_PER_DEFECTE
    config.lema = (lema or '').strip()[:200] or None
    config.config = {
        **(config.config or {}),
        'blocs': [{'id': b, 'visible': b in blocs_visibles} for b in ordre_blocs if b in disponibles],
    }