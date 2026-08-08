from models import db

class TraducioCategoria(db.Model):
    __tablename__ = 'traduccions_categories_portada'
    
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    idioma = db.Column(db.String(5), nullable=False)
    nom = db.Column(db.String(255), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('categoria_id', 'idioma', name='traduccio_categoria_portada_unica'),
    )
    
    def __repr__(self):
        return f'<TraducioCategoria {self.idioma}: {self.nom}>'
        