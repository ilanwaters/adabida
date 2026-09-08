# routes/repositori.py

from flask import Blueprint, render_template, request, url_for, abort
from models import Entrada, Usuari, Pais, Regio, Municipi, Conversa, UbicacioOrigenFamilia
from sqlalchemy import or_, and_, func
from utils import generar_miniatura_entrada
import re
from datetime import datetime

repositori_bp = Blueprint("repositori", __name__)


def preparar_conversa_per_vista(conversa, usuari_nom_login):
    """Converteix una Conversa en format dict per renderitzar com caixa"""
    # Obtenir nom del participant principal
    participant_nom = "Desconegut"
    if conversa.participants:
        primer = conversa.participants[0]
        participant_nom = f"{primer.nom} {primer.primer_cognom or ''} {primer.segon_cognom or ''}".strip()
    
    # Construir lloc
    parts_lloc = [conversa.lloc_municipi, conversa.lloc_regio, conversa.lloc_pais]
    lloc = ", ".join([p for p in parts_lloc if p]) or None
    
    # Extreure any
    any = conversa.data_conversa.year if conversa.data_conversa else None
    
    # Resum del contingut
    resum = ""
    if conversa.contingut:
        contingut_net = re.sub(r'<[^>]+>', '', conversa.contingut)
        contingut_net = contingut_net.replace('&nbsp;', ' ').replace('&amp;', '&')
        resum = contingut_net[:120] + "..." if len(contingut_net) > 120 else contingut_net
    
    return {
        "id": conversa.id,
        "tipus": "conversa",
        "usuari_id": conversa.usuari_id,
        "entrada_id": conversa.entrada_id,
        "participant_nom": participant_nom,
        "tema": conversa.tema,
        "any": any,
        "lloc": lloc,
        "durada_minuts": conversa.durada_minuts,
        "resum": resum,
        "data": conversa.data_conversa.strftime("%d/%m/%Y") if conversa.data_conversa else conversa.created_at.strftime("%d/%m/%Y"),
        "data_ordenacio": conversa.data_conversa or conversa.created_at,
        "miniatura": Entrada.query.get(conversa.entrada_id).miniatura if conversa.entrada_id else "/static/icons/entrevista.svg",
        "usuari": conversa.usuari
    }
def preparar_familia_per_vista(familia):
    """Converteix un EspaiFamiliar en format dict per renderitzar com a targeta"""
    lloc = None
    origen = familia.ubicacions_origen[0] if familia.ubicacions_origen else None
    if origen:
        parts_lloc = [origen.municipi, origen.regio, origen.pais]
        lloc = ", ".join([p for p in parts_lloc if p]) or None

    resum = ""
    if familia.descripcio:
        contingut_net = re.sub(r'<[^>]+>', '', familia.descripcio)
        resum = contingut_net[:120] + "..." if len(contingut_net) > 120 else contingut_net

    return {
        "id": familia.id,
        "tipus": "familia",
        "nom": familia.nom,
        "motiu": familia.motiu,
        "lloc": lloc,
        "resum": resum,
        "nombre_membres": familia.nombre_membres,
        "data": familia.data_creacio.strftime("%d/%m/%Y") if familia.data_creacio else "",
        "data_ordenacio": familia.data_creacio,
        "miniatura": familia.imatge_card_home or "/static/icons/familia.svg",
        "url": familia.url
    }

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
        condicions.append(Entrada.municipi.ilike(f"%{ciutat}%"))

    if any_inici and any_fi:
        condicions.append(Entrada.any_text.between(any_inici, any_fi))
    elif any_inici:
        condicions.append(Entrada.any_text >= any_inici)
    elif any_fi:
        condicions.append(Entrada.any_text <= any_fi)
        
    if text:
        nom_complet_usuari = func.concat(
            func.coalesce(Usuari.nom, ''), ' ',
            func.coalesce(Usuari.primer_cognom, ''), ' ',
            func.coalesce(Usuari.segon_cognom, '')
        )
        subquery_usuaris_text = Usuari.query.filter(or_(
            nom_complet_usuari.ilike(f"%{text}%"),
            Usuari.nom_login.ilike(f"%{text}%")
        )).with_entities(Usuari.id)
        condicions.append(or_(
            Entrada.titol.ilike(f"%{text}%"),
            Entrada.tema.ilike(f"%{text}%"),
            Entrada.contingut.ilike(f"%{text}%"),
            Entrada.any_text.ilike(f"%{text}%"),
            Entrada.titol_imatge.ilike(f"%{text}%"),
            Entrada.descripcio_imatge.ilike(f"%{text}%"),
            Entrada.referencia.ilike(f"%{text}%"),
            Entrada.usuari_id.in_(subquery_usuaris_text)
        ))

    if nom_usuari:
        subquery = Usuari.query.filter(Usuari.nom_login.ilike(f"%{nom_usuari}%")).with_entities(Usuari.id)
        condicions.append(Entrada.usuari_id.in_(subquery))

    if pais:
        condicions.append(Entrada.pais.ilike(f"%{pais}%"))

    if validat:
        subquery_validats = Usuari.query.filter(Usuari.nivell_usuari == 'verd').with_entities(Usuari.id)
        condicions.append(Entrada.usuari_id.in_(subquery_validats))

    cerca_realitzada = bool(condicions)

    if cerca_realitzada:
        page = request.args.get("page", 1, type=int)
        per_page = 10

        entrada_ids_amb_conversa = [c.entrada_id for c in Conversa.query.filter(Conversa.entrada_id.isnot(None), Conversa.tipus_conversa == 'entrevista_adabida').all()]
        query_base = Entrada.query.filter(~Entrada.id.in_(entrada_ids_amb_conversa), Entrada.es_publica == True)

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
    # Obtenir converses (sense filtres de moment, TODO: afegir filtres)
    if cerca_realitzada:
        condicions_conversa = []

        if nom:
            condicions_conversa.append(Conversa.titol.ilike(f"%{nom}%"))

        if tema:
            condicions_conversa.append(Conversa.tema.ilike(f"%{tema}%"))

        if ciutat:
            condicions_conversa.append(Conversa.lloc_municipi.ilike(f"%{ciutat}%"))

        if text:
            from models import ConversaParticipant
          

            nom_complet_participant = func.concat(
                func.coalesce(ConversaParticipant.nom, ''), ' ',
                func.coalesce(ConversaParticipant.primer_cognom, ''), ' ',
                func.coalesce(ConversaParticipant.segon_cognom, '')
            )
            subquery_participants = ConversaParticipant.query.filter(
                nom_complet_participant.ilike(f"%{text}%")
            ).with_entities(ConversaParticipant.conversa_id)

            condicions_conversa.append(or_(
                Conversa.titol.ilike(f"%{text}%"),
                Conversa.tema.ilike(f"%{text}%"),
                Conversa.contingut.ilike(f"%{text}%"),
                Conversa.id.in_(subquery_participants)
            ))

        if nom_usuari:
            subquery_conv = Usuari.query.filter(Usuari.nom_login.ilike(f"%{nom_usuari}%")).with_entities(Usuari.id)
            condicions_conversa.append(Conversa.usuari_id.in_(subquery_conv))

        if pais:
            condicions_conversa.append(Conversa.lloc_pais.ilike(f"%{pais}%"))

        if validat:
            condicions_conversa.append(Conversa.usuari_id.in_(subquery_validats))

        if condicions_conversa:
            base_conv = Conversa.query.join(Entrada, Conversa.entrada_id == Entrada.id).filter(Entrada.es_publica == True, Conversa.tipus_conversa == 'entrevista_adabida')
            if strict:
                converses_raw = base_conv.filter(and_(*condicions_conversa)).limit(per_page).all()
            else:
                converses_raw = base_conv.filter(or_(*condicions_conversa)).limit(per_page).all()
        else:
            converses_raw = []
    else:
        converses_raw = []

    # Obtenir famílies (visibles públicament)
    if cerca_realitzada:
        from models import EspaiFamiliar, MembreFamilia

        condicions_familia = []

        if text:
            nom_complet_membre = func.concat(
                func.coalesce(MembreFamilia.nom, ''), ' ',
                func.coalesce(MembreFamilia.primer_cognom, ''), ' ',
                func.coalesce(MembreFamilia.segon_cognom, '')
            )
            subquery_membres = MembreFamilia.query.filter(
                nom_complet_membre.ilike(f"%{text}%")
            ).with_entities(MembreFamilia.espai_familiar_id)

            condicions_familia.append(or_(
                EspaiFamiliar.nom.ilike(f"%{text}%"),
                EspaiFamiliar.descripcio.ilike(f"%{text}%"),
                EspaiFamiliar.id.in_(subquery_membres)
            ))

        if pais:
            subquery_pais_origen = UbicacioOrigenFamilia.query.filter(
                UbicacioOrigenFamilia.pais.ilike(f"%{pais}%")
            ).with_entities(UbicacioOrigenFamilia.espai_familiar_id)
            condicions_familia.append(EspaiFamiliar.id.in_(subquery_pais_origen))

        if condicions_familia:
            base_familia = EspaiFamiliar.query.filter(EspaiFamiliar.visible_publicament == True)
            if strict:
                families_raw = base_familia.filter(and_(*condicions_familia)).limit(per_page).all()
            else:
                families_raw = base_familia.filter(or_(*condicions_familia)).limit(per_page).all()
        else:
            families_raw = []
    else:
        families_raw = []

    converses = []
    for conversa in converses_raw:
        conv_dict = preparar_conversa_per_vista(conversa, conversa.usuari.nom_login if conversa.usuari else 'anonim')
        converses.append(conv_dict)

    families = [preparar_familia_per_vista(f) for f in families_raw]

    # Barrejar entrades + converses + families
    entrades = entrades + converses + families
    from datetime import date

    def normalitza_data(d):
        if isinstance(d, datetime):
            return d
        elif isinstance(d, date):
            return datetime.combine(d, datetime.min.time())
        return datetime.min

    entrades.sort(key=lambda x: normalitza_data(x.get("data_ordenacio")), reverse=True)

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
    if not entrada.es_publica:
        abort(404)
    return render_template('entrada_publica.html', entrada=entrada)
