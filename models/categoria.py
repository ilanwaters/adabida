from models import db

class Categoria(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    icona = db.Column(db.String(50))
    ordre = db.Column(db.Integer, default=0)
    activa = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Categoria {self.nom}>'