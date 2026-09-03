from models import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets


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
    nivell_usuari = db.Column(db.String(10), default='blau')  
    data_registre = db.Column(db.DateTime, default=datetime.utcnow) 
    bandera_preferida = db.Column(db.String(10), nullable=True)
    imatge_card_biografia = db.Column(db.String(255))
    imatge_card_entrades = db.Column(db.String(255))
    imatge_card_nova_entrada = db.Column(db.String(255))
    imatge_card_perfil = db.Column(db.String(255))
    imatge_card_organitzacions = db.Column(db.String(255))
    imatge_card_familia = db.Column(db.String(255))
    imatge_card_conversa = db.Column(db.String(255))
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
    
    # Verificació email i reset password
    email_verificat = db.Column(db.Boolean, default=False, nullable=False)
    token_verificacio = db.Column(db.String(100), unique=True, nullable=True)
    data_token = db.Column(db.DateTime, nullable=True)
    token_reset_password = db.Column(db.String(100), unique=True, nullable=True)
    data_token_reset = db.Column(db.DateTime, nullable=True)

    # Mètodes
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

    def eliminar_token_reset_password(self):
        self.token_reset_password = None
        self.token_reset_expiracio = None

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

    def calcular_nivell_usuari(self):
        """
        Calcula automàticament el nivell de l'usuari segons criteris.
        Retorna el nivell calculat però NO el guarda (cal fer db.session.commit després).
        """
        from models.entrades import Entrada
        
        # Comptar entrades creades per l'usuari
        nombre_entrades = Entrada.query.filter_by(usuari_id=self.id).count()
        
        # Criteris simples per començar (es poden ajustar després)
        if nombre_entrades >= 5:
            return 'verd'
        elif nombre_entrades >= 1:
            return 'groc'
        else:
            return 'blau'
    
    def actualitzar_nivell_usuari(self):
        """
        Actualitza el nivell de l'usuari i guarda a la BD.
        """
        nou_nivell = self.calcular_nivell_usuari()
        if self.nivell_usuari != nou_nivell:
            self.nivell_usuari = nou_nivell
            db.session.commit()
            return True
        return False
    
    def es_usuari_verificat(self):
        """
        Retorna True si l'usuari és nivell verd (verificat).
        """
        return self.nivell_usuari == 'verd'
    
    def pot_denunciar(self):
        """
        Només usuaris verificats poden denunciar contingut.
        """
        return self.es_usuari_verificat()
    
    def pot_crear_tema_forum(self):
        """
        Només usuaris verificats poden crear temes al fòrum.
        """
        return self.es_usuari_verificat()


    def afegir_contacte(self, usuari_contacte, nom_personalitzat=None):
        """Afegeix un usuari als contactes"""
        from models.interaccions import Contacte
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
        from models.interaccions import Contacte
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
        from models.interaccions import Contacte
        return Contacte.query.filter_by(
            usuari_id=self.id,
            contacte_id=usuari.id
        ).first() is not None

    def obtenir_contactes(self):
        """Obté tots els meus contactes"""
        from models.interaccions import Contacte
        return db.session.query(Contacte, Usuari).join(
            Usuari, Contacte.contacte_id == Usuari.id
        ).filter(Contacte.usuari_id == self.id).all()

    def obtenir_seccions_biografia_ordenades(self, nomes_visibles=False):
        """
        Obté les seccions de biografia ordenades.
        
        Args:
            nomes_visibles: Si True, només retorna seccions visibles (per perfil públic)
        """
        from models.usuari import BiografiaSeccion
        query = self.seccions_biografia.order_by(
            BiografiaSeccion.any_inici.asc().nullslast(),
            BiografiaSeccion.ordre.asc()
        )
        if nomes_visibles:
            query = query.filter_by(visible=True)
        return query.all()

    @property
    def nom_pais_residencia(self):
        try:
            if self.pais_residencia:
            # Intentar convertir a int si és string numèric
                pais_id = int(self.pais_residencia) if isinstance(self.pais_residencia, str) and self.pais_residencia.isdigit() else self.pais_residencia
            
                if isinstance(pais_id, int):
                    from models.ubicacions import Pais
                    pais = Pais.query.get(pais_id)
                    return pais.nom if pais else f"País {pais_id} no trobat"
                return str(self.pais_residencia)
            return "Sense país"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @property
    def nom_pais_naixement(self):
        try:
            if self.pais_naixement:
            # Intentar convertir a int si és string numèric
                pais_id = int(self.pais_naixement) if isinstance(self.pais_naixement, str) and self.pais_naixement.isdigit() else self.pais_naixement
            
                if isinstance(pais_id, int):
                    from models.ubicacions import Pais
                    pais = Pais.query.get(pais_id)
                    return pais.nom if pais else f"País {pais_id} no trobat"
                return str(self.pais_naixement)
            return "Sense país"
        except Exception as e:
            return f"Error: {str(e)}"

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
    # Dates (anys) per ordenació cronològica
    any_inici = db.Column(db.Integer, nullable=True)  # Any d'inici del període
    any_final = db.Column(db.Integer, nullable=True)  # Any final (opcional)
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
    nom_fitxer = db.Column(db.String(255), nullable=False)
    ruta_relativa = db.Column(db.String(500), nullable=False)
    ext = db.Column(db.String(10), nullable=True)
    tipus = db.Column(db.String(10), nullable=True)
    mida_bytes = db.Column(db.Integer, nullable=True)

    titol = db.Column(db.String(200), nullable=True)
    descripcio = db.Column(db.Text, nullable=True)

    creat_el = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Missatge(db.Model):
    __tablename__ = 'missatges'
    
    id = db.Column(db.Integer, primary_key=True)
    emissor_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    assumpte = db.Column(db.String(150), nullable=False)  
    contingut = db.Column(db.Text, nullable=False)
    llegit = db.Column(db.Boolean, default=False)
    data_env = db.Column(db.DateTime, default=datetime.utcnow)

    emissor = db.relationship("Usuari", foreign_keys=[emissor_id], backref="missatges_enviats")
    receptor = db.relationship("Usuari", foreign_keys=[receptor_id], backref="missatges_rebuts")
    arxius_adjunts = db.relationship("ArxiuMissatge", back_populates="missatge", cascade="all, delete-orphan")

    tipus_missatge = db.Column(db.String(50), nullable=True)  # 'vinculacio_familia', 'convit_organitzacio', etc.
    dades_json = db.Column(db.Text, nullable=True)

class ArxiuMissatge(db.Model):
    __tablename__ = 'arxius_missatges'

    id = db.Column(db.Integer, primary_key=True)
    missatge_id = db.Column(db.Integer, db.ForeignKey('missatges.id'), nullable=False)
    nom_fitxer = db.Column(db.String(255), nullable=False)
    tipus = db.Column(db.String(50))
    tipus_media = db.Column(db.String(20), nullable=True, default='desconegut')
    data_pujada = db.Column(db.DateTime, default=datetime.utcnow)

    missatge = db.relationship("Missatge", back_populates="arxius_adjunts")