from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.tematiques import Tema
from models.categoria import Categoria  # ← AFEGIR
from models.traduccio_tema import TraducioTema
from models.traduccio_categoria_portada import TraducioCategoria  # ← AFEGIR
from config import Config

admin_traduccions_bp = Blueprint('admin_traduccions', __name__, url_prefix='/admin')

@admin_traduccions_bp.route('/traduccions')
@login_required
def traduccions():
    if not current_user.es_admin: 
        flash('Accés denegat', 'error')
        return redirect(url_for('inici.inici'))
    
    # Obtenir tipus: 'temes' (defecte) o 'categories'
    tipus = request.args.get('tipus', 'temes')
    
    # Obtenir objectes segons tipus
    if tipus == 'categories':
        objectes = Categoria.query.all()  
        ModelTraduccio = TraducioCategoria  
        camp_fk = 'categoria_id'
    else:  
        objectes = Tema.query.all()
        ModelTraduccio = TraducioTema
        camp_fk = 'tema_id'
    
    idiomes = Config.IDIOMES_DISPONIBLES
    idiomes_noms = Config.IDIOMES_NOMS
    
    # Calcular estat de cada objecte
    dades_amb_estat = []
    for obj in objectes:
        traduccions_count = ModelTraduccio.query.filter_by(**{camp_fk: obj.id}).count()
        dades_amb_estat.append({
            'objecte': obj,
            'traduccions_count': traduccions_count,
            'total_idiomes': len(idiomes)
        })
    
    # Ordenar: sense traduccions primer
    dades_amb_estat.sort(key=lambda x: x['traduccions_count'])
    
    return render_template('admin/traduccions.html', 
                          dades=dades_amb_estat,
                          idiomes=idiomes,
                          idiomes_noms=idiomes_noms,
                          tipus=tipus)


@admin_traduccions_bp.route('/traduccions/guardar', methods=['POST'])
@login_required
def guardar_traduccions():
    if not current_user.es_admin:
        return redirect(url_for('inici.inici'))
    
    tipus = request.form.get('tipus')
    objecte_id = int(request.form.get('objecte_id'))
    
    # Determinar model segons tipus
    # Determinar model segons tipus
    if tipus == 'categories':
        objecte = Categoria.query.get_or_404(objecte_id)  # ← CANVIAT (abans CategoriaTema)
        ModelTraduccio = TraducioCategoria  # ← CANVIAT (abans TraducioCategoriaTema)
        camp_fk = 'categoria_id'
    else:  # temes
        objecte = Tema.query.get_or_404(objecte_id)
        ModelTraduccio = TraducioTema
        camp_fk = 'tema_id'
    
    idiomes = Config.IDIOMES_DISPONIBLES
    
    for idioma in idiomes:
        nom_traduit = request.form.get(f'trad_{idioma}', '').strip()
        if nom_traduit:
            # Buscar si ja existeix
            traduccio = ModelTraduccio.query.filter_by(**{camp_fk: objecte_id, 'idioma': idioma}).first()
            if traduccio:
                traduccio.nom = nom_traduit
            else:
                nova = ModelTraduccio(**{camp_fk: objecte_id, 'idioma': idioma, 'nom': nom_traduit})
                db.session.add(nova)
    
    db.session.commit()
    flash(f'Traduccions guardades per: {objecte.nom}', 'success')
    return redirect(url_for('admin_traduccions.traduccions', tipus=tipus))