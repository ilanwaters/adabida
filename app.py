import os
import pathlib
from datetime import datetime, timedelta

from flask import Flask, session, request, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_babel import Babel, _, get_locale
from flask_login import LoginManager, current_user, login_required, login_user

from config import Config
from models import db
from models.usuari import Usuari
from flask_mail import Mail
from utils.email import mail

from routes.auth import auth_bp


app = Flask(__name__)

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config["SECRET_KEY"] = "abadia_2025_clau_secreta"
app.config.from_object(Config)  # ← PRIMER carregar configuració
mail.init_app(app)  # ← DESPRÉS inicialitzar mail

pathlib.Path(os.path.join(os.path.dirname(__file__), "database")).mkdir(exist_ok=True)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'


@login_manager.user_loader
def carrega_usuari(user_id):
    return Usuari.query.get(int(user_id))

migrate = Migrate(app, db)        
# ─── Babel ──────────────────────────────────────────────────────
app.config["BABEL_DEFAULT_LOCALE"] = "ca"
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"

def seleccionar_idioma() -> str:
    # 1. Prioritat: sessió (usuari ha triat manualment)
    if "idioma" in session:
        return session["idioma"]
    
    # 2. Detecció per domini
    host = request.host.lower()
    if '.cat' in host:
        return 'ca'
    elif '.es' in host:
        return 'es'
    elif '.org' in host or '.com' in host:
        return 'en'
    
    # 3. Fallback: navegador
    return request.accept_languages.best_match(
        ["ca", "es", "en", "ru", "de", "fr", "uk", "eu"]
    ) or "ca"

babel = Babel(app, locale_selector=seleccionar_idioma)

@app.context_processor
def inject_traductor():
    return dict(_=_, get_locale=get_locale)

@app.context_processor
def inject_traductor():
    return dict(_=_, get_locale=get_locale)

@app.context_processor
def inject_missatges_nous():
    """Injecta el comptador de missatges nous a tots els templates"""
    if current_user.is_authenticated:
        from models.usuari import Missatge
        missatges_nous = Missatge.query.filter_by(
            receptor_id=current_user.id,
            llegit=False
        ).count()
        return dict(missatges_nous=missatges_nous)
    return dict(missatges_nous=0)

@app.context_processor
def inject_nivells_usuari():
    """Injecta els textos dels nivells d'usuari a tots els templates"""
    nivell_text = {
        'blau': 'Usuari novell',
        'groc': 'Usuari actiu',
        'verd': 'Usuari verificat'
    }
    return dict(nivell_text=nivell_text)
    
# ─── Blueprints ────────────────────────────────────────────────
from routes.inici import inici_bp
from routes.login import login_bp
from routes.registre_individual import registre_individual_routes
from routes.pagina_personal import pagina_personal_bp, personal_biografia_bp, perfil_public_bp, biografia_seccions_bp
from routes.nova_entrada_personal import nova_entrada_bp
from routes.pujar_arxiu_async import pujar_arxiu_bp
from routes.pujar_arxiu_temp import pujar_temp_bp
from routes.serveis_media import serveis_media_bp
from routes import questionari
from routes.repositori import repositori_bp
from routes.reset_contrasenya import reset_bp
from routes.crear_admin import crear_admin_bp
from routes.galeria import galeria_bp
from routes.blog import blog_bp
from routes.exposicio import exposicio_bp
from routes.usuari_admin import usuari_admin_bp
from routes.api_guardades import api_guardades_bp
from routes.missatges import missatges_bp
from routes.organitzacions.organitzacions import organitzacions_bp
from routes.converses import converses_bp
from routes.home import home_bp
from routes.organitzacions.admin_organitzacions import admin_organitzacions_bp
from routes.organitzacions.missatges_organitzacions import missatges_organitzacions_bp
from routes.contactes import contactes_bp
from routes.aportacions import aportacions_bp
from routes.auth import auth_bp
from routes.familia.familia import familia_bp
from routes.familia.membres import membres_bp
from routes.familia.administrar import administrar_bp
from routes.familia.historia_familia import historia_familia_bp
from routes.organitzacions.historia_organitzacio import historia_organitzacio_bp
from routes.legal import legal_bp
from routes.api_ubicacions import api_ubicacions_bp
from routes.api.api import api_bp
from routes.api.tematiques import tematiques_api_bp
from routes.admin.admin import admin_bp
from routes.admin.galeria import admin_galeria_bp
from routes.admin.dades import admin_dades_bp
from routes.admin.tematiques import admin_tematiques_bp
from routes.api.barra_lateral import barra_lateral_api_bp
from routes.admin.traduccions import admin_traduccions_bp
from routes.admin.aportacions import admin_aportacions_bp
from routes.api_usuaris import api_usuaris_bp
from routes.projecte import projecte_bp

app.register_blueprint(pagina_personal_bp)
app.register_blueprint(inici_bp)
app.register_blueprint(login_bp)
app.register_blueprint(registre_individual_routes)
app.register_blueprint(nova_entrada_bp)
app.register_blueprint(pujar_arxiu_bp)
app.register_blueprint(pujar_temp_bp)
app.register_blueprint(serveis_media_bp)
app.register_blueprint(api_bp)
app.register_blueprint(questionari.questionari_bp)
app.register_blueprint(repositori_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(reset_bp)
app.register_blueprint(crear_admin_bp)
app.register_blueprint(galeria_bp)
app.register_blueprint(admin_galeria_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(exposicio_bp)
app.register_blueprint(usuari_admin_bp)
app.register_blueprint(api_guardades_bp)
app.register_blueprint(perfil_public_bp)
app.register_blueprint(admin_dades_bp)
app.register_blueprint(missatges_bp, url_prefix="/missatges")
app.register_blueprint(organitzacions_bp)
app.register_blueprint(converses_bp)
app.register_blueprint(home_bp)
app.register_blueprint(admin_organitzacions_bp)
app.register_blueprint(missatges_organitzacions_bp)
app.register_blueprint(contactes_bp, url_prefix='/contactes')
app.register_blueprint(aportacions_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(familia_bp)
app.register_blueprint(membres_bp, url_prefix='/familia/membre')
app.register_blueprint(administrar_bp)
app.register_blueprint(personal_biografia_bp)
app.register_blueprint(biografia_seccions_bp)
app.register_blueprint(historia_familia_bp)
app.register_blueprint(historia_organitzacio_bp)
app.register_blueprint(legal_bp)
app.register_blueprint(api_ubicacions_bp)
app.register_blueprint(tematiques_api_bp)
app.register_blueprint(admin_tematiques_bp) 
app.register_blueprint(barra_lateral_api_bp)
app.register_blueprint(admin_traduccions_bp)
app.register_blueprint(admin_aportacions_bp)
app.register_blueprint(api_usuaris_bp)
app.register_blueprint(projecte_bp)
# ─── Ping ──────────────────────────────────────────────────────

@app.route("/prova_tema")
def prova_tema():
    return render_template("tria_tema.html")

@app.route("/prova_login")
def prova_login():
    if current_user.is_authenticated:
        return f"✅ Estàs loguejat com: {current_user.nom_login}"
    else:
        return "❌ No estàs loguejat"
        from datetime import datetime

@app.template_filter('format_data')
def format_data(data_str):
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d')
        return data.strftime('%d/%m/%Y')
    except Exception:
        return data_str  # Si ja està formatada o buida

@app.route("/")
def splash():
    # comprovar si l’usuari ja ha dit "no tornar a mostrar"
    return render_template("splash.html")

@app.route("/inici")
def inici():
    return render_template("inici.html")

@app.template_filter('nl2br')
def nl2br_filter(text):
    """Converteix salts de línia en <br> tags"""
    if text:
        return text.replace('\n', '<br>')
    return text

@app.context_processor
def inject_usuari():
    if current_user.is_authenticated:
        return {'usuari': current_user}
    return {'usuari': None}

@app.context_processor
def inject_rtl():
    return {
        "is_rtl": str(get_locale()) in Config.RTL_LANGS
    }

@app.route('/app/login', methods=['GET', 'POST'])
def app_login():
    if current_user.is_authenticated:
        return redirect('/app')
    
    if request.method == 'POST':
        from models.usuari import Usuari
        username = request.form.get('username')
        password = request.form.get('password')
        
        usuari = Usuari.query.filter_by(nom_login=username).first()
        
        if usuari and usuari.check_contrasenya(password):
            session.permanent = True
            session["usuari"] = usuari.nom_login  # ← AFEGIR AIXÒ
            session["usuari_id"] = usuari.id      # ← AFEGIR AIXÒ
            session["es_admin"] = usuari.es_admin # ← AFEGIR AIXÒ
            login_user(usuari, remember=True)
            return redirect('/app')
        else:
            return render_template('app/login.html', error='Usuari o contrasenya incorrectes')
    
    return render_template('app/login.html')

@app.route('/app')
@login_required
def app_home():
    return render_template('app/home.html')

if __name__ == "__main__":
    app.run(debug=True)
