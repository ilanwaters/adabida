from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, EspaiFamiliar, MembreFamilia, Matrimoni, Entrada, EntradaFamilia, DocumentMembreFamilia
from sqlalchemy import func
from utils.paisos import normalitza_pais
import os
from datetime import datetime

administrar_bp = Blueprint('administrar', __name__, url_prefix='/familia/<int:familia_id>/administrar')


def es_administrador_familia(familia_id):
    """Comprova si l'usuari actual és administrador de la família"""
    membre = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia_id,
        rol='administrador'
    ).first()
    return membre is not None


@administrar_bp.route('/')
@login_required
def index(familia_id):
    """Pàgina principal d'administració de l'espai familiar"""
    familia = EspaiFamiliar.query.get_or_404(familia_id)
    
    # Verificar permisos
    if not es_administrador_familia(familia_id):
        flash('No tens permisos per administrar aquest espai', 'error')
        return redirect(url_for('familia.veure', familia_id=familia_id))
    
    # Calcular estadístiques
    estadistiques = {
        'total_relacions_parent': calcular_relacions_parent(familia_id),
        'total_matrimonis': Matrimoni.query.filter_by(espai_familiar_id=familia_id).count(),
        'membres_sense_parents': calcular_membres_sense_parents(familia_id),
        'generacions': calcular_generacions(familia_id),
        'total_records': calcular_total_records(familia_id),
        'total_documents': calcular_total_documents(familia_id),
        'espai_utilitzat': calcular_espai_utilitzat(familia_id)
    }
    
    # Detectar problemes en relacions
    problemes_relacions = detectar_problemes_relacions(familia_id)
    
    # Obtenir últims 5 records
    records_recents = db.session.query(Entrada).join(
        EntradaFamilia,
        Entrada.id == EntradaFamilia.entrada_id
    ).filter(
        EntradaFamilia.espai_familiar_id == familia_id
    ).order_by(
        Entrada.data_creacio.desc()
    ).limit(5).all()
    
    return render_template('familia/administrar_espai.html',
                     familia=familia,
                     estadistiques=estadistiques,
                     problemes_relacions=problemes_relacions,
                     records_recents=records_recents)
                       


@administrar_bp.route('/membre/<int:membre_id>/canviar-rol', methods=['POST'])
@login_required
def canviar_rol_membre(familia_id, membre_id):
    """Canviar el rol d'un membre (administrador ↔ membre)"""
    if not es_administrador_familia(familia_id):
        return jsonify({'success': False, 'message': 'No tens permisos'}), 403
    
    try:
        data = request.get_json()
        nou_rol = data.get('rol')
        
        if nou_rol not in ['administrador', 'membre']:
            return jsonify({'success': False, 'message': 'Rol no vàlid'}), 400
        
        membre = MembreFamilia.query.filter_by(
            id=membre_id,
            espai_familiar_id=familia_id
        ).first_or_404()
        
        # Comprovar que no s'està revocant l'últim administrador
        if membre.rol == 'administrador' and nou_rol == 'membre':
            total_admins = MembreFamilia.query.filter_by(
                espai_familiar_id=familia_id,
                rol='administrador'
            ).count()
            
            if total_admins <= 1:
                return jsonify({
                    'success': False, 
                    'message': 'No pots revocar l\'últim administrador'
                }), 400
        
        membre.rol = nou_rol
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Rol canviat a {nou_rol}'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error canviant rol: {e}")
        return jsonify({'success': False, 'message': 'Error al canviar el rol'}), 500


@administrar_bp.route('/membre/<int:membre_id>/eliminar', methods=['POST'])
@login_required
def eliminar_membre(familia_id, membre_id):
    """Eliminar un membre de l'espai familiar"""
    if not es_administrador_familia(familia_id):
        return jsonify({'success': False, 'message': 'No tens permisos'}), 403
    
    try:
        membre = MembreFamilia.query.filter_by(
            id=membre_id,
            espai_familiar_id=familia_id
        ).first_or_404()
        
        # No permetre eliminar-se a un mateix si és l'últim admin
        if membre.usuari_id == current_user.id:
            total_admins = MembreFamilia.query.filter_by(
                espai_familiar_id=familia_id,
                rol='administrador'
            ).count()
            
            if total_admins <= 1:
                return jsonify({
                    'success': False,
                    'message': 'No pots eliminar-te si ets l\'últim administrador'
                }), 400
        
        # Eliminar relacions associades
        # TODO: Decidir si eliminar també les relacions o deixar òrfens
        
        db.session.delete(membre)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Membre eliminat correctament'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error eliminant membre: {e}")
        return jsonify({'success': False, 'message': 'Error al eliminar el membre'}), 500


@administrar_bp.route('/ubicacio/<int:ubicacio_id>/eliminar', methods=['POST'])
@login_required
def eliminar_ubicacio(familia_id, ubicacio_id):
    """Eliminar una ubicació"""
    if not es_administrador_familia(familia_id):
        return jsonify({'success': False, 'message': 'No tens permisos'}), 403
    
    try:
        from models import UbicacioFamilia
        
        ubicacio = UbicacioFamilia.query.filter_by(
            id=ubicacio_id,
            espai_familiar_id=familia_id
        ).first_or_404()
        
        db.session.delete(ubicacio)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Ubicació eliminada'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error eliminant ubicació: {e}")
        return jsonify({'success': False, 'message': 'Error al eliminar'}), 500


@administrar_bp.route('/recalcular-ubicacions', methods=['POST'])
@login_required
def recalcular_ubicacions(familia_id):
    """Recalcular ubicacions actuals basant-se en els membres"""
    if not es_administrador_familia(familia_id):
        return jsonify({'success': False, 'message': 'No tens permisos'}), 403
    
    try:
        from models import UbicacioFamilia
        
        familia = EspaiFamiliar.query.get_or_404(familia_id)
        
        # Eliminar ubicacions provisionals antigues
        UbicacioFamilia.query.filter_by(
            espai_familiar_id=familia_id,
            tipus='actual',
            es_provisional=True
        ).delete()
        
        # Obtenir ubicacions úniques dels membres
        ubicacions_membres = db.session.query(
            MembreFamilia.municipi_actual,
            MembreFamilia.regio_actual,
            MembreFamilia.pais_actual
        ).filter(
            MembreFamilia.espai_familiar_id == familia_id,
            MembreFamilia.pais_actual.isnot(None)
        ).distinct().all()
        
        # Crear noves ubicacions provisionals
        for ubicacio in ubicacions_membres:
            nova_ubicacio = UbicacioFamilia(
                espai_familiar_id=familia_id,
                tipus='actual',
                municipi=ubicacio.municipi_actual,
                regio=ubicacio.regio_actual,
                pais=ubicacio.pais_actual,
                es_provisional=True
            )
            db.session.add(nova_ubicacio)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Ubicacions recalculades: {len(ubicacions_membres)} ubicacions trobades'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error recalculant ubicacions: {e}")
        return jsonify({'success': False, 'message': 'Error al recalcular'}), 500


@administrar_bp.route('/configuracio', methods=['POST'])
@login_required
def desar_configuracio(familia_id):
    """Desar la configuració avançada de l'espai"""
    if not es_administrador_familia(familia_id):
        return jsonify({'success': False, 'message': 'No tens permisos'}), 403
    
    try:
        data = request.get_json()
        familia = EspaiFamiliar.query.get_or_404(familia_id)
        
        # Actualitzar configuració
        if 'visible_globalment' in data:
            familia.visible_globalment = data['visible_globalment']
        
        # TODO: Afegir més camps de configuració segons necessitat
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Configuració desada correctament'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error desant configuració: {e}")
        return jsonify({'success': False, 'message': 'Error al desar'}), 500


@administrar_bp.route('/exportar-pdf')
@login_required
def exportar_pdf(familia_id):
    """Exportar l'espai familiar a PDF"""
    if not es_administrador_familia(familia_id):
        flash('No tens permisos', 'error')
        return redirect(url_for('familia.veure', familia_id=familia_id))
    
    # TODO: Implementar generació de PDF
    flash('Funció en desenvolupament', 'info')
    return redirect(url_for('administrar.index', familia_id=familia_id))


@administrar_bp.route('/backup')
@login_required
def fer_backup(familia_id):
    """Crear un backup complet de l'espai familiar"""
    if not es_administrador_familia(familia_id):
        flash('No tens permisos', 'error')
        return redirect(url_for('familia.veure', familia_id=familia_id))
    
    # TODO: Implementar backup en ZIP
    flash('Funció en desenvolupament', 'info')
    return redirect(url_for('administrar.index', familia_id=familia_id))


@administrar_bp.route('/arxivar', methods=['POST'])
@login_required
def arxivar_espai(familia_id):
    """Arxivar l'espai familiar (només lectura)"""
    if not es_administrador_familia(familia_id):
        return jsonify({'success': False, 'message': 'No tens permisos'}), 403
    
    try:
        familia = EspaiFamiliar.query.get_or_404(familia_id)
        # TODO: Afegir camp 'arxivat' al model
        # familia.arxivat = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Espai arxivat correctament'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error al arxivar'}), 500


@administrar_bp.route('/eliminar', methods=['POST'])
@login_required
def eliminar_espai(familia_id):
    """Eliminar permanentment l'espai familiar"""
    if not es_administrador_familia(familia_id):
        return jsonify({'success': False, 'message': 'No tens permisos'}), 403
    
    try:
        familia = EspaiFamiliar.query.get_or_404(familia_id)
        
        # Eliminar tot el contingut associat
        # TODO: Implementar eliminació en cascada de:
        # - Membres
        # - Relacions
        # - Matrimonis
        # - Documents
        # - Entrades compartides
        
        db.session.delete(familia)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Espai familiar eliminat permanentment'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error eliminant espai: {e}")
        return jsonify({'success': False, 'message': 'Error al eliminar'}), 500


# ========================================
# FUNCIONS AUXILIARS
# ========================================

def calcular_relacions_parent(familia_id):
    """Compte el total de relacions pare/mare"""
    total = db.session.query(MembreFamilia).filter(
        MembreFamilia.espai_familiar_id == familia_id,
        db.or_(
            MembreFamilia.pare_id.isnot(None),
            MembreFamilia.mare_id.isnot(None)
        )
    ).count()
    return total


def calcular_membres_sense_parents(familia_id):
    """Compte membres sense pare ni mare definits"""
    total = db.session.query(MembreFamilia).filter(
        MembreFamilia.espai_familiar_id == familia_id,
        MembreFamilia.pare_id.is_(None),
        MembreFamilia.mare_id.is_(None)
    ).count()
    return total


def calcular_generacions(familia_id):
    """Calcula el nombre de generacions (aproximat)"""
    # TODO: Implementar algorisme BFS per comptar nivells reals
    # Per ara retornem un valor estimat
    return 3


def calcular_total_records(familia_id):
    """Compte records compartits amb la família"""
    total = EntradaFamilia.query.filter_by(
        espai_familiar_id=familia_id
    ).count()
    return total


def calcular_total_documents(familia_id):
    """Compte documents totals dels membres"""
    total = db.session.query(DocumentMembreFamilia).join(
        MembreFamilia,
        DocumentMembreFamilia.membre_familia_id == MembreFamilia.id
    ).filter(
        MembreFamilia.espai_familiar_id == familia_id
    ).count()
    return total


def calcular_espai_utilitzat(familia_id):
    """Calcula l'espai en MB utilitzat (aproximat)"""
    # TODO: Sumar mida real dels fitxers
    # Per ara retornem valor estimat
    return round(12.5, 2)


def detectar_problemes_relacions(familia_id):
    """Detecta inconsistències en les relacions familiars"""
    problemes = []
    
    # Membres amb només pare o només mare
    membres_pare_sol = MembreFamilia.query.filter(
        MembreFamilia.espai_familiar_id == familia_id,
        MembreFamilia.pare_id.isnot(None),
        MembreFamilia.mare_id.is_(None)
    ).count()
    
    membres_mare_sol = MembreFamilia.query.filter(
        MembreFamilia.espai_familiar_id == familia_id,
        MembreFamilia.pare_id.is_(None),
        MembreFamilia.mare_id.isnot(None)
    ).count()
    
    if membres_pare_sol > 0:
        problemes.append(f"{membres_pare_sol} membre(s) amb només pare definit")
    
    if membres_mare_sol > 0:
        problemes.append(f"{membres_mare_sol} membre(s) amb només mare definida")
    
    # TODO: Afegir més validacions:
    # - Dates incoherents (fill nascut abans dels pares)
    # - Relacions circulars
    # - Matrimonis sense dates
    
    return problemes

@administrar_bp.route('/toggle-visibilitat-publica', methods=['POST'])
@login_required
def toggle_visibilitat_publica(familia_id):
    """Alternar la visibilitat pública d'una família al cercador/repositori"""
    if not es_administrador_familia(familia_id):
        return jsonify({'success': False, 'error': 'No tens permisos'}), 403

    familia = EspaiFamiliar.query.get_or_404(familia_id)
    familia.visible_publicament = not familia.visible_publicament
    db.session.commit()

    return jsonify({'success': True, 'visible_publicament': familia.visible_publicament})

@administrar_bp.route('/portada', methods=['POST'])
@login_required
def canviar_portada_familia(familia_id):
    if not es_administrador_familia(familia_id):
        return jsonify(success=False, error="No autoritzat"), 403

    familia = EspaiFamiliar.query.get_or_404(familia_id)

    imatge = request.files.get("imatge")
    if not imatge or not imatge.filename:
        return jsonify(success=False, error="No s'ha rebut cap imatge"), 400

    extensio = imatge.filename.rsplit('.', 1)[-1].lower()
    if extensio not in ('jpg', 'jpeg', 'png', 'webp'):
        return jsonify(success=False, error="Format d'imatge no vàlid"), 400

    any_str = str(familia.data_creacio.year)
    mes_str = str(familia.data_creacio.month).zfill(2)
    pais = normalitza_pais(current_user.pais_residencia)
    carpeta_final = os.path.join("umberto", "usuaris", pais, any_str, mes_str, current_user.nom_login, "families", str(familia.id))
    os.makedirs(carpeta_final, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    nom_fitxer = f"portada_{current_user.nom_login}_{timestamp}.{extensio}"
    ruta_final = os.path.join(carpeta_final, nom_fitxer)
    imatge.save(ruta_final)

    familia.imatge_card_home = f"/umberto/{current_user.nom_login}/{familia.id}/{nom_fitxer}"
    db.session.commit()

    return jsonify(success=True, nom_fitxer=nom_fitxer)