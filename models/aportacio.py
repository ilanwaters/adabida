from models import db
from datetime import datetime
from utils.temps import ara_utc

class Aportacio(db.Model):
    __tablename__ = 'aportacions'
    
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=True)
    quantitat = db.Column(db.Numeric(10, 2), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=ara_utc)
    metode_pagament = db.Column(db.String(50), nullable=True)
    estat = db.Column(db.String(20), nullable=False, default='confirmada')
    notes = db.Column(db.Text, nullable=True)
    
    # Tracking de referits
    pais = db.Column(db.String(100), nullable=True)
    referit_per = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=True)
    comissio_percentatge = db.Column(db.Numeric(5, 2), nullable=True)
    comissio_pagada = db.Column(db.Boolean, nullable=False, default=False)
    
    usuari = db.relationship('Usuari', foreign_keys=[usuari_id], backref='aportacions')
    referidor = db.relationship('Usuari', foreign_keys=[referit_per], backref='aportacions_referides')