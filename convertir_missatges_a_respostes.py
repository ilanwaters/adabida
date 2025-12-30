from models import db, PerfilBiografic, Missatge, RespostaEntrevista, Entrevista
from app import app
from sqlalchemy.orm import joinedload

with app.app_context():
    print("📦 CONNECTANT A:", app.config["SQLALCHEMY_DATABASE_URI"])

    # Carreguem tots els missatges, amb accés a l'entrevista vinculada
    missatges = Missatge.query.options(joinedload(Missatge.entrevista)).all()

    if not missatges:
        print("⚠️ No s’han trobat missatges.")
        exit()

    # Esborrar respostes anteriors per evitar duplicats
    RespostaEntrevista.query.delete()
    db.session.commit()

    comptador = 0
    for missatge in missatges:
        if missatge.autor == "usuari":
            entrevista = missatge.entrevista
            if entrevista and entrevista.perfil_id:
                resposta = RespostaEntrevista(
                    perfil_id=entrevista.perfil_id,
                    tema="Sense tema",  # 🔧 Canvia això més endavant si tens temes
                    subtema="",
                    pregunta="",
                    resposta=missatge.text,
                    data=missatge.timestamp
                )
                db.session.add(resposta)
                comptador += 1

    db.session.commit()
    print(f"✅ Conversió completada: {comptador} respostes afegides.")
