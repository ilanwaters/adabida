from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, BiografiaOrganitzacioSeccion, Organitzacio, MembreOrganitzacio
from datetime import datetime

historia_organitzacio_bp = Blueprint('historia_organitzacio', __name__, url_prefix='/organitzacio/<int:organitzacio_id>/historia')


def _es_membre_organitzacio(organitzacio_id):
    """Comprova si l'usuari actual és membre de l'organització"""
    return MembreOrganitzacio.query.filter_by(
        organitzacio_id=organitzacio_id,
        usuari_id=current_user.id
    ).first() is not None


def _es_admin_organitzacio(organitzacio_id):
    """Comprova si l'usuari actual és admin de l'organització"""
    membre = MembreOrganitzacio.query.filter_by(
        organitzacio_id=organitzacio_id,
        usuari_id=current_user.id
    ).first()
    return membre and membre.rol in ['admin', 'administrador', 'creador']


# ============================================
# VISUALITZACIÓ
# ============================================

@historia_organitzacio_bp.route('/')
@login_required
def llistar(organitzacio_id):
    """
    Mostra totes les seccions d'història de l'organització.
    Interfície estil Wikipedia amb botons [Editar] a cada secció.
    """
    organitzacio = Organitzacio.query.get_or_404(organitzacio_id)
    
    # Verificar que és membre
    if not _es_membre_organitzacio(organitzacio_id):
        flash('No tens permís per veure aquesta organització', 'error')
        return redirect(url_for('inici.inici_pagina'))
    
    # Obtenir seccions ordenades
    seccions = BiografiaOrganitzacioSeccion.query.filter_by(
        organitzacio_id=organitzacio_id
    ).order_by(BiografiaOrganitzacioSeccion.ordre.asc()).all()
    
    es_admin = _es_admin_organitzacio(organitzacio_id)
    
    return render_template(
        'organitzacions/historia_organitzacio.html',
        organitzacio=organitzacio,
        seccions=seccions,
        es_admin=es_admin
    )


# ============================================
# CREAR SECCIÓ
# ============================================

@historia_organitzacio_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def crear_seccio(organitzacio_id):
    """
    Crea una nova secció d'història d'organització.
    Només admins poden crear seccions.
    """
    organitzacio = Organitzacio.query.get_or_404(organitzacio_id)
    
    # Verificar que és admin
    if not _es_admin_organitzacio(organitzacio_id):
        flash('Només els administradors poden crear seccions', 'error')
        return redirect(url_for('historia_organitzacio.llistar', organitzacio_id=organitzacio_id))
    
    if request.method == 'POST':
        titol = request.form.get('titol', '').strip()
        contingut = request.form.get('contingut', '').strip()
        visible = request.form.get('visible') == 'on'
        
        if not titol:
            flash('El títol és obligatori', 'error')
            return redirect(url_for('historia_organitzacio.crear_seccio', organitzacio_id=organitzacio_id))
        
        # Determinar ordre (afegir al final)
        ultima_seccio = BiografiaOrganitzacioSeccion.query.filter_by(
            organitzacio_id=organitzacio_id
        ).order_by(BiografiaOrganitzacioSeccion.ordre.desc()).first()
        
        nou_ordre = (ultima_seccio.ordre + 1) if ultima_seccio else 0
        
        # Crear secció
        nova_seccio = BiografiaOrganitzacioSeccion(
            organitzacio_id=organitzacio_id,
            titol=titol,
            contingut=contingut,
            ordre=nou_ordre,
            visible=visible
        )
        
        db.session.add(nova_seccio)
        db.session.commit()
        
        flash(f'Secció "{titol}" creada correctament', 'success')
        return redirect(url_for('historia_organitzacio.llistar', organitzacio_id=organitzacio_id))
    
    return render_template('organitzacions/historia_organitzacio_form.html', organitzacio=organitzacio, seccio=None)


# ============================================
# EDITAR SECCIÓ
# ============================================

@historia_organitzacio_bp.route('/<int:seccio_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_seccio(organitzacio_id, seccio_id):
    """
    Edita una secció existent.
    Només admins poden editar.
    """
    organitzacio = Organitzacio.query.get_or_404(organitzacio_id)
    seccio = BiografiaOrganitzacioSeccion.query.get_or_404(seccio_id)
    
    # Verificar que la secció pertany a aquesta organització
    if seccio.organitzacio_id != organitzacio_id:
        flash('Secció no trobada', 'error')
        return redirect(url_for('historia_organitzacio.llistar', organitzacio_id=organitzacio_id))
    
    # Verificar que és admin
    if not _es_admin_organitzacio(organitzacio_id):
        flash('Només els administradors poden editar seccions', 'error')
        return redirect(url_for('historia_organitzacio.llistar', organitzacio_id=organitzacio_id))
    
    if request.method == 'POST':
        seccio.titol = request.form.get('titol', '').strip()
        seccio.contingut = request.form.get('contingut', '').strip()
        seccio.visible = request.form.get('visible') == 'on'
        seccio.data_modificacio = datetime.utcnow()
        
        if not seccio.titol:
            flash('El títol és obligatori', 'error')
            return render_template('organitzacions/historia_organitzacio_form.html', organitzacio=organitzacio, seccio=seccio)
        
        db.session.commit()
        flash(f'Secció "{seccio.titol}" actualitzada correctament', 'success')
        return redirect(url_for('historia_organitzacio.llistar', organitzacio_id=organitzacio_id))
    
    return render_template('organitzacions/historia_organitzacio_form.html', organitzacio=organitzacio, seccio=seccio)


# ============================================
# ELIMINAR SECCIÓ
# ============================================

@historia_organitzacio_bp.route('/<int:seccio_id>/eliminar', methods=['POST'])
@login_required
def eliminar_seccio(organitzacio_id, seccio_id):
    """
    Elimina una secció d'història d'organització.
    Només admins poden eliminar.
    """
    seccio = BiografiaOrganitzacioSeccion.query.get_or_404(seccio_id)
    
    # Verificar que la secció pertany a aquesta organització
    if seccio.organitzacio_id != organitzacio_id:
        return jsonify({'success': False, 'error': 'Secció no trobada'}), 404
    
    # Verificar que és admin
    if not _es_admin_organitzacio(organitzacio_id):
        return jsonify({'success': False, 'error': 'No autoritzat'}), 403
    
    titol = seccio.titol
    db.session.delete(seccio)
    db.session.commit()
    
    # Reordenar les seccions restants
    seccions_restants = BiografiaOrganitzacioSeccion.query.filter_by(
        organitzacio_id=organitzacio_id
    ).order_by(BiografiaOrganitzacioSeccion.ordre.asc()).all()
    
    for i, s in enumerate(seccions_restants):
        s.ordre = i
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({'success': True, 'message': f'Secció "{titol}" eliminada'})
    
    flash(f'Secció "{titol}" eliminada correctament', 'success')
    return redirect(url_for('historia_organitzacio.llistar', organitzacio_id=organitzacio_id))


# ============================================
# MOURE SECCIÓ (AMUNT/AVALL)
# ============================================

@historia_organitzacio_bp.route('/<int:seccio_id>/moure/<direccio>', methods=['POST'])
@login_required
def moure_seccio(organitzacio_id, seccio_id, direccio):
    """
    Mou una secció amunt o avall.
    Només admins poden moure seccions.
    """
    if direccio not in ['amunt', 'avall']:
        return jsonify({'success': False, 'error': 'Direcció no vàlida'}), 400
    
    seccio = BiografiaOrganitzacioSeccion.query.get_or_404(seccio_id)
    
    # Verificar que la secció pertany a aquesta organització
    if seccio.organitzacio_id != organitzacio_id:
        return jsonify({'success': False, 'error': 'Secció no trobada'}), 404
    
    # Verificar que és admin
    if not _es_admin_organitzacio(organitzacio_id):
        return jsonify({'success': False, 'error': 'No autoritzat'}), 403
    
    # Obtenir totes les seccions ordenades
    seccions = BiografiaOrganitzacioSeccion.query.filter_by(
        organitzacio_id=organitzacio_id
    ).order_by(BiografiaOrganitzacioSeccion.ordre.asc()).all()
    
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

@historia_organitzacio_bp.route('/<int:seccio_id>/toggle-visibilitat', methods=['POST'])
@login_required
def toggle_visibilitat(organitzacio_id, seccio_id):
    """
    Canvia la visibilitat d'una secció (pública/privada).
    Només admins poden canviar visibilitat.
    """
    seccio = BiografiaOrganitzacioSeccion.query.get_or_404(seccio_id)
    
    # Verificar que la secció pertany a aquesta organització
    if seccio.organitzacio_id != organitzacio_id:
        return jsonify({'success': False, 'error': 'Secció no trobada'}), 404
    
    # Verificar que és admin
    if not _es_admin_organitzacio(organitzacio_id):
        return jsonify({'success': False, 'error': 'No autoritzat'}), 403
    
    seccio.visible = not seccio.visible
    db.session.commit()
    
    estat = 'pública' if seccio.visible else 'privada'
    
    return jsonify({
        'success': True,
        'visible': seccio.visible,
        'message': f'Secció ara és {estat}'
    })