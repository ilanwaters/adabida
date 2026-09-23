from flask import Blueprint

familia_bp = Blueprint('familia', __name__, url_prefix='/familia')

from routes.familia import familia
from .historia_familia import historia_familia_bp

__all__ = ['familia_bp', 'membres_bp', 'administrar_bp', 'historia_familia_bp']