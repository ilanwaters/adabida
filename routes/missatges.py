from flask import Blueprint, request, redirect, url_for, flash, jsonify, render_template, send_from_directory, abort
from flask_login import login_required, current_user
from models import db, Missatge, Usuari
import os
from werkzeug.utils import secure_filename
from models import ArxiuMissatge


EXTENSIONS_PERMESES = {'jpg', 'jpeg', 'png', 'webp', 'gif', 'pdf', 'doc', 'docx'}
MIDA_MAXIMA = 10 * 1024 * 1024  # 10 MB per fitxer

def _extensio_permesa(nom_fitxer):
    return '.' in nom_fitxer and nom_fitxer.rsplit('.', 1)[1].lower() in EXTENSIONS_PERMESES

import shutil

def _esborra_arxius_fisics(missatge_id):
    carpeta = os.path.join("umberto", "missatges", str(missatge_id))
    if os.path.isdir(carpeta):
        shutil.rmtree(carpeta, ignore_errors=True)

missatges_bp = Blueprint("missatges", __name__)


@missatges_bp.route("/enviar_missatge", methods=["POST"])
@login_required
def enviar():
    receptor_id = request.form.get("receptor_id")
    assumpte = request.form.get("assumpte", "").strip()
    contingut = request.form.get("contingut", "").strip()
    arxius = request.files.getlist("arxius")

    es_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if not receptor_id or not contingut or not assumpte:
        if es_ajax:
            return jsonify({"success": False, "error": "Missatge incomplet."}), 400
        flash("Missatge incomplet.", "error")
        return redirect(request.referrer)

    if receptor_id.isdigit():
        receptor = Usuari.query.get(int(receptor_id))
    else:
        receptor = Usuari.query.filter_by(nom_login=receptor_id).first()

    if not receptor:
        if es_ajax:
            return jsonify({"success": False, "error": "Usuari no trobat."}), 404
        flash("Usuari no trobat.", "error")
        return redirect(request.referrer)

    if not receptor.rebre_missatges:
        if es_ajax:
            return jsonify({"success": False, "error": "Aquest usuari no accepta missatges."}), 400
        flash("Aquest usuari no accepta missatges.", "error")
        return redirect(request.referrer)

    # Validació prèvia dels arxius (abans de tocar BD ni disc)
    for arxiu in arxius:
        if not arxiu or not arxiu.filename:
            continue
        if not _extensio_permesa(arxiu.filename):
            error = f"Tipus de fitxer no permès: {arxiu.filename}"
            if es_ajax:
                return jsonify({"success": False, "error": error}), 400
            flash(error, "error")
            return redirect(request.referrer)

    missatge = Missatge(
        emissor_id=current_user.id,
        receptor_id=receptor.id,
        assumpte=assumpte,
        contingut=contingut
    )
    db.session.add(missatge)
    db.session.commit()  # cal l'id per crear la carpeta

    carpeta = os.path.join("umberto", "missatges", str(missatge.id))
    for arxiu in arxius:
        if not arxiu or not arxiu.filename:
            continue

        arxiu.seek(0, os.SEEK_END)
        mida = arxiu.tell()
        arxiu.seek(0)
        if mida > MIDA_MAXIMA:
            continue  # fitxer massa gran, s'ignora silenciosament

        os.makedirs(carpeta, exist_ok=True)
        nom_segur = secure_filename(arxiu.filename)
        arxiu.save(os.path.join(carpeta, nom_segur))

        ext = nom_segur.rsplit('.', 1)[1].lower()
        tipus_media = 'imatge' if ext in {'jpg', 'jpeg', 'png', 'webp', 'gif'} else 'document'

        db.session.add(ArxiuMissatge(
            missatge_id=missatge.id,
            nom_fitxer=nom_segur,
            tipus=ext,
            tipus_media=tipus_media
        ))

    db.session.commit()

    if es_ajax:
        return jsonify({"success": True})

    flash("Missatge enviat correctament.", "success")
    return redirect(request.referrer)

@missatges_bp.route("/rebuts")
@login_required
def veure_rebuts():
    missatges = (
        Missatge.query
        .filter_by(receptor_id=current_user.id)
        .order_by(Missatge.data.desc())
        .all()
    )
    return render_template("missatges/rebuts.html", missatges=missatges)

@missatges_bp.route("/eliminar_missatge/<int:missatge_id>", methods=["POST"])
@login_required
def elimina_missatge(missatge_id):
    missatge = Missatge.query.get_or_404(missatge_id)

    # Només el receptor pot eliminar-lo
    if missatge.receptor_id != current_user.id:
        flash("No tens permís per eliminar aquest missatge.", "error")
        return redirect(url_for("pagina_personal", perfil_id=current_user.id))


    _esborra_arxius_fisics(missatge.id)
    db.session.delete(missatge)
    db.session.commit()
    flash("Missatge eliminat.", "success")
    return redirect(url_for("pagina_personal.pagina_personal", pestanya="perfil", obrir="missatges"))

@missatges_bp.route("/eliminar_missatge_enviat/<int:missatge_id>", methods=["POST"])
@login_required
def elimina_missatge_enviat(missatge_id):
    missatge = Missatge.query.get_or_404(missatge_id)

    # Només l'emissor pot eliminar-lo
    if missatge.emissor_id != current_user.id:
        flash("No tens permís per eliminar aquest missatge.", "error")
        return redirect(url_for("pagina_personal.pagina_personal", perfil_id=current_user.id))

    _esborra_arxius_fisics(missatge.id)
    db.session.delete(missatge)
    db.session.commit()
    flash("Missatge enviat eliminat.", "success")
    return redirect(url_for("pagina_personal.pagina_personal", pestanya="perfil", obrir="missatges"))

@missatges_bp.route("/api/missatge/<int:missatge_id>")
@login_required
def api_missatge(missatge_id):
    print(f"🔍 API CRIDADA - ID: {missatge_id}")
    
    try:
        missatge = Missatge.query.get_or_404(missatge_id)
        print(f"✅ MISSATGE TROBAT: {missatge.assumpte}")
        
        # Test dels camps
        print(f"📅 DATA_ENV: {missatge.data_env}")
        print(f"👤 EMISSOR: {missatge.emissor.nom}")
        
        # Només emissor o receptor poden veure el missatge
        if missatge.receptor_id != current_user.id and missatge.emissor_id != current_user.id:
            return jsonify({"error": "No autoritzat"}), 403

        # Només si ets el receptor, es marca com a llegit
        if missatge.receptor_id == current_user.id:
            missatge.llegit = True
            db.session.commit()

        # Si és un missatge amb plantilla, traduir-lo
        if missatge.tipus_missatge:
            from utils.plantilles_missatges import obtenir_missatge_traduit
            from flask import session
            import json
            
            # Obtenir idioma actual de la sessió
            idioma = session.get('idioma', 'ca')
            
            # Carregar dades JSON
            dades = json.loads(missatge.dades_json) if missatge.dades_json else {}
            
            # Traduir
            assumpte_traduit, contingut_traduit = obtenir_missatge_traduit(
                missatge.tipus_missatge,
                idioma,
                **dades
            )
            
            if assumpte_traduit and contingut_traduit:
                missatge.assumpte = assumpte_traduit
                missatge.contingut = contingut_traduit

        # Determinem si ets el receptor o l'emissor
        remitent = f"{missatge.emissor.nom} {missatge.emissor.primer_cognom}"
        receptor = f"{missatge.receptor.nom} {missatge.receptor.primer_cognom}"
        es_contacte = current_user.es_contacte(missatge.emissor) if missatge.emissor_id != current_user.id else True
        
        arxius_info = [{
            "nom_fitxer": a.nom_fitxer,
            "tipus": a.tipus,
            "tipus_media": a.tipus_media,
            "url": url_for("missatges.servir_arxiu_missatge", missatge_id=missatge.id, nom_fitxer=a.nom_fitxer)
        } for a in missatge.arxius_adjunts]
        
        return jsonify({
            "id": missatge.id,
            "assumpte": missatge.assumpte,
            "contingut": missatge.contingut,
            "data": missatge.data_env.strftime("%d/%m/%Y %H:%M"),
            "remitent": remitent,
            "receptor": receptor,
            "es_contacte": es_contacte,
            "emissor_id": missatge.emissor_id,
            "emissor_login": missatge.emissor.nom_login,
            "arxius": arxius_info
        })      
    except Exception as e:
        print(f"❌ ERROR API: {e}")
        return jsonify({"error": str(e)}), 500

@missatges_bp.route('/missatgeria')
@login_required
def missatgeria():
    """Pàgina principal de missatgeria de l'usuari"""
    print(f"=== ACCEDINT A MISSATGERIA - USUARI: {current_user.nom} ===")
    
    # Obtenir tots els missatges de l'usuari (rebuts i enviats)
    missatges = Missatge.query.filter(
        (Missatge.receptor_id == current_user.id) | 
        (Missatge.emissor_id == current_user.id)
    ).order_by(Missatge.data_env.desc()).all()
    
    print(f"MISSATGES TROBATS: {len(missatges)}")
    
    return render_template('pagina_personal/missatgeria.html', missatges=missatges)

@missatges_bp.route('/api/usuaris')
@login_required
def api_usuaris():
    query = request.args.get('q', '').strip()
    usuaris = Usuari.query.filter(
        Usuari.nom.ilike(f'%{query}%'),
        Usuari.rebre_missatges == True
    ).limit(10).all()
    
    return jsonify([{
        'id': u.id,
        'nom': u.nom,
        'login': u.nom_login
    } for u in usuaris])

@missatges_bp.route("/missatge/arxiu/<int:missatge_id>/<path:nom_fitxer>")
@login_required
def servir_arxiu_missatge(missatge_id, nom_fitxer):
    missatge = Missatge.query.get_or_404(missatge_id)

    if current_user.id not in (missatge.emissor_id, missatge.receptor_id):
        abort(403)

    carpeta = os.path.join(
        os.getcwd(), "umberto", "missatges", str(missatge_id)
    )
    return send_from_directory(carpeta, nom_fitxer)  



