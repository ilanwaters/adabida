from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, EntradaBlog, Usuari
from datetime import datetime
from utils.temps import ara_utc
from sqlalchemy import extract, func

blog_bp = Blueprint("blog", __name__)

@blog_bp.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Validar per_page
    if per_page not in [5, 10, 15]:
        per_page = 10
    
    # Paginació amb SQLAlchemy
    entrades_blog = EntradaBlog.query.order_by(
        EntradaBlog.data_creacio.desc()
    ).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    # Mesos disponibles per l'arxiu
    any_ = func.extract('year', EntradaBlog.data_creacio).label("any")
    mes = func.extract('month', EntradaBlog.data_creacio).label("mes")
    mesos_disponibles = (
        db.session.query(any_, mes)
        .group_by(any_, mes)
        .order_by(any_.desc(), mes.desc())
        .all()
    )
    
    return render_template("blog/blog.html", 
                         entrades_blog=entrades_blog,
                         mesos_disponibles=mesos_disponibles,
                         per_page=per_page,
                         datetime=datetime)

@blog_bp.route("/blog/entrada/<int:entrada_id>")
def entrada_completa(entrada_id):
    """Nova ruta per mostrar entrada completa"""
    entrada = EntradaBlog.query.get_or_404(entrada_id)
    return render_template("blog/entrada_completa.html", entrada=entrada)

# Formulari per crear entrada
@blog_bp.route("/crear_entrada_blog", methods=["GET"])
def crear_entrada_blog():
    if "usuari" not in session:
        flash("Cal iniciar sessió")
        return redirect(url_for("login.login"))
    return render_template("blog/crear_entrada_blog.html")

# Desa entrada a la base de dades
@blog_bp.route("/guardar_entrada_blog", methods=["POST"])
def guardar_entrada_blog():
    if "usuari" not in session:
        flash("Cal iniciar sessió")
        return redirect(url_for("login.login"))

    titol = request.form.get("titol")
    contingut = request.form.get("contingut")
    firma = request.form.get("firma")

    usuari = Usuari.query.filter_by(nom_login=session["usuari"]).first()

    nova_entrada = EntradaBlog(
        titol=titol,
        contingut=contingut,
        autor=usuari,
        firma=firma,
        data_creacio=ara_utc()
    )

    db.session.add(nova_entrada)
    db.session.commit()

    flash("Entrada desada correctament")
    return redirect(url_for("admin.pagina_admin"))

# Mostrar totes les entrades del blog
@blog_bp.route("/llista_blog")
def llista_blog():
    entrades = EntradaBlog.query.order_by(EntradaBlog.data_creacio.desc()).all()
    return render_template("llista_blog.html", entrades=entrades)

@blog_bp.route("/cercar_blog", methods=["GET"])
def cercar_blog():
    consulta = request.args.get("q", "")
    if consulta:
        entrades = EntradaBlog.query.filter(
            EntradaBlog.contingut.ilike(f"%{consulta}%")
        ).order_by(EntradaBlog.data_creacio.desc()).all()
    else:
        entrades = []

    return render_template("blog/resultats_cerca_blog.html", entrades=entrades, consulta=consulta)

@blog_bp.route("/arxiu/<int:any>/<int:mes>")
def arxiu_per_mes(any, mes):
    entrades = EntradaBlog.query\
        .filter(extract('year', EntradaBlog.data_creacio) == any)\
        .filter(extract('month', EntradaBlog.data_creacio) == mes)\
        .order_by(EntradaBlog.data_creacio.desc())\
        .all()
    nom_mes = datetime(any, mes, 1).strftime("%B").capitalize()

    return render_template("blog/resultats_cerca_blog.html", entrades=entrades, consulta=f"{nom_mes} {any}")

@blog_bp.route('/gestio_blog')
def gestio_blog():
    entrades = EntradaBlog.query.order_by(EntradaBlog.data_creacio.desc()).all()
    return render_template('admin_blog.html', entrades=entrades)

@blog_bp.route("/editar_entrada_blog/<int:entrada_id>", methods=["GET", "POST"])
def editar_entrada_blog(entrada_id):
    entrada = EntradaBlog.query.get_or_404(entrada_id)

    if request.method == "POST":
        entrada.titol = request.form.get("titol")
        entrada.contingut = request.form.get("contingut")
        entrada.firma = request.form.get("firma")
        db.session.commit()
        flash("Entrada actualitzada correctament")
        return redirect(url_for("blog.gestio_blog"))

    return render_template("blog/crear_entrada_blog.html", entrada=entrada, mode="editar")

@blog_bp.route("/eliminar_entrada_blog/<int:entrada_id>", methods=["POST"])
def eliminar_entrada_blog(entrada_id):
    entrada = EntradaBlog.query.get_or_404(entrada_id)
    db.session.delete(entrada)
    db.session.commit()
    flash("Entrada eliminada correctament")
    return redirect(url_for("blog.gestio_blog"))

@blog_bp.route("/blog/firma/<firma>")
def entrades_per_firma(firma):
    """Llista entrades amb una firma específica"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if per_page not in [5, 10, 15]:
        per_page = 10
    
    entrades_blog = EntradaBlog.query.filter_by(firma=firma).order_by(
        EntradaBlog.data_creacio.desc()
    ).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template("blog/entrades_autor.html", 
                         entrades_blog=entrades_blog,
                         autor_nom=firma,  # Passem la firma com a nom
                         per_page=per_page)