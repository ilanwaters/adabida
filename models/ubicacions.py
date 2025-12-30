from models import db

class Pais(db.Model):
    __tablename__ = 'paisos'
    
    id = db.Column(db.Integer, primary_key=True)
    codi_iso = db.Column(db.String(2), unique=True, nullable=False)  # ES, FR, GR...
    nom_oficial_en = db.Column(db.String(100), nullable=False)  # Nom oficial en anglès (referència)
    revisat_per_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    regions = db.relationship('Regio', backref='pais', lazy=True, cascade='all, delete-orphan')
    categories = db.relationship('CategoriaTema', backref='pais', lazy=True)
    traduccions = db.relationship('TraduccioPais', backref='pais', lazy=True, cascade='all, delete-orphan')
    
    def obtenir_nom(self, idioma='ca'):
        """
        Retorna el nom del país en l'idioma especificat.
        Si no troba traducció, retorna el nom oficial en anglès.
        """
        traduccio = TraduccioPais.query.filter_by(
            pais_id=self.id,
            idioma=idioma
        ).first()
        
        if traduccio:
            return traduccio.nom
        
        # Si no hi ha traducció, retornar nom oficial en anglès
        return self.nom_oficial_en
    
    @property
    def nom(self):
        """
        Propietat per compatibilitat amb codi existent.
        Retorna nom en català per defecte.
        """
        return self.obtenir_nom('ca')


class TraduccioPais(db.Model):
    __tablename__ = 'traduccions_paisos'
    
    id = db.Column(db.Integer, primary_key=True)
    pais_id = db.Column(db.Integer, db.ForeignKey('paisos.id'), nullable=False)
    idioma = db.Column(db.String(5), nullable=False)  # ca, es, en, el, ja, ru...
    nom = db.Column(db.String(200), nullable=False)
    
    # Constraint: només una traducció per idioma per país
    __table_args__ = (
        db.UniqueConstraint('pais_id', 'idioma', name='traduccio_pais_unica'),
    )
    
    def __repr__(self):
        return f'<TraduccioPais {self.idioma}: {self.nom}>'


class Regio(db.Model):
    __tablename__ = 'regions'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    pais_id = db.Column(db.Integer, db.ForeignKey('paisos.id'), nullable=False)
    
    municipis = db.relationship('Municipi', backref='regio', lazy=True, cascade='all, delete-orphan')

class Municipi(db.Model):
    __tablename__ = 'municipis'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    regio_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)

class TraducioUbicacio(db.Model):
    __tablename__ = 'traduccions_ubicacions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Tipus i ID de l'element traduït
    tipus = db.Column(db.String(20), nullable=False)  # 'pais', 'regio', 'municipi'
    element_id = db.Column(db.Integer, nullable=False)  # ID del país/regió/municipi
    
    # Traducció
    idioma = db.Column(db.String(5), nullable=False)  # 'ca', 'es', 'en', 'fr'...
    nom = db.Column(db.String(200), nullable=False)
    
    # Índex per buscar ràpid
    __table_args__ = (
        db.Index('idx_traduccio_lookup', 'tipus', 'element_id', 'idioma'),
        db.UniqueConstraint('tipus', 'element_id', 'idioma', name='traduccio_unica'),
    )
    
    def __repr__(self):
        return f'<TraducioUbicacio {self.tipus} {self.element_id} [{self.idioma}]: {self.nom}>'