from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, EspaiFamiliar, MembreFamilia, DocumentMembreFamilia, Matrimoni
from werkzeug.utils import secure_filename
import os

membres_bp = Blueprint('membres', __name__, url_prefix='/familia/membre')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@membres_bp.route('/afegir/<int:familia_id>', methods=['GET', 'POST'])
@login_required
def afegir(familia_id):
    """Afegir un nou membre a l'espai familiar"""
    familia = EspaiFamiliar.query.get_or_404(familia_id)
    
    # Comprovar que l'usuari és administrador
    es_membre = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia_id
    ).first()
    
    if not es_membre or es_membre.rol != 'administrador':
        flash('Només els administradors poden afegir membres', 'error')
        return redirect(url_for('familia.veure', url=familia.url))
    
    # Detectar si ve des de gestió de relacions
    relacio = request.args.get('relacio')
    membre_relacionat_id = request.args.get('membre_id')
    
    if request.method == 'GET':
        # Carregar tots els membres de la família per al selector
        tots_membres_obj = MembreFamilia.query.filter_by(espai_familiar_id=familia_id).all()
        
        # Convertir a diccionaris per JSON
        tots_membres = [{
            'id': m.id,
            'nom': m.nom,
            'primer_cognom': m.primer_cognom,
            'data_naixement': m.data_naixement.isoformat() if m.data_naixement else None
        } for m in tots_membres_obj]
        
        return render_template('familia/afegir_membre.html', 
                             familia=familia,
                             relacio=relacio,
                             membre_relacionat_id=membre_relacionat_id,
                             tots_membres=tots_membres)
    
    # POST - Processar formulari
    try:
        from datetime import datetime as dt
        
        # COMPROVAR SI S'HA SELECCIONAT MEMBRE EXISTENT
        membre_existent_id = request.form.get('membre_existent_id')
        
        if membre_existent_id and membre_existent_id.strip():
            # USAR MEMBRE EXISTENT
            nou_membre = MembreFamilia.query.get(int(membre_existent_id))
            
            if not nou_membre or nou_membre.espai_familiar_id != familia_id:
                flash('Membre no vàlid', 'error')
                return redirect(url_for('membres.afegir', familia_id=familia_id))
            
        else:
            # CREAR NOU MEMBRE
            nom = request.form.get('nom', '').strip()
            primer_cognom = request.form.get('primer_cognom', '').strip()
            segon_cognom = request.form.get('segon_cognom', '').strip() or None
            genere = request.form.get('genere', '').strip()
            
            if not nom or not primer_cognom or not genere:
                flash('El nom, cognom i gènere són obligatoris', 'error')
                return redirect(url_for('membres.afegir', familia_id=familia_id))
            
            # Dates
            data_naixement = request.form.get('data_naixement')
            data_defuncio = request.form.get('data_defuncio')
            
            data_naixement = dt.strptime(data_naixement, '%Y-%m-%d').date() if data_naixement else None
            data_defuncio = dt.strptime(data_defuncio, '%Y-%m-%d').date() if data_defuncio else None
            
            # Crear membre
            nou_membre = MembreFamilia(
                espai_familiar_id=familia_id,
                nom=nom,
                primer_cognom=primer_cognom,
                segon_cognom=segon_cognom,
                genere=genere,
                data_naixement=data_naixement,
                municipi_naixement=request.form.get('municipi_naixement', '').strip() or None,
                regio_naixement=request.form.get('regio_naixement', '').strip() or None,
                pais_naixement=request.form.get('pais_naixement', '').strip() or None,
                data_defuncio=data_defuncio,
                municipi_defuncio=request.form.get('municipi_defuncio', '').strip() or None,
                regio_defuncio=request.form.get('regio_defuncio', '').strip() or None,
                pais_defuncio=request.form.get('pais_defuncio', '').strip() or None,
                municipi_actual=request.form.get('municipi_actual', '').strip() or None,
                regio_actual=request.form.get('regio_actual', '').strip() or None,
                pais_actual=request.form.get('pais_actual', '').strip() or None,
                biografia=request.form.get('biografia', '').strip() or None,
                rol='membre'
            )
            
            # Vincular amb usuari si s'ha seleccionat
            usuari_id = request.form.get('usuari_id')
            if usuari_id and usuari_id.strip():
                nou_membre.usuari_id = int(usuari_id)

            db.session.add(nou_membre)
            db.session.flush()
        
        # ESTABLIR RELACIÓ AUTOMÀTICAMENT
        relacio_param = request.form.get('relacio_hidden')
        membre_relacionat_id_param = request.form.get('membre_relacionat_id_hidden')
        
        if relacio_param and membre_relacionat_id_param:
            membre_relacionat = MembreFamilia.query.get(int(membre_relacionat_id_param))
            
            if relacio_param == 'pare':
                membre_relacionat.pare_id = nou_membre.id
                flash(f'{nou_membre.nom} afegit com a pare!', 'success')
                
            elif relacio_param == 'mare':
                membre_relacionat.mare_id = nou_membre.id
                flash(f'{nou_membre.nom} afegida com a mare!', 'success')
                
            elif relacio_param == 'fill':
                if membre_relacionat.genere == 'home':
                    nou_membre.pare_id = membre_relacionat.id
                elif membre_relacionat.genere == 'dona':
                    nou_membre.mare_id = membre_relacionat.id
                flash(f'{nou_membre.nom} afegit/da com a fill/a!', 'success')
                 
            elif relacio_param == 'germa':
                nou_membre.pare_id = membre_relacionat.pare_id
                nou_membre.mare_id = membre_relacionat.mare_id
                flash(f'{nou_membre.nom} afegit/da com a germà/na!', 'success')
        
        # Processar documents (només si és membre nou)
        if not membre_existent_id:
            fitxers = request.files.getlist('document[]')
            tipus_documents = request.form.getlist('tipus_document[]')
            visibilitats = request.form.getlist('visibilitat_document[]')
            descripcions = request.form.getlist('descripcio_document[]')
            
            for i, fitxer in enumerate(fitxers):
                if fitxer and fitxer.filename != '' and allowed_file(fitxer.filename):
                    filename = secure_filename(fitxer.filename)
                    ext = filename.rsplit('.', 1)[1].lower()
                    
                    carpeta_documents = f'static/documents_membres/{familia_id}'
                    os.makedirs(carpeta_documents, exist_ok=True)
                    
                    nom_fitxer = f"membre_{nou_membre.id}_doc_{i+1}.{ext}"
                    ruta_fitxer = os.path.join(carpeta_documents, nom_fitxer)
                    fitxer.save(ruta_fitxer)
                    
                    document = DocumentMembreFamilia(
                        membre_familia_id=nou_membre.id,
                        tipus_document=tipus_documents[i] if i < len(tipus_documents) else None,
                        nom_fitxer=nom_fitxer,
                        descripcio=descripcions[i] if i < len(descripcions) else None,
                        visibilitat=visibilitats[i] if i < len(visibilitats) else 'familia',
                        pujat_per_id=current_user.id
                    )
                    db.session.add(document)
        
        db.session.commit()
        
        # Redirigir segons context
        if membre_relacionat_id_param:
            return redirect(url_for('membres.gestionar_relacions', membre_id=int(membre_relacionat_id_param)))
        else:
            flash(f'Membre afegit correctament!', 'success')
            return redirect(url_for('familia.seccio', url=familia.url, seccio='membres'))
        
    except Exception as e:
        db.session.rollback()
        print(f"Error afegint membre: {e}")
        import traceback
        traceback.print_exc()
        flash('Error afegint el membre. Torna-ho a provar.', 'error')
        return redirect(url_for('familia.veure', url=familia.url))
        
@membres_bp.route('/<int:membre_id>')
@login_required
def veure(membre_id):
    """Veure perfil d'un membre de la família"""
    from models import Pais, Regio, Municipi
    
    membre = MembreFamilia.query.get_or_404(membre_id)
    familia = membre.espai_familiar
    
    # Comprovar que l'usuari és membre de la família
    es_membre_familia = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id
    ).first()
    
    if not es_membre_familia:
        flash('No tens accés a aquest membre', 'error')
        return redirect(url_for('familia.les_meves'))
    
    # Comprovar si és admin
    es_admin = (es_membre_familia.rol == 'administrador')
    
    # CONVERTIR IDs A NOMS - FUNCIÓ AUXILIAR
    def id_a_nom(valor, model):
        """Converteix ID a nom, retorna el valor original si no és ID"""
        if not valor:
            return None
        if str(valor).isdigit():
            obj = model.query.get(int(valor))
            return obj.nom if obj else str(valor)
        return valor
    
    # Crear diccionari amb ubicacions convertides
    ubicacions = {
        'pais_naix': id_a_nom(membre.pais_naixement, Pais),
        'regio_naix': id_a_nom(membre.regio_naixement, Regio),
        'municipi_naix': id_a_nom(membre.municipi_naixement, Municipi),
        'pais_def': id_a_nom(membre.pais_defuncio, Pais),
        'regio_def': id_a_nom(membre.regio_defuncio, Regio),
        'municipi_def': id_a_nom(membre.municipi_defuncio, Municipi),
        'pais_act': id_a_nom(membre.pais_actual, Pais),
        'regio_act': id_a_nom(membre.regio_actual, Regio),
        'municipi_act': id_a_nom(membre.municipi_actual, Municipi)
    }
    
    # Filtrar documents segons permisos
    if es_admin:
        documents = membre.documents
    else:
        documents = [doc for doc in membre.documents if doc.visibilitat == 'familia']
    
    return render_template('familia/veure_membre.html', 
                         membre=membre, 
                         familia=familia,
                         es_admin=es_admin,
                         documents=documents,
                         ub=ubicacions)

@membres_bp.route('/<int:membre_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(membre_id):
    """Editar un membre de la família"""
    membre = MembreFamilia.query.get_or_404(membre_id)
    familia = membre.espai_familiar
    
    # Comprovar que l'usuari és administrador
    es_admin = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id,
        rol='administrador'
    ).first()
    
    if not es_admin:
        flash('Només els administradors poden editar membres', 'error')
        return redirect(url_for('familia.veure', url=familia.url))
    
    if request.method == 'GET':
        return render_template('familia/editar_membre.html', membre=membre, familia=familia)
    
    # POST - Actualitzar
    try:
        from datetime import datetime as dt
        from models import Pais, Regio, Municipi
        
        # 1. OBTENIR VALORS
        nom = request.form.get('nom', '').strip()
        primer_cognom = request.form.get('primer_cognom', '').strip()
        segon_cognom = request.form.get('segon_cognom', '').strip() or None
        genere = request.form.get('genere', '').strip() or None
        
        # 2. VALIDAR
        if not nom or not primer_cognom or not genere:
            flash('El nom, cognom i gènere són obligatoris', 'error')
            return render_template('familia/editar_membre.html', membre=membre, familia=familia)
        
        # 3. ACTUALITZAR DADES BÀSIQUES
        membre.nom = nom
        membre.primer_cognom = primer_cognom
        membre.segon_cognom = segon_cognom
        membre.genere = genere
        
        # 4. DATES (amb comprovació)
        data_naix = request.form.get('data_naixement', '').strip()
        data_def = request.form.get('data_defuncio', '').strip()
        
        membre.data_naixement = dt.strptime(data_naix, '%Y-%m-%d').date() if data_naix else None
        membre.data_defuncio = dt.strptime(data_def, '%Y-%m-%d').date() if data_def else None
        
        # 5. FUNCIÓ AUXILIAR UBICACIONS
        def obtenir_id(valor, model):
            if not valor or not valor.strip():
                return None
            if str(valor).isdigit():
                return int(valor)
            obj = model.query.filter_by(nom=valor).first()
            return obj.id if obj else valor
        
        # 6. UBICACIONS
        membre.pais_naixement = obtenir_id(request.form.get('pais_naixement'), Pais)
        membre.regio_naixement = obtenir_id(request.form.get('regio_naixement'), Regio)
        membre.municipi_naixement = obtenir_id(request.form.get('municipi_naixement'), Municipi)
        
        membre.pais_defuncio = obtenir_id(request.form.get('pais_defuncio'), Pais)
        membre.regio_defuncio = obtenir_id(request.form.get('regio_defuncio'), Regio)
        membre.municipi_defuncio = obtenir_id(request.form.get('municipi_defuncio'), Municipi)
        
        membre.pais_actual = obtenir_id(request.form.get('pais_actual'), Pais)
        membre.regio_actual = obtenir_id(request.form.get('regio_actual'), Regio)
        membre.municipi_actual = obtenir_id(request.form.get('municipi_actual'), Municipi)
        
        # 7. BIOGRAFIA
        membre.biografia = request.form.get('biografia', '').strip() or None
        
        # 8. USUARI VINCULAT
        usuari_id = request.form.get('usuari_id', '').strip()
        membre.usuari_id = int(usuari_id) if usuari_id else None
        
        # 9. COMMIT
        db.session.commit()
        
        flash(f'Membre {membre.nom} {membre.primer_cognom} actualitzat!', 'success')
        return redirect(url_for('membres.veure', membre_id=membre.id))
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ ERROR editant membre: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error editant el membre: {str(e)}', 'error')
        return render_template('familia/editar_membre.html', membre=membre, familia=familia)
        
@membres_bp.route('/<int:membre_id>/relacions', methods=['GET'])
@login_required
def gestionar_relacions(membre_id):
    """Gestionar les relacions familiars d'un membre"""
    from models import Matrimoni
    
    membre = MembreFamilia.query.get_or_404(membre_id)
    familia = membre.espai_familiar
    
    # Comprovar que l'usuari és admin
    es_admin = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id,
        rol='administrador'
    ).first()
    
    if not es_admin:
        flash('Només els administradors poden gestionar relacions', 'error')
        return redirect(url_for('membres.veure', membre_id=membre_id))
    
    # Obtenir matrimonis
    matrimonis = Matrimoni.query.filter(
        db.or_(
            Matrimoni.membre_1_id == membre.id,
            Matrimoni.membre_2_id == membre.id
        )
    ).all()
    
    # Calcular germans (mateix pare o mateixa mare)
    germans = []
    if membre.pare_id:
        germans.extend([f for f in membre.pare.fills_com_pare if f.id != membre.id])
    if membre.mare_id:
        germans.extend([f for f in membre.mare.fills_com_mare if f.id != membre.id and f not in germans])
    
    # Calcular fills
    fills = list(membre.fills_com_pare) if hasattr(membre, 'fills_com_pare') else []
    if hasattr(membre, 'fills_com_mare'):
        fills.extend([f for f in membre.fills_com_mare if f not in fills])
    
    tots_membres = MembreFamilia.query.filter_by(espai_familiar_id=familia.id).order_by(MembreFamilia.nom).all()
    
    return render_template('familia/gestionar_relacions.html',
                         membre=membre,
                         familia=familia,
                         germans=germans,
                         fills=fills,
                         matrimonis=matrimonis,
                         tots_membres=tots_membres,  
                         es_admin=True)

@membres_bp.route('/matrimoni/afegir/<int:membre_id>', methods=['POST'])
@login_required
def afegir_matrimoni(membre_id):
    """Afegir un matrimoni per un membre"""
    membre = MembreFamilia.query.get_or_404(membre_id)
    familia = membre.espai_familiar
    
    # Comprovar que l'usuari és administrador
    es_membre = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id
    ).first()
    
    if not es_membre or es_membre.rol != 'administrador':
        flash('Només els administradors poden afegir matrimonis', 'error')
        return redirect(url_for('membres.gestionar_relacions', membre_id=membre_id))
    
    try:
        from datetime import datetime as dt
        
        conjuge_id = request.form.get('conjuge_id')
        data_casament = request.form.get('data_casament')
        data_fi = request.form.get('data_fi')
        estat = request.form.get('estat', 'actiu')
        
        if not conjuge_id:
            flash('Has de seleccionar un cònjuge', 'error')
            return redirect(url_for('membres.gestionar_relacions', membre_id=membre_id))
        
        # Convertir dates
        data_casament = dt.strptime(data_casament, '%Y-%m-%d').date() if data_casament else None
        data_fi = dt.strptime(data_fi, '%Y-%m-%d').date() if data_fi else None
        
        # Comprovar que el matrimoni no existeix ja
        matrimoni_existent = Matrimoni.query.filter(
            db.or_(
                db.and_(Matrimoni.membre_1_id == membre_id, Matrimoni.membre_2_id == conjuge_id),
                db.and_(Matrimoni.membre_1_id == conjuge_id, Matrimoni.membre_2_id == membre_id)
            )
        ).first()
        
        if matrimoni_existent:
            flash('Ja existeix un matrimoni registrat entre aquestes dues persones', 'warning')
            return redirect(url_for('membres.gestionar_relacions', membre_id=membre_id))
        
        # Crear matrimoni
        # Crear matrimoni
        nou_matrimoni = Matrimoni(
            espai_familiar_id=familia.id,
            membre_1_id=membre_id,
            membre_2_id=int(conjuge_id),
            data_casament=data_casament,
            data_fi=data_fi,
            estat=estat
        )
        
        db.session.add(nou_matrimoni)
        db.session.flush()  # Obtenir ID matrimoni
        
        # Processar fills seleccionats
        fills_seleccionats = request.form.getlist('fills[]')
        if fills_seleccionats:
            for fill_id in fills_seleccionats:
                fill = MembreFamilia.query.get(int(fill_id))
                if fill:
                    fill.matrimoni_id = nou_matrimoni.id
        
        db.session.commit()
        
        conjuge = MembreFamilia.query.get(conjuge_id)
        flash(f'Matrimoni amb {conjuge.nom} {conjuge.primer_cognom} afegit correctament!', 'success')
        return redirect(url_for('membres.veure_matrimoni', matrimoni_id=nou_matrimoni.id))
        
    except Exception as e:
        db.session.rollback()
        print(f"Error afegint matrimoni: {e}")
        import traceback
        traceback.print_exc()
        flash('Error afegint el matrimoni. Torna-ho a provar.', 'error')
        return redirect(url_for('membres.gestionar_relacions', membre_id=membre_id))

@membres_bp.route('/<int:membre_id>/eliminar', methods=['GET', 'POST'])
@login_required
def eliminar(membre_id):
    """Eliminar un membre de la família (només admins)"""
    membre = MembreFamilia.query.get_or_404(membre_id)
    familia = membre.espai_familiar
    
    # Comprovar que l'usuari és administrador
    es_admin = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id,
        rol='administrador'
    ).first()
    
    if not es_admin:
        flash('Només els administradors poden eliminar membres', 'error')
        return redirect(url_for('familia.veure', url=familia.url))
    
    try:
        # 1. Eliminar documents físics
        for doc in membre.documents:
            ruta_fitxer = os.path.join('static', 'documents_membres', str(familia.id), doc.nom_fitxer)
            if os.path.exists(ruta_fitxer):
                os.remove(ruta_fitxer)
            db.session.delete(doc)
        
        # 2. Actualitzar relacions familiars (no eliminar fills, només trencar vincles)
        # Fills que tenien aquest membre com a pare
        fills_com_pare = MembreFamilia.query.filter_by(pare_id=membre.id).all()
        for fill in fills_com_pare:
            fill.pare_id = None
        
        # Fills que tenien aquest membre com a mare
        fills_com_mare = MembreFamilia.query.filter_by(mare_id=membre.id).all()
        for fill in fills_com_mare:
            fill.mare_id = None
        
        # 3. Eliminar matrimonis
        matrimonis = Matrimoni.query.filter(
            db.or_(
                Matrimoni.membre_1_id == membre.id,
                Matrimoni.membre_2_id == membre.id
            )
        ).all()
        for matrimoni in matrimonis:
            db.session.delete(matrimoni)
        
        # 4. Eliminar el membre
        nom_complet = f"{membre.nom} {membre.primer_cognom}"
        db.session.delete(membre)
        db.session.commit()
        
        flash(f'Membre {nom_complet} eliminat correctament', 'success')
        return redirect(url_for('familia.seccio', url=familia.url, seccio='membres'))
        
    except Exception as e:
        db.session.rollback()
        print(f"Error eliminant membre: {e}")
        import traceback
        traceback.print_exc()
        flash('Error eliminant el membre. Torna-ho a provar.', 'error')
        return redirect(url_for('membres.editar', membre_id=membre_id))

@membres_bp.route('/matrimoni/<int:matrimoni_id>')
@login_required
def veure_matrimoni(matrimoni_id):
    """Pàgina detall matrimoni amb cònjuges i fills"""
    matrimoni = Matrimoni.query.get_or_404(matrimoni_id)
    familia = matrimoni.espai_familiar
    
    # Verificar accés
    es_membre = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id
    ).first()
    
    if not es_membre:
        flash('No tens accés a aquesta família', 'error')
        return redirect(url_for('home.index'))
    
    # Obtenir fills d'aquest matrimoni
    fills = MembreFamilia.query.filter_by(matrimoni_id=matrimoni_id).all()
    
    return render_template('familia/matrimoni_detall.html',
                         matrimoni=matrimoni,
                         familia=familia,
                         fills=fills,
                         es_admin=(es_membre.rol == 'administrador'))

@membres_bp.route('/matrimoni/<int:matrimoni_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_matrimoni(matrimoni_id):
    """Editar matrimoni"""
    matrimoni = Matrimoni.query.get_or_404(matrimoni_id)
    familia = matrimoni.espai_familiar
    
    # Verificar admin
    es_admin = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id,
        rol='administrador'
    ).first()
    
    if not es_admin:
        flash('Només els administradors poden editar matrimonis', 'error')
        return redirect(url_for('membres.veure_matrimoni', matrimoni_id=matrimoni_id))
    
    if request.method == 'GET':
        # Obtenir tots els fills possibles (dels dos cònjuges)
        fills_membre1 = list(matrimoni.membre_1.fills_com_pare if hasattr(matrimoni.membre_1, 'fills_com_pare') else [])
        fills_membre1.extend([f for f in (matrimoni.membre_1.fills_com_mare if hasattr(matrimoni.membre_1, 'fills_com_mare') else []) if f not in fills_membre1])
        
        fills_membre2 = list(matrimoni.membre_2.fills_com_pare if hasattr(matrimoni.membre_2, 'fills_com_pare') else [])
        fills_membre2.extend([f for f in (matrimoni.membre_2.fills_com_mare if hasattr(matrimoni.membre_2, 'fills_com_mare') else []) if f not in fills_membre2])
        
        tots_fills = fills_membre1 + [f for f in fills_membre2 if f not in fills_membre1]
        fills_actuals = MembreFamilia.query.filter_by(matrimoni_id=matrimoni_id).all()
        
        return render_template('familia/editar_matrimoni.html',
                             matrimoni=matrimoni,
                             familia=familia,
                             tots_fills=tots_fills,
                             fills_actuals=fills_actuals)
    
    # POST
    try:
        from datetime import datetime as dt
        
        data_casament = request.form.get('data_casament')
        data_fi = request.form.get('data_fi')
        estat = request.form.get('estat', 'actiu')
        
        matrimoni.data_casament = dt.strptime(data_casament, '%Y-%m-%d').date() if data_casament else None
        matrimoni.data_fi = dt.strptime(data_fi, '%Y-%m-%d').date() if data_fi else None
        matrimoni.estat = estat
        
        # Desassignar tots els fills primers
        fills_antics = MembreFamilia.query.filter_by(matrimoni_id=matrimoni_id).all()
        for fill in fills_antics:
            fill.matrimoni_id = None
        
        # Assignar fills seleccionats
        fills_seleccionats = request.form.getlist('fills[]')
        if fills_seleccionats:
            for fill_id in fills_seleccionats:
                fill = MembreFamilia.query.get(int(fill_id))
                if fill:
                    fill.matrimoni_id = matrimoni_id
        
        db.session.commit()
        flash('Matrimoni actualitzat correctament!', 'success')
        return redirect(url_for('membres.veure_matrimoni', matrimoni_id=matrimoni_id))
        
    except Exception as e:
        db.session.rollback()
        print(f"Error editant matrimoni: {e}")
        import traceback
        traceback.print_exc()
        flash('Error afegint el matrimoni. Torna-ho a provar.', 'error')
        return redirect(url_for('membres.gestionar_relacions', membre_id=membre_id))

@membres_bp.route('/<int:membre_id>/toggle-visibilitat', methods=['POST'])
@login_required
def toggle_visibilitat(membre_id):
    """Alternar la visibilitat pública d'un membre"""
    membre = MembreFamilia.query.get_or_404(membre_id)
    familia = membre.espai_familiar

    es_admin = MembreFamilia.query.filter_by(
        usuari_id=current_user.id,
        espai_familiar_id=familia.id,
        rol='administrador'
    ).first()

    if not es_admin:
        return jsonify({'success': False, 'error': 'No tens permisos'}), 403

    membre.visible_public = not membre.visible_public
    db.session.commit()

    return jsonify({'success': True, 'visible_public': membre.visible_public})