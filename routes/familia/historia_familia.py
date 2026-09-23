from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, BiografiaFamiliaSeccion, EspaiFamiliar, MembreFamilia
from datetime import datetime
from utils.temps import ara_utc

historia_familia_bp = Blueprint('historia_familia', __name__, url_prefix='/familia/<int:familia_id>/historia')


def _es_membre_familia(familia_id):
    """Comprova si l'usuari actual és membre de la família"""
    return MembreFamilia.query.filter_by(
        espai_familiar_id=familia_id,
        usuari_id=current_user.id
    ).first() is not None


def _es_admin_familia(familia_id):
    """Comprova si l'usuari actual és admin de la família"""
    membre = MembreFamilia.query.filter_by(
        espai_familiar_id=familia_id,
        usuari_id=current_user.id
    ).first()
    return membre and membre.rol in ['admin','administrador', 'creador']


# ============================================
# VISUALITZACIÓ
# ============================================

@historia_familia_bp.route('/')
@login_required
def llistar(familia_id):
    """
    Mostra totes les seccions d'història de la família.
    Interfície estil Wikipedia amb botons [Editar] a cada secció.
    """
    familia = EspaiFamiliar.query.get_or_404(familia_id)
    
    # Verificar que és membre
    if not _es_membre_familia(familia_id):
        flash('No tens permís per veure aquesta família', 'error')
        return redirect(url_for('inici.inici_pagina'))
    
    # Obtenir seccions ordenades
    seccions = BiografiaFamiliaSeccion.query.filter_by(
        familia_id=familia_id
    ).order_by(BiografiaFamiliaSeccion.ordre.asc()).all()
    
    es_admin = _es_admin_familia(familia_id)
    
    return render_template(
        'familia/historia_familia.html',
        familia=familia,
        seccions=seccions,
        es_admin=es_admin
    )
# ============================================
# CREAR SECCIÓ
# ============================================

@historia_familia_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def crear_seccio(familia_id):
    """
    Crea una nova secció d'història familiar.
    Només admins poden crear seccions.
    """
    familia = EspaiFamiliar.query.get_or_404(familia_id)
    
    # Verificar que és admin
    if not _es_admin_familia(familia_id):
        flash('Només els administradors poden crear seccions', 'error')
        return redirect(url_for('historia_familia.llistar', familia_id=familia_id))
    
    if request.method == 'POST':
        titol = request.form.get('titol', '').strip()
        contingut = request.form.get('contingut', '').strip()
        visible = request.form.get('visible') == 'on'
        
        if not titol:
            flash('El títol és obligatori', 'error')
            return redirect(url_for('historia_familia.crear_seccio', familia_id=familia_id))
        
        # Determinar ordre (afegir al final)
        ultima_seccio = BiografiaFamiliaSeccion.query.filter_by(
            familia_id=familia_id
        ).order_by(BiografiaFamiliaSeccion.ordre.desc()).first()
        
        nou_ordre = (ultima_seccio.ordre + 1) if ultima_seccio else 0
        
        # Crear secció
        nova_seccio = BiografiaFamiliaSeccion(
            familia_id=familia_id,
            titol=titol,
            contingut=contingut,
            ordre=nou_ordre,
            visible=visible
        )
        
        db.session.add(nova_seccio)
        db.session.commit()
        
        flash(f'Secció "{titol}" creada correctament', 'success')
        return redirect(url_for('historia_familia.llistar', familia_id=familia_id))
    
    return render_template('familia/historia_familia_form.html', familia=familia, seccio=None)


# ============================================
# EDITAR SECCIÓ
# ============================================

@historia_familia_bp.route('/<int:seccio_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_seccio(familia_id, seccio_id):
    """
    Edita una secció existent.
    Només admins poden editar.
    """
    familia = EspaiFamiliar.query.get_or_404(familia_id)
    seccio = BiografiaFamiliaSeccion.query.get_or_404(seccio_id)
    
    # Verificar que la secció pertany a aquesta família
    if seccio.familia_id != familia_id:
        flash('Secció no trobada', 'error')
        return redirect(url_for('historia_familia.llistar', familia_id=familia_id))
    
    # Verificar que és admin
    if not _es_admin_familia(familia_id):
        flash('Només els administradors poden editar seccions', 'error')
        return redirect(url_for('historia_familia.llistar', familia_id=familia_id))
    
    if request.method == 'POST':
        seccio.titol = request.form.get('titol', '').strip()
        seccio.contingut = request.form.get('contingut', '').strip()
        seccio.visible = request.form.get('visible') == 'on'
        seccio.data_modificacio = ara_utc()
        
        if not seccio.titol:
            flash('El títol és obligatori', 'error')
            return render_template('familia/historia_seccio_form.html', familia=familia, seccio=seccio)
        
        db.session.commit()
        flash(f'Secció "{seccio.titol}" actualitzada correctament', 'success')
        return redirect(url_for('historia_familia.llistar', familia_id=familia_id))
    
    return render_template('familia/historia_seccio_form.html', familia=familia, seccio=seccio)


# ============================================
# ELIMINAR SECCIÓ
# ============================================

@historia_familia_bp.route('/<int:seccio_id>/eliminar', methods=['POST'])
@login_required
def eliminar_seccio(familia_id, seccio_id):
    """
    Elimina una secció d'història familiar.
    Només admins poden eliminar.
    """
    seccio = BiografiaFamiliaSeccion.query.get_or_404(seccio_id)
    
    # Verificar que la secció pertany a aquesta família
    if seccio.familia_id != familia_id:
        return jsonify({'success': False, 'error': 'Secció no trobada'}), 404
    
    # Verificar que és admin
    if not _es_admin_familia(familia_id):
        return jsonify({'success': False, 'error': 'No autoritzat'}), 403
    
    titol = seccio.titol
    db.session.delete(seccio)
    db.session.commit()
    
    # Reordenar les seccions restants
    seccions_restants = BiografiaFamiliaSeccion.query.filter_by(
        familia_id=familia_id
    ).order_by(BiografiaFamiliaSeccion.ordre.asc()).all()
    
    for i, s in enumerate(seccions_restants):
        s.ordre = i
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({'success': True, 'message': f'Secció "{titol}" eliminada'})
    
    flash(f'Secció "{titol}" eliminada correctament', 'success')
    return redirect(url_for('historia_familia.llistar', familia_id=familia_id))


# ============================================
# MOURE SECCIÓ (AMUNT/AVALL)
# ============================================

@historia_familia_bp.route('/<int:seccio_id>/moure/<direccio>', methods=['POST'])
@login_required
def moure_seccio(familia_id, seccio_id, direccio):
    """
    Mou una secció amunt o avall.
    Només admins poden moure seccions.
    """
    if direccio not in ['amunt', 'avall']:
        return jsonify({'success': False, 'error': 'Direcció no vàlida'}), 400
    
    seccio = BiografiaFamiliaSeccion.query.get_or_404(seccio_id)
    
    # Verificar que la secció pertany a aquesta família
    if seccio.familia_id != familia_id:
        return jsonify({'success': False, 'error': 'Secció no trobada'}), 404
    
    # Verificar que és admin
    if not _es_admin_familia(familia_id):
        return jsonify({'success': False, 'error': 'No autoritzat'}), 403
    
    # Obtenir totes les seccions ordenades
    seccions = BiografiaFamiliaSeccion.query.filter_by(
        familia_id=familia_id
    ).order_by(BiografiaFamiliaSeccion.ordre.asc()).all()
    
    index_actual = next(i for i, s in enumerate(seccions) if s.id == seccio_id)
    
    if direccio == 'amunt' and index_actual > 0:
        # Intercanviar amb l'anterior
        seccions[index_actual].ordre, seccions[index_actual - 1].ordre = \
            seccions[index_actual - 1].ordre, seccions[index_actual].ordre
    
    elif direccio == 'avall' and index_actual < len(seccions) - 1:
        # Intercanviar amb el següent
        seccions[index_actual].ordre, seccions[index_actual + 1].ordre = \
            seccions[index_actual + 1].ordre, seccions[index_actual].ordre
    
    else:
        return jsonify({'success': False, 'message': 'No es pot moure més'})
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Secció moguda'})


# ============================================
# CANVIAR VISIBILITAT
# ============================================

@historia_familia_bp.route('/<int:seccio_id>/toggle-visibilitat', methods=['POST'])
@login_required
def toggle_visibilitat(familia_id, seccio_id):
    """
    Canvia la visibilitat d'una secció (pública/privada).
    Només admins poden canviar visibilitat.
    """
    seccio = BiografiaFamiliaSeccion.query.get_or_404(seccio_id)
    
    # Verificar que la secció pertany a aquesta família
    if seccio.familia_id != familia_id:
        return jsonify({'success': False, 'error': 'Secció no trobada'}), 404
    
    # Verificar que és admin
    if not _es_admin_familia(familia_id):
        return jsonify({'success': False, 'error': 'No autoritzat'}), 403
    
    seccio.visible = not seccio.visible
    db.session.commit()
    
    estat = 'pública' if seccio.visible else 'privada'
    
    return jsonify({
        'success': True,
        'visible': seccio.visible,
        'message': f'Secció ara és {estat}'
    })