from models import db
from datetime import datetime
from utils.temps import ara_utc


class Contacte(db.Model):
    __tablename__ = 'contactes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    contacte_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    nom_personalitzat = db.Column(db.String(100))
    data_afegit = db.Column(db.DateTime, default=ara_utc)

    usuari = db.relationship('Usuari', foreign_keys=[usuari_id], backref='contactes_propis')
    contacte = db.relationship('Usuari', foreign_keys=[contacte_id], backref='contactes_aliens')
    
    __table_args__ = (db.UniqueConstraint('usuari_id', 'contacte_id', name='_usuari_contacte_uc'),)