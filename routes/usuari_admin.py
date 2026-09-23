from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Usuari, PerfilBiografic, Experiencia, Estudi, CarrecPublic, Obra
from datetime import datetime
from flask_babel import _
import os
from werkzeug.utils import secure_filename

usuari_admin_bp = Blueprint("usuari_admin", __name__)

def parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except ValueError:
        return None

def clean(val):
    return val.strip() if isinstance(val, str) and val.strip() != "" else None

def to_bool(val):
    return str(val).lower() in ("on", "true", "1", "si", "sí")

@usuari_admin_bp.route("/admin_usuari", methods=["GET", "POST"])
def usuari_admin():
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get_or_404(usuari_id)
    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()
    if not perfil:
        perfil = PerfilBiografic(usuari_id=usuari.id)
        db.session.add(perfil)
        db.session.flush()

    if request.method == "POST":
        bloc = request.form.get("bloc")

        usuari.email = clean(request.form.get("direccion_email") or request.form.get("email")) or usuari.email
        usuari.idioma = clean(request.form.get("idioma")) or usuari.idioma
        usuari.pais_residencia = clean(request.form.get("pais_residencia")) or usuari.pais_residencia
        
        print("📌 Abans de guardar — rebre_missatges:", request.form.get("rebre_missatges"))
        print("📌 Abans de guardar — valor real:", usuari.rebre_missatges)
        usuari.rebre_missatges = request.form.get("rebre_missatges") == "on"


        perfil.professio = clean(request.form.get("professio")) or perfil.professio
        perfil.frase_destacada = clean(request.form.get("frase_destacada")) or perfil.frase_destacada

        perfil.mostrar_experiencia = to_bool(request.form.get("mostrar_experiencia"))
        perfil.mostrar_estudis = to_bool(request.form.get("mostrar_estudis"))
        perfil.mostrar_obres = to_bool(request.form.get("mostrar_obres"))
        perfil.mostrar_carrecs = to_bool(request.form.get("mostrar_carrecs"))
        perfil.mostrar_pare = to_bool(request.form.get("mostrar_pare"))
        perfil.mostrar_mare = to_bool(request.form.get("mostrar_mare"))
        perfil.mostrar_biografia = to_bool(request.form.get("mostrar_biografia"))

        if bloc == "pare_update":
            perfil.pare_nom = clean(request.form.get("pare_nom")) or perfil.pare_nom
            perfil.pare_primer_cognom = clean(request.form.get("pare_primer_cognom")) or perfil.pare_primer_cognom
            perfil.pare_segon_cognom = clean(request.form.get("pare_segon_cognom")) or perfil.pare_segon_cognom
            perfil.pare_data_naixement = parse_date(request.form.get("pare_data_naixement"))
            perfil.pare_pais_naixement = clean(request.form.get("pare_pais_naixement")) or perfil.pare_pais_naixement
            perfil.pare_regio_naixement = clean(request.form.get("pare_regio_naixement")) or perfil.pare_regio_naixement
            perfil.pare_municipi_naixement = clean(request.form.get("pare_municipi_naixement")) or perfil.pare_municipi_naixement
            perfil.pare_data_defuncio = parse_date(request.form.get("pare_data_defuncio"))
            perfil.pare_municipi_defuncio = clean(request.form.get("pare_municipi_defuncio")) or perfil.pare_municipi_defuncio
            perfil.pare_regio_defuncio = clean(request.form.get("pare_regio_defuncio")) or perfil.pare_regio_defuncio
            perfil.pare_pais_defuncio = clean(request.form.get("pare_pais_defuncio")) or perfil.pare_pais_defuncio

        elif bloc == "mare_update":
            perfil.mare_nom = clean(request.form.get("mare_nom")) or perfil.mare_nom
            perfil.mare_primer_cognom = clean(request.form.get("mare_primer_cognom")) or perfil.mare_primer_cognom
            perfil.mare_segon_cognom = clean(request.form.get("mare_segon_cognom")) or perfil.mare_segon_cognom
            perfil.mare_data_naixement = parse_date(request.form.get("mare_data_naixement"))
            perfil.mare_pais_naixement = clean(request.form.get("mare_pais_naixement")) or perfil.mare_pais_naixement
            perfil.mare_regio_naixement = clean(request.form.get("mare_regio_naixement")) or perfil.mare_regio_naixement
            perfil.mare_municipi_naixement = clean(request.form.get("mare_municipi_naixement")) or perfil.mare_municipi_naixement
            perfil.mare_data_defuncio = parse_date(request.form.get("mare_data_defuncio"))
            perfil.mare_municipi_defuncio = clean(request.form.get("mare_municipi_defuncio")) or perfil.mare_municipi_defuncio
            perfil.mare_regio_defuncio = clean(request.form.get("mare_regio_defuncio")) or perfil.mare_regio_defuncio
            perfil.mare_pais_defuncio = clean(request.form.get("mare_pais_defuncio")) or perfil.mare_pais_defuncio
        
        
        db.session.commit()
        flash(_("Canvis desats correctament"))
        return redirect(url_for("usuari_admin.usuari_admin"))

    documents = []  # Omple si cal
    url_personal = url_for("pagina_personal.pagina_personal")


    boto_retorna_perfil = True

    return render_template("usuari_admin.html", usuari=usuari, perfil=perfil, documents=documents, url_personal=url_personal, boto_retorna_perfil=boto_retorna_perfil)

@usuari_admin_bp.route("/eliminar_compte", methods=["POST"], endpoint="eliminar_compte")
def eliminar_compte():
    from flask import session
    uid = session.get("usuari_id")
    if not uid:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get_or_404(uid)

    db.session.delete(usuari)
    db.session.commit()
    session.clear()
    flash(_("El teu compte s'ha eliminat definitivament."))
    return redirect(url_for("inici.inici_pagina"))

def _int_or_none(v):
    try:
        return int(v) if v not in (None, "",) else None
    except ValueError:
        return None

def _bool(v):
    return str(v).lower() in ("on", "true", "1", "si", "sí")

# ── EXPERIÈNCIES
@usuari_admin_bp.route("/admin_usuari/experiencia/add", methods=["POST"])
def add_experiencia():
    uid = session.get("usuari_id")
    if not uid:
        flash(_("Sessió no vàlida")); return redirect(url_for("login.login"))
    print("📥 add_experiencia cridada amb dades:", request.form.to_dict())


    perfil = PerfilBiografic.query.filter_by(usuari_id=uid).first()
    if not perfil:
        perfil = PerfilBiografic(usuari_id=uid); db.session.add(perfil); db.session.flush()

    e = Experiencia(
        perfil_id=perfil.id,
        carrec=(request.form.get("carrec") or "").strip(),
        organitzacio=(request.form.get("organitzacio") or "").strip() or None,
        ambit=(request.form.get("ambit") or "").strip() or None,
        any_inici=_int_or_none(request.form.get("any_inici")),
        any_fi=_int_or_none(request.form.get("any_fi")),
        actualment=_bool(request.form.get("actualment")),
        descripcio=(request.form.get("descripcio") or "").strip() or None,
    )
    # si actualment, ignorem any_fi
    if e.actualment:
        e.any_fi = None
    # validació simple
    if e.carrec == "":
        flash(_("Cal indicar el càrrec")); return redirect(url_for("usuari_admin.usuari_admin"))
    if e.any_inici and e.any_fi and e.any_fi < e.any_inici:
        flash(_("Any de fi no pot ser anterior a l'any d'inici")); return redirect(url_for("usuari_admin.usuari_admin"))

    # ordre al final
    last = Experiencia.query.filter_by(perfil_id=perfil.id).order_by(Experiencia.ordre.desc()).first()
    e.ordre = (last.ordre + 1) if last and last.ordre is not None else 0

    db.session.add(e); db.session.commit()
    flash(_("Experiència afegida"))
    return redirect(url_for("usuari_admin.usuari_admin"))

@usuari_admin_bp.route("/admin_usuari/experiencia/delete/<int:exp_id>", methods=["POST"])
def delete_experiencia(exp_id):
    uid = session.get("usuari_id")
    if not uid:
        flash(_("Sessió no vàlida")); return redirect(url_for("login.login"))
    e = Experiencia.query.get_or_404(exp_id)
    # opcional: comprovar que pertany a l’usuari:
    perfil = PerfilBiografic.query.filter_by(usuari_id=uid).first()
    if not perfil or e.perfil_id != perfil.id:
        flash(_("No autoritzat")); return redirect(url_for("usuari_admin.usuari_admin"))
    db.session.delete(e); db.session.commit()
    flash(_("Experiència eliminada"))
    return redirect(url_for("usuari_admin.usuari_admin"))

# ── ESTUDIS
@usuari_admin_bp.route("/admin_usuari/estudi/add", methods=["POST"])
def add_estudi():
    uid = session.get("usuari_id")
    if not uid:
        flash(_("Sessió no vàlida")); return redirect(url_for("login.login"))

    perfil = PerfilBiografic.query.filter_by(usuari_id=uid).first()
    if not perfil:
        perfil = PerfilBiografic(usuari_id=uid); db.session.add(perfil); db.session.flush()

    s = Estudi(
        perfil_id=perfil.id,
        titulacio=(request.form.get("titulacio") or "").strip(),
        centre=(request.form.get("centre") or "").strip() or None,
        ciutat=(request.form.get("ciutat") or "").strip() or None,
        pais=(request.form.get("pais") or "").strip() or None,
        any_inici=_int_or_none(request.form.get("any_inici")),
        any_fi=_int_or_none(request.form.get("any_fi")),
        descripcio=(request.form.get("descripcio") or "").strip() or None,
    )
    if s.titulacio == "":
        flash(_("Cal indicar la titulació")); return redirect(url_for("usuari_admin.usuari_admin"))
    if s.any_inici and s.any_fi and s.any_fi < s.any_inici:
        flash(_("Any de fi no pot ser anterior a l'any d'inici")); return redirect(url_for("usuari_admin.usuari_admin"))

    last = Estudi.query.filter_by(perfil_id=perfil.id).order_by(Estudi.ordre.desc()).first()
    s.ordre = (last.ordre + 1) if last and last.ordre is not None else 0

    db.session.add(s); db.session.commit()
    flash(_("Estudi afegit"))
    return redirect(url_for("usuari_admin.usuari_admin"))

@usuari_admin_bp.route("/admin_usuari/estudi/delete/<int:estudi_id>", methods=["POST"])
def delete_estudi(estudi_id):
    uid = session.get("usuari_id")
    if not uid:
        flash(_("Sessió no vàlida")); return redirect(url_for("login.login"))
    s = Estudi.query.get_or_404(estudi_id)
    perfil = PerfilBiografic.query.filter_by(usuari_id=uid).first()
    if not perfil or s.perfil_id != perfil.id:
        flash(_("No autoritzat")); return redirect(url_for("usuari_admin.usuari_admin"))
    db.session.delete(s); db.session.commit()
    flash(_("Estudi eliminat"))
    return redirect(url_for("usuari_admin.usuari_admin"))


@usuari_admin_bp.route("/admin/afegir_carrec_public", methods=["POST"])
def add_carrec_public():
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari_id).first()
    if not perfil:
        flash(_("No s'ha trobat el perfil biogràfic."))
        return redirect(url_for("pagina_personal.pagina_personal", pestanya="perfil"))

    titol = request.form.get("titol", "").strip()
    any_inici = request.form.get("any_inici") or None
    any_fi = request.form.get("any_fi") or None

    if not titol:
        flash(_("El títol és obligatori."))
        return redirect(url_for("usuari_admin.usuari_admin"))

    carrec = CarrecPublic(
        perfil_id=perfil.id,
        titol=titol,
        any_inici=int(any_inici) if any_inici else None,
        any_fi=int(any_fi) if any_fi else None,
        municipi=request.form.get("municipi", "").strip() or None,
        regio=request.form.get("regio", "").strip() or None,
        pais=request.form.get("pais", "").strip() or None,
    )

    db.session.add(carrec)
    db.session.commit()
    flash(_("Càrrec afegit correctament."))
    return redirect(url_for("usuari_admin.usuari_admin"))

@usuari_admin_bp.route("/admin/eliminar_carrec_public/<int:carrec_id>", methods=["POST"])
def delete_carrec_public(carrec_id):
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    carrec = CarrecPublic.query.get_or_404(carrec_id)
    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari_id).first()
    if not perfil or carrec.perfil_id != perfil.id:
        flash(_("No tens permís per eliminar aquest càrrec."))
        return redirect(url_for("usuari_admin.usuari_admin"))

    db.session.delete(carrec)
    db.session.commit()
    flash(_("Càrrec eliminat."))
    return redirect(url_for("usuari_admin.usuari_admin"))

    
ALLOWED = {"pdf","png","jpg","jpeg","webp","gif","tiff"}

def _word_count(txt: str) -> int:
    return len([w for w in (txt or "").strip().split() if w])

@usuari_admin_bp.route("/puja_obra", methods=["POST"])
def puja_obra():
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida")); 
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get_or_404(usuari_id)
    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()
    if not perfil:
        perfil = PerfilBiografic(usuari_id=usuari.id)
        db.session.add(perfil)
        db.session.flush()

    any_obra = (request.form.get("any_obra") or "").strip()
    titol = (request.form.get("titol_obra") or "").strip()
    descripcio = (request.form.get("descripcio_obra") or "").strip()
    fitxers = request.files.getlist("fitxers_obra")

    # Validacions bàsiques
    if not titol:
        flash(_("El títol és obligatori.")); 
        return redirect(url_for("usuari_admin.usuari_admin"))
    if _word_count(descripcio) > 200:
        flash(_("La descripció no pot superar 200 paraules.")); 
        return redirect(url_for("usuari_admin.usuari_admin"))
    if not (any_obra.isdigit() and 1800 <= int(any_obra) <= 2100):
        flash(_("Indica un any vàlid (1800–2100).")); 
        return redirect(url_for("usuari_admin.usuari_admin"))
    if not fitxers or all(not f.filename for f in fitxers):
        flash(_("Afegeix almenys un fitxer (PDF o imatge).")); 
        return redirect(url_for("usuari_admin.usuari_admin"))

    # Carpeta destí
    ara = datetime.now()
    pais = (usuari.pais_residencia or "altres").lower()
    carpeta = os.path.join("umberto","usuaris",pais,str(ara.year),f"{ara.month:02}",usuari.nom_login,"obra")
    os.makedirs(carpeta, exist_ok=True)

    pujats = 0; rebutjats = 0
    for f in fitxers:
        if not f or not f.filename:
            continue
        ext = f.filename.rsplit(".",1)[-1].lower()
        if ext not in ALLOWED:
            rebutjats += 1
            continue

        nom_final = f"{usuari.nom_login}_{any_obra}_{secure_filename(f.filename)}"
        dest = os.path.join(carpeta, nom_final)
        f.save(dest)

        # Registre a BD
        tipus = "pdf" if ext == "pdf" else "image"
        mida = os.path.getsize(dest)
        ruta_rel = os.path.join(carpeta).replace("\\","/") + "/" + nom_final

        db.session.add(Obra(
            perfil_id=perfil.id,
            any=int(any_obra),
            titol=titol,
            descripcio=descripcio,
            nom_fitxer=nom_final,
            ruta_relativa=ruta_rel,
            ext=ext,
            tipus=tipus,
            mida_bytes=mida,
        ))
        pujats += 1

    db.session.commit()

    if pujats and not rebutjats:
        flash(_("Obra pujada correctament."))
    elif pujats:
        flash(_("%(ok)d pujats, %(ko)d rebutjats (només PDF o imatges).", ok=pujats, ko=rebutjats))
    else:
        flash(_("Cap fitxer pujat."))
    return redirect(url_for("usuari_admin.usuari_admin"))

@usuari_admin_bp.route('/pujar-avatar', methods=['POST'])
@login_required
def pujar_avatar():
    """Pujar avatar de l'usuari"""
    import os
    from werkzeug.utils import secure_filename
    from PIL import Image
    
    try:
        avatar = request.files.get('avatar')
        
        if not avatar:
            return jsonify({'success': False, 'error': 'No s\'ha rebut cap imatge'}), 400
        
        # Validar que és una imatge
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        filename = secure_filename(avatar.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if ext not in allowed_extensions:
            return jsonify({'success': False, 'error': 'Format d\'imatge no vàlid'}), 400
        
        # Nom final: usuari_{id}_avatar.{ext}
        nom_final = f"usuari_{current_user.id}_avatar.{ext}"
        
        # Crear carpeta si no existeix
        carpeta = os.path.join('static', 'avatars')
        os.makedirs(carpeta, exist_ok=True)
        
        # Guardar fitxer temporalment
        ruta_temp = os.path.join(carpeta, nom_final)
        avatar.save(ruta_temp)
        
        # Redimensionar i fer quadrat (200x200)
        try:
            img = Image.open(ruta_temp)
            
            # Fer quadrat (crop al centre)
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2
            img = img.crop((left, top, right, bottom))
            
            # Redimensionar a 200x200
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            img.save(ruta_temp, quality=85, optimize=True)
            
        except Exception as e:
            print(f"Error processant imatge: {e}")
            # Si falla el processament, deixem la imatge original
        
        # Actualitzar BD
        perfil = current_user.perfil
        if not perfil:
            from models import PerfilBiografic
            perfil = PerfilBiografic(usuari_id=current_user.id)
            db.session.add(perfil)
        
        perfil.imatge_perfil = nom_final
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Avatar guardat correctament'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error pujant avatar: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500