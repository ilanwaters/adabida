from models import db
from datetime import datetime
from collections import Counter


class EspaiFamiliar(db.Model):
    __tablename__ = 'espais_familiars'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(100), unique=True, nullable=True)
    motiu = db.Column(db.String(100))
    descripcio = db.Column(db.Text)
    periode_referencia = db.Column(db.String(50))
    heraldica_fitxer = db.Column(db.String(255))
    
    # Imatges personalitzades per cards
    imatge_card_home = db.Column(db.String(255))
    imatge_card_arbre = db.Column(db.String(255))
    imatge_card_membres = db.Column(db.String(255))
    imatge_card_records = db.Column(db.String(255))
    imatge_card_documents = db.Column(db.String(255))
    
    data_creacio = db.Column(db.DateTime, default=datetime.utcnow)
    creat_per_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    activa = db.Column(db.Boolean, default=True)
    visible_globalment = db.Column(db.Boolean, default=True)
    visible_publicament = db.Column(db.Boolean, default=False)
    
    # Relacions
    creador = db.relationship('Usuari', backref='families_creades')
    membres = db.relationship('MembreFamilia', back_populates='espai_familiar', cascade='all, delete-orphan')
    
    @property
    def ubicacions_principals_calculades(self):
        """Retorna les 3 ubicacions amb més membres REALS (no provisionals)"""
        ubicacions = []
        for membre in self.membres:
            if membre.pais_actual and membre.municipi_actual:
                ubicacio = f"{membre.municipi_actual}"
                if membre.regio_actual:
                    ubicacio += f", {membre.regio_actual}"
                ubicacio += f", {membre.pais_actual}"
                ubicacions.append(ubicacio)
        
        if not ubicacions:
            return []
        
        comptador = Counter(ubicacions)
        top_3 = comptador.most_common(3)
        return [(ubicacio, count) for ubicacio, count in top_3]
    
    @property
    def ubicacions_mostrar(self):
        """Retorna ubicacions per mostrar: provisionals si no hi ha membres, calculades si n'hi ha"""
        calculades = self.ubicacions_principals_calculades
        
        if calculades:
            return calculades
        else:
            return [(f"{u.municipi}, {u.regio}, {u.pais}", None) 
                    for u in self.ubicacions_actuals if u.es_provisional][:3]
    
    @property
    def nombre_membres(self):
        return len(self.membres)
    
    def __repr__(self):
        motiu_str = f" ({self.motiu})" if self.motiu else ""
        return f'<EspaiFamiliar {self.nom}{motiu_str}>'


class MembreFamilia(db.Model):
    __tablename__ = 'membres_familia'
    
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=True)
    espai_familiar_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='membre')
    data_adhesio = db.Column(db.DateTime, default=datetime.utcnow)
    visible_public = db.Column(db.Boolean, default=True, nullable=False)
    
    # Ubicació actual del membre
    pais_actual = db.Column(db.String(100))
    regio_actual = db.Column(db.String(100))
    municipi_actual = db.Column(db.String(100))

    nom = db.Column(db.String(100))
    primer_cognom = db.Column(db.String(100))
    segon_cognom = db.Column(db.String(100))
    visibilitat_dades = db.Column(db.String(20), default='complet')
    
    data_naixement = db.Column(db.Date)
    municipi_naixement = db.Column(db.String(200))
    regio_naixement = db.Column(db.String(200))
    pais_naixement = db.Column(db.String(200))
    
    data_defuncio = db.Column(db.Date)
    municipi_defuncio = db.Column(db.String(200))
    regio_defuncio = db.Column(db.String(200))
    pais_defuncio = db.Column(db.String(200))
    
    biografia = db.Column(db.Text)
    genere = db.Column(db.String(10)) 
    foto = db.Column(db.String(255))
    # Relacions familiars
    pare_id = db.Column(db.Integer, db.ForeignKey('membres_familia.id'), nullable=True)
    mare_id = db.Column(db.Integer, db.ForeignKey('membres_familia.id'), nullable=True)
    matrimoni_id = db.Column(db.Integer, db.ForeignKey('matrimonis.id'), nullable=True)
    pare = db.relationship('MembreFamilia', remote_side=[id], foreign_keys=[pare_id], backref='fills_com_pare')
    mare = db.relationship('MembreFamilia', remote_side=[id], foreign_keys=[mare_id], backref='fills_com_mare')
    matrimoni = db.relationship('Matrimoni', foreign_keys=[matrimoni_id], backref='fills')
   
    # Relacions
    usuari = db.relationship('Usuari', backref='membresies_families')
    espai_familiar = db.relationship('EspaiFamiliar', back_populates='membres')
    
    __table_args__ = (db.UniqueConstraint('usuari_id', 'espai_familiar_id', name='usuari_familia_unique'),)
    
    def __repr__(self):
        nom_membre = self.nom or (self.usuari.nom if self.usuari else "Sense nom")
        nom_familia = self.espai_familiar.nom if self.espai_familiar else "None"
        return f'<MembreFamilia {nom_membre} a {nom_familia}>'
    # NAIXEMENT
    @property
    def nom_pais_naixement(self):
        return obtenir_nom_pais(self.pais_naixement)

    @property
    def nom_regio_naixement(self):
        return obtenir_nom_regio(self.regio_naixement)

    @property
    def nom_municipi_naixement(self):
        return obtenir_nom_municipi(self.municipi_naixement)

# DEFUNCIÓ
    @property
    def nom_pais_defuncio(self):
        return obtenir_nom_pais(self.pais_defuncio)

    @property
    def nom_regio_defuncio(self):
        return obtenir_nom_regio(self.regio_defuncio)

    @property
    def nom_municipi_defuncio(self):
        return obtenir_nom_municipi(self.municipi_defuncio)

# ACTUAL
 
    @property
    def nom_pais_actual(self):
        return obtenir_nom_pais(self.pais_actual)

    @property
    def nom_regio_actual(self):
        return obtenir_nom_regio(self.regio_actual)

    @property
    def nom_municipi_actual(self):
        return obtenir_nom_municipi(self.municipi_actual)

class EntradaFamilia(db.Model):
    __tablename__ = 'entrades_families'
    
    id = db.Column(db.Integer, primary_key=True)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=False)
    espai_familiar_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)
    data_compartit = db.Column(db.DateTime, default=datetime.utcnow)
    
    entrada = db.relationship('Entrada', back_populates='families_compartides')
    espai_familiar = db.relationship('EspaiFamiliar', backref='entrades_vinculades')
    
    __table_args__ = (db.UniqueConstraint('entrada_id', 'espai_familiar_id', name='entrada_fam_unique'),)


class UbicacioOrigenFamilia(db.Model):
    __tablename__ = 'ubicacions_origen_familia'
    
    id = db.Column(db.Integer, primary_key=True)
    espai_familiar_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)
    
    pais = db.Column(db.String(100), nullable=False)
    regio = db.Column(db.String(100), nullable=False)
    municipi = db.Column(db.String(100), nullable=False)
    ordre = db.Column(db.Integer, default=1)
    
    espai_familiar = db.relationship('EspaiFamiliar', backref='ubicacions_origen')
    
    def __repr__(self):
        return f'<UbicacioOrigen {self.municipi}, {self.regio}, {self.pais}>'


class UbicacioActualFamilia(db.Model):
    __tablename__ = 'ubicacions_actuals_familia'
    
    id = db.Column(db.Integer, primary_key=True)
    espai_familiar_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)
    
    pais = db.Column(db.String(100), nullable=False)
    regio = db.Column(db.String(100), nullable=False)
    municipi = db.Column(db.String(100), nullable=False)
    ordre = db.Column(db.Integer, default=1)
    es_provisional = db.Column(db.Boolean, default=True)
    
    espai_familiar = db.relationship('EspaiFamiliar', backref='ubicacions_actuals')
    
    def __repr__(self):
        return f'<UbicacioActual {self.municipi}, {self.regio}, {self.pais}>'


class Matrimoni(db.Model):
    __tablename__ = 'matrimonis'
    
    id = db.Column(db.Integer, primary_key=True)
    espai_familiar_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)
    
    membre_1_id = db.Column(db.Integer, db.ForeignKey('membres_familia.id'), nullable=False)
    membre_2_id = db.Column(db.Integer, db.ForeignKey('membres_familia.id'), nullable=False)
    
    data_casament = db.Column(db.Date)
    data_fi = db.Column(db.Date)
    estat = db.Column(db.String(20), default='actiu')
    
    espai_familiar = db.relationship('EspaiFamiliar')
    membre_1 = db.relationship('MembreFamilia', foreign_keys=[membre_1_id], backref='matrimonis_com_1')
    membre_2 = db.relationship('MembreFamilia', foreign_keys=[membre_2_id], backref='matrimonis_com_2')
    
    def __repr__(self):
        return f'<Matrimoni {self.membre_1_id} - {self.membre_2_id} ({self.estat})>'

class DocumentMembreFamilia(db.Model):
    __tablename__ = 'documents_membres_familia'
    
    id = db.Column(db.Integer, primary_key=True)
    membre_familia_id = db.Column(db.Integer, db.ForeignKey('membres_familia.id'), nullable=False)
    
    tipus_document = db.Column(db.String(50))
    nom_fitxer = db.Column(db.String(255), nullable=False)
    descripcio = db.Column(db.String(500))
    visibilitat = db.Column(db.String(20), default='familia')
    
    data_pujada = db.Column(db.DateTime, default=datetime.utcnow)
    pujat_per_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'))
    
    membre = db.relationship('MembreFamilia', backref='documents')
    pujat_per = db.relationship('Usuari')
    
    def __repr__(self):
        return f'<DocumentMembreFamilia {self.tipus_document} - {self.nom_fitxer}>'


class BiografiaFamiliaSeccion(db.Model):
    __tablename__ = 'biografia_familia_seccions'

    id = db.Column(db.Integer, primary_key=True)
    familia_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)
    
    titol = db.Column(db.String(200), nullable=False)
    contingut = db.Column(db.Text)
    ordre = db.Column(db.Integer, default=0)
    visible = db.Column(db.Boolean, default=True)
    
    data_creacio = db.Column(db.DateTime, default=datetime.utcnow)
    data_modificacio = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    espai_familiar = db.relationship('EspaiFamiliar', backref=db.backref('seccions_historia', lazy='dynamic', cascade='all, delete-orphan'))

class DocumentFamilia(db.Model):
    __tablename__ = 'documents_familia'

    id = db.Column(db.Integer, primary_key=True)
    espai_familiar_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)

    nom_fitxer = db.Column(db.String(255), nullable=False)
    tipus = db.Column(db.String(10))
    titol = db.Column(db.String(200))
    any_document = db.Column(db.String(10))
    descripcio = db.Column(db.String(500))
    visible_public = db.Column(db.Boolean, default=False, nullable=False)

    data_pujada = db.Column(db.DateTime, default=datetime.utcnow)
    pujat_per_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'))

    espai_familiar = db.relationship('EspaiFamiliar', backref=db.backref('documents_familia', cascade='all, delete-orphan'))
    pujat_per = db.relationship('Usuari')

    def __repr__(self):
        return f'<DocumentFamilia {self.nom_fitxer} ({self.espai_familiar_id})>'




def obtenir_nom_pais(pais_id):
    """Converteix ID de país a nom"""
    from models import Pais
    if not pais_id or pais_id == '':
        return ''
    try:
        pais_id_int = int(pais_id)
        pais = Pais.query.get(pais_id_int)
        return pais.nom if pais else pais_id
    except (ValueError, TypeError):
        # Si no és un número, assumir que ja és un nom (cas "Altre país")
        return pais_id

def obtenir_nom_regio(regio_id):
    """Converteix ID de regió a nom"""
    from models import Regio
    if not regio_id or regio_id == '':
        return ''
    try:
        regio_id_int = int(regio_id)
        regio = Regio.query.get(regio_id_int)
        return regio.nom if regio else regio_id
    except (ValueError, TypeError):
        return regio_id

def obtenir_nom_municipi(municipi_id):
    """Converteix ID de municipi a nom"""
    from models import Municipi
    if not municipi_id or municipi_id == '':
        return ''
    try:
        municipi_id_int = int(municipi_id)
        municipi = Municipi.query.get(municipi_id_int)
        return municipi.nom if municipi else municipi_id
    except (ValueError, TypeError):
        return municipi_id