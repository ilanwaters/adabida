from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from models import Aportacio, Usuari
from models import db
from datetime import datetime

admin_aportacions_bp = Blueprint('admin_aportacions', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            flash('Accés no autoritzat', 'error')
            return redirect(url_for('inici'))
        return f(*args, **kwargs)
    return decorated_function

@admin_aportacions_bp.route('/aportacions')
@login_required
@admin_required
def aportacions():
    aportacions = Aportacio.query.order_by(Aportacio.data.desc()).all()
    total = db.session.query(db.func.sum(Aportacio.quantitat)).filter_by(estat='confirmada').scalar() or 0
    return render_template('admin/aportacions.html', 
                         aportacions=aportacions,
                         total=total)

@admin_aportacions_bp.route('/aportacions/nova', methods=['GET', 'POST'])
@login_required
@admin_required
def nova_aportacio():
    if request.method == 'POST':
        aportacio = Aportacio(
            usuari_id=request.form.get('usuari_id') or None,
            quantitat=request.form['quantitat'],
            data=datetime.strptime(request.form['data'], '%Y-%m-%d'),
            metode_pagament=request.form.get('metode_pagament'),
            estat=request.form['estat'],
            notes=request.form.get('notes'),
            pais=request.form.get('pais'),
            referit_per=request.form.get('referit_per') or None,
            comissio_percentatge=request.form.get('comissio_percentatge') or None,
            comissio_pagada=request.form.get('comissio_pagada') == 'on'
        )
        db.session.add(aportacio)
        db.session.commit()
        flash('Aportació registrada correctament', 'success')
        return redirect(url_for('admin_aportacions.aportacions'))
    
    usuaris = Usuari.query.order_by(Usuari.nom).all()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('admin/nova_aportacio.html', usuaris=usuaris, today=today)