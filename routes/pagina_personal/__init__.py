# routes/pagina_personal/__init__.py

from .pagina_personal import pagina_personal_bp
from .personal_biografia import personal_biografia_bp
from .perfil_public import perfil_public_bp  # ← Importar des del fitxer local
from .biografia_seccions import biografia_seccions_bp 

__all__ = ['pagina_personal_bp', 'personal_biografia_bp', 'perfil_public_bp']