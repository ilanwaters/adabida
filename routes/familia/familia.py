from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from models import db, Usuari, PerfilBiografic, Contacte, Entrada, EntradaFamilia
from models.families import Matrimoni, EspaiFamiliar, MembreFamilia
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os


familia_bp = Blueprint('familia', __name__, url_prefix='/familia')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER_HERALDICA = 'static/heraldica'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@familia_bp.route('/')
@login_required
def hub():
    """Pàgina principal de gestió familiar"""
    return render_template('familia/familia.html')

@familia_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear un nou espai familiar amb múltiples ubicacions"""
    
    if request.method == 'GET':
        return render_template('familia/crear_espai_familiar.html')
    
    # POST - processar formulari
    try:
        # Recollir dades bàsiques
        nom = request.form.get('nom', '').strip()
        motiu = request.form.get('motiu', '').strip() or None
        descripcio = request.form.get('descripcio', '').strip() or None
        periode_referencia = request.form.get('periode_referencia', '').strip() or None
        
        # Validacions bàsiques
        if not nom:
            flash('El nom de la família és obligatori', 'error')
            return redirect(url_for('familia.crear'))
        
        # Recollir ubicacions d'origen (arrays)
        paisos_origen = request.form.getlist('pais_origen[]')
        regions_origen = request.form.getlist('regio_origen[]')
        municipis_origen = request.form.getlist('municipi_origen[]')
        
        # Validar que hi ha almenys una ubicació d'origen completa
        ubicacions_origen = []
        for i in range(len(paisos_origen)):
            if paisos_origen[i] and regions_origen[i] and municipis_origen[i]:
                ubicacions_origen.append({
                    'pais': obtenir_nom_pais(paisos_origen[i]),
                    'regio': obtenir_nom_regio(regions_origen[i]),
                    'municipi': obtenir_nom_municipi(municipis_origen[i]),
                    'ordre': i + 1
                })
        if not ubicacions_origen:
            flash('Cal indicar almenys una ubicació d\'origen', 'error')
            return redirect(url_for('familia.crear'))
        
        # Recollir ubicacions actuals (opcionals)
        paisos_actual = request.form.getlist('pais_actual[]')
        regions_actual = request.form.getlist('regio_actual[]')
        municipis_actual = request.form.getlist('municipi_actual[]')
        
        ubicacions_actuals = []
        if paisos_actual and regions_actual and municipis_actual:
            for i in range(min(len(paisos_actual), len(regions_actual), len(municipis_actual))):
                if municipis_actual[i]:
                    ubicacions_actuals.append({
                        'pais': obtenir_nom_pais(paisos_actual[i]) if paisos_actual[i] else '',
                        'regio': obtenir_nom_regio(regions_actual[i]) if regions_actual[i] else '',
                        'municipi': obtenir_nom_municipi(municipis_actual[i]),
                        'ordre': i + 1
                    })


        
        
        # Gestionar heràldica (fitxer)
        heraldica_fitxer = None
        if 'heraldica' in request.files:
            file = request.files['heraldica']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower()
                
                os.makedirs(UPLOAD_FOLDER_HERALDICA, exist_ok=True)
                
                temp_filename = f"temp_{current_user.id}_{filename}"
                temp_path = os.path.join(UPLOAD_FOLDER_HERALDICA, temp_filename)
                file.save(temp_path)
                
                heraldica_fitxer = temp_filename
        
        # Generar URL única (slug)
        import re
        slug_base = nom.lower().strip()
        # Si hi ha ubicació d'origen, afegir primer municipi
        if ubicacions_origen:
            primer_municipi = ubicacions_origen[0]['municipi'].lower().strip()
            slug_base = f"{slug_base}-{primer_municipi}"
        
        # Netejar: només lletres, números i guions
        slug_base = re.sub(r'[^a-z0-9-]', '-', slug_base)
        slug_base = re.sub(r'-+', '-', slug_base)  # Múltiples guions → un sol
        slug_base = slug_base.strip('-')  # Treure guions dels extrems
        
        # Comprovar si ja existeix i afegir número si cal
        slug_final = slug_base
        contador = 1
        while EspaiFamiliar.query.filter_by(url=slug_final).first():
            slug_final = f"{slug_base}-{contador}"
            contador += 1
        
        # Crear espai familiar
        espai = EspaiFamiliar(
            nom=nom,
            url=slug_final,
            motiu=motiu,
            descripcio=descripcio,
            periode_referencia=periode_referencia,
            creat_per_id=current_user.id
        )
        
        db.session.add(espai)
        db.session.flush()  # Per obtenir l'ID
        
        # Renombrar heràldica amb ID real
        if heraldica_fitxer:
            temp_path = os.path.join(UPLOAD_FOLDER_HERALDICA, heraldica_fitxer)
            ext = heraldica_fitxer.rsplit('.', 1)[1].lower()
            final_filename = f"familia_{espai.id}_escut.{ext}"
            final_path = os.path.join(UPLOAD_FOLDER_HERALDICA, final_filename)
            
            if os.path.exists(temp_path):
                os.rename(temp_path, final_path)
                espai.heraldica_fitxer = final_filename
        
        # Afegir ubicacions d'origen
        from models import UbicacioOrigenFamilia
        for ub in ubicacions_origen:
            ubicacio = UbicacioOrigenFamilia(
                espai_familiar_id=espai.id,
                pais=ub['pais'],
                regio=ub['regio'],
                municipi=ub['municipi'],
                ordre=ub['ordre']
            )
            db.session.add(ubicacio)
        
        # Afegir ubicacions actuals provisionals
        from models import UbicacioActualFamilia
        for ub in ubicacions_actuals:
            ubicacio = UbicacioActualFamilia(
                espai_familiar_id=espai.id,
                pais=ub['pais'],
                regio=ub['regio'],
                municipi=ub['municipi'],
                ordre=ub['ordre'],
                es_provisional=True
            )
            db.session.add(ubicacio)
        
        # Afegir creador com a administrador
        membre_admin = MembreFamilia(
            usuari_id=current_user.id,
            espai_familiar_id=espai.id,
            rol='administrador',
            pais_actual=current_user.pais_residencia,
            regio_actual=current_user.regio_naixement,
            municipi_actual=current_user.municipi_naixement
        )
        
        db.session.add(membre_admin)
        db.session.commit()
        
        flash(f'Espai familiar "{nom}" creat correctament!', 'success')
        return redirect(url_for('familia.veure', url=espai.url))
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creant espai familiar: {e}")
        import traceback
        traceback.print_exc()
        flash('Error creant l\'espai familiar. Torna-ho a provar.', 'error')
        return redirect(url_for('familia.crear'))


@familia_bp.route('/<url>/<seccio>')
@login_required
def seccio(url, seccio):
    """Gestiona les diferents seccions d'un espai familiar"""
    
    # Buscar espai familiar
    familia = EspaiFamiliar.query.filter_by(url=url).first_or_404()
    
    # Verificar si l'usuari és membre
    es_membre = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id
    ).first()
    
    if not es_membre:
        flash('No tens accés a aquest espai familiar', 'error')
        return redirect(url_for('familia.les_meves'))
    
    es_admin = (es_membre.rol == 'administrador')
    
    # Segons la secció, carregar dades diferents
    if seccio == 'qui-som':
        return  gestionar_qui_som(familia, es_admin)
    elif seccio == 'membres':
        return gestionar_seccio_membres(familia, es_admin)
    elif seccio == 'arbre':
        return gestionar_seccio_arbre(familia, es_admin)
    elif seccio == 'records':
        return gestionar_seccio_records(familia, es_admin)
    else:
        abort(404)

def gestionar_seccio_home(familia, es_admin):
    """Secció HOME - Informació general i estadístiques"""
    
    # Calcular estadístiques
    membres_count = len(familia.membres)
    
    # Entrades compartides
    records_count = db.session.query(Entrada).join(
        EntradaFamilia, EntradaFamilia.entrada_id == Entrada.id
    ).filter(
        EntradaFamilia.espai_familiar_id == familia.id
    ).count()
    
    # Records aquest mes
    primer_dia_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    records_mes_actual = db.session.query(Entrada).join(
        EntradaFamilia, EntradaFamilia.entrada_id == Entrada.id
    ).filter(
        EntradaFamilia.espai_familiar_id == familia.id,
        Entrada.data_creacio >= primer_dia_mes
    ).count()
    
    # Dies activa (des de la creació)
    dies_activa = (datetime.now() - familia.data_creacio).days
    
    estadistiques = {
        'membres_count': membres_count,
        'records_count': records_count,
        'records_mes_actual': records_mes_actual,
        'dies_activa': dies_activa
    }
    
    # Activitat recent
    activitat_recent = []
    
    # Últims records compartits
    ultims_records = db.session.query(Entrada).join(
        EntradaFamilia, EntradaFamilia.entrada_id == Entrada.id
    ).filter(
        EntradaFamilia.espai_familiar_id == familia.id
    ).order_by(Entrada.data_creacio.desc()).limit(5).all()
    
    for entrada in ultims_records:
        activitat_recent.append({
            'tipus': 'record',
            'descripcio': f'{entrada.usuari.nom} va compartir "{entrada.titol}"',
            'data': entrada.data_creacio
        })
    
    # Últims membres
    ultims_membres = MembreFamilia.query.filter_by(
        espai_familiar_id=familia.id
    ).order_by(MembreFamilia.data_adhesio.desc()).limit(3).all()
    
    for membre in ultims_membres:
        nom_membre = membre.nom or (membre.usuari.nom if membre.usuari else "Sense nom")
        activitat_recent.append({
            'tipus': 'membre',
            'descripcio': f'{nom_membre} es va afegir a la família',
            'data': membre.data_adhesio
        })
    
    # Ordenar per data
    activitat_recent.sort(key=lambda x: x['data'], reverse=True)
    activitat_recent = activitat_recent[:10]  # Últimes 10
    
    return render_template('familia/familia_home.html',
                         familia=familia,
                         es_admin=es_admin,
                         estadistiques=estadistiques,
                         activitat_recent=activitat_recent)
def gestionar_seccio_membres(familia, es_admin):
    """Secció MEMBRES - Llistat de membres"""
    
    # Carregar tots els membres de la família
    membres = MembreFamilia.query.filter_by(
        espai_familiar_id=familia.id
    ).order_by(MembreFamilia.nom, MembreFamilia.primer_cognom).all()
    
    # Filtrar administradors
    membres_admins = [m for m in membres if m.rol == 'administrador']
    
    # Calcular generacions (opcional, pot ser None)
    generacions = len(set(m.data_naixement.year // 30 for m in membres if m.data_naixement)) if membres else None
    
    return render_template('familia/familia_membres.html',
                         familia=familia,
                         membres=membres,
                         membres_admins=membres_admins,
                         generacions=generacions,
                         es_admin=es_admin)

def gestionar_seccio_arbre(familia, es_admin):
    """Secció ARBRE - Arbre genealògic interactiu"""
    return render_template('familia/seccio_arbre.html',
                         familia=familia,
                         es_admin=es_admin)

def gestionar_seccio_records(familia, es_admin):
    """Secció RECORDS - Entrades compartides"""
    # TODO: Implementar
    return render_template('familia/seccio_records.html',
                         familia=familia,
                         es_admin=es_admin)

# Nova funció per afegir a familia.py
# Aquesta substitueix gestionar_seccio_home

def gestionar_qui_som(familia, es_admin):
    """Secció QUI SOM - Informació completa, cronologia i evolució unificats"""
    
    # ========== ESTADÍSTIQUES (del home) ==========
    membres_count = len(familia.membres)
    
    # Records compartits
    records_count = db.session.query(Entrada).join(
        EntradaFamilia, EntradaFamilia.entrada_id == Entrada.id
    ).filter(
        EntradaFamilia.espai_familiar_id == familia.id
    ).count()
    
    # Records aquest mes
    primer_dia_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    records_mes_actual = db.session.query(Entrada).join(
        EntradaFamilia, EntradaFamilia.entrada_id == Entrada.id
    ).filter(
        EntradaFamilia.espai_familiar_id == familia.id,
        Entrada.data_creacio >= primer_dia_mes
    ).count()
    
    # Dies activa (des de la creació)
    dies_activa = (datetime.now() - familia.data_creacio).days
    
    estadistiques = {
        'membres_count': membres_count,
        'records_count': records_count,
        'records_mes_actual': records_mes_actual,
        'dies_activa': dies_activa
    }
    
    # ========== ACTIVITAT RECENT (del home) ==========
    activitat_recent = []
    
    # Últims records compartits
    ultims_records = db.session.query(Entrada).join(
        EntradaFamilia, EntradaFamilia.entrada_id == Entrada.id
    ).filter(
        EntradaFamilia.espai_familiar_id == familia.id
    ).order_by(Entrada.data_creacio.desc()).limit(5).all()
    
    for entrada in ultims_records:
        activitat_recent.append({
            'tipus': 'record',
            'descripcio': f'{entrada.usuari.nom} va compartir "{entrada.titol}"',
            'data': entrada.data_creacio
        })
    
    # Últims membres
    ultims_membres = MembreFamilia.query.filter_by(
        espai_familiar_id=familia.id
    ).order_by(MembreFamilia.data_adhesio.desc()).limit(3).all()
    
    for membre in ultims_membres:
        nom_membre = membre.nom or (membre.usuari.nom if membre.usuari else "Sense nom")
        activitat_recent.append({
            'tipus': 'membre',
            'descripcio': f'{nom_membre} es va afegir a la família',
            'data': membre.data_adhesio
        })
    
    # Ordenar per data
    activitat_recent.sort(key=lambda x: x['data'], reverse=True)
    activitat_recent = activitat_recent[:10]  # Últimes 10
    
    # ========== CRONOLOGIA I EVOLUCIÓ ==========
    
    # Primer membre
    primer_membre = MembreFamilia.query.filter_by(
        espai_familiar_id=familia.id
    ).order_by(MembreFamilia.data_adhesio.asc()).first()
    
    # Primer record
    primer_record = db.session.query(Entrada).join(
        EntradaFamilia, EntradaFamilia.entrada_id == Entrada.id
    ).filter(
        EntradaFamilia.espai_familiar_id == familia.id
    ).order_by(Entrada.data_creacio.asc()).first()
    
    # Fites importants
    fites_importants = []
    
    # Fita de membres
    if membres_count >= 10:
        fites_importants.append({
            'titol': f'10 membres assolits',
            'descripcio': 'La família va arribar als 10 membres',
            'data': datetime.now() - timedelta(days=30)  # Aproximació
        })
    
    # Evolució últims 6 mesos
    ultims_6_mesos = []
    for i in range(6):
        mes_actual = datetime.now() - timedelta(days=30*i)
        inici_mes = mes_actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        fi_mes = (inici_mes + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
        
        nous_membres = MembreFamilia.query.filter(
            MembreFamilia.espai_familiar_id == familia.id,
            MembreFamilia.data_adhesio >= inici_mes,
            MembreFamilia.data_adhesio <= fi_mes
        ).count()
        
        nous_records = db.session.query(Entrada).join(
            EntradaFamilia, EntradaFamilia.entrada_id == Entrada.id
        ).filter(
            EntradaFamilia.espai_familiar_id == familia.id,
            Entrada.data_creacio >= inici_mes,
            Entrada.data_creacio <= fi_mes
        ).count()
        
        ultims_6_mesos.append({
            'nom': mes_actual.strftime('%B'),
            'nous_membres': nous_membres,
            'nous_records': nous_records
        })
    
    ultims_6_mesos.reverse()  # Més antic primer
    
    # Màxims per normalitzar gràfics
    max_nous_membres = max([m['nous_membres'] for m in ultims_6_mesos]) or 1
    max_nous_records = max([m['nous_records'] for m in ultims_6_mesos]) or 1
    
    # ========== RENDERITZAR TEMPLATE UNIFICAT ==========
    return render_template('familia/familia_qui_som.html',
                         familia=familia,
                         es_admin=es_admin,
                         estadistiques=estadistiques,
                         activitat_recent=activitat_recent,
                         primer_membre=primer_membre,
                         primer_record=primer_record,
                         fites_importants=fites_importants,
                         ultims_6_mesos=ultims_6_mesos,
                         max_nous_membres=max_nous_membres,
                         max_nous_records=max_nous_records)
# ============================================
# RUTA ANTIGA (mantenir per compatibilitat temporal)
# ============================================
@familia_bp.route('/<url>')
@login_required
def veure(url):
    """Vista principal distribuïdora de la família amb cards"""
    familia = EspaiFamiliar.query.filter_by(url=url).first_or_404()
    
    # Verificar que l'usuari és membre
    es_membre = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id
    ).first()
    
    if not es_membre:
        flash('No tens accés a aquest espai familiar', 'error')
        return redirect(url_for('familia.les_meves'))
    
    es_admin = (es_membre.rol == 'administrador')
    
    return render_template('familia/familia_distribuidor.html', 
                         familia=familia,
                         es_admin=es_admin)

@familia_bp.route('/<url>/pujar-imatge-card', methods=['POST'])
@login_required
def pujar_imatge_card(url):
    """Pujar imatge personalitzada per un card"""
    try:
        familia = EspaiFamiliar.query.filter_by(url=url).first_or_404()
        
        # Verificar que és admin
        es_membre = MembreFamilia.query.filter_by(
            usuari_id=current_user.id,
            espai_familiar_id=familia.id
        ).first()
        
        if not es_membre or es_membre.rol != 'administrador':
            return jsonify({'success': False, 'error': 'No tens permisos'}), 403
        
        # Obtenir dades
        card_type = request.form.get('card_type')
        imatge = request.files.get('imatge')
        
        if not card_type or not imatge:
            return jsonify({'success': False, 'error': 'Falten dades'}), 400
        
        # Validar tipus card
        camps_permesos = ['home', 'arbre', 'membres', 'records', 'documents']
        if card_type not in camps_permesos:
            return jsonify({'success': False, 'error': 'Tipus de card invàlid'}), 400
        
        # Guardar imatge
        from werkzeug.utils import secure_filename
        filename = secure_filename(imatge.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
        
        # Nom final: familia_{id}_card_{tipus}.{ext}
        nom_final = f"familia_{familia.id}_card_{card_type}.{ext}"
        
        # Crear carpeta si no existeix
        carpeta = os.path.join('static', 'cards_familia')
        os.makedirs(carpeta, exist_ok=True)
        
        # Guardar fitxer
        ruta_completa = os.path.join(carpeta, nom_final)
        imatge.save(ruta_completa)
        
        # Actualitzar BD
        camp_bd = f'imatge_card_{card_type}'
        setattr(familia, camp_bd, nom_final)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Imatge guardada correctament'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error pujant imatge card: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500                        

@familia_bp.route('/les-meves')
@login_required
def les_meves():
    """Llista els espais familiars de l'usuari"""
    # Obtenir espais on sóc administrador
    families_admin = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        rol='administrador'
    ).all()
    
    # Obtenir espais on sóc membre (no admin)
    families_membre = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        rol='membre'
    ).all()
    
    return render_template('familia/les_meves_families.html', 
                         usuari=current_user,
                         families_admin=families_admin,
                         families_membre=families_membre)

def obtenir_nom_pais(pais_id):
    """Converteix ID de país a nom"""
    from models import Pais
    if not pais_id or pais_id == '':
        return ''
    try:
        pais_id_int = int(pais_id)
        pais = Pais.query.get(pais_id_int)
        return pais.nom if pais else pais_id
    except (ValueError, TypeError):
        # Si no és un número, assumir que ja és un nom (cas "Altre país")
        return pais_id

def obtenir_nom_regio(regio_id):
    """Converteix ID de regió a nom"""
    from models import Regio
    if not regio_id or regio_id == '':
        return ''
    try:
        regio_id_int = int(regio_id)
        regio = Regio.query.get(regio_id_int)
        return regio.nom if regio else regio_id
    except (ValueError, TypeError):
        return regio_id

def obtenir_nom_municipi(municipi_id):
    """Converteix ID de municipi a nom"""
    from models import Municipi
    if not municipi_id or municipi_id == '':
        return ''
    try:
        municipi_id_int = int(municipi_id)
        municipi = Municipi.query.get(municipi_id_int)
        return municipi.nom if municipi else municipi_id
    except (ValueError, TypeError):
        return municipi_id

@familia_bp.route('/<url>/arbre/dades')
@login_required
def arbre_dades(url):
    """API endpoint: retorna dades de l'arbre genealògic en format JSON"""
    familia = EspaiFamiliar.query.filter_by(url=url).first_or_404()
    
    # Verificar que l'usuari és membre
    es_membre = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id
    ).first()
    
    if not es_membre:
        return jsonify({'error': 'No tens accés a aquest espai familiar'}), 403
    
    # Obtenir tots els membres
    membres = MembreFamilia.query.filter_by(espai_familiar_id=familia.id).all()
    
    # Convertir a format JSON
    nodes = []
    for m in membres:
        nodes.append({
            'id': m.id,
            'nom': m.nom,
            'primer_cognom': m.primer_cognom,
            'segon_cognom': m.segon_cognom,
            'nom_complet': f"{m.nom} {m.primer_cognom}" + (f" {m.segon_cognom}" if m.segon_cognom else ""),
            'data_naixement': m.data_naixement.isoformat() if m.data_naixement else None,
            'data_defuncio': m.data_defuncio.isoformat() if m.data_defuncio else None,
            'genere': m.genere,
            'pare_id': m.pare_id,
            'mare_id': m.mare_id,
            'viu': m.data_defuncio is None
        })
    
    # Generar links (relacions pare-fill)
    links = []
    for m in membres:
        if m.pare_id:
            links.append({
                'source': m.pare_id,
                'target': m.id,
                'type': 'pare'
            })
        if m.mare_id:
            links.append({
                'source': m.mare_id,
                'target': m.id,
                'type': 'mare'
            })
    
    # Obtenir matrimonis
    matrimonis_data = []
    matrimonis = Matrimoni.query.filter_by(espai_familiar_id=familia.id).all()
    
    for mat in matrimonis:
        matrimonis_data.append({
            'id': mat.id,
            'membre_1_id': mat.membre_1_id,
            'membre_2_id': mat.membre_2_id,
            'data_casament': mat.data_casament.isoformat() if mat.data_casament else None,
            'estat': mat.estat
        })
    
    return jsonify({
        'nodes': nodes,
        'links': links,
        'matrimonis': matrimonis_data,
        'usuari_actual_id': es_membre.id
    })

# ============================================
# RUTES PÚBLIQUES (sense login requerit)
# ============================================

@familia_bp.route('/publica/<url>')
def publica(url):
    """Perfil públic de la família - vista principal amb 4 cards"""
    familia = EspaiFamiliar.query.filter_by(url=url).first_or_404()
    
    # TODO: Verificar si la família té perfil públic activat
    # if not familia.perfil_public_actiu:
    #     abort(404)
    
    return render_template('familia/familia_publica.html', familia=familia)
    
@familia_bp.route('/publica/<url>/<seccio>')
def seccio_publica(url, seccio):
    """Seccions públiques de la família"""
    familia = EspaiFamiliar.query.filter_by(url=url).first_or_404()
    
    # TODO: Verificar perfil públic
    # if not familia.perfil_public_actiu:
    #     abort(404)
    
    if seccio == 'historia':
        # Carregar seccions públiques
        from models import BiografiaFamiliaSeccion
        seccions_publiques = BiografiaFamiliaSeccion.query.filter_by(
            familia_id=familia.id,
            visible=True
        ).order_by(BiografiaFamiliaSeccion.ordre).all()
    
        return render_template('familia/publica_historia.html', 
                        familia=familia,
                        seccions_publiques=seccions_publiques)
    
    elif seccio == 'arbre':
        return render_template('familia/publica_arbre.html', familia=familia)
    
    elif seccio == 'membres':
        from datetime import datetime
    # De moment mostrem tots (després afegirem camp visible_public)
        membres_publics = MembreFamilia.query.filter_by(
            espai_familiar_id=familia.id
        ).order_by(MembreFamilia.nom, MembreFamilia.primer_cognom).all()

        return render_template('familia/publica_membres.html', 
                        familia=familia, 
                        membres=membres_publics,
                        now=datetime.now())
    
    elif seccio == 'documents':
        return render_template('familia/publica_documents.html', familia=familia)
    
    else:
        abort(404)

@familia_bp.route('/membre/pujar-foto', methods=['POST'])
@login_required
def pujar_foto_membre():
    """Puja foto per membre sense usuari"""
    from werkzeug.utils import secure_filename
    import os
    from flask import current_app
    
    try:
        membre_id = request.form.get('membre_id')
        if not membre_id:
            return jsonify({'success': False, 'error': 'No s\'ha especificat membre'}), 400
        
        membre = MembreFamilia.query.get_or_404(membre_id)
        
        # Verificar permisos (opcional, per ara comentat)
        # if not es_admin_familia(current_user.id, membre.espai_familiar_id):
        #     return jsonify({'success': False, 'error': 'No tens permisos'}), 403
        
        if 'foto' not in request.files:
            return jsonify({'success': False, 'error': 'No s\'ha rebut cap fitxer'}), 400
        
        foto = request.files['foto']
        if foto.filename == '':
            return jsonify({'success': False, 'error': 'Fitxer buit'}), 400
        
        # Crear directori si no existeix
        fotos_dir = os.path.join(current_app.root_path, 'static', 'fotos_membres')
        os.makedirs(fotos_dir, exist_ok=True)
        
        # Guardar foto
        filename = secure_filename(f'membre_{membre_id}_{foto.filename}')
        foto_path = os.path.join(fotos_dir, filename)
        foto.save(foto_path)
        
        # Actualitzar BD
        membre.foto = filename
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error pujant foto: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500