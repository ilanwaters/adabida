from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.tematiques import Tema
from models.traduccio_tema import TraducioTema
from config import Config

admin_traduccions_bp = Blueprint('admin_traduccions', __name__, url_prefix='/admin')

@admin_traduccions_bp.route('/traduccions-temes')
@login_required
def traduccions_temes():
    if not current_user.es_admin: 
        flash('Accés denegat', 'error')
        return redirect(url_for('inici.inici'))
    
    temes = Tema.query.all()
    idiomes = Config.IDIOMES_DISPONIBLES if hasattr(Config, 'IDIOMES_DISPONIBLES') else ['ca', 'es', 'en']
    
    # Calcular estat de cada tema
    temes_amb_estat = []
    for tema in temes:
        traduccions_count = TraducioTema.query.filter_by(tema_id=tema.id).count()
        temes_amb_estat.append({
            'tema': tema,
            'traduccions_count': traduccions_count,
            'total_idiomes': len(idiomes)
        })
    
    # Ordenar: sense traduccions primer
    temes_amb_estat.sort(key=lambda x: x['traduccions_count'])
    
    return render_template('admin/traduccions_temes.html', 
                          temes_data=temes_amb_estat,
                          idiomes=idiomes)


@admin_traduccions_bp.route('/traduccions-temes/guardar/<int:tema_id>', methods=['POST'])
@login_required
def guardar_traduccions(tema_id):
    if not current_user.es_admin:
        return redirect(url_for('inici.inici'))
    
    tema = Tema.query.get_or_404(tema_id)
    idiomes = Config.IDIOMES_DISPONIBLES if hasattr(Config, 'IDIOMES_DISPONIBLES') else ['ca', 'es', 'en']
    
    for idioma in idiomes:
        nom_traduit = request.form.get(f'trad_{idioma}', '').strip()
        if nom_traduit:
            # Buscar si ja existeix
            traduccio = TraducioTema.query.filter_by(tema_id=tema_id, idioma=idioma).first()
            if traduccio:
                traduccio.nom = nom_traduit
            else:
                nova = TraducioTema(tema_id=tema_id, idioma=idioma, nom=nom_traduit)
                db.session.add(nova)
    
    db.session.commit()
    flash(f'Traduccions guardades per: {tema.nom}', 'success')
    return redirect(url_for('admin_traduccions.traduccions_temes'))