from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, MissatgeOrganitzacio, Organitzacio

missatges_organitzacions_bp = Blueprint("missatges_organitzacions", __name__, url_prefix="/organitzacions")

@missatges_organitzacions_bp.route("/contactar_org", methods=["POST"])
@login_required
def enviar_missatge():
    print("FUNCIO EXECUTADA!")
    print(f"🔍 USUARI ACTUAL: {current_user.nom}")
    
    data = request.get_json()
    print(f"📄 DADES REBUDES: {data}")
    
    receptor_nom = data.get("receptor_login")
    assumpte = data.get("assumpte", "").strip()
    contingut = data.get("contingut", "").strip()
    
    print(f"🎯 CERCANT ORGANITZACIÓ: '{receptor_nom}'")

    if not receptor_nom or not contingut or not assumpte:
        print("❌ MISSATGE INCOMPLET")
        return jsonify({"success": False, "error": "Missatge incomplet"})

    # Buscar organització per nom
    org = Organitzacio.query.filter_by(nom=receptor_nom).first()
    print(f"🏢 ORGANITZACIÓ TROBADA: {org}")
    
    if not org:
        print("❌ ORGANITZACIÓ NO TROBADA!")
        return jsonify({"success": False, "error": "Organització no trobada"})

    print(f"✅ CREANT MISSATGE: org_id={org.id}, emissor_id={current_user.id}")

    # Crear missatge a organització
    missatge = MissatgeOrganitzacio(
        organitzacio_id=org.id,
        emissor_id=current_user.id,
        assumpte=assumpte,
        contingut=contingut,
        tipus='rebut'
    )
    
    db.session.add(missatge)
    db.session.commit()
    
    print("✅ MISSATGE GUARDAT CORRECTAMENT")
    
    return jsonify({"success": True, "message": "Missatge enviat a l'organització"})
