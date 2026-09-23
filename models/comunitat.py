from models import db
from datetime import datetime
from utils.temps import ara_utc


class PeticioTestimoni(db.Model):
    """
    Model per gestionar peticions de testimonis de la comunitat.
    Qualsevol usuari pot demanar testimonis sobre un tema,
    i qualsevol usuari pot respondre creant una entrada.
    """
    __tablename__ = 'peticions_testimoni'

    id = db.Column(db.Integer, primary_key=True)
    
    # Usuari que fa la petició
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    
    # Contingut de la petició
    tema = db.Column(db.String(200), nullable=False)  # Ex: "la guerra yugoslava"
    descripcio = db.Column(db.Text)  # Descripció opcional més detallada
    
    # Estat
    completada = db.Column(db.Boolean, default=False)
    data_creacio = db.Column(db.DateTime, default=ara_utc)
    data_completada = db.Column(db.DateTime, nullable=True)
    
    # Si algú respon, qui ho fa i quina entrada crea
    resposta_usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=True)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=True)
    
    # Relacions
    usuari = db.relationship('Usuari', foreign_keys=[usuari_id], backref='peticions_creades')
    resposta_usuari = db.relationship('Usuari', foreign_keys=[resposta_usuari_id], backref='peticions_respostes')
    entrada = db.relationship('Entrada', backref='peticio_origen')

    def __repr__(self):
        return f'<PeticioTestimoni {self.tema}>'


class Denuncia(db.Model):
    """
    Model per gestionar denúncies de contingut per part de la comunitat.
    Només usuaris verificats (nivell verd) poden denunciar.
    """
    __tablename__ = 'denuncies'

    id = db.Column(db.Integer, primary_key=True)
    
    # Qui denuncia (només usuaris nivell verd)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    
    # Què es denuncia
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=False)
    
    # Categoria de denúncia
    categoria = db.Column(db.String(50), nullable=False)  
    # Opcions: 'contingut_inadequat', 'desinformacio', 'dades_controvertides', 'ofensiu', 'altres'
    
    # Detalls
    descripcio = db.Column(db.Text, nullable=False)  # Explicació de la denúncia
    
    # Estat de la denúncia
    estat = db.Column(db.String(20), default='pendent')  
    # Opcions: 'pendent', 'revisada', 'acceptada', 'rebutjada'
    
    # Dates
    data_creacio = db.Column(db.DateTime, default=ara_utc)
    data_revisio = db.Column(db.DateTime, nullable=True)
    
    # Admin que revisa
    revisat_per_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=True)
    notes_admin = db.Column(db.Text, nullable=True)  # Notes internes de l'admin
    
    # Acció presa
    accio = db.Column(db.String(50), nullable=True)  
    # Opcions: 'eliminada', 'editada', 'ignorada', 'advertencia_usuari'
    
    # Relacions
    usuari = db.relationship('Usuari', foreign_keys=[usuari_id], backref='denuncies_creades')
    entrada = db.relationship('Entrada', backref='denuncies')
    revisat_per = db.relationship('Usuari', foreign_keys=[revisat_per_id], backref='denuncies_revisades')

    def __repr__(self):
        return f'<Denuncia {self.id} - Entrada {self.entrada_id}>'


class CategoriaForum(db.Model):
    """
    Categories del fòrum (ex: Història local, Memòria oral, Qüestions tècniques, etc.)
    """
    __tablename__ = 'categories_forum'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    descripcio = db.Column(db.Text)
    ordre = db.Column(db.Integer, default=0)  # Per ordenar les categories
    activa = db.Column(db.Boolean, default=True)
    
    # Relacions
    temes = db.relationship('TemaForum', back_populates='categoria', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<CategoriaForum {self.nom}>'


class TemaForum(db.Model):
    """
    Tema de discussió al fòrum.
    Pot estar vinculat a una entrada específica del repositori.
    """
    __tablename__ = 'temes_forum'

    id = db.Column(db.Integer, primary_key=True)
    
    # Categoria i títol
    categoria_id = db.Column(db.Integer, db.ForeignKey('categories_forum.id'), nullable=False)
    titol = db.Column(db.String(200), nullable=False)
    
    # Usuari que crea el tema (només usuaris nivell verd)
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    
    # Vinculació opcional amb entrada
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrades.id'), nullable=True)
    
    # Estat
    tancat = db.Column(db.Boolean, default=False)  # Els admins poden tancar temes
    fixat = db.Column(db.Boolean, default=False)   # Temes destacats
    
    # Dates
    data_creacio = db.Column(db.DateTime, default=ara_utc)
    data_ultim_missatge = db.Column(db.DateTime, default=ara_utc)
    
    # Comptadors
    nombre_respostes = db.Column(db.Integer, default=0)
    nombre_visites = db.Column(db.Integer, default=0)
    
    # Relacions
    categoria = db.relationship('CategoriaForum', back_populates='temes')
    usuari = db.relationship('Usuari', backref='temes_forum')
    entrada = db.relationship('Entrada', backref='temes_discussio')
    missatges = db.relationship('MissatgeForum', back_populates='tema', cascade='all, delete-orphan', order_by='MissatgeForum.data_creacio')

    def __repr__(self):
        return f'<TemaForum {self.titol}>'


class MissatgeForum(db.Model):
    """
    Missatge individual dins d'un tema del fòrum.
    """
    __tablename__ = 'missatges_forum'

    id = db.Column(db.Integer, primary_key=True)
    
    # Tema al qual pertany
    tema_id = db.Column(db.Integer, db.ForeignKey('temes_forum.id'), nullable=False)
    
    # Autor del missatge
    usuari_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'), nullable=False)
    
    # Contingut
    contingut = db.Column(db.Text, nullable=False)
    
    # Dates
    data_creacio = db.Column(db.DateTime, default=ara_utc)
    data_modificacio = db.Column(db.DateTime, nullable=True)
    editat = db.Column(db.Boolean, default=False)
    
    # Moderació
    moderat = db.Column(db.Boolean, default=False)  # Si ha estat moderat per un admin
    motiu_moderacio = db.Column(db.Text, nullable=True)
    
    # Relacions
    tema = db.relationship('TemaForum', back_populates='missatges')
    usuari = db.relationship('Usuari', backref='missatges_forum')

    def __repr__(self):
        return f'<MissatgeForum {self.id} - Tema {self.tema_id}>'