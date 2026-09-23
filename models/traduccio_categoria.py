from models import db

class TraducioCategoriaTema(db.Model):
    __tablename__ = 'traduccions_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categories_tema.id'), nullable=False)
    idioma = db.Column(db.String(5), nullable=False)
    nom = db.Column(db.String(255), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('categoria_id', 'idioma', name='traduccio_categoria_unica'),
    )
    
    def __repr__(self):
        return f'<TraducioCategoriaTema {self.idioma}: {self.nom}>'