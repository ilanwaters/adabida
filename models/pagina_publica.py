from sqlalchemy.dialects.postgresql import JSONB

from models import db
from utils.temps import ara_utc


class PaginaPublica(db.Model):
    """Configuració de la pàgina pública d'una persona, família o organització."""
    __tablename__ = 'pagines_publiques'

    TIPUS_PERSONAL = 'personal'
    TIPUS_FAMILIA = 'familia'
    TIPUS_ORGANITZACIO = 'organitzacio'

    id = db.Column(db.Integer, primary_key=True)
    tipus_entitat = db.Column(db.String(20), nullable=False)
    entitat_id = db.Column(db.Integer, nullable=False)

    tema = db.Column(db.String(30), nullable=False, server_default='classic')
    lema = db.Column(db.String(200))
    imatge_portada = db.Column(db.String(255))
    config = db.Column(JSONB, nullable=False, server_default='{}')

    data_creacio = db.Column(db.DateTime, default=ara_utc)
    data_modificacio = db.Column(db.DateTime, default=ara_utc, onupdate=ara_utc)

    __table_args__ = (
        db.UniqueConstraint('tipus_entitat', 'entitat_id', name='uq_pagina_publica_entitat'),
    )

    def __repr__(self):
        return f'<PaginaPublica {self.tipus_entitat}:{self.entitat_id} tema={self.tema}>'
    