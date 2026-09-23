from flask import Blueprint, render_template, session

home_bp = Blueprint('home', __name__, url_prefix='/home')

@home_bp.route('/')
def home():
    idioma = session.get('idioma', 'ca')
    
    # Intentar carregar per idioma
    try:
        return render_template(f'home/home_{idioma}.html')
    except:
        return render_template('home/home_ca.html')

# Aquestes rutes ja no calen perquè tot està a home_ca.html amb àncores
# Però si vols mantenir-les per compatibilitat, pots redirigir:

@home_bp.route("/qui_som")
def qui_som():
    return redirect(url_for('home.home') + '#qui-som')

@home_bp.route("/manifest_etic")
def manifest_etic():
    return redirect(url_for('home.home') + '#manifest-etic')
