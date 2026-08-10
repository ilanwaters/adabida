from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_login import UserMixin
import secrets

db = SQLAlchemy()

# ---------- Usuari ----------

class Usuari(db.Model, UserMixin):
    __tablename__ = 'usuaris'

    id = db.Column(db.Integer, primary_key=True)
    nom_login = db.Column(db.String(80), unique=True, nullable=False)
    contrasenya_hash = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    rol = db.Column(db.String, default='usuari')
    nom = db.Column(db.String(100), nullable=False)
    primer_cognom = db.Column(db.String(100), nullable=False)
    segon_cognom = db.Column(db.String(100))
    municipi_naixement = db.Column(db.String(100))
    regio_naixement = db.Column(db.String(100))
    data_naixement = db.Column(db.String(20))
    pais_naixement = db.Column(db.String(100))
    idioma = db.Column(db.String(50))
    pais_residencia = db.Column(db.String(100))
    es_admin = db.Column(db.Boolean, default=False)
    identificador_abadia = db.Column(db.String(64), unique=True)
    perfil = db.relationship(
        "PerfilBiografic",
        uselist=False,
        back_populates="usuari",
        cascade="all, delete-orphan"
    )
    entrades = db.relationship("Entrada", back_populates="usuari", cascade="all, delete-orphan")
    entrades_blog = db.relationship('EntradaBlog', backref='autor', lazy=True)
    entrades_guardades = db.relationship("EntradaGuardada", back_populates="usuari", cascade="all, delete-orphan")
    rebre_missatges = db.Column(db.Boolean, default=False)
    biografia = db.Column(db.Text, nullable=True) 
    
    email_verificat = db.Column(db.Boolean, default=False, nullable=False)
    token_verificacio = db.Column(db.String(100), unique=True, nullable=True)
    data_token = db.Column(db.DateTime, nullable=True)
    token_reset_password = db.Column(db.String(100), unique=True, nullable=True)
    data_token_reset = db.Column(db.DateTime, nullable=True)

    def set_contrasenya(self, contrasenya):
        self.contrasenya_hash = generate_password_hash(contrasenya)

    def check_contrasenya(self, contrasenya):
        return check_password_hash(self.contrasenya_hash, contrasenya)
        
    def generar_token_verificacio(self):
        self.token_verificacio = secrets.token_urlsafe(32)
        self.data_token = datetime.utcnow()
        return self.token_verificacio
    
    def generar_token_reset_password(self):
        self.token_reset_password = secrets.token_urlsafe(32)
        self.data_token_reset = datetime.utcnow()
        return self.token_reset_password
    
    def verificar_token(self, token, tipus='verificacio', hores_expiracio=24):
        if tipus == 'verificacio':
            token_guardat = self.token_verificacio
            data_token = self.data_token
        elif tipus == 'reset_password':
            token_guardat = self.token_reset_password
            data_token = self.data_token_reset
        else:
            return False
        
        if not token_guardat or token_guardat != token:
            return False
        
        if not data_token:
            return False
        
        expiracio = data_token + timedelta(hours=hores_expiracio)
        if datetime.utcnow() > expiracio:
            return False
        
        return True
    
    def eliminar_token_verificacio(self):
        self.token_verificacio = None
        self.data_token = None
    
    def eliminar_token_reset(self):
        self.token_reset_password = None
        self.data_token_reset = None

    @property
    def nom_complet(self):
        '''Retorna nom complet de l'usuari per mostrar al template'''
        cognoms = []
        if self.primer_cognom:
            cognoms.append(self.primer_cognom)
        if self.segon_cognom:
            cognoms.append(self.segon_cognom)
        return f"{self.nom} {' '.join(cognoms)}".strip()

    def afegir_contacte(self, usuari_contacte, nom_personalitzat=None):
        """Afegeix un usuari als contactes"""
        if not self.es_contacte(usuari_contacte) and usuari_contacte.id != self.id:
            contacte = Contacte(
                usuari_id=self.id,
                contacte_id=usuari_contacte.id,
                nom_personalitzat=nom_personalitzat
            )
            db.session.add(contacte)
            return True
        return False

    def eliminar_contacte(self, usuari_contacte):
        """Elimina un usuari dels contactes"""
        contacte = Contacte.query.filter_by(
            usuari_id=self.id,
            contacte_id=usuari_contacte.id
        ).first()
        if contacte:
            db.session.delete(contacte)
            return True
        return False

    def es_contacte(self, usuari):
        """Comprova si un usuari és als meus contactes"""
        return Contacte.query.filter_by(
            usuari_id=self.id,
            contacte_id=usuari.id
        ).first() is not None

    def obtenir_contactes(self):
        """Obté tots els meus contactes"""
        return db.session.query(Contacte, Usuari).join(
            Usuari, Contacte.contacte_id == Usuari.id
        ).filter(Contacte.usuari_id == self.id).all()

    def obtenir_seccions_biografia_ordenades(self, nomes_visibles=False):
        """
     Obté les seccions de biografia ordenades.
    
     Args:
        nomes_visibles: Si True, només retorna seccions visibles (per perfil públic)
    """
        query = self.seccions_biografia.order_by(BiografiaSeccion.ordre.asc())
        if nomes_visibles:
            query = query.filter_by(visible=True)
        return query.all()

# ---------- Perfil Biogràfic ----------
class PerfilBiografic(db.Model):
    __tablename__ = 'perfil_biografic'

    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    usuari = db.relationship("Usuari", back_populates="perfil", uselist=False)

    nom = db.Column(db.String(100))
    primer_cognom = db.Column(db.String(100))
    segon_cognom = db.Column(db.String(100))
    professio = db.Column(db.String(120))
    frase_destacada = db.Column(db.String(255))
    imatge_perfil = db.Column(db.String(255))

    mostrar_biografia = db.Column(db.Boolean, default=True)
    mostrar_contacte = db.Column(db.Boolean, default=False)
    mostrar_data_naixement = db.Column(db.Boolean, default=True)
    mostrar_ubicacio = db.Column(db.Boolean, default=True)
    mostrar_origen_familiar = db.Column(db.Boolean, default=True)

    pais_naixement = db.Column(db.String(100))
    regio_naixement = db.Column(db.String(100))
    municipi_naixement = db.Column(db.String(100))
    data_naixement = db.Column(db.Date)

    pare_nom = db.Column(db.String(100))
    pare_primer_cognom = db.Column(db.String(100))
    pare_segon_cognom = db.Column(db.String(100))
    pare_data_naixement = db.Column(db.Date)
    pare_pais_naixement = db.Column(db.String(100))
    pare_regio_naixement = db.Column(db.String(100))
    pare_municipi_naixement = db.Column(db.String(100))
    pare_pais_defuncio = db.Column(db.String(100))
    pare_regio_defuncio = db.Column(db.String(100))
    pare_municipi_defuncio = db.Column(db.String(100))
    pare_data_defuncio = db.Column(db.Date)

    mare_pais_naixement = db.Column(db.String(100))
    mare_regio_naixement = db.Column(db.String(100))
    mare_municipi_naixement = db.Column(db.String(100))
    mare_pais_defuncio = db.Column(db.String(100))
    mare_regio_defuncio = db.Column(db.String(100))
    mare_municipi_defuncio = db.Column(db.String(100))
    mare_data_defuncio = db.Column(db.Date)
    mare_nom = db.Column(db.String(100))
    mare_primer_cognom = db.Column(db.String(100))
    mare_segon_cognom = db.Column(db.String(100))
    mare_data_naixement = db.Column(db.Date)
  
    experiencies = db.relationship("Experiencia", backref="perfil", cascade="all, delete-orphan", order_by="Experiencia.ordre")
    estudis = db.relationship("Estudi", backref="perfil", cascade="all, delete-orphan", order_by="Estudi.ordre")
    obres = db.relationship(
        "Obra",
        backref="perfil",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    codi_identificacio = db.Column(db.String(128), unique=True)
    carrecs_publics = db.relationship(
    'CarrecPublic',
    back_populates='perfil',
    cascade='all, delete-orphan',
    lazy='dynamic'
)
    mostrar_experiencia = db.Column(db.Boolean, default=False)
    mostrar_estudis = db.Column(db.Boolean, default=False)
    mostrar_obres = db.Column(db.Boolean, default=False)
    mostrar_carrecs = db.Column(db.Boolean, default=False)
    mostrar_pare = db.Column(db.Boolean, default=False)
    mostrar_mare = db.Column(db.Boolean, default=False)

class BiografiaSeccion(db.Model):
    """
    Model per gestionar seccions de biografia estil Wikipedia.
    Cada usuari pot tenir múltiples seccions editables individualment.
    """
    __tablename__ = 'biografia_seccions'

    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    
    # Contingut de la secció
    titol = db.Column(db.String(200), nullable=False)
    contingut = db.Column(db.Text)
    
    # Ordenació i visibilitat
    ordre = db.Column(db.Integer, default=0)  # Per ordenar les seccions
    visible = db.Column(db.Boolean, default=True)  # Si es mostra al perfil públic
    
    # Timestamps
    data_creacio = db.Column(db.DateTime, default=datetime.utcnow)
    data_modificacio = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relació amb usuari
    usuari = db.relationship('Usuari', backref=db.backref('seccions_biografia', lazy='dynamic', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<BiografiaSeccion {self.titol} - Usuari {self.usuari_id}>'



    def obtenir_seccions_biografia_ordenades(self, nomes_visibles=False):
        """
        Obté les seccions de biografia ordenades.
        
        Args:
            nomes_visibles: Si True, només retorna seccions visibles (per perfil públic)
        """
        query = self.seccions_biografia.order_by(BiografiaSeccion.ordre.asc())
        if nomes_visibles:
            query = query.filter_by(visible=True)
        return query.all()
    
    def conte_seccions_biografia(self):
        """Comprova si l'usuari té alguna secció de biografia"""
        return self.seccions_biografia.count() > 0

# Taula intermèdia: Entrada ↔ Organització (many-to-many)
class EntradaOrganitzacio(db.Model):
    __tablename__ = 'entrades_organitzacions'
    
    id = db.Column(db.Integer, primary_key=True)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=False)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=False)
    data_compartit = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacions
    entrada = db.relationship('Entrada', back_populates='organitzacions_compartides')
    organitzacio = db.relationship('Organitzacio', backref='entrades_vinculades')
    
    __table_args__ = (db.UniqueConstraint('entrada_id', 'organitzacio_id', name='entrada_org_unique'),)

class EntradaFamilia(db.Model):
    __tablename__ = 'entrades_families'
    
    id = db.Column(db.Integer, primary_key=True)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=False)
    espai_familiar_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)
    data_compartit = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacions
    entrada = db.relationship('Entrada', back_populates='families_compartides')
    espai_familiar = db.relationship('EspaiFamiliar', backref='entrades_vinculades')
    
    __table_args__ = (db.UniqueConstraint('entrada_id', 'espai_familiar_id', name='entrada_fam_unique'),)

class UbicacioOrigenFamilia(db.Model):
    """Ubicacions d'origen d'una família (pot tenir múltiples)"""
    __tablename__ = 'ubicacions_origen_familia'
    
    id = db.Column(db.Integer, primary_key=True)
    espai_familiar_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)
    
    pais = db.Column(db.String(100), nullable=False)
    regio = db.Column(db.String(100), nullable=False)
    municipi = db.Column(db.String(100), nullable=False)
    
    ordre = db.Column(db.Integer, default=1)  # Per mantenir ordre d'afegit
    
    # Relació
    espai_familiar = db.relationship('EspaiFamiliar', backref='ubicacions_origen')
    
    def __repr__(self):
        return f'<UbicacioOriGen {self.municipi}, {self.regio}, {self.pais}>'

class UbicacioActualFamilia(db.Model):
    """Ubicacions actuals provisionals d'una família (abans d'afegir membres)"""
    __tablename__ = 'ubicacions_actuals_familia'
    
    id = db.Column(db.Integer, primary_key=True)
    espai_familiar_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)
    
    pais = db.Column(db.String(100), nullable=False)
    regio = db.Column(db.String(100), nullable=False)
    municipi = db.Column(db.String(100), nullable=False)
    
    ordre = db.Column(db.Integer, default=1)
    es_provisional = db.Column(db.Boolean, default=True)  # Marca si és provisional o calculat
    
    # Relació
    espai_familiar = db.relationship('EspaiFamiliar', backref='ubicacions_actuals')
    
    def __repr__(self):
        return f'<UbicacioActual {self.municipi}, {self.regio}, {self.pais}>'

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
    
    # Relacions
    creador = db.relationship('Usuari', backref='families_creades')
    membres = db.relationship('MembreFamilia', back_populates='espai_familiar', cascade='all, delete-orphan')
    visible_globalment = db.Column(db.Boolean, default=True)
    
    @property
    def ubicacions_principals_calculades(self):
        """Retorna les 3 ubicacions amb més membres REALS (no provisionals)"""
        from collections import Counter
        
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
            # Hi ha membres amb ubicacions, mostrem les calculades
            return calculades
        else:
            # No hi ha membres, mostrem les provisionals
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
    rol = db.Column(db.String(20), nullable=False, default='membre')  # 'administrador', 'membre'
    data_adhesio = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ubicació actual del membre
    pais_actual = db.Column(db.String(100))
    regio_actual = db.Column(db.String(100))
    municipi_actual = db.Column(db.String(100))

    nom = db.Column(db.String(100))
    primer_cognom = db.Column(db.String(100))
    segon_cognom = db.Column(db.String(100))
    
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
    # Relacions familiars
    pare_id = db.Column(db.Integer, db.ForeignKey('membres_familia.id'), nullable=True)
    mare_id = db.Column(db.Integer, db.ForeignKey('membres_familia.id'), nullable=True)
    pare = db.relationship('MembreFamilia', remote_side=[id], foreign_keys=[pare_id], backref='fills_com_pare')
    mare = db.relationship('MembreFamilia', remote_side=[id], foreign_keys=[mare_id], backref='fills_com_mare')
   
    # Relacions
    usuari = db.relationship('Usuari', backref='membresies_families')
    espai_familiar = db.relationship('EspaiFamiliar', back_populates='membres')
    
    __table_args__ = (db.UniqueConstraint('usuari_id', 'espai_familiar_id', name='usuari_familia_unique'),)
    
    def __repr__(self):
        nom_membre = self.nom or (self.usuari.nom if self.usuari else "Sense nom")
        nom_familia = self.espai_familiar.nom if self.espai_familiar else "None"
        return f'<MembreFamilia {nom_membre} a {nom_familia}>'

class Matrimoni(db.Model):
    __tablename__ = 'matrimonis'
    
    id = db.Column(db.Integer, primary_key=True)
    espai_familiar_id = db.Column(db.Integer, db.ForeignKey('espais_familiars.id'), nullable=False)
    
    # Els dos cònjuges
    membre_1_id = db.Column(db.Integer, db.ForeignKey('membres_familia.id'), nullable=False)
    membre_2_id = db.Column(db.Integer, db.ForeignKey('membres_familia.id'), nullable=False)
    
    # Dates
    data_casament = db.Column(db.Date)
    data_fi = db.Column(db.Date)  # Divorci o mort d'un dels cònjuges
    
    # Estat
    estat = db.Column(db.String(20), default='actiu')  # 'actiu', 'divorciat', 'vidu'
    
    # Relacions
    espai_familiar = db.relationship('EspaiFamiliar')
    membre_1 = db.relationship('MembreFamilia', foreign_keys=[membre_1_id], backref='matrimonis_com_1')
    membre_2 = db.relationship('MembreFamilia', foreign_keys=[membre_2_id], backref='matrimonis_com_2')
    
    def __repr__(self):
        return f'<Matrimoni {self.membre_1_id} - {self.membre_2_id} ({self.estat})>'
        
class DocumentMembreFamilia(db.Model):
    __tablename__ = 'documents_membres_familia'
    
    id = db.Column(db.Integer, primary_key=True)
    membre_familia_id = db.Column(db.Integer, db.ForeignKey('membres_familia.id'), nullable=False)
    
    # Tipus i fitxer
    tipus_document = db.Column(db.String(50))  # 'dni', 'partida_naixement', etc.
    nom_fitxer = db.Column(db.String(255), nullable=False)
    descripcio = db.Column(db.String(500))
    
    # Visibilitat
    visibilitat = db.Column(db.String(20), default='familia')  # 'familia' o 'admin'
    
    # Metadades
    data_pujada = db.Column(db.DateTime, default=datetime.utcnow)
    pujat_per_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'))
    
    # Relacions
    membre = db.relationship('MembreFamilia', backref='documents')
    pujat_per = db.relationship('Usuari')
    
    def __repr__(self):
        return f'<DocumentMembreFamilia {self.tipus_document} - {self.nom_fitxer}>'

# ---------- Secció d'Història Familiar ----------
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

class Entrada(db.Model):
    __tablename__ = 'entrades'

    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    usuari = db.relationship("Usuari", back_populates="entrades")

    titol = db.Column(db.String(255))
    tema = db.Column(db.String(255))
    any_text = db.Column(db.String(10))
    contingut = db.Column(db.Text)
    pais = db.Column(db.String(100), nullable=True)
    regio = db.Column(db.String(100), nullable=True)
    municipi = db.Column(db.String(100), nullable=True)
    data_creacio = db.Column(db.DateTime, default=datetime.utcnow)

    titol_imatge = db.Column(db.String(255))
    descripcio_imatge = db.Column(db.Text)
    any_imatge = db.Column(db.String(10))
    pais_imatge = db.Column(db.String(100), nullable=True)
    regio_imatge = db.Column(db.String(100), nullable=True)
    municipi_imatge = db.Column(db.String(100), nullable=True)
    referencia = db.Column(db.String(255))
    nom_fitxer = db.Column(db.String(255))
    visible_publicament = db.Column(db.Boolean, default=False)
    es_publica = db.Column(db.Boolean, default=True)
    exposicions = db.relationship("Exposicio", back_populates="entrada")
    organitzacions_compartides = db.relationship('EntradaOrganitzacio', back_populates='entrada', cascade='all, delete-orphan')
    families_compartides = db.relationship('EntradaFamilia', back_populates='entrada', cascade='all, delete-orphan')
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    arxius_adjuntats = db.relationship("ArxiuAdjunt", back_populates="entrada", cascade="all, delete-orphan")
    imatges = db.relationship("ImatgeGaleria", back_populates="entrada", cascade="all, delete-orphan")
    tipus_fitxer = db.Column(db.String(10))
    tipus_media = db.Column(db.String(20), nullable=True, default='desconegut')
    
@property
def es_publica(self):
    '''Indica si l'entrada és pública'''
    if hasattr(self, 'publica'):
        return self.publica
    elif hasattr(self, 'es_publica_attr'):
        return self.es_publica_attr
    else:
        return False  # Per defecte privada

@property 
def autor(self):
    '''Àlies per usuari - per compatibilitat amb template'''
    return self.usuari if hasattr(self, 'usuari') else None
@property
def te_conversa(self):
    """Detecta si aquesta entrada té fitxers de conversa"""
    print(f"🔍 Comprovant conversa per entrada {self.id}")
    
    import os
    from utils.paisos import normalitza_pais
    from genera_identificadors import extreu_dades_identificador
    
    try:
        _, any_str, mes_str = extreu_dades_identificador(self.usuari.identificador_abadia)
        pais = normalitza_pais(self.usuari.pais_residencia)
        
        carpeta_entrada = os.path.join(
            "umberto", "usuaris", pais, any_str, mes_str, 
            self.usuari.nom_login, "entrades", str(self.id)
        )
        
        print(f"📁 Buscant a: {carpeta_entrada}")
        print(f"📁 Existeix carpeta: {os.path.exists(carpeta_entrada)}")
        
        if os.path.exists(carpeta_entrada):
            fitxers = os.listdir(carpeta_entrada)
            print(f"📄 Fitxers trobats: {fitxers}")
            
            for fitxer in fitxers:
                if "conversa" in fitxer.lower():
                    print(f"✅ Fitxer conversa trobat: {fitxer}")
                    return True
        
        print(f"❌ No trobat fitxers de conversa")
        return False
    except Exception as e:
        print(f"💥 Error: {e}")
        return False
# ---------- Arxius adjunts ----------
class ArxiuAdjunt(db.Model):
    __tablename__ = 'arxius_adjuntats'

    id = db.Column(db.Integer, primary_key=True)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=False)
    nom_fitxer = db.Column(db.String(255), nullable=False)
    tipus = db.Column(db.String(50))
    tipus_media = db.Column(db.String(20), nullable=True, default='desconegut')
    data_pujada = db.Column(db.DateTime, default=datetime.utcnow)
    entrada = db.relationship("Entrada", back_populates="arxius_adjuntats")


# ---------- Entrada Blog ----------
class EntradaBlog(db.Model):
    __tablename__ = 'entrades_blog'

    id = db.Column(db.Integer, primary_key=True)
    titol = db.Column(db.String(200), nullable=False)
    contingut = db.Column(db.Text, nullable=False)
    data_creacio = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'))
    firma = db.Column(db.String(120))

# ---------- Tema Entrevista ----------
class TemaEntrevista(db.Model):
    __tablename__ = 'tema_entrevista'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    data_creacio = db.Column(db.DateTime, default=datetime.utcnow)
    creat_per = db.Column(db.String(100))
# ---------- Entrevista ----------
class Entrevista(db.Model):
    __tablename__ = 'entrevistes'

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_biografic.id"), nullable=False)
    tema_id = db.Column(db.Integer, db.ForeignKey("tema_entrevista.id"), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    numero = db.Column(db.Integer, default=1)


    tema = db.relationship("TemaEntrevista", backref="entrevistes")
    perfil = db.relationship("PerfilBiografic", backref="entrevistes")

# ---------- Missatge ----------
class MissatgeEntrevista(db.Model):
    __tablename__ = 'missatges'

    id = db.Column(db.Integer, primary_key=True)
    entrevista_id = db.Column(db.Integer, db.ForeignKey('entrevistes.id'), nullable=False)
    autor = db.Column(db.String(20), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Resposta Entrevista ----------
class RespostaEntrevista(db.Model):
    __tablename__ = 'respostes_entrevista'

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_biografic.id"), nullable=False)

    tema = db.Column(db.String(255))
    subtema = db.Column(db.String(255))
    pregunta = db.Column(db.Text)
    resposta = db.Column(db.Text)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    entrevista_id = db.Column(db.Integer, db.ForeignKey("entrevistes.id"), nullable=False)

    perfil = db.relationship("PerfilBiografic", backref="respostes_entrevista")

#------------Exposició--------------------
class Exposicio(db.Model):
    __tablename__ = "exposicions"
    id = db.Column(db.Integer, primary_key=True)
    titol = db.Column(db.String(150), nullable=False)
    descripcio = db.Column(db.Text, nullable=False)
    codi = db.Column(db.String(50), unique=True, nullable=False)
    pais = db.Column(db.String(50), nullable=False)
    any = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    carpeta = db.Column(db.String(300), nullable=False)
    entrada_id = db.Column(db.Integer, db.ForeignKey("entrades.id"), nullable=True)
    entrada = db.relationship("Entrada", back_populates="exposicions")

    imatges = db.relationship("ImatgeGaleria", back_populates="exposicio")

class ImatgeExposicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imatge_id = db.Column(db.Integer, db.ForeignKey('imatges_galeria.id'), nullable=False)
    ruta_expo = db.Column(db.String(255), nullable=False)  # Ex: spain/2025/07/01-nomexpo
    data_afegit = db.Column(db.DateTime, default=datetime.utcnow)
    exposicio_id = db.Column(db.Integer, db.ForeignKey("exposicions.id"))

    imatge = db.relationship('ImatgeGaleria', backref='exposicions')

class EntradaGuardada(db.Model):
    __tablename__ = 'entrades_guardades'
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=False)

    usuari = db.relationship("Usuari", back_populates="entrades_guardades")
    entrada = db.relationship("Entrada", backref="guardada_per")

class ArxiuEntrada(db.Model):
    __tablename__ = 'arxius_entrada'

    id = db.Column(db.Integer, primary_key=True)
    nom_fitxer = db.Column(db.String, nullable=False)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=False)

    entrada_rel = db.relationship('Entrada', backref='arxius')

class Experiencia(db.Model):
    __tablename__ = "experiencies"
    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil_biografic.id'), nullable=False) 
    carrec = db.Column(db.String(200), nullable=False)      
    organitzacio = db.Column(db.String(200))               
    ambit = db.Column(db.String(100))                    
    any_inici = db.Column(db.Integer)
    any_fi = db.Column(db.Integer)                         
    actualment = db.Column(db.Boolean, default=False)
    descripcio = db.Column(db.Text)
    ordre = db.Column(db.Integer, default=0)

class Estudi(db.Model):
    __tablename__ = "estudis"
    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil_biografic.id'), nullable=False)
    titulacio = db.Column(db.String(200), nullable=False)   
    centre = db.Column(db.String(200))
    ciutat = db.Column(db.String(100))
    pais = db.Column(db.String(100))
    any_inici = db.Column(db.Integer)
    any_fi = db.Column(db.Integer)
    descripcio = db.Column(db.Text)
    ordre = db.Column(db.Integer, default=0)

class CarrecPublic(db.Model):
    __tablename__ = 'carrecs_publics'
    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil_biografic.id'), nullable=False)
    perfil = db.relationship('PerfilBiografic', back_populates='carrecs_publics')
    titol = db.Column(db.String(150), nullable=False)
    any_inici = db.Column(db.Integer)
    any_fi = db.Column(db.Integer)
    municipi = db.Column(db.String(100))
    regio = db.Column(db.String(100))
    pais = db.Column(db.String(100))

class Obra(db.Model):
    __tablename__ = "obres"

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_biografic.id"), nullable=False)

    any = db.Column(db.Integer, nullable=False)
    nom_fitxer = db.Column(db.String(255), nullable=False)      # nom final guardat
    ruta_relativa = db.Column(db.String(500), nullable=False)   # ex: umberto/usuaris/es/2025/08/ilan/obra/ilan_obra_001_1998.pdf
    ext = db.Column(db.String(10), nullable=True)               # pdf, jpg, png...
    tipus = db.Column(db.String(10), nullable=True)             # "pdf" o "image"
    mida_bytes = db.Column(db.Integer, nullable=True)

    titol = db.Column(db.String(200), nullable=True)            # opcional
    descripcio = db.Column(db.Text, nullable=True)              # opcional

    creat_el = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
class Missatge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emissor_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    assumpte = db.Column(db.String(150), nullable=False)  
    contingut = db.Column(db.Text, nullable=False)
    llegit = db.Column(db.Boolean, default=False)
    data_env = db.Column(db.DateTime, default=datetime.utcnow)

    emissor = db.relationship("Usuari", foreign_keys=[emissor_id], backref="missatges_enviats")
    receptor = db.relationship("Usuari", foreign_keys=[receptor_id], backref="missatges_rebuts")

class Organitzacio(db.Model):
    __tablename__ = 'organitzacions'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    tipus = db.Column(db.String(20), nullable=False)  # 'organitzacio' o 'familia'
    descripcio = db.Column(db.Text)
    pais = db.Column(db.String(100), nullable=False)      # Per visitant
    regio = db.Column(db.String(100), nullable=False)     # Per filtres  
    municipi = db.Column(db.String(100), nullable=False)  # Per visitant
    codi_postal = db.Column(db.String(20)) 
    
    # URLs i configuració web
    url_publica = db.Column(db.String(100), unique=True)  # nom per /o/nom-hospital
    url_personalitzada = db.Column(db.String(200))  # domini personalitzat (premium)
    
    # Configuració visual (per webs personalitzades)
    color_primary = db.Column(db.String(7), default='#007bff')  # color hexadecimal
    logo_fitxer = db.Column(db.String(255))  # nom fitxer logo
    # Imatges personalitzades per cards
    imatge_card_home = db.Column(db.String(255))
    imatge_card_historia = db.Column(db.String(255))
    imatge_card_entrades = db.Column(db.String(255))
    imatge_card_membres = db.Column(db.String(255))
    imatge_card_imatges = db.Column(db.String(255))
    
    # Configuració premium
    es_premium = db.Column(db.Boolean, default=False)
    data_premium = db.Column(db.Date)  # quan va pagar
    
    # Metadades
    data_creacio = db.Column(db.DateTime, default=datetime.utcnow)
    creat_per_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    activa = db.Column(db.Boolean, default=True)
    
    # Contacte automàtic Adabida (obligatori)
    email_adabida = db.Column(db.String(200), nullable=False)  # ex: voluntaris.hospitalcalalella@adabida.cat
    
    # Contacte extern (opcional - si volen redirigir a altre email)
    email_extern = db.Column(db.String(200))
    telefon_contacte = db.Column(db.String(20))
    adresa = db.Column(db.String(300))
    
    # Relacions
    creador = db.relationship('Usuari', backref='organitzacions_creades')
    membres = db.relationship('MembreOrganitzacio', back_populates='organitzacio', cascade='all, delete-orphan')
    solicituds = db.relationship('SolicitudOrganitzacio', back_populates='organitzacio', cascade='all, delete-orphan')
    
    # PROPIETATS CALCULADES PER AL TEMPLATE
    @property
    def slug(self):
        """Àlies per url_publica - per compatibilitat amb template"""
        return self.url_publica
    
    @property 
    def solicituds_pendents(self):
        """Compta sol·licituds pendents d'aquesta organització"""
        return len([s for s in self.solicituds if s.estat == 'pendent'])
    
    @property
    def entrades_totals(self):
        """Compta totes les entrades dels membres d'aquesta organització"""
        total = 0
        for membre in self.membres:
            if membre.usuari and membre.usuari.entrades:
                total += len(membre.usuari.entrades)
        return total
    
    @property
    def entrades(self):
        """Retorna totes les entrades dels membres d'aquesta organització"""
        entrades = []
        for membre in self.membres:
            if membre.usuari and membre.usuari.entrades and membre.mostrar_entrades:
                entrades.extend(membre.usuari.entrades)
        # Ordenar per data de creació (més recents primer)
        return sorted(entrades, key=lambda x: x.data_creacio, reverse=True)
    
    def __repr__(self):
        return f'<Organitzacio {self.nom}>'

class MembreOrganitzacio(db.Model):
    __tablename__ = 'membres_organitzacio'
    
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=False)
    
    # Rol dins l'organització
    rol = db.Column(db.String(20), nullable=False)  # 'admin', 'entrevistador', 'adherit'
    
    # Estat del membre
    estat = db.Column(db.String(20), default='actiu')  # 'actiu', 'inactiu', 'pendent'
    data_adhesio = db.Column(db.DateTime, default=datetime.utcnow)
    data_sortida = db.Column(db.DateTime)
    
    # Configuració de visibilitat
    mostrar_entrades = db.Column(db.Boolean, default=True)  # si les seves entrades surten a la pàgina org
    mostrar_perfil = db.Column(db.Boolean, default=False)  # si el seu perfil surt a la pàgina org
    
    # Notes internes (per admins)
    notes = db.Column(db.Text)
    
    # Relacions
    usuari = db.relationship('Usuari', backref='membresies_organitzacions')
    organitzacio = db.relationship('Organitzacio', back_populates='membres')
    
    # Constraint per evitar duplicats usuari-organització
    __table_args__ = (db.UniqueConstraint('usuari_id', 'organitzacio_id', name='usuari_organitzacio_unique'),)
    
    def __repr__(self):
        return f'<MembreOrganitzacio {self.usuari.nom if self.usuari else "None"} a {self.organitzacio.nom if self.organitzacio else "None"} com {self.rol}>'

class SolicitudOrganitzacio(db.Model):
    """Nova taula per gestionar sol·licituds d'adhesió a organitzacions"""
    __tablename__ = 'solicituds_organitzacio'
    
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=False)
    
    # Estat de la sol·licitud
    estat = db.Column(db.String(20), default='pendent')  # 'pendent', 'acceptada', 'rebutjada'
    
    # Dates
    data_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    data_resposta = db.Column(db.DateTime)  # quan admin accepta/rebutja
    
    # Missatge opcional de l'usuari
    missatge = db.Column(db.Text)
    
    # Notes internes de l'admin
    notes_admin = db.Column(db.Text)
    
    # Qui ha processat la sol·licitud
    processat_per_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'))
    
    # Relacions
    usuari = db.relationship('Usuari', foreign_keys=[usuari_id], backref='solicituds_organitzacions')
    organitzacio = db.relationship('Organitzacio', back_populates='solicituds')
    processat_per = db.relationship('Usuari', foreign_keys=[processat_per_id])
    
    # Constraint per evitar sol·licituds duplicades pendents
    __table_args__ = (
        db.UniqueConstraint('usuari_id', 'organitzacio_id', 'estat', 
                          name='usuari_org_estat_unique'),
    )
    
    def __repr__(self):
        return f'<SolicitudOrganitzacio {self.usuari.nom if self.usuari else "None"} -> {self.organitzacio.nom if self.organitzacio else "None"} ({self.estat})>'

"""
@property
def nom_complet(self):
    '''Retorna nom complet de l'usuari per mostrar al template'''
    if hasattr(self, 'nom') and hasattr(self, 'cognoms'):
        return f"{self.nom} {self.cognoms}".strip()
    elif hasattr(self, 'nom_usuari'):
        return self.nom_usuari
    else:
        return f"Usuari {self.id}"

@property  
def entrades_count(self):
    '''Compta el nombre d'entrades de l'usuari'''
    if hasattr(self, 'entrades') and self.entrades:
        return len(self.entrades)
    return 0
"""
"""
@property
def es_publica(self):
    '''Indica si l'entrada és pública'''
    if hasattr(self, 'publica'):
        return self.publica
    elif hasattr(self, 'es_publica_attr'):
        return self.es_publica_attr
    else:
        return False  # Per defecte privada

@property 
def autor(self):
    '''Àlies per usuari - per compatibilitat amb template'''
    return self.usuari if hasattr(self, 'usuari') else None
"""
class BiografiaOrganitzacioSeccion(db.Model):
    __tablename__ = 'biografia_organitzacio_seccions'
    
    id = db.Column(db.Integer, primary_key=True)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=False)
    titol = db.Column(db.String(200), nullable=False)
    contingut = db.Column(db.Text)
    ordre = db.Column(db.Integer, default=0)
    visible = db.Column(db.Boolean, default=True)
    data_creacio = db.Column(db.DateTime, default=datetime.utcnow)
    data_modificacio = db.Column(db.DateTime)
    
    # Relació
    organitzacio = db.relationship('Organitzacio', backref='seccions_historia')
    
class Conversa(db.Model):
    """Model per gestionar converses i diàlegs entre humans"""
    __tablename__ = 'conversa'
    
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    
    # Dades de la conversa
    lloc_municipi = db.Column(db.String(100))
    lloc_regio = db.Column(db.String(100))
    lloc_pais = db.Column(db.String(100))
    data_conversa = db.Column(db.Date)
    durada_minuts = db.Column(db.Integer)
    observacions_generals = db.Column(db.Text)
    # Arxiu multimèdia (mateixa lògica que entrades)
    arxiu_nom = db.Column(db.String(255))
    arxiu_tipus = db.Column(db.String(50))  # 'audio', 'video'
    arxiu_tamany = db.Column(db.BigInteger)  # en bytes  
    # Organització (opcional - per compartir)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=True)    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
    # Relacions
    usuari = db.relationship('Usuari', backref='converses')
    organitzacio = db.relationship('Organitzacio', backref='converses')
    participants = db.relationship('ConversaParticipant', backref='conversa', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Conversa {self.id}: {self.data_conversa}>'
    
    @property
    def ruta_arxiu(self):
        """Generar ruta d'arxiu seguint estructura umberto/"""
        if not self.arxiu_nom or not self.data_conversa:
            return None
        
        any = self.data_conversa.year
        mes = f"{self.data_conversa.month:02d}"
        return f"umberto/{self.lloc_pais or 'desconegut'}/{any}/{mes}/{self.arxiu_nom}"
    
    @property
    def participants_noms(self):
        """Llista noms participants per mostrar"""
        return [p.nom for p in self.participants if p.nom]

class ConversaParticipant(db.Model):
    """Model per participants en converses/diàlegs"""
    __tablename__ = 'conversa_participant'
    
    id = db.Column(db.Integer, primary_key=True)
    conversa_id = db.Column(db.Integer, db.ForeignKey('conversa.id'), nullable=False)
    # Dades participant
    nom = db.Column(db.String(100), nullable=False)           
    primer_cognom = db.Column(db.String(100), nullable=False) 
    segon_cognom = db.Column(db.String(100))                 
    data_naixement = db.Column(db.Date)  
    lloc_municipi = db.Column(db.String(100))
    lloc_regio = db.Column(db.String(100))
    lloc_pais = db.Column(db.String(100)) 
    # Observacions sobre el participant
    observacions = db.Column(db.Text)
    
    # Ordre en la conversa (per mantenir ordre d'afegit)
    ordre = db.Column(db.Integer, default=1)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Participant {self.nom} - Conversa {self.conversa_id}>'
    
    @property
    def edat_aproximada(self):
        """Calcular edat aproximada si tenim data naixement"""
        if not self.data_naixement:
            return None
        
        from datetime import date
        avui = date.today()
        return avui.year - self.data_naixement.year - (
            (avui.month, avui.day) < (self.data_naixement.month, self.data_naixement.day)
        )
    
    @property
    def lloc_complet(self):
        """Lloc complet formatat"""
        parts = [self.lloc_municipi, self.lloc_regio, self.lloc_pais]
        return ", ".join([p for p in parts if p])
        
class MissatgeOrganitzacio(db.Model):
    __tablename__ = 'missatges_organitzacio'
    
    id = db.Column(db.Integer, primary_key=True)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=False)
    emissor_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'))  # Opcional per enviats
    assumpte = db.Column(db.String(150), nullable=False)
    contingut = db.Column(db.Text, nullable=False)
    llegit = db.Column(db.Boolean, default=False)
    tipus = db.Column(db.String(10), default='rebut')  # 'rebut' o 'enviat'
    data_env = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacions
    organitzacio = db.relationship('Organitzacio', backref='missatges_organitzacio')
    emissor = db.relationship('Usuari', foreign_keys=[emissor_id])
    receptor = db.relationship('Usuari', foreign_keys=[receptor_id])

class Contacte(db.Model):
    __tablename__ = 'contactes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    contacte_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    nom_personalitzat = db.Column(db.String(100))  # Opcional: "Joan de l'hospital"
    data_afegit = db.Column(db.DateTime, default=datetime.utcnow)

    usuari = db.relationship('Usuari', foreign_keys=[usuari_id], backref='contactes_propis')
    contacte = db.relationship('Usuari', foreign_keys=[contacte_id], backref='contactes_aliens')
    
    __table_args__ = (db.UniqueConstraint('usuari_id', 'contacte_id', name='_usuari_contacte_uc'),)

