from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
from models.usuari import (
    Usuari, PerfilBiografic, BiografiaSeccion,
    Experiencia, Estudi, CarrecPublic, Obra, Missatge
)
from models.entrades import (
    Entrada, ArxiuAdjunt, Exposicio, ImatgeGaleria, 
    ImatgeExposicio, EntradaGuardada, ArxiuEntrada,
    Conversa, ConversaParticipant  
)
from models.organitzacions import (
    Organitzacio, MembreOrganitzacio, EntradaOrganitzacio,
    SolicitudOrganitzacio, BiografiaOrganitzacioSeccion, MissatgeOrganitzacio
)
from models.families import (
    EspaiFamiliar, MembreFamilia, EntradaFamilia,
    UbicacioOrigenFamilia, UbicacioActualFamilia, Matrimoni,
    DocumentMembreFamilia, BiografiaFamiliaSeccion
)
from models.ubicacions import Pais, Regio, Municipi, TraducioUbicacio
from models.blog import EntradaBlog
from models.interaccions import Contacte
from models.comunitat import (
    PeticioTestimoni, Denuncia,
    CategoriaForum, TemaForum, MissatgeForum
)
from models.tematiques import CategoriaTema, Tema
from models.categoria import Categoria

from models.traduccio_tema import TraducioTema

from models.tematiques import CategoriaTema, Tema, TemaExclusio

from .aportacio import Aportacio

__all__ = [
    'db',
    'Usuari', 
    'PerfilBiografic',
    'BiografiaSeccion',
    'Experiencia',
    'Estudi',
    'CarrecPublic',
    'Obra',
    'Missatge',
    'Contacte',
    'Entrada',
    'ArxiuAdjunt',
    'Exposicio',
    'ImatgeGaleria',
    'ImatgeExposicio',
    'EntradaGuardada',
    'ArxiuEntrada',
    'Conversa',
    'ConversaParticipant',
    'Organitzacio',
    'SolicitudOrganitzacio',
    'BiografiaOrganitzacioSeccion',
    'MissatgeOrganitzacio',
    'MembreOrganitzacio',
    'EntradaOrganitzacio',
    'EspaiFamiliar',
    'MembreFamilia',
    'EntradaFamilia','UbicacioOrigenFamilia',
    'UbicacioActualFamilia',
    'Matrimoni',
    'DocumentMembreFamilia',
    'BiografiaFamiliaSeccion',
    'Pais',
    'Regio',
    'Municipi',
    'TraducioUbicacio',
    'EntradaBlog',
    'PeticioTestimoni',
    'Denuncia',
    'CategoriaForum',
    'TemaForum',
    'MissatgeForum',
    'CategoriaTema', 
    'Tema',
    'TemaExclusio',
    'Categoria',
    'TraduccioTema',
    'Aportacio'
]