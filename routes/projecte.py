from flask import Blueprint, render_template

projecte_bp = Blueprint('projecte', __name__, url_prefix='/projecte')


@projecte_bp.route('/')
def index():
    """Pàgina principal del projecte"""
    return render_template('projecte/index.html')


@projecte_bp.route('/metodologia')
def metodologia():
    """Metodologia d'entrevista"""
    return render_template('projecte/metodologia.html')


@projecte_bp.route('/tallers')
def tallers():
    """Informació sobre tallers"""
    return render_template('projecte/tallers.html')


@projecte_bp.route('/faq')
def faq():
    """Preguntes freqüents"""
    return render_template('projecte/faq.html')


@projecte_bp.route('/documents')
def documents():
    """Centre de descàrregues"""
    return render_template('projecte/documents.html')


@projecte_bp.route('/contacte')
def contacte():
    """Contacte per organitzacions"""
    return render_template('projecte/contacte.html')