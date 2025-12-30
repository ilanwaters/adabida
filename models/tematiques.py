from models import db
from models.ubicacions import Pais  # ← Importem el Pais existent

# ELIMINAR la classe Pais (ja existeix a ubicacions)

class CategoriaTema(db.Model):
    __tablename__ = 'categories_tema'
    
    id = db.Column(db.Integer, primary_key=True)
    pais_id = db.Column(db.Integer, db.ForeignKey('paisos.id'), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    ordre = db.Column(db.Integer, default=0)
    
   
class Tema(db.Model):
    __tablename__ = 'temes'
    
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categories_tema.id'), nullable=True)  # ← Ara pot ser NULL
    categories = db.relationship('CategoriaTema', secondary='tema_categoria', backref='temes_relacio')
    nom = db.Column(db.String(100), nullable=False)
    ordre = db.Column(db.Integer, default=0)
    aplicar_a_tots_paisos = db.Column(db.Boolean, default=False, nullable=False)
    traduccions = db.relationship('TraducioTema', backref='tema', lazy=True, cascade='all, delete-orphan')

    def obtenir_nom(self, idioma='ca'):
        idioma_curt = idioma.split('_')[0].lower()
    
        print(f"DEBUG obtenir_nom: tema_id={self.id}, idioma='{idioma}', idioma_curt='{idioma_curt}'")
    
        from models.traduccio_tema import TraducioTema
        traduccio = TraducioTema.query.filter_by(
            tema_id=self.id,
            idioma=idioma_curt
        ).first()
    
        print(f"DEBUG: Traducció trobada: {traduccio}")
    
        if traduccio:
            return traduccio.nom
    
        return self.nom

class TemaExclusio(db.Model):
    """Exclusions de temes globals per país"""
    __tablename__ = 'temes_exclusions'
    
    id = db.Column(db.Integer, primary_key=True)
    tema_id = db.Column(db.Integer, db.ForeignKey('temes.id'), nullable=False)
    pais_id = db.Column(db.Integer, db.ForeignKey('paisos.id'), nullable=False)
    data_exclusio = db.Column(db.DateTime, default=db.func.now())
    
    # Relacions
    tema = db.relationship('Tema', backref='exclusions')
    pais = db.relationship('Pais', backref='temes_exclosos')
    
    # Constraint: un tema només pot estar exclòs un cop per país
    __table_args__ = (
        db.UniqueConstraint('tema_id', 'pais_id', name='uq_tema_pais_exclusio'),
    )
    
    def __repr__(self):
        return f'<TemaExclusio tema={self.tema_id} pais={self.pais_id}>'

class TemaCategoria(db.Model):
    """Taula intermèdia per relació N:M entre Temes i Categories"""
    __tablename__ = 'tema_categoria'
    
    tema_id = db.Column(db.Integer, db.ForeignKey('temes.id'), primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categories_tema.id'), primary_key=True)