import os
import shutil
from flask import Flask
from config import Config
from models import db, Usuari, PerfilBiografic, Entrada, Entrevista, RespostaEntrevista, ArxiuAdjunt, Etiqueta
from models import ImatgeGaleria  # Imatges de galeria
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UMBERTO_DIR = os.path.join(BASE_DIR, "umberto")
CARPETES = ["usuaris", "media", "documentacio"]

def esborrar_carpetes_excepte_admin():
    print("📁 Esborrant carpetes d'usuaris...")
    for carpeta in CARPETES:
        ruta_base = os.path.join(UMBERTO_DIR, carpeta)
        if not os.path.exists(ruta_base):
            continue

        for sub in os.listdir(ruta_base):
            if not sub.startswith("admin"):
                ruta_completa = os.path.join(ruta_base, sub)
                print(f"🗑️ Esborrant: {ruta_completa}")
                shutil.rmtree(ruta_completa, ignore_errors=True)

def netejar_bd():
    with app.app_context():
        print("📦 Netejant base de dades (excepte admin)...")

        try:
            # Comptadors previs
            usuaris_eliminats = Usuari.query.filter(Usuari.nom_login != 'admin').count()
            perfils_eliminats = PerfilBiografic.query.join(Usuari).filter(Usuari.nom_login != 'admin').count()
            entrades_eliminades = Entrada.query.count()
            entrevistes_eliminades = Entrevista.query.count()
            respostes_eliminades = RespostaEntrevista.query.count()
            arxius_eliminats = ArxiuAdjunt.query.count()
            imatges_eliminades = ImatgeGaleria.query.count()

            # 🔥 ORDRE DE NETEJA (relacions creuades)
            db.session.execute(text("DELETE FROM entrada_etiquetes"))
            db.session.execute(text("DELETE FROM missatges"))
            ImatgeGaleria.query.delete()
            RespostaEntrevista.query.delete()
            ArxiuAdjunt.query.delete()
            Entrada.query.delete()
            Entrevista.query.delete()
            Etiqueta.query.delete()
            PerfilBiografic.query.filter(~PerfilBiografic.usuari.has(nom_login='admin')).delete(synchronize_session=False)
            Usuari.query.filter(Usuari.nom_login != 'admin').delete()
            db.session.commit()

            print("\n✅ Dades eliminades:")
            print(f"  🖼️ Imatges de galeria eliminades: {imatges_eliminades}")
            print(f"  💬 missatges d’entrevista IA esborrats.")
            print(f"  👤 Usuaris eliminats: {usuaris_eliminats}")
            print(f"  🧾 Perfils biogràfics eliminats: {perfils_eliminats}")
            print(f"  📝 Entrades eliminades: {entrades_eliminades}")
            print(f"  🎤 Entrevistes eliminades: {entrevistes_eliminades}")
            print(f"  💬 Respostes d'entrevista eliminades: {respostes_eliminades}")
            print(f"  📎 Arxius adjunts eliminats: {arxius_eliminats}")
            

        except Exception as e:
            print(f"\n❌ ERROR durant la neteja de la base de dades:\n{e}")

if __name__ == "__main__":
    print("🚀 Executant neteja completa...")
    esborrar_carpetes_excepte_admin()
    netejar_bd()
