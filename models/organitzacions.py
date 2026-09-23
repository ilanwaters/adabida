from models import db
from datetime import datetime
from utils.temps import ara_utc


class Organitzacio(db.Model):
    __tablename__ = 'organitzacions'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    tipus = db.Column(db.String(20), nullable=False)  # 'organitzacio' o 'familia'
    descripcio = db.Column(db.Text)
    pais = db.Column(db.String(100), nullable=False)
    regio = db.Column(db.String(100), nullable=False)
    municipi = db.Column(db.String(100), nullable=False)
    codi_postal = db.Column(db.String(20)) 
    
    # URLs i configuració web
    url_publica = db.Column(db.String(100), unique=True)
    url_personalitzada = db.Column(db.String(200))
    
    # Configuració visual
    color_primary = db.Column(db.String(7), default='#007bff')
    logo_fitxer = db.Column(db.String(255))
    imatge_card_home = db.Column(db.String(255))
    imatge_card_historia = db.Column(db.String(255))
    imatge_card_entrades = db.Column(db.String(255))
    imatge_card_membres = db.Column(db.String(255))
    imatge_card_imatges = db.Column(db.String(255))
    
    # Configuració premium
    es_premium = db.Column(db.Boolean, default=False)
    data_premium = db.Column(db.Date)
    
    # Metadades
    data_creacio = db.Column(db.DateTime, default=ara_utc)
    creat_per_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    activa = db.Column(db.Boolean, default=True)
    
    # Contacte
    email_adabida = db.Column(db.String(200), nullable=False)
    email_extern = db.Column(db.String(200))
    telefon_contacte = db.Column(db.String(20))
    adresa = db.Column(db.String(300))
    
    # Relacions
    creador = db.relationship('Usuari', backref='organitzacions_creades')
    membres = db.relationship('MembreOrganitzacio', back_populates='organitzacio', cascade='all, delete-orphan')
    solicituds = db.relationship('SolicitudOrganitzacio', back_populates='organitzacio', cascade='all, delete-orphan')
    
    @property
    def slug(self):
        return self.url_publica
    
    @property 
    def solicituds_pendents(self):
        return len([s for s in self.solicituds if s.estat == 'pendent'])
    
    @property
    def entrades_totals(self):
        total = 0
        for membre in self.membres:
            if membre.usuari and membre.usuari.entrades:
                total += len(membre.usuari.entrades)
        return total
    
    @property
    def entrades(self):
        entrades = []
        for membre in self.membres:
            if membre.usuari and membre.usuari.entrades and membre.mostrar_entrades:
                entrades.extend(membre.usuari.entrades)
        return sorted(entrades, key=lambda x: x.data_creacio, reverse=True)
    
    def __repr__(self):
        return f'<Organitzacio {self.nom}>'


class MembreOrganitzacio(db.Model):
    __tablename__ = 'membres_organitzacio'
    
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=False)
    
    rol = db.Column(db.String(20), nullable=False)
    estat = db.Column(db.String(20), default='actiu')
    data_adhesio = db.Column(db.DateTime, default=ara_utc)
    data_sortida = db.Column(db.DateTime)
    
    mostrar_entrades = db.Column(db.Boolean, default=True)
    mostrar_perfil = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    
    usuari = db.relationship('Usuari', backref='membresies_organitzacions')
    organitzacio = db.relationship('Organitzacio', back_populates='membres')
    
    __table_args__ = (db.UniqueConstraint('usuari_id', 'organitzacio_id', name='usuari_organitzacio_unique'),)
    
    def __repr__(self):
        return f'<MembreOrganitzacio {self.usuari.nom if self.usuari else "None"} a {self.organitzacio.nom if self.organitzacio else "None"} com {self.rol}>'


class SolicitudOrganitzacio(db.Model):
    __tablename__ = 'solicituds_organitzacio'
    
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=False)
    
    estat = db.Column(db.String(20), default='pendent')
    data_solicitud = db.Column(db.DateTime, default=ara_utc)
    data_resposta = db.Column(db.DateTime)
    missatge = db.Column(db.Text)
    notes_admin = db.Column(db.Text)
    processat_per_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'))
    
    usuari = db.relationship('Usuari', foreign_keys=[usuari_id], backref='solicituds_organitzacions')
    organitzacio = db.relationship('Organitzacio', back_populates='solicituds')
    processat_per = db.relationship('Usuari', foreign_keys=[processat_per_id])
    
    __table_args__ = (
        db.UniqueConstraint('usuari_id', 'organitzacio_id', 'estat', name='usuari_org_estat_unique'),
    )
    
    def __repr__(self):
        return f'<SolicitudOrganitzacio {self.usuari.nom if self.usuari else "None"} -> {self.organitzacio.nom if self.organitzacio else "None"} ({self.estat})>'


class BiografiaOrganitzacioSeccion(db.Model):
    __tablename__ = 'biografia_organitzacio_seccions'
    
    id = db.Column(db.Integer, primary_key=True)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=False)
    titol = db.Column(db.String(200), nullable=False)
    contingut = db.Column(db.Text)
    ordre = db.Column(db.Integer, default=0)
    visible = db.Column(db.Boolean, default=True)
    data_creacio = db.Column(db.DateTime, default=ara_utc)
    data_modificacio = db.Column(db.DateTime)
    
    organitzacio = db.relationship('Organitzacio', backref='seccions_historia')


class EntradaOrganitzacio(db.Model):
    __tablename__ = 'entrades_organitzacions'
    
    id = db.Column(db.Integer, primary_key=True)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=False)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=False)
    data_compartit = db.Column(db.DateTime, default=ara_utc)
    
    entrada = db.relationship('Entrada', back_populates='organitzacions_compartides')
    organitzacio = db.relationship('Organitzacio', backref='entrades_vinculades')
    
    __table_args__ = (db.UniqueConstraint('entrada_id', 'organitzacio_id', name='entrada_org_unique'),)


class MissatgeOrganitzacio(db.Model):
    __tablename__ = 'missatges_organitzacio'
    
    id = db.Column(db.Integer, primary_key=True)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=False)
    emissor_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'))
    assumpte = db.Column(db.String(150), nullable=False)
    contingut = db.Column(db.Text, nullable=False)
    llegit = db.Column(db.Boolean, default=False)
    tipus = db.Column(db.String(10), default='rebut')
    data_env = db.Column(db.DateTime, default=ara_utc)
    
    organitzacio = db.relationship('Organitzacio', backref='missatges_organitzacio')
    emissor = db.relationship('Usuari', foreign_keys=[emissor_id])
    receptor = db.relationship('Usuari', foreign_keys=[receptor_id])