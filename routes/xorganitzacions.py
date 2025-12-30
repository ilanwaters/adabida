from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app, abort
from flask_login import login_required, current_user
from flask_babel import gettext as _
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_, or_  # ← Aquí va func, and_, or_
from models import db, Organitzacio, MembreOrganitzacio, Usuari, Entrada, SolicitudOrganitzacio, MissatgeOrganitzacio, EntradaOrganitzacio
import os
import uuid
from datetime import datetime, timedelta

organitzacions_bp = Blueprint('organitzacions', __name__, url_prefix='/organitzacions')
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

@organitzacions_bp.route('/test')
def test():
    print("=== RUTA TEST FUNCIONANT ===")
    return "RUTA TEST OK!"

@organitzacions_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    """Crear nova organització"""
    print(f"=== RUTA /CREAR - MÈTODE: {request.method} ===")
    print(f"CURRENT_USER: {current_user}")
    print(f"IS_AUTHENTICATED: {current_user.is_authenticated if hasattr(current_user, 'is_authenticated') else 'NO_ATTR'}")
    
    # Verificació manual de login
    if not current_user.is_authenticated:
        print("*** USUARI NO LOGUEJAT - REDIRIGINT ***")
        flash('Has d\'estar loguejat per crear una organització', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        print("*** PROCESSANT FORMULARI POST ***")
        print(f"DADES FORMULARI: {dict(request.form)}")
        
        # Obtenir dades del formulari
        nom = request.form.get('nom')
        tipus = request.form.get('tipus')
        descripcio = request.form.get('descripcio')
        pais = request.form.get('pais')
        regio = request.form.get('regio')
        municipi = request.form.get('municipi')
        codi_postal = request.form.get('codi_postal')
        url_publica = request.form.get('url_publica')
        email_extern = request.form.get('email_extern')
        telefon_contacte = request.form.get('telefon_contacte')
        adresa = request.form.get('adresa')
        
        print(f"NOM: {nom}, TIPUS: {tipus}, URL_PUBLICA: {url_publica}")
        
        # Validació bàsica
        if not nom or not tipus or not pais or not regio or not municipi or not url_publica:
            flash('Nom, tipus, país, regió, municipi i URL són obligatoris', 'error')
            return render_template('organitzacions/crear.html')
        
        try:
            print("*** CREANT ORGANITZACIÓ A LA BD... ***")
            
            # Generar slug únic basat en url_publica
            slug_base = url_publica.lower().strip()
            slug_base = ''.join(c for c in slug_base if c.isalnum() or c == '-')
            
            # Comprovar si el slug ja existeix
            contador = 1
            slug_final = slug_base
            while Organitzacio.query.filter_by(url_publica=slug_final).first():
                slug_final = f"{slug_base}-{contador}"
                contador += 1
            
            print(f"SLUG FINAL: {slug_final}")
            
            # Crear nova organització
            nova_org = Organitzacio(
                nom=nom,
                tipus=tipus,
                descripcio=descripcio if descripcio else None,
                pais=pais,
                regio=regio,
                municipi=municipi,
                codi_postal=codi_postal if codi_postal else None,
                url_publica=slug_final,
                email_adabida=f"{slug_final}@adabida.cat",
                email_extern=email_extern if email_extern else None,
                telefon_contacte=telefon_contacte if telefon_contacte else None,
                adresa=adresa if adresa else None,
                creat_per_id=current_user.id,
                data_creacio=datetime.utcnow()
            )
            
            print("AFEGINT ORGANITZACIÓ A LA SESSIÓ...")
            db.session.add(nova_org)
            db.session.flush()  # Per obtenir l'ID abans del commit
            print(f"ORGANITZACIÓ CREADA AMB ID: {nova_org.id}")
            
            # CLAU: Fer l'usuari actual administrador automàticament
            print("*** AFEGINT USUARI COM A ADMINISTRADOR ***")
            membre_admin = MembreOrganitzacio(
                usuari_id=current_user.id,
                organitzacio_id=nova_org.id,
                rol='admin',
                data_adhesio=datetime.utcnow()
            )
            
            db.session.add(membre_admin)
            
            print("FENT COMMIT FINAL...")
            db.session.commit()
            print("*** ÈXIT TOTAL! ORGANITZACIÓ I MEMBRE ADMIN CREATS ***")
            
            flash(f'Organització "{nom}" creada correctament! Ja pots gestionar-la.', 'success')
            
            # REDIRIGIR AL PANELL D'ADMINISTRACIÓ
            print(f"*** REDIRIGINT A ADMIN AMB ID: {nova_org.id} ***")
            return redirect(url_for('organitzacions.admin', id=nova_org.id))
            
        except Exception as e:
            print(f"*** ERROR CRÍTIC: {str(e)} ***")
            import traceback
            print(f"TRACEBACK: {traceback.format_exc()}")
            db.session.rollback()
            flash(f'Error en crear l\'organització: {str(e)}', 'error')
            return render_template('organitzacions/crear.html')
    
    # Si és GET, mostrar formulari
    print("*** MOSTRANT FORMULARI DE CREACIÓ ***")
    return render_template('organitzacions/crear.html')

@organitzacions_bp.route('/publica/<slug>')
def publica(slug):
    """Pàgina pública de l'organització"""
    print(f"=== ACCEDINT A PÀGINA PÚBLICA: {slug} ===")
    
    organitzacio = Organitzacio.query.filter_by(url_publica=slug).first_or_404()
    
    # Obtenir entrades públiques dels membres - CORREGIT
    entrades = db.session.query(Entrada)\
        .join(Usuari, Entrada.usuari_id == Usuari.id)\
        .join(MembreOrganitzacio, MembreOrganitzacio.usuari_id == Usuari.id)\
        .filter(
            MembreOrganitzacio.organitzacio_id == organitzacio.id,
            Entrada.es_publica == True
        ).order_by(Entrada.data_creacio.desc()).all()
    
    # Detectar si l'usuari actual és membre o admin
    es_membre = False
    es_admin = False
    
    if current_user.is_authenticated:
        membre = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id, 
            organitzacio_id=organitzacio.id
        ).first()
        
        if membre:
            es_membre = True
            es_admin = (membre.rol == 'admin')
    
    return render_template('organitzacions/organitzacions.html', 
                         organitzacio=organitzacio, 
                         entrades=entrades,
                         es_membre=es_membre,
                         es_admin=es_admin)
        
@organitzacions_bp.route('/toggle_entrada_publica/<int:entrada_id>', methods=['POST'])
@login_required
def toggle_entrada_publica(entrada_id):
    """Canviar estat públic d'una entrada"""
    try:
        entrada = Entrada.query.get_or_404(entrada_id)
        
        # Verificar permisos (admin o propietari de l'entrada)
        admin = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            rol='admin'
        ).first()
        
        if not admin and entrada.usuari_id != current_user.id:
            return jsonify({'success': False, 'error': 'No tens permisos'})
        
        entrada.publica = not entrada.publica
        db.session.commit()
        
        estat = 'pública' if entrada.publica else 'privada'
        return jsonify({'success': True, 'message': f'Entrada ara és {estat}'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@organitzacions_bp.route('/')
def llistat():
    """Llistat i buscador d'organitzacions"""
    print("=== ACCEDINT A LLISTAT ORGANITZACIONS ===")
    
    # Paràmetres de cerca
    nom = request.args.get('nom', '').strip()
    tipus = request.args.get('tipus', '')
    pais = request.args.get('pais', '').strip()
    regio = request.args.get('regio', '').strip()
    municipi = request.args.get('municipi', '').strip()

    cerca_activa = bool(nom or tipus or pais or regio or municipi)

    if not cerca_activa:
        # No mostrar res si no hi ha paràmetres de cerca
        organitzacions = []
        print("CAP CRITERI DE CERCA - LLISTA BUIDA")
    else:
        # Query base només si hi ha cerca
        query = Organitzacio.query
    
        # Aplicar filtres
        if nom:
            query = query.filter(Organitzacio.nom.ilike(f'%{nom}%'))
        if tipus:
            query = query.filter(Organitzacio.tipus == tipus)
        if pais:
            query = query.filter(Organitzacio.pais.ilike(f'%{pais}%'))
        if regio:
            query = query.filter(Organitzacio.regio.ilike(f'%{regio}%'))
        if municipi:
            query = query.filter(Organitzacio.municipi.ilike(f'%{municipi}%'))
    
        organitzacions = query.order_by(Organitzacio.data_creacio.desc()).all()
        print(f"CERCA ACTIVA - ORGANITZACIONS TROBADES: {len(organitzacions)}")

    # Afegir info de membres i estat de sol·licituds
    for org in organitzacions:
        org.nombre_membres = len(org.membres)
        
        # Inicialitzar estats
        org.ja_membre = False
        org.solicitud_pendent = False
        org.solicitud_rebutjada = False
        org.estat_boto = 'sol_licitar'  # Estat per defecte
        
        if current_user.is_authenticated:
            # Comprovar si ja és membre
            org.ja_membre = any(m.usuari_id == current_user.id for m in org.membres)
            
            if org.ja_membre:
                org.estat_boto = 'ja_membre'
            else:
                # Si no és membre, comprovar estat de sol·licituds
                solicitud = SolicitudOrganitzacio.query.filter_by(
                    usuari_id=current_user.id,
                    organitzacio_id=org.id
                ).order_by(SolicitudOrganitzacio.data_solicitud.desc()).first()
                
                if solicitud:
                    if solicitud.estat == 'pendent':
                        org.solicitud_pendent = True
                        org.estat_boto = 'pendent'
                    elif solicitud.estat == 'rebutjada':
                        org.solicitud_rebutjada = True
                        org.estat_boto = 'rebutjada'
                    elif solicitud.estat == 'acceptada':
                        # Cas estrany - hauria de ser membre ja, però per si de cas
                        org.estat_boto = 'acceptada'
                # Si no hi ha sol·licitud, estat per defecte 'sol_licitar'
        else:
            # Usuari no loguejat
            org.estat_boto = 'no_loguejat'
    
    cerca_activa = bool(nom or tipus or pais or regio or municipi)
    
    return render_template('organitzacions/llistat.html', 
                         organitzacions=organitzacions,
                         cerca_activa=cerca_activa)

@organitzacions_bp.route('/solicitar', methods=['POST'])
@login_required
def solicitar():
    """Crear sol·licitud d'adhesió"""
    try:
        data = request.get_json()
        org_id = data.get('organitzacio_id')
        missatge = data.get('missatge', '').strip()
        
        # Verificar que l'organització existeix
        organitzacio = Organitzacio.query.get_or_404(org_id)
        
        # Verificar que no sigui ja membre
        membre_existent = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=org_id
        ).first()
        
        if membre_existent:
            return jsonify({'success': False, 'error': 'Ja ets membre d\'aquesta organització'})
        
        # Verificar que no tingui ja una sol·licitud pendent
        solicitud_existent = SolicitudOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=org_id,
            estat='pendent'
        ).first()
        
        if solicitud_existent:
            return jsonify({'success': False, 'error': 'Ja tens una sol·licitud pendent'})
        
        # Crear nova sol·licitud
        nova_solicitud = SolicitudOrganitzacio(
            usuari_id=current_user.id,
            organitzacio_id=org_id,
            missatge=missatge if missatge else None
        )
        
        db.session.add(nova_solicitud)
        db.session.commit()
        
        print(f"NOVA SOL·LICITUD CREADA: {current_user.nom} -> {organitzacio.nom}")
        
        return jsonify({'success': True, 'message': 'Sol·licitud enviada correctament'})
        
    except Exception as e:
        db.session.rollback()
        print(f"ERROR CREANT SOL·LICITUD: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


@organitzacions_bp.route('/hub')
@login_required
def hub():
    """Hub central d'organitzacions"""
    return render_template('organitzacions.html')

@organitzacions_bp.route('/les-meves')
@login_required
def les_meves():
    """Les organitzacions on l'usuari és membre/admin"""
    
    # Obtenir organitzacions on l'usuari és admin
    organitzacions_admin = MembreOrganitzacio.query.filter_by(
        usuari_id=current_user.id,
        rol='admin'
    ).join(Organitzacio).order_by(Organitzacio.nom).all()
    
    # També pots obtenir les altres on és membre (no admin)
    organitzacions_membre = MembreOrganitzacio.query.filter_by(
        usuari_id=current_user.id
    ).filter(MembreOrganitzacio.rol != 'admin').join(Organitzacio).order_by(Organitzacio.nom).all()
    
    return render_template('organitzacions/les_meves.html', 
                         organitzacions_admin=organitzacions_admin,
                         organitzacions_membre=organitzacions_membre)


@organitzacions_bp.route('/<slug>/<seccio>')
def seccio(slug, seccio):
    """Gestiona les diferents seccions d'una organització"""
    
    # Buscar organització
    organitzacio = Organitzacio.query.filter_by(url_publica=slug).first_or_404()
    
    # Verificar si l'usuari és membre
    es_membre = False
    es_admin = False
    if current_user.is_authenticated:
        membre = MembreOrganitzacio.query.filter_by(
            usuari_id=current_user.id,
            organitzacio_id=organitzacio.id
        ).first()
        if membre:
            es_membre = True
            es_admin = membre.rol == 'admin'
    
    # Segons la secció, carregar dades diferents
    if seccio == 'qui-som':
        return gestionar_qui_som(organitzacio, es_membre, es_admin)
    elif seccio == 'historia':
        return gestionar_seccio_historia(organitzacio, es_membre, es_admin)
    elif seccio == 'entrades':
        return gestionar_seccio_entrades(organitzacio, es_membre, es_admin)
    elif seccio == 'membres':
        return gestionar_seccio_membres(organitzacio, es_membre, es_admin)
    elif seccio == 'imatges':
        return gestionar_seccio_imatges(organitzacio, es_membre, es_admin)
    else:
        abort(404)

def gestionar_seccio_home(organitzacio, es_membre, es_admin):
    """Secció HOME - Informació general"""
    
    # Calcular estadístiques
    membres_count = MembreOrganitzacio.query.filter_by(organitzacio_id=organitzacio.id).count()
    
    entrades_count = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True
    ).count()
    
    # Entrades aquest mes
    primer_dia_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    entrades_mes_actual = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True,
        Entrada.data_creacio >= primer_dia_mes
    ).count()
    # Dies activa (des de la creació)
    dies_activa = (datetime.now() - organitzacio.data_creacio).days
    
    estadistiques = {
        'membres_count': membres_count,
        'entrades_count': entrades_count,
        'entrades_mes_actual': entrades_mes_actual,
        'dies_activa': dies_activa
    }
    
    # Activitat recent (últimes 10 accions)
    activitat_recent = []
    
    # Últimes entrades compartides
    ultimes_entrades = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True
    ).order_by(Entrada.data_creacio.desc()).limit(5).all()
    
    for entrada in ultimes_entrades:
        activitat_recent.append({
            'tipus': 'entrada',
            'descripcio': f'{entrada.usuari.nom} va compartir "{entrada.titol}"',
            'data': entrada.data_creacio
        })
    
    # Últims membres
    ultims_membres = MembreOrganitzacio.query.filter_by(
        organitzacio_id=organitzacio.id
    ).order_by(MembreOrganitzacio.data_adhesio.desc()).limit(3).all()
    
    for membre in ultims_membres:
        activitat_recent.append({
            'tipus': 'membre',
            'descripcio': f'{membre.usuari.nom} es va unir a l\'organització',
            'data': membre.data_adhesio
        })
    
    # Ordenar per data
    activitat_recent.sort(key=lambda x: x['data'], reverse=True)
    activitat_recent = activitat_recent[:10]  # Últimes 10
    
    return render_template('organitzacions/seccio_home.html',
                         organitzacio=organitzacio,
                         es_membre=es_membre,
                         es_admin=es_admin,
                         estadistiques=estadistiques,
                         activitat_recent=activitat_recent)

def gestionar_seccio_historia(organitzacio, es_membre, es_admin):
    """Secció HISTÒRIA - Timeline i evolució"""
    
    # Primer membre
    primer_membre = MembreOrganitzacio.query.filter_by(
        organitzacio_id=organitzacio.id
    ).order_by(MembreOrganitzacio.data_adhesio.asc()).first()
    
    # Primera entrada
    primera_entrada = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True
    ).order_by(Entrada.data_creacio.asc()).first()
    
    # Fites importants (exemple: cada 10 membres, cada 50 entrades)
    fites_importants = []
    
    membres_count = MembreOrganitzacio.query.filter_by(organitzacio_id=organitzacio.id).count()
    entrades_count = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True
    ).count()
    
    # Fita de membres
    if membres_count >= 10:
        fites_importants.append({
            'titol': f'10 membres assolits',
            'descripcio': 'L\'organització va arribar als 10 membres',
            'data': datetime.now() - timedelta(days=30)  # Aproximació
        })
    
    # Evolució últims 6 mesos
    ultims_6_mesos = []
    for i in range(6):
        mes_actual = datetime.now() - timedelta(days=30*i)
        inici_mes = mes_actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        fi_mes = (inici_mes + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
        
        nous_membres = MembreOrganitzacio.query.filter(
            MembreOrganitzacio.organitzacio_id == organitzacio.id,
            MembreOrganitzacio.data_adhesio >= inici_mes,
            MembreOrganitzacio.data_adhesio <= fi_mes
        ).count()
        
        noves_entrades = db.session.query(Entrada).join(
            EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
        ).filter(
            EntradaOrganitzacio.organitzacio_id == organitzacio.id,
            Entrada.es_publica == True,
            Entrada.data_creacio >= inici_mes,
            Entrada.data_creacio <= fi_mes
        ).count()
        
        ultims_6_mesos.append({
            'nom': mes_actual.strftime('%B'),
            'nous_membres': nous_membres,
            'noves_entrades': noves_entrades
        })
    
    ultims_6_mesos.reverse()  # Més antic primer
    
    # Màxims per normalitzar gràfics
    max_nous_membres = max([m['nous_membres'] for m in ultims_6_mesos]) or 1
    max_noves_entrades = max([m['noves_entrades'] for m in ultims_6_mesos]) or 1
    
    return render_template('organitzacions/seccio_historia.html',
                         organitzacio=organitzacio,
                         es_membre=es_membre,
                         es_admin=es_admin,
                         primer_membre=primer_membre,
                         primera_entrada=primera_entrada,
                         fites_importants=fites_importants,
                         ultims_6_mesos=ultims_6_mesos,
                         max_nous_membres=max_nous_membres,
                         max_noves_entrades=max_noves_entrades)

def gestionar_seccio_entrades(organitzacio, es_membre, es_admin):
    """Secció ENTRADES - Llistat d'entrades compartides"""
    
    # Carregar entrades compartides amb aquesta organització
    entrades = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True
    ).order_by(Entrada.data_creacio.desc()).all()
    
    # Anys disponibles per filtrar
    anys_disponibles = db.session.query(
        func.extract('year', Entrada.data_creacio).label('any')
    ).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True
    ).distinct().order_by('any').all()
    
    anys_disponibles = [int(any[0]) for any in anys_disponibles]
    
    return render_template('organitzacions/seccio_entrades.html',
                         organitzacio=organitzacio,
                         entrades=entrades,
                         anys_disponibles=anys_disponibles,
                         es_membre=es_membre,
                         es_admin=es_admin)

def gestionar_seccio_membres(organitzacio, es_membre, es_admin):
    """Secció MEMBRES - Llistat de membres"""
    
    # Carregar membres de l'organització amb informació adicional
    membres_query = db.session.query(
        MembreOrganitzacio,
        func.count(Entrada.id).label('entrades_compartides')
    ).select_from(MembreOrganitzacio)\
     .filter(MembreOrganitzacio.organitzacio_id == organitzacio.id)\
     .join(Usuari, MembreOrganitzacio.usuari_id == Usuari.id)\
     .outerjoin(Entrada, Entrada.usuari_id == Usuari.id)\
     .outerjoin(EntradaOrganitzacio, and_(
         EntradaOrganitzacio.entrada_id == Entrada.id,
         EntradaOrganitzacio.organitzacio_id == organitzacio.id
     ))\
     .group_by(MembreOrganitzacio.id)\
     .all()
    
    # Processar dades dels membres
    membres = []
    for membre_data, entrades_count in membres_query:
        membre_info = membre_data
        membre_info.entrades_compartides = entrades_count
        membre_info.dies_membre = (datetime.now() - membre_info.data_adhesio).days
        membre_info.ultima_activitat = None  # Aquí es podria calcular últim login
        membres.append(membre_info)
    
    # Estadístiques
    membres_admins = [m for m in membres if m.rol == 'admin']
    membres_actius_mes = len([m for m in membres if m.dies_membre <= 30])  # Aproximació
    dies_promig_membre = sum([m.dies_membre for m in membres]) / len(membres) if membres else 0
    
    return render_template('organitzacions/seccio_membres.html',
                         organitzacio=organitzacio,
                         membres=membres,
                         membres_admins=membres_admins,
                         membres_actius_mes=membres_actius_mes,
                         dies_promig_membre=dies_promig_membre,
                         es_membre=es_membre,
                         es_admin=es_admin)
                         
def gestionar_seccio_imatges(organitzacio, es_membre, es_admin):
    """Secció IMATGES - Galeria d'imatges"""
    
    # Carregar entrades d'imatges compartides
    entrades_amb_imatges = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True,
        Entrada.tipus_fitxer.in_(['jpg', 'jpeg', 'png', 'webp', 'gif'])
    ).order_by(Entrada.data_creacio.desc()).all()
    
    # Anys disponibles
    anys_imatges = db.session.query(
        func.extract('year', Entrada.data_creacio).label('any')
    ).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True,
        Entrada.tipus_fitxer.in_(['jpg', 'jpeg', 'png', 'webp', 'gif'])
    ).distinct().order_by('any').all()
    
    anys_imatges = [int(any[0]) for any in anys_imatges]
    
    return render_template('organitzacions/seccio_imatges.html',
                         organitzacio=organitzacio,
                         entrades_amb_imatges=entrades_amb_imatges,
                         anys_imatges=anys_imatges,
                         es_membre=es_membre,
                         es_admin=es_admin)

@organitzacions_bp.route('/api/entrada/<int:entrada_id>')
def api_entrada(entrada_id):
    """API per obtenir dades d'una entrada específica"""
    entrada = Entrada.query.options(
        db.joinedload(Entrada.usuari),
        db.joinedload(Entrada.arxius_adjuntats)
    ).get_or_404(entrada_id)
    
    # Verificar que l'entrada és pública
    if not entrada.es_publica:
        abort(403)
    
    # Comprovar si està guardada (si l'usuari està loguejat)
    ja_guardada = False
    if 'usuari' in session:
        from models import EntradaGuardada
        actual = Usuari.query.filter_by(nom_login=session['usuari']).first()
        if actual:
            ja_guardada = EntradaGuardada.query.filter_by(
                usuari_id=actual.id, entrada_id=entrada.id
            ).first() is not None

    es_propietari = session.get("usuari") == entrada.usuari.nom_login

    # Calcular ubicació per entrada principal
    ubicacio_parts = []
    if entrada.municipi:
        ubicacio_parts.append(entrada.municipi)
    if entrada.regio:
        ubicacio_parts.append(entrada.regio)  
    if entrada.pais:
        ubicacio_parts.append(entrada.pais)
    ubicacio = ', '.join(ubicacio_parts)

    # Calcular ubicació per imatge
    ubicacio_imatge_parts = []
    if entrada.municipi_imatge:
        ubicacio_imatge_parts.append(entrada.municipi_imatge)
    if entrada.regio_imatge:
        ubicacio_imatge_parts.append(entrada.regio_imatge)
    if entrada.pais_imatge:
        ubicacio_imatge_parts.append(entrada.pais_imatge)
    ubicacio_imatge = ', '.join(ubicacio_imatge_parts)
    
    return jsonify({
        'id': entrada.id,
        'titol': entrada.titol,
        'tema': entrada.tema,
        'contingut': entrada.contingut,
        'usuari_nom': f"{entrada.usuari.nom} {entrada.usuari.primer_cognom} {entrada.usuari.segon_cognom or ''}".strip(),
        'usuari_login': entrada.usuari.nom_login,
        'data_creacio': entrada.data_creacio.strftime('%d/%m/%Y') if entrada.data_creacio else None,
        'any': entrada.any_text,
        'ubicacio': ubicacio,
        'ubicacio_imatge': ubicacio_imatge,
        'titol_imatge': entrada.titol_imatge,
        'any_imatge': entrada.any_imatge,
        'descripcio_imatge': entrada.descripcio_imatge,
        'referencia': entrada.referencia,
        'tipus_fitxer': entrada.tipus_fitxer,
        'nom_fitxer': entrada.nom_fitxer,
        'propietari': es_propietari,
        'ja_guardada': ja_guardada,
        'arxius': [
            {
                "nom_fitxer": f.nom_fitxer,
                "tipus": f.tipus,
                "ruta": f"/umberto/{entrada.usuari.nom_login}/{entrada.id}/{f.nom_fitxer}"
            }
            for f in entrada.arxius_adjuntats
        ]
    })


@organitzacions_bp.route('/contactar/<int:org_id>')
def contactar_organitzacio(org_id):
    """Pàgina per contactar una organització (per sol·licituds rebutjades)"""
    organitzacio = Organitzacio.query.get_or_404(org_id)
    
    # Obtenir admins de l'organització
    admins = MembreOrganitzacio.query.filter_by(
        organitzacio_id=org_id,
        rol='admin'
    ).join(Usuari).all()
    
    return render_template('organitzacions/contactar.html',
                         organitzacio=organitzacio,
                         admins=admins)

@organitzacions_bp.route('/enviar_contacte', methods=['POST'])
@login_required
def enviar_contacte_organitzacio():
    """Enviar missatge de contacte a organització"""
    try:
        data = request.get_json()
        org_id = data.get('organitzacio_id')
        admin_id = data.get('admin_id')  # Admin específic o None per tots
        assumpte = data.get('assumpte')
        contingut = data.get('contingut')
        
        organitzacio = Organitzacio.query.get_or_404(org_id)
        
        if admin_id:
            # Enviar a admin específic
            admins = [MembreOrganitzacio.query.filter_by(
                organitzacio_id=org_id,
                usuari_id=admin_id,
                rol='admin'
            ).first()]
        else:
            # Enviar a tots els admins
            admins = MembreOrganitzacio.query.filter_by(
                organitzacio_id=org_id,
                rol='admin'
            ).all()
        
        # Crear missatge per cada admin
        for admin in admins:
            if admin:
                # Missatge individual a l'admin
                missatge = Missatge(
                    emissor_id=current_user.id,
                    receptor_id=admin.usuari_id,
                    assumpte=f"[{organitzacio.nom}] {assumpte}",
                    contingut=contingut
                )
                db.session.add(missatge)
                
                # Còpia a la bústia de l'organització
                missatge_org = MissatgeOrganitzacio(
                    organitzacio_id=org_id,
                    emissor_id=current_user.id,
                    assumpte=assumpte,
                    contingut=contingut,
                    tipus='rebut'
                )
                db.session.add(missatge_org)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Missatge enviat a l\'organització'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Nova funció per afegir a xorganitzacions.py
# Aquesta funció substitueix gestionar_seccio_home i gestionar_seccio_historia

def gestionar_qui_som(organitzacio, es_membre, es_admin):
    """Secció QUI SOM - Informació completa, cronologia i evolució unificats"""
    
    # ========== ESTADÍSTIQUES (del home) ==========
    membres_count = MembreOrganitzacio.query.filter_by(organitzacio_id=organitzacio.id).count()
    
    entrades_count = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True
    ).count()
    
    # Entrades aquest mes
    primer_dia_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    entrades_mes_actual = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True,
        Entrada.data_creacio >= primer_dia_mes
    ).count()
    
    # Dies activa (des de la creació)
    dies_activa = (datetime.now() - organitzacio.data_creacio).days
    
    estadistiques = {
        'membres_count': membres_count,
        'entrades_count': entrades_count,
        'entrades_mes_actual': entrades_mes_actual,
        'dies_activa': dies_activa
    }
    
    # ========== ACTIVITAT RECENT (del home) ==========
    activitat_recent = []
    
    # Últimes entrades compartides
    ultimes_entrades = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True
    ).order_by(Entrada.data_creacio.desc()).limit(5).all()
    
    for entrada in ultimes_entrades:
        activitat_recent.append({
            'tipus': 'entrada',
            'descripcio': f'{entrada.usuari.nom} va compartir "{entrada.titol}"',
            'data': entrada.data_creacio
        })
    
    # Últims membres
    ultims_membres = MembreOrganitzacio.query.filter_by(
        organitzacio_id=organitzacio.id
    ).order_by(MembreOrganitzacio.data_adhesio.desc()).limit(3).all()
    
    for membre in ultims_membres:
        activitat_recent.append({
            'tipus': 'membre',
            'descripcio': f'{membre.usuari.nom} es va unir a l\'organització',
            'data': membre.data_adhesio
        })
    
    # Ordenar per data
    activitat_recent.sort(key=lambda x: x['data'], reverse=True)
    activitat_recent = activitat_recent[:10]  # Últimes 10
    
    # ========== CRONOLOGIA I EVOLUCIÓ (de historia) ==========
    
    # Primer membre
    primer_membre = MembreOrganitzacio.query.filter_by(
        organitzacio_id=organitzacio.id
    ).order_by(MembreOrganitzacio.data_adhesio.asc()).first()
    
    # Primera entrada
    primera_entrada = db.session.query(Entrada).join(
        EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
    ).filter(
        EntradaOrganitzacio.organitzacio_id == organitzacio.id,
        Entrada.es_publica == True
    ).order_by(Entrada.data_creacio.asc()).first()
    
    # Fites importants
    fites_importants = []
    
    # Fita de membres
    if membres_count >= 10:
        fites_importants.append({
            'titol': f'10 membres assolits',
            'descripcio': 'L\'organització va arribar als 10 membres',
            'data': datetime.now() - timedelta(days=30)  # Aproximació
        })
    
    # Evolució últims 6 mesos
    ultims_6_mesos = []
    for i in range(6):
        mes_actual = datetime.now() - timedelta(days=30*i)
        inici_mes = mes_actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        fi_mes = (inici_mes + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
        
        nous_membres = MembreOrganitzacio.query.filter(
            MembreOrganitzacio.organitzacio_id == organitzacio.id,
            MembreOrganitzacio.data_adhesio >= inici_mes,
            MembreOrganitzacio.data_adhesio <= fi_mes
        ).count()
        
        noves_entrades = db.session.query(Entrada).join(
            EntradaOrganitzacio, EntradaOrganitzacio.entrada_id == Entrada.id
        ).filter(
            EntradaOrganitzacio.organitzacio_id == organitzacio.id,
            Entrada.es_publica == True,
            Entrada.data_creacio >= inici_mes,
            Entrada.data_creacio <= fi_mes
        ).count()
        
        ultims_6_mesos.append({
            'nom': mes_actual.strftime('%B'),
            'nous_membres': nous_membres,
            'noves_entrades': noves_entrades
        })
    
    ultims_6_mesos.reverse()  # Més antic primer
    
    # Màxims per normalitzar gràfics
    max_nous_membres = max([m['nous_membres'] for m in ultims_6_mesos]) or 1
    max_noves_entrades = max([m['noves_entrades'] for m in ultims_6_mesos]) or 1
    
    # ========== RENDERITZAR TEMPLATE UNIFICAT ==========
    return render_template('organitzacions/organitzacio_qui_som.html',
                         organitzacio=organitzacio,
                         es_membre=es_membre,
                         es_admin=es_admin,
                         estadistiques=estadistiques,
                         activitat_recent=activitat_recent,
                         primer_membre=primer_membre,
                         primera_entrada=primera_entrada,
                         fites_importants=fites_importants,
                         ultims_6_mesos=ultims_6_mesos,
                         max_nous_membres=max_nous_membres,
                         max_noves_entrades=max_noves_entrades)