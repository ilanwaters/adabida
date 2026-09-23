
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, BiografiaSeccion
from datetime import datetime
from utils.temps import ara_utc

biografia_seccions_bp = Blueprint('biografia_seccions', __name__, url_prefix='/perfil/biografia-seccions')


# ============================================
# VISUALITZACIÓ
# ============================================

@biografia_seccions_bp.route('/')
@login_required
def llistar():
    """
    Mostra totes les seccions de biografia de l'usuari.
    Interfície estil Wikipedia amb botons [Editar] a cada secció.
    """
    seccions = current_user.obtenir_seccions_biografia_ordenades(nomes_visibles=False)
    
    return render_template(
        'pagina_personal/biografia_seccions.html',
        seccions=seccions
    )


# ============================================
# CREAR SECCIÓ
# ============================================

@biografia_seccions_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def crear_seccio():
    """
    Crea una nova secció de biografia.
    """
    if request.method == 'POST':
        titol = request.form.get('titol', '').strip()
        contingut = request.form.get('contingut', '').strip()
        visible = request.form.get('visible') == 'on'
        any_inici = request.form.get('any_inici', '').strip()
        any_final = request.form.get('any_final', '').strip()
        if not titol:
            flash('El títol és obligatori', 'error')
            return redirect(url_for('biografia_seccions.crear_seccio'))
        
        # Determinar ordre (afegir al final)
        ultima_seccio = BiografiaSeccion.query.filter_by(
            usuari_id=current_user.id
        ).order_by(BiografiaSeccion.ordre.desc()).first()
        
        nou_ordre = (ultima_seccio.ordre + 1) if ultima_seccio else 0
        
        # Crear secció
        nova_seccio = BiografiaSeccion(
            usuari_id=current_user.id,
            titol=titol,
            contingut=contingut,
            ordre=nou_ordre,
            visible=visible,
            any_inici=int(any_inici) if any_inici else None,
            any_final=int(any_final) if any_final else None

        )
        
        db.session.add(nova_seccio)
        db.session.commit()
        
        flash(f'Secció "{titol}" creada correctament', 'success')
        return redirect(url_for('biografia_seccions.llistar'))
    
    return render_template('pagina_personal/biografia_seccio_form.html', seccio=None)


# ============================================
# EDITAR SECCIÓ
# ============================================

@biografia_seccions_bp.route('/<int:seccio_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_seccio(seccio_id):
    """
    Edita una secció existent.
    Estil Wikipedia: formulari amb editor TinyMCE.
    """
    seccio = BiografiaSeccion.query.get_or_404(seccio_id)
    
    # Verificar que és del usuari actual
    if seccio.usuari_id != current_user.id:
        flash('No tens permís per editar aquesta secció', 'error')
        return redirect(url_for('biografia_seccions.llistar'))
    
    if request.method == 'POST':
        seccio.titol = request.form.get('titol', '').strip()
        seccio.contingut = request.form.get('contingut', '').strip()
        seccio.visible = request.form.get('visible') == 'on'
        any_inici = request.form.get('any_inici', '').strip()
        any_final = request.form.get('any_final', '').strip()
        seccio.any_inici = int(any_inici) if any_inici else None
        seccio.any_final = int(any_final) if any_final else None
        seccio.data_modificacio = ara_utc()
        
        if not seccio.titol:
            flash('El títol és obligatori', 'error')
            return render_template('pagina_personal/biografia_seccio_form.html', seccio=seccio)
        
        db.session.commit()
        flash(f'Secció "{seccio.titol}" actualitzada correctament', 'success')
        return redirect(url_for('biografia_seccions.llistar'))
    
    return render_template('pagina_personal/biografia_seccio_form.html', seccio=seccio)


# ============================================
# ELIMINAR SECCIÓ
# ============================================

@biografia_seccions_bp.route('/<int:seccio_id>/eliminar', methods=['POST'])
@login_required
def eliminar_seccio(seccio_id):
    """
    Elimina una secció de biografia.
    """
    seccio = BiografiaSeccion.query.get_or_404(seccio_id)
    
    # Verificar que és del usuari actual
    if seccio.usuari_id != current_user.id:
        return jsonify({'success': False, 'error': 'No autoritzat'}), 403
    
    titol = seccio.titol
    db.session.delete(seccio)
    db.session.commit()
    
    # Reordenar les seccions restants
    seccions_restants = BiografiaSeccion.query.filter_by(
        usuari_id=current_user.id
    ).order_by(BiografiaSeccion.ordre.asc()).all()
    
    for i, s in enumerate(seccions_restants):
        s.ordre = i
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({'success': True, 'message': f'Secció "{titol}" eliminada'})
    
    flash(f'Secció "{titol}" eliminada correctament', 'success')
    return redirect(url_for('biografia_seccions.llistar'))


# ============================================
# REORDENAR SECCIONS
# ============================================

@biografia_seccions_bp.route('/reordenar', methods=['POST'])
@login_required
def reordenar_seccions():
    """
    Canvia l'ordre de les seccions.
    Espera un array d'IDs en el nou ordre: [3, 1, 2, 4]
    """
    try:
        nou_ordre = request.json.get('ordre', [])
        
        for i, seccio_id in enumerate(nou_ordre):
            seccio = BiografiaSeccion.query.get(seccio_id)
            if seccio and seccio.usuari_id == current_user.id:
                seccio.ordre = i
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Ordre actualitzat'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ============================================
# CANVIAR VISIBILITAT
# ============================================

@biografia_seccions_bp.route('/<int:seccio_id>/toggle-visibilitat', methods=['POST'])
@login_required
def toggle_visibilitat(seccio_id):
    """
    Canvia la visibilitat d'una secció (pública/privada).
    """
    seccio = BiografiaSeccion.query.get_or_404(seccio_id)
    
    if seccio.usuari_id != current_user.id:
        return jsonify({'success': False, 'error': 'No autoritzat'}), 403
    
    seccio.visible = not seccio.visible
    db.session.commit()
    
    estat = 'pública' if seccio.visible else 'privada'
    
    return jsonify({
        'success': True,
        'visible': seccio.visible,
        'message': f'Secció ara és {estat}'
    })


# ============================================
# MOURE SECCIÓ (AMUNT/AVALL)
# ============================================

@biografia_seccions_bp.route('/<int:seccio_id>/moure/<direccio>', methods=['POST'])
@login_required
def moure_seccio(seccio_id, direccio):
    """
    Mou una secció amunt o avall.
    """
    if direccio not in ['amunt', 'avall']:
        return jsonify({'success': False, 'error': 'Direcció no vàlida'}), 400
    
    seccio = BiografiaSeccion.query.get_or_404(seccio_id)
    
    if seccio.usuari_id != current_user.id:
        return jsonify({'success': False, 'error': 'No autoritzat'}), 403
    
    # Obtenir totes les seccions ordenades
    seccions = BiografiaSeccion.query.filter_by(
        usuari_id=current_user.id
    ).order_by(BiografiaSeccion.ordre.asc()).all()
    
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