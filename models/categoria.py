from models import db
from models.traduccio_categoria_portada import TraducioCategoria  # ← AFEGIR

class Categoria(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    icona = db.Column(db.String(50))
    ordre = db.Column(db.Integer, default=0)
    activa = db.Column(db.Boolean, default=True)
    
    # ← AFEGIR AQUESTA LÍNIA
    traduccions = db.relationship('TraducioCategoria', backref='categoria', lazy=True, cascade='all, delete-orphan')
    
    # ← AFEGIR TOT AQUEST MÈTODE
    def obtenir_nom(self, idioma='ca'):
        """Retorna nom traduït o nom original"""
        idioma_curt = idioma.split('_')[0].lower()
        
        traduccio = TraducioCategoria.query.filter_by(
            categoria_id=self.id,
            idioma=idioma_curt
        ).first()
        
        if traduccio:
            return traduccio.nom
        
        return self.nom
    
    def __repr__(self):
        return f'<Categoria {self.nom}>'