# routes/repositori.py

from flask import Blueprint, render_template, request, url_for
from models import Entrada, Usuari, Pais, Regio, Municipi
from sqlalchemy import or_, and_
from utils import generar_miniatura_entrada
import re

repositori_bp = Blueprint("repositori", __name__)

@repositori_bp.route("/repositori", methods=["GET"])
def consulta_repositori():
    nom = request.args.get("nom", "").strip()
    tema = request.args.get("tema", "").strip()
    ciutat = request.args.get("ciutat", "").strip()
    any_inici = request.args.get("any_inici")
    any_fi = request.args.get("any_fi")
    text = request.args.get("text", "").strip()
    strict = request.args.get("strict")  # 'on' si marcat
    nom_usuari = request.args.get("usuari", "").strip()
    pais = request.args.get("pais", "").strip()
    validat = request.args.get("validat")  # 'on' si marcat

    condicions = []

    if nom:
        condicions.append(Entrada.titol.ilike(f"%{nom}%"))

    if tema:
        condicions.append(Entrada.tema.ilike(f"%{tema}%"))

    if ciutat:
        condicions.append(Entrada.ubicacio.ilike(f"%{ciutat}%"))

    if any_inici and any_fi:
        condicions.append(Entrada.any_text.between(any_inici, any_fi))

    if text:
        condicions.append(or_(
            Entrada.titol.ilike(f"%{text}%"),
            Entrada.tema.ilike(f"%{text}%"),
            Entrada.contingut.ilike(f"%{text}%")
        ))

    if nom_usuari:
        subquery = Usuari.query.filter(Usuari.nom_login.ilike(f"%{nom_usuari}%")).with_entities(Usuari.id)
        condicions.append(Entrada.usuari_id.in_(subquery))

    if pais:
        condicions.append(Entrada.pais.ilike(f"%{pais}%"))

    if validat:
        condicions.append(Entrada.validada == True)

    cerca_realitzada = bool(condicions)

    if cerca_realitzada:
        page = request.args.get("page", 1, type=int)
        per_page = 10

        query_base = Entrada.query

        if strict:
            query = query_base.filter(and_(*condicions))
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            entrades_raw = pagination.items

            if not entrades_raw:
                query_flexible = query_base.filter(or_(*condicions))
                pagination = query_flexible.paginate(page=page, per_page=per_page, error_out=False)
                entrades_raw = pagination.items
                resultats_parcials = True
            else:
                resultats_parcials = False
        else:
            query = query_base.filter(or_(*condicions))
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            entrades_raw = pagination.items
            resultats_parcials = False
    else:
        pagination = None
        entrades_raw = []
        resultats_parcials = False

    # Convertir entrades a diccionaris (igual que a pagina_personal)
    entrades = []
    for entrada in entrades_raw:
        usuari = Usuari.query.get(entrada.usuari_id)
        miniatura = generar_miniatura_entrada(entrada, usuari.nom_login)
        
        # Construir lloc amb noms reals
        parts_lloc = []
        
        if entrada.municipi:
            try:
                if entrada.municipi.isdigit():
                    mun = Municipi.query.get(int(entrada.municipi))
                    parts_lloc.append(mun.nom if mun else entrada.municipi)
                else:
                    parts_lloc.append(entrada.municipi)
            except:
                parts_lloc.append(entrada.municipi)
        
        if entrada.regio:
            try:
                if entrada.regio.isdigit():
                    reg = Regio.query.get(int(entrada.regio))
                    parts_lloc.append(reg.nom if reg else entrada.regio)
                else:
                    parts_lloc.append(entrada.regio)
            except:
                parts_lloc.append(entrada.regio)
        
        if entrada.pais:
            try:
                if entrada.pais.isdigit():
                    pai = Pais.query.get(int(entrada.pais))
                    parts_lloc.append(pai.nom if pai else entrada.pais)
                else:
                    parts_lloc.append(entrada.pais)
            except:
                parts_lloc.append(entrada.pais)
        
        lloc = ", ".join(parts_lloc) if parts_lloc else None
        
        # Netejar HTML del contingut
        resum = ""
        if entrada.contingut:
            contingut_net = re.sub(r'<[^>]+>', '', entrada.contingut)
            contingut_net = contingut_net.replace('&nbsp;', ' ').replace('&amp;', '&')
            resum = contingut_net[:120] + "..." if len(contingut_net) > 120 else contingut_net
        
        entrades.append({
            "id": entrada.id,
            "titol": entrada.titol,
            "tema": entrada.tema,
            "any": entrada.any_text,
            "lloc": lloc,
            "resum": resum,
            "data": entrada.data_creacio.strftime("%d/%m/%Y") if entrada.data_creacio else "",
            "miniatura": miniatura,
            "usuari": usuari,  # Objecte usuari complet
            "usuari_id": entrada.usuari_id
        })

    args_copia = request.args.to_dict()
    args_copia.pop('page', None)

    return render_template(
        "repositori.html",
        entrades=entrades,
        pagination=pagination,
        cerca=cerca_realitzada,
        args_copia=args_copia,
        resultats_parcials=resultats_parcials
    )

@repositori_bp.route("/mostra_entrada/<int:entrada_id>")
def mostra_entrada(entrada_id):
    entrada = Entrada.query.get_or_404(entrada_id)
    usuari = Usuari.query.get_or_404(entrada.usuari_id)
    return render_template("mostra_entrada.html", entrada=entrada, usuari=usuari)

@repositori_bp.route('/entrada/<int:entrada_id>')
def entrada_publica(entrada_id):
    entrada = Entrada.query.get_or_404(entrada_id)
    return render_template('entrada_publica.html', entrada=entrada)