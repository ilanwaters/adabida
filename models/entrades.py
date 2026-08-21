from models import db
from datetime import datetime


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
    data_modificacio = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
    
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
    @property
    def miniatura(self):
        """Retorna la portada triada per l'usuari, si n'hi ha, si no la primera imatge, si no placeholder"""
        portada = next((a for a in self.arxius_adjuntats if a.es_portada), None)
        if portada:
            any_mes = portada.data_pujada.strftime('%Y/%m') if portada.data_pujada else ''
            return f"/umberto/{self.usuari.nom_login}/{self.id}/mini/{portada.nom_fitxer}"
        if self.imatges:
            primera_imatge = self.imatges[0]
            any_mes = primera_imatge.data_publicacio.strftime('%Y/%m')
            return f"/umberto/media/galeria/{any_mes}/{primera_imatge.nom_fitxer}"
        return '/static/icons/sense_imatge.png'

    @property
    def imatge_gran(self):
        """Igual que miniatura per ara"""
        return self.miniatura


class ArxiuAdjunt(db.Model):
    __tablename__ = 'arxius_adjuntats'

    id = db.Column(db.Integer, primary_key=True)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=False)
    nom_fitxer = db.Column(db.String(255), nullable=False)
    tipus = db.Column(db.String(50))
    tipus_media = db.Column(db.String(20), nullable=True, default='desconegut')
    data_pujada = db.Column(db.DateTime, default=datetime.utcnow)
    titol = db.Column(db.String(255), nullable=True)
    any_arxiu = db.Column(db.Integer, nullable=True)
    pais = db.Column(db.String(100), nullable=True)
    regio = db.Column(db.String(100), nullable=True)
    municipi = db.Column(db.String(100), nullable=True)
    descripcio = db.Column(db.Text, nullable=True)
    referencia = db.Column(db.String(255), nullable=True)
    es_conversa = db.Column(db.Boolean, default=False, nullable=False)
    es_portada = db.Column(db.Boolean, default=False, nullable=False)
    entrada = db.relationship("Entrada", back_populates="arxius_adjuntats")


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


class ImatgeGaleria(db.Model):
    __tablename__ = 'imatges_galeria'
    
    id = db.Column(db.Integer, primary_key=True)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=True)
    exposicio_id = db.Column(db.Integer, db.ForeignKey('exposicions.id'), nullable=True)
    nom_fitxer = db.Column(db.String(255), nullable=False)
    destinacio = db.Column(db.String(50))
    data_publicacio = db.Column(db.DateTime, default=datetime.utcnow)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'))
    mida = db.Column(db.String, default="mitjana")
    descripcio = db.Column(db.Text)
    entrada = db.relationship("Entrada", back_populates="imatges")
    exposicio = db.relationship("Exposicio", back_populates="imatges")
    usuari = db.relationship("Usuari", backref="imatges_galeria")


class ImatgeExposicio(db.Model):
    __tablename__ = 'imatges_exposicio'
    
    id = db.Column(db.Integer, primary_key=True)
    imatge_id = db.Column(db.Integer, db.ForeignKey('imatges_galeria.id'), nullable=False)
    ruta_expo = db.Column(db.String(255), nullable=False)
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

class Conversa(db.Model):
    """Model per gestionar converses i diàlegs entre humans"""
    __tablename__ = 'conversa'
    
    id = db.Column(db.Integer, primary_key=True)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    
    # Dades de la conversa
    lloc_institucio = db.Column(db.String(200))
    lloc_municipi = db.Column(db.String(100))
    lloc_regio = db.Column(db.String(100))
    lloc_pais = db.Column(db.String(100))
    data_conversa = db.Column(db.Date)
    durada_minuts = db.Column(db.Integer)
    observacions_generals = db.Column(db.Text)
    # Tipus conversa
    tipus_conversa = db.Column(db.String(50), default='lliure')

# Contingut testimoni (per entrevistes Adabida)
    titol = db.Column(db.String(255))
    tema = db.Column(db.String(255))
    contingut = db.Column(db.Text)

# Protocol Entrevista Adabida
    consentiment_informat = db.Column(db.Boolean, default=False)
    notes_preparacio = db.Column(db.Text)
    notes_camp = db.Column(db.Text)
    observacions_post = db.Column(db.Text)

# Visibilitat
    visible_publicament = db.Column(db.Boolean, default=False)
    notes_metodologiques_publiques = db.Column(db.Boolean, default=False)
    # Arxiu multimèdia (mateixa lògica que entrades)
    arxiu_nom = db.Column(db.String(255))
    arxiu_tipus = db.Column(db.String(50))  # 'audio', 'video'
    arxiu_tamany = db.Column(db.BigInteger)  # en bytes  
    
    # Organització (opcional - per compartir)
    organitzacio_id = db.Column(db.Integer, db.ForeignKey('organitzacions.id'), nullable=True)    
    # Vinculació amb entrada (si és entrevista Adabida)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=True)
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