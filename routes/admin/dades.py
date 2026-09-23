
from flask import Blueprint, jsonify, render_template 
from models import db
from models.usuari import Usuari, PerfilBiografic
from models.entrades import Entrada
admin_dades_bp = Blueprint("admin_dades_bp", __name__)

@admin_dades_bp.route("/api/admin/dades/usuaris")
def dades_usuaris():
    usuaris = Usuari.query.all()
    resultat = []
    for u in usuaris:
        resultat.append({
            "id": u.id,
            "nom_login": u.nom_login,
            "email": u.email,
            "rol": u.rol,
            "nom": u.nom,
            "primer_cognom": u.primer_cognom,
            "segon_cognom": u.segon_cognom or "",  # 👈 canvi aquí
            "pais_residencia": u.pais_residencia,
        })
    return jsonify(resultat)


@admin_dades_bp.route("/admin_dades")
def mostra_admin_dades():
    return render_template("admin/admin_dades.html")


@admin_dades_bp.route("/api/admin/dades/perfils")
def dades_perfils():
    perfils = PerfilBiografic.query.all()
    resultat = []
    for p in perfils:
        resultat.append({
            "id": p.id,
            "usuari_id": p.usuari_id,
            "codi_identificacio": p.codi_identificacio,
            "nom": p.nom,
            "primer_cognom": p.primer_cognom,
            "segon_cognom": p.segon_cognom,
            "professio": p.professio,
            "frase_destacada": p.frase_destacada,
            "pais_naixement": p.pais_naixement,
            "regio_naixement": p.regio_naixement,
            "municipi_naixement": p.municipi_naixement,
            "data_naixement": p.data_naixement,
            "pare_pais_naixement": p.pare_pais_naixement,
            "pare_regio_naixement": p.pare_regio_naixement,
            "pare_municipi_naixement": p.pare_municipi_naixement,
            "mare_pais_naixement": p.mare_pais_naixement,
            "mare_regio_naixement": p.mare_regio_naixement,
            "mare_municipi_naixement": p.mare_municipi_naixement,
            "mostrar_biografia": p.mostrar_biografia,
            "mostrar_contacte": p.mostrar_contacte,
            "mostrar_data_naixement": p.mostrar_data_naixement,
            "mostrar_ubicacio": p.mostrar_ubicacio,
            "mostrar_origen_familiar": p.mostrar_origen_familiar,
        })

    return jsonify(resultat)

@admin_dades_bp.route("/api/admin/dades/entrades")
def dades_entrades():
    from models import Entrada  
    entrades = Entrada.query.all()
    resultat = []

    for e in entrades:
        item = {
            "id": getattr(e, "id", None),
            "titol": getattr(e, "titol", ""),
            "tema": getattr(e, "tema", ""),
            "text": getattr(e, "text", ""),
            "ubicacio": getattr(e, "ubicacio", ""),
            "any": getattr(e, "any", ""),
            "nom_fitxer": getattr(e, "nom_fitxer", ""),
            "color": getattr(e, "color", ""),
            "data_creacio": e.data_creacio.strftime("%Y-%m-%d %H:%M") if getattr(e, "data_creacio", None) else "",
        }

        for fk in ("perfil_id", "perfil_biografic_id", "usuari_id", "autor_id"):
            if hasattr(e, fk):
                item[fk] = getattr(e, fk)
                break

        resultat.append(item)

    return jsonify(resultat)

