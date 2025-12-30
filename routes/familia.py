from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from flask_babel import _
from models import db, Usuari, PerfilBiografic, Contacte
from flask_login import current_user

familia_bp = Blueprint("familia", __name__)

@familia_bp.route("/familia")
def familia_inici():
    """Pàgina principal de família amb tiles de navegació"""
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get(usuari_id)
    if not usuari:
        flash(_("Usuari inexistent"))
        return redirect(url_for("login.login"))

    return render_template('familia/familia_inici.html', usuari=usuari)

@familia_bp.route("/familia/arbre")
def arbre_genealogic():
    """Visualització de l'arbre genealògic"""
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get(usuari_id)
    if not usuari:
        flash(_("Usuari inexistent"))
        return redirect(url_for("login.login"))

    # Carregar dades familiars del perfil
    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()
    
    # Carregar contactes marcats com a família
    contactes_familia = []
    if perfil:
        contactes_familia = Contacte.query.filter_by(
            perfil_id=perfil.id,
            tipus='familia'
        ).all()

    return render_template('familia/arbre_genealogic.html', 
                          usuari=usuari, 
                          perfil=perfil,
                          contactes_familia=contactes_familia)

@familia_bp.route("/familia/contactes")
def contactes_familia():
    """Gestió de contactes familiars"""
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get(usuari_id)
    if not usuari:
        flash(_("Usuari inexistent"))
        return redirect(url_for("login.login"))

    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()
    
    contactes = []
    if perfil:
        contactes = Contacte.query.filter_by(perfil_id=perfil.id).all()

    return render_template('familia/contactes_familia.html', 
                          usuari=usuari, 
                          perfil=perfil,
                          contactes=contactes)

@familia_bp.route("/familia/afegir_contacte", methods=["GET", "POST"])
def afegir_contacte():
    """Afegir nou contacte familiar"""
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    usuari = Usuari.query.get(usuari_id)
    if not usuari:
        flash(_("Usuari inexistent"))
        return redirect(url_for("login.login"))

    if request.method == "POST":
        perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()
        if not perfil:
            flash(_("Cal tenir un perfil biogràfic per afegir contactes"))
            return redirect(url_for("pagina_personal.perfil"))

        # Crear nou contacte
        nou_contacte = Contacte(
            perfil_id=perfil.id,
            nom=request.form.get('nom'),
            cognoms=request.form.get('cognoms'),
            relacio=request.form.get('relacio'),
            telefon=request.form.get('telefon'),
            email=request.form.get('email'),
            tipus='familia'
        )
        
        db.session.add(nou_contacte)
        db.session.commit()
        
        flash(_("Contacte familiar afegit correctament"))
        return redirect(url_for("familia.contactes_familia"))

    return render_template('familia/afegir_contacte.html', usuari=usuari)

@familia_bp.route("/familia/editar_contacte/<int:contacte_id>", methods=["GET", "POST"])
def editar_contacte(contacte_id):
    """Editar contacte familiar existent"""
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        flash(_("Sessió no vàlida"))
        return redirect(url_for("login.login"))

    contacte = Contacte.query.get_or_404(contacte_id)
    
    # Verificar que el contacte pertany a l'usuari actual
    if contacte.perfil.usuari_id != usuari_id:
        flash(_("No tens permisos per editar aquest contacte"))
        return redirect(url_for("familia.contactes_familia"))

    if request.method == "POST":
        contacte.nom = request.form.get('nom')
        contacte.cognoms = request.form.get('cognoms')
        contacte.relacio = request.form.get('relacio')
        contacte.telefon = request.form.get('telefon')
        contacte.email = request.form.get('email')
        
        db.session.commit()
        flash(_("Contacte actualitzat correctament"))
        return redirect(url_for("familia.contactes_familia"))

    usuari = Usuari.query.get(usuari_id)
    return render_template('familia/editar_contacte.html', 
                          usuari=usuari, 
                          contacte=contacte)

@familia_bp.route("/familia/eliminar_contacte/<int:contacte_id>", methods=["POST"])
def eliminar_contacte(contacte_id):
    """Eliminar contacte familiar"""
    usuari_id = session.get("usuari_id")
    if not usuari_id:
        return jsonify({"error": "Sessió no vàlida"}), 401

    contacte = Contacte.query.get_or_404(contacte_id)
    
    # Verificar permisos
    if contacte.perfil.usuari_id != usuari_id:
        return jsonify({"error": "Sense permisos"}), 403

    db.session.delete(contacte)
    db.session.commit()
    
    return jsonify({"success": True})