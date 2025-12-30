from models import db

class TraducioTema(db.Model):
    __tablename__ = 'traduccions_temes'
    
    id = db.Column(db.Integer, primary_key=True)
    tema_id = db.Column(db.Integer, db.ForeignKey('temes.id'), nullable=False)
    idioma = db.Column(db.String(5), nullable=False)
    nom = db.Column(db.String(255), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('tema_id', 'idioma', name='traduccio_tema_unica'),
    )
    
    def __repr__(self):
        return f'<TraducioTema {self.idioma}: {self.nom}>'