from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
import os
import shutil
from datetime import datetime
from models import db
from models.entrades import ImatgeGaleria, Exposicio
from models.entrades import Entrada, ArxiuEntrada
from PIL import Image, ImageOps

admin_galeria_bp = Blueprint("admin_galeria", __name__)

def generar_miniatura(ruta_original, ruta_miniatura, max_costat=200):
    try:
        img = Image.open(ruta_original).convert("RGB")
        img = ImageOps.exif_transpose(img)

        img.thumbnail((max_costat, max_costat), Image.LANCZOS)

        # Crea un fons quadrat del mateix color que el fons web
        mida_final = (max_costat, max_costat)
        fons = Image.new("RGB", mida_final, (255, 255, 255))

        x = (max_costat - img.width) // 2
        y = (max_costat - img.height) // 2
        fons.paste(img, (x, y))

        os.makedirs(os.path.dirname(ruta_miniatura), exist_ok=True)
        fons.save(ruta_miniatura)

        return True

    except Exception as e:
        print(f"❌ Error generant miniatura: {e}")
        return False

@admin_galeria_bp.route("/admin/galeria", endpoint="gestio_galeria")
def mostrar_anys():
    base_path = os.path.join("umberto", "media", "pendents")

    carpetes = []

    if os.path.exists(base_path):
        for nom in os.listdir(base_path):
            ruta = os.path.join(base_path, nom)
            if os.path.isdir(ruta):
                carpetes.append(nom)

    return render_template("admin/admin_galeria.html", carpetes=carpetes, ruta="")

@admin_galeria_bp.route("/gestio_imatges", defaults={"subpath": ""})
@admin_galeria_bp.route("/gestio_imatges/<path:subpath>")
def navegar_carpetes(subpath):
    base_path = os.path.join("umberto", "media", "pendents")
    ruta_completa = os.path.join(base_path, subpath)

    if not os.path.isdir(ruta_completa):
        flash("Carpeta no trobada.")
        return redirect(url_for("admin_galeria.gestio_galeria"))

    carpetes = []
    imatges = []

    db_imatges = {i.nom_fitxer: i.destinacio for i in ImatgeGaleria.query.all()}

    for nom in os.listdir(ruta_completa):
        ruta_absoluta = os.path.join(ruta_completa, nom)
        if os.path.isdir(ruta_absoluta) and nom == "mini":
            continue

        if os.path.isdir(ruta_absoluta):
            carpetes.append(nom)
            continue

        if not nom.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue

        # Evitem carpeta mini
        if "mini" in subpath.split("/"):
            continue

        # Busquem entrada associada
        entrada_id = None
        from models import ArxiuAdjunt
        arxiu = ArxiuAdjunt.query.filter_by(nom_fitxer=nom).first()
        if arxiu and arxiu.entrada:
            entrada_id = arxiu.entrada.id

        # Miniatura
        ruta_original = os.path.join("umberto", "media", "pendents", subpath, nom)
        ruta_mini = os.path.join("umberto", "media", "pendents", subpath, "mini", nom)

        if not os.path.exists(ruta_mini):
            generar_miniatura(ruta_original, ruta_mini)

        ruta_mini_url = url_for('serveis_media.serveix_media', filepath=f"pendents/{subpath}/mini/{nom}")

        # Busquem exposicions on apareix
        imatge_obj = ImatgeGaleria.query.filter_by(nom_fitxer=nom).first()
        exposicions = []
        if imatge_obj:
            exposicions = [e.ruta_expo for e in imatge_obj.exposicions]

        imatges.append({
            "fitxer": nom,
            "ruta": ruta_mini_url,
            "destinacio": db_imatges.get(nom),
            "entrada_id": entrada_id,
            "exposicions": exposicions
        })
    print("📂 subpath rebut:", subpath)


    return render_template("admin/admin_galeria.html", carpetes=carpetes, imatges=imatges, ruta=subpath, amaga_nav=True )

# 🔹 Marcar com enviada a galeria
@admin_galeria_bp.route("/admin/afegir_a_galeria", methods=["POST"])
def afegir_a_galeria():
    from models import Entrada  # afegim aquí si no està dalt

    fitxer = request.form.get("fitxer")
    carpeta = request.form.get("carpeta")
    mida = request.form.get("mida", "mitjana")
    entrada_id = request.form.get("entrada_id")

    if not fitxer or not carpeta or not entrada_id or not entrada_id.isdigit():
        flash("Falten dades per afegir a galeria (fitxer, carpeta o entrada_id).")
        return redirect(url_for("admin_galeria.navegar_carpetes", subpath=carpeta))

    entrada = Entrada.query.get(entrada_id)
    if not entrada or not entrada.usuari:
        flash("❌ Entrada no trobada o sense usuari. No es pot afegir aquesta imatge.")
        return redirect(url_for("admin_galeria.navegar_carpetes", subpath=carpeta))

    # --- Ruta origen ---
    origen = os.path.join("umberto", "media", "pendents", carpeta, fitxer)

    # --- Crear carpeta de galeria (ANY/MES) ---
    any_actual = datetime.now().strftime("%Y")
    mes_actual = datetime.now().strftime("%m")
    carpeta_galeria = os.path.join("umberto", "media", "galeria", any_actual, mes_actual)
    os.makedirs(carpeta_galeria, exist_ok=True)

    desti_galeria = os.path.join(carpeta_galeria, fitxer)

    # --- Copiar fitxer ---
    try:
        shutil.copy2(origen, desti_galeria)
    except Exception as e:
        flash(f"❌ Error en copiar a galeria: {e}")
        return redirect(url_for("admin_galeria.navegar_carpetes", subpath=carpeta))

    # --- Registrar a base de dades ---
    imatge = ImatgeGaleria.query.filter_by(nom_fitxer=fitxer).first()
    if not imatge:
        imatge = ImatgeGaleria(nom_fitxer=fitxer)
        db.session.add(imatge)

    imatge.mida = mida
    imatge.destinacio = "galeria"
    imatge.data_publicacio = datetime.utcnow()
    imatge.entrada_id = entrada.id
    db.session.commit()

    flash(f"📷 Imatge enviada a galeria correctament: {fitxer}")
    return redirect(url_for("admin_galeria.navegar_carpetes", subpath=carpeta))

# 🔹 Marcar com obviada
@admin_galeria_bp.route("/obviar_imatge", methods=["POST"])
def obviar_imatge():
    fitxer = request.form.get("fitxer")
    carpeta = request.form.get("carpeta")

    if not fitxer or not carpeta:
        flash("Falten dades per obviar la imatge.")
        return redirect(url_for("admin_galeria.navegar_carpetes", subpath=carpeta))

    imatge = ImatgeGaleria.query.filter_by(nom_fitxer=fitxer).first()
    if not imatge:
        imatge = ImatgeGaleria(nom_fitxer=fitxer)
        db.session.add(imatge)

    # 🟥 Marquem com obviada
    imatge.destinacio = "obviada"
    db.session.commit()

    # 🧹 Eliminem de INICI i GALERIA si existeix
    ruta_inici = os.path.join("umberto", "media", "inici", fitxer)
    if os.path.exists(ruta_inici):
        os.remove(ruta_inici)

    if imatge.data_publicacio:
        any_mes = imatge.data_publicacio.strftime('%Y/%m')
        ruta_galeria = os.path.join("umberto", "media", "galeria", any_mes, fitxer)
        if os.path.exists(ruta_galeria):
            os.remove(ruta_galeria)

    flash(f"🚫 Imatge marcada com obviada i eliminada de la visualització: {fitxer}")
    return redirect(url_for("admin_galeria.navegar_carpetes", subpath=carpeta))

@admin_galeria_bp.route("/assignar_expo_galeria", methods=["POST"])
def assignar_exposicio():

    from models import ImatgeExposicio

    fitxer = request.form.get("fitxer")
    ruta_expo = request.form.get("ruta_expo")  # format: spain/2025/07/01-codi
    if not fitxer or not ruta_expo:
        flash("Falten dades per assignar la imatge a l'exposició.")
        return redirect(request.referrer or url_for("admin_galeria.gestio_galeria"))

    origen = os.path.join("umberto", "media", "pendents")
    desti = os.path.join("umberto", "media", "expo", ruta_expo)
    os.makedirs(desti, exist_ok=True)

    origen_fitxer = None
    for root, _, files in os.walk(origen):
        if fitxer in files:
            origen_fitxer = os.path.join(root, fitxer)
            break

    if not origen_fitxer or not os.path.isfile(origen_fitxer):
        flash("No s'ha trobat el fitxer original.")
        return redirect(request.referrer or url_for("admin_galeria.gestio_galeria"))

    try:
        shutil.copy2(origen_fitxer, os.path.join(desti, fitxer))
    except Exception as e:
        flash(f"Error copiant la imatge a l'exposició: {e}")
        return redirect(request.referrer or url_for("admin_galeria.gestio_galeria"))

    # Registrem a la base de dades
    imatge_obj = ImatgeGaleria.query.filter_by(nom_fitxer=fitxer).first()

    if not imatge_obj:
        from models import Entrada, ArxiuEntrada

        # Busquem si aquest fitxer està vinculat a alguna entrada
        entrada = Entrada.query \
            .join(ArxiuEntrada, Entrada.id == ArxiuEntrada.entrada_id) \
            .filter(ArxiuEntrada.nom_fitxer == fitxer) \
            .first()

        imatge_obj = ImatgeGaleria(
            nom_fitxer=fitxer,
            entrada_id=entrada.id if entrada else None,
            usuari_id=entrada.usuari_id if entrada else None,
            mida="mitjana",
            descripcio="",
            destinacio="exposicio"
        )
        db.session.add(imatge_obj)
        db.session.commit()

    if imatge_obj:
        ja_assignada = ImatgeExposicio.query.filter_by(
            imatge_id=imatge_obj.id, ruta_expo=ruta_expo).first()
        if not ja_assignada:
            nova_relacio = ImatgeExposicio(imatge_id=imatge_obj.id, ruta_expo=ruta_expo)
            db.session.add(nova_relacio)
            db.session.commit()

    flash("Imatge assignada correctament a l'exposició.")
    return redirect(request.referrer or url_for("admin_galeria.gestio_galeria"))

from flask import jsonify

@admin_galeria_bp.route("/api/exposicions/rutes")
def exposicions_rutes():
    base = os.path.join("umberto", "media", "expo")
    rutes = []

    for root, dirs, files in os.walk(base):
        for d in dirs:
            ruta_relativa = os.path.relpath(os.path.join(root, d), base)
            rutes.append(ruta_relativa.replace("\\", "/"))  # compatibilitat Windows

    rutes_ordenades = sorted(rutes)
    return jsonify(success=True, rutes=rutes_ordenades)

@admin_galeria_bp.route("/api/exposicions/arbre")
def exposicions_arbre():
    base = os.path.join("umberto","media", "expo")
    arbre = {}

    for root, dirs, files in os.walk(base):
        rel = os.path.relpath(root, base).replace("\\", "/")
        parts = rel.split("/")

        if len(parts) == 4:  # Ex: spain/2025/07/01-202507machado
            pais, any_, mes, expo = parts
            arbre.setdefault(pais, {}).setdefault(any_, {}).setdefault(mes, []).append(expo)

    return jsonify(success=True, arbre=arbre)

@admin_galeria_bp.route("/admin/exposicions/eliminar/<int:id>", methods=["POST"])
def elimina_exposicio(id):
    exposicio = Exposicio.query.get_or_404(id)

    # Opcional: eliminar carpeta física associada
    ruta = os.path.join("umberto", "media", exposicio.carpeta)
    if os.path.exists(ruta):
        import shutil
        shutil.rmtree(ruta)

    db.session.delete(exposicio)
    db.session.commit()

    return redirect(url_for("admin.admin_exposicions"))


