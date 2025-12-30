from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db
from models.ubicacions import Pais
from models.tematiques import CategoriaTema, Tema
from functools import wraps
from flask import session
import pycountry
from difflib import get_close_matches

admin_tematiques_bp = Blueprint('admin_tematiques', __name__, url_prefix='/admin/tematiques')

# Diccionari AMPLIAT per detectar codi ISO des de qualsevol idioma
# Inclou: català, castellà, anglès, idiomes locals (grec, japonès, rus, xinès, etc.)

NOMS_A_CODI_ISO = {
    # ESPANYA
    'espanya': 'ES', 'españa': 'ES', 'spain': 'ES', 'espagne': 'ES', 'espainia': 'ES', 
    
    # FRANÇA
    'frança': 'FR', 'francia': 'FR', 'france': 'FR',
    
    # ALEMANYA
    'alemanya': 'DE', 'alemania': 'DE', 'germany': 'DE', 'deutschland': 'DE', 'allemagne': 'DE',
    
    # ITÀLIA
    'itàlia': 'IT', 'italia': 'IT', 'italy': 'IT', 'italie': 'IT',
    
    # GRÈCIA
    'grècia': 'GR', 'grecia': 'GR', 'greece': 'GR', 'grèce': 'GR',
    'ελλάδα': 'GR', 'ellada': 'GR',  # Grec
    
    # JAPÓ
    'japó': 'JP', 'japón': 'JP', 'japan': 'JP', 'japon': 'JP',
    '日本': 'JP', 'nihon': 'JP', 'nippon': 'JP',  # Japonès
    
    # RÚSSIA
    'rússia': 'RU', 'rusia': 'RU', 'russia': 'RU', 'russie': 'RU',
    'россия': 'RU', 'rossiya': 'RU',  # Rus
    
    # XINA
    'xina': 'CN', 'china': 'CN', 'chine': 'CN',
    '中国': 'CN', 'zhongguo': 'CN',  # Xinès
    
    # BRASIL
    'brasil': 'BR', 'brazil': 'BR', 'brésil': 'BR',
    
    # ESTATS UNITS
    'estats units': 'US', 'estados unidos': 'US', 'united states': 'US', 'états-unis': 'US',
    'usa': 'US', 'eeuu': 'US', 'eua': 'US',
    
    # PORTUGAL
    'portugal': 'PT',
    
    # REGNE UNIT
    'regne unit': 'GB', 'reino unido': 'GB', 'united kingdom': 'GB', 'royaume-uni': 'GB',
    'anglaterra': 'GB', 'inglaterra': 'GB', 'england': 'GB',
    
    # HONGRIA (IMPORTANT!)
    'hongria': 'HU', 'hungria': 'HU', 'hungría': 'HU', 'hungary': 'HU', 'hongrie': 'HU',
    'magyarország': 'HU',  # Hongarès
    
    # BULGÀRIA
    'bulgària': 'BG', 'bulgaria': 'BG', 'bulgarie': 'BG',
    'българия': 'BG',  # Búlgar
    
    # POLÒNIA
    'polònia': 'PL', 'polonia': 'PL', 'poland': 'PL', 'pologne': 'PL',
    'polska': 'PL',  # Polonès
    
    # ROMANIA
    'romania': 'RO', 'roumanie': 'RO', 'românia': 'RO',
    
    # TURQUIA
    'turquia': 'TR', 'turquía': 'TR', 'turkey': 'TR', 'turquie': 'TR',
    'türkiye': 'TR',  # Turc
    
    # SUÈCIA
    'suècia': 'SE', 'suecia': 'SE', 'sweden': 'SE', 'suède': 'SE',
    'sverige': 'SE',  # Suec
    
    # NORUEGA
    'noruega': 'NO', 'norway': 'NO', 'norvège': 'NO',
    'norge': 'NO',  # Noruec
    
    # FINLÀNDIA
    'finlàndia': 'FI', 'finlandia': 'FI', 'finland': 'FI', 'finlande': 'FI',
    'suomi': 'FI',  # Finès
    
    # COREA DEL SUD
    'corea del sud': 'KR', 'corea del sur': 'KR', 'south korea': 'KR', 'corée du sud': 'KR',
    '한국': 'KR', 'hanguk': 'KR',  # Coreà
    
    # ÍNDIA
    'índia': 'IN', 'india': 'IN', 'inde': 'IN',
    'भारत': 'IN', 'bharat': 'IN',  # Hindi
    
    # MÈXIC
    'mèxic': 'MX', 'méxico': 'MX', 'mexico': 'MX', 'mexique': 'MX',
    
    # ARGENTINA
    'argentina': 'AR', 'argentine': 'AR',
    
    # XILE
    'xile': 'CL', 'chile': 'CL', 'chili': 'CL',
    
    # PERÚ
    'perú': 'PE', 'perù': 'PE', 'peru': 'PE', 'pérou': 'PE',
    
    # COLÒMBIA
    'colòmbia': 'CO', 'colombia': 'CO', 'colombie': 'CO',
    
    # EGIPTE
    'egipte': 'EG', 'egipto': 'EG', 'egypt': 'EG', 'égypte': 'EG',
    'مصر': 'EG', 'misr': 'EG',  # Àrab
    
    # MARROC
    'marroc': 'MA', 'marruecos': 'MA', 'morocco': 'MA', 'maroc': 'MA',
    'المغرب': 'MA',  # Àrab
    
    # AUSTRÀLIA
    'austràlia': 'AU', 'australia': 'AU', 'australie': 'AU',
    
    # CANADÀ
    'canadà': 'CA', 'canadá': 'CA', 'canada': 'CA',
    
    # BÈLGICA
    'bèlgica': 'BE', 'bélgica': 'BE', 'belgium': 'BE', 'belgique': 'BE', 'belgië': 'BE',
    
    # SUÏSSA
    'suïssa': 'CH', 'suiza': 'CH', 'switzerland': 'CH', 'suisse': 'CH', 'schweiz': 'CH',
    
    # ÀUSTRIA
    'àustria': 'AT', 'austria': 'AT', 'autriche': 'AT', 'österreich': 'AT',
    
    # PAÏSOS BAIXOS
    'països baixos': 'NL', 'paises bajos': 'NL', 'netherlands': 'NL', 'pays-bas': 'NL',
    'holanda': 'NL', 'holland': 'NL', 'nederland': 'NL',
    
    # DINAMARCA
    'dinamarca': 'DK', 'denmark': 'DK', 'danemark': 'DK', 'danmark': 'DK',
    
    # CROÀCIA
    'croàcia': 'HR', 'croacia': 'HR', 'croatia': 'HR', 'croatie': 'HR', 'hrvatska': 'HR',
    
    # IRLANDA
    'irlanda': 'IE', 'ireland': 'IE', 'irlande': 'IE', 'éire': 'IE',
    
    # ISLÀNDIA
    'islàndia': 'IS', 'islandia': 'IS', 'iceland': 'IS', 'islande': 'IS', 'ísland': 'IS',
}

# Diccionari invers: codi ISO → nom en català (per normalitzar)
CODI_ISO_A_NOM_CA = {
    'ES': 'Espanya',
    'FR': 'França',
    'DE': 'Alemanya',
    'IT': 'Itàlia',
    'GR': 'Grècia',
    'JP': 'Japó',
    'RU': 'Rússia',
    'CN': 'Xina',
    'BR': 'Brasil',
    'US': 'Estats Units',
    'PT': 'Portugal',
    'GB': 'Regne Unit',
    'HU': 'Hongria',
    'BG': 'Bulgària',
    'PL': 'Polònia',
    'RO': 'Romania',
    'TR': 'Turquia',
    'SE': 'Suècia',
    'NO': 'Noruega',
    'FI': 'Finlàndia',
    'KR': 'Corea del Sud',
    'IN': 'Índia',
    'MX': 'Mèxic',
    'AR': 'Argentina',
    'CL': 'Xile',
    'PE': 'Perú',
    'CO': 'Colòmbia',
    'EG': 'Egipte',
    'MA': 'Marroc',
    'AU': 'Austràlia',
    'CA': 'Canadà',
    'BE': 'Bèlgica',
    'CH': 'Suïssa',
    'AT': 'Àustria',
    'NL': 'Països Baixos',
    'DK': 'Dinamarca',
    'HR': 'Croàcia',
    'IE': 'Irlanda',
    'IS': 'Islàndia',
}
# Decorador per protegir rutes admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuari' not in session:
            flash('Necessites ser administrador', 'error')
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function

def obtenir_codi_iso(nom_pais):
    """
    Obté el codi ISO d'un país a partir del seu nom en QUALSEVOL idioma.
    Utilitza pycountry per cercar en tots els camps disponibles.
    Retorna el codi ISO-2 o None si no el troba.
    """
    try:
        nom_normalitzat = nom_pais.strip()
        
        # 1. Buscar per nom oficial en anglès (name)
        try:
            pais = pycountry.countries.get(name=nom_normalitzat)
            if pais:
                return pais.alpha_2
        except:
            pass
        
        # 2. Buscar per nom oficial complet (official_name)
        try:
            pais = pycountry.countries.get(official_name=nom_normalitzat)
            if pais:
                return pais.alpha_2
        except:
            pass
        
        # 3. Buscar per nom comú (common_name) si existeix
        try:
            pais = pycountry.countries.get(common_name=nom_normalitzat)
            if pais:
                return pais.alpha_2
        except:
            pass
        
        # 4. Buscar en TOTS els camps de TOTS els països (cerca exhaustiva)
        nom_lower = nom_normalitzat.lower()
        for pais in pycountry.countries:
            # Comprovar tots els atributs del país
            atributs = [
                getattr(pais, 'name', ''),
                getattr(pais, 'official_name', ''),
                getattr(pais, 'common_name', ''),
            ]
            
            # Comprovar coincidència exacta (case-insensitive)
            for atribut in atributs:
                if atribut.lower() == nom_lower:
                    return pais.alpha_2
        
        # 5. Fuzzy search en tots els noms
        # Crear llista amb tots els noms possibles
        tots_noms = []
        for pais in pycountry.countries:
            tots_noms.append((pais.name, pais.alpha_2))
            if hasattr(pais, 'official_name'):
                tots_noms.append((pais.official_name, pais.alpha_2))
            if hasattr(pais, 'common_name'):
                tots_noms.append((pais.common_name, pais.alpha_2))
        
        # Buscar similituds
        noms_disponibles = [n[0] for n in tots_noms]
        coincidencies = get_close_matches(nom_normalitzat, noms_disponibles, n=1, cutoff=0.7)
        
        if coincidencies:
            # Trobar el codi ISO corresponent
            for nom, codi in tots_noms:
                if nom == coincidencies[0]:
                    return codi
        
        # 6. Si encara no hem trobat res, intentar cerca més permissiva
        coincidencies_baixes = get_close_matches(nom_normalitzat, noms_disponibles, n=1, cutoff=0.5)
        
        if coincidencies_baixes:
            for nom, codi in tots_noms:
                if nom == coincidencies_baixes[0]:
                    return codi
        
        # Si no troba res, retornar None
        return None
        
    except Exception as e:
        print(f"Error obtenint codi ISO per '{nom_pais}': {e}")
        return None

# ============== PAÏSOS ==============

@admin_tematiques_bp.route('/paisos')
@admin_required
def llistar_paisos():
    paisos = Pais.query.order_by(Pais.nom_oficial_en).all()
    
    # Comptar països nous (no revisats)
    paisos_nous = sum(1 for p in paisos if not p.revisat_per_admin)
    
    return render_template('admin/tematiques/paisos.html', 
                         paisos=paisos,
                         paisos_nous=paisos_nous)

@admin_tematiques_bp.route('/paisos/afegir', methods=['GET', 'POST'])
@admin_required
def afegir_pais():
    if request.method == 'POST':
        nom = request.form.get('nom').strip()
        codi_iso = request.form.get('codi_iso', '').strip().upper()
        
        if not nom:
            flash('El nom és obligatori', 'error')
            return redirect(url_for('admin_tematiques.afegir_pais'))
        
        # Si no hi ha codi ISO, intentar generar-lo automàticament
        if not codi_iso:
            codi_iso = obtenir_codi_iso(nom)
            
            if not codi_iso:
                flash(f'No s\'ha pogut trobar el codi ISO per "{nom}". Introdueix-lo manualment.', 'warning')
                return render_template('admin/tematiques/afegir_pais.html', nom_introduit=nom)
        
        # Validar longitud del codi
        if len(codi_iso) != 2:
            flash('El codi ISO ha de tenir 2 lletres', 'error')
            return render_template('admin/tematiques/afegir_pais.html', nom_introduit=nom)
        
        # Comprovar si ja existeix
        if Pais.query.filter_by(codi_iso=codi_iso).first():
            flash(f'Ja existeix un país amb el codi {codi_iso}', 'error')
            return redirect(url_for('admin_tematiques.afegir_pais'))
        
        if Pais.query.filter_by(nom=nom).first():
            flash(f'Ja existeix un país amb el nom "{nom}"', 'error')
            return redirect(url_for('admin_tematiques.afegir_pais'))
        
        nou_pais = Pais(nom_oficial_en=nom, codi_iso=codi_iso, revisat_per_admin=True)
        db.session.add(nou_pais)
        db.session.commit()
        
        flash(f'País {nom} ({codi_iso}) creat correctament', 'success')
        return redirect(url_for('admin_tematiques.llistar_paisos'))
    
    return render_template('admin/tematiques/afegir_pais.html')

@admin_tematiques_bp.route('/paisos/<int:pais_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_pais(pais_id):
    pais = Pais.query.get_or_404(pais_id)
    
    if request.method == 'POST':
        nom = request.form.get('nom').strip()
        codi_iso = request.form.get('codi_iso', '').strip().upper()
        
        if not nom:
            flash('El nom és obligatori', 'error')
            return redirect(url_for('admin_tematiques.editar_pais', pais_id=pais_id))
        
        # Si no hi ha codi ISO, intentar generar-lo
        if not codi_iso:
            codi_iso = obtenir_codi_iso(nom)
            if not codi_iso:
                flash(f'No s\'ha pogut trobar el codi ISO per "{nom}". Introdueix-lo manualment.', 'warning')
                return render_template('admin/tematiques/editar_pais.html', pais=pais)
        
        if len(codi_iso) != 2:
            flash('El codi ISO ha de tenir 2 lletres', 'error')
            return redirect(url_for('admin_tematiques.editar_pais', pais_id=pais_id))
        
        # Comprovar si el codi ja existeix (excepte si és el mateix país)
        pais_existent = Pais.query.filter_by(codi_iso=codi_iso).first()
        if pais_existent and pais_existent.id != pais_id:
            flash(f'Ja existeix un país amb el codi {codi_iso}', 'error')
            return redirect(url_for('admin_tematiques.editar_pais', pais_id=pais_id))
        
        pais.nom_oficial_en = nom
        pais.codi_iso = codi_iso
        pais.revisat_per_admin = True
        
        db.session.commit()
        
        flash(f'País {nom} actualitzat correctament', 'success')
        return redirect(url_for('admin_tematiques.llistar_paisos'))
    
    return render_template('admin/tematiques/editar_pais.html', pais=pais)

@admin_tematiques_bp.route('/paisos/<int:pais_id>/marcar-revisat', methods=['POST'])
@admin_required
def marcar_pais_revisat(pais_id):
    pais = Pais.query.get_or_404(pais_id)
    pais.revisat_per_admin = True
    db.session.commit()
    
    flash(f'País {pais.nom} marcat com revisat', 'success')
    return redirect(url_for('admin_tematiques.llistar_paisos'))

@admin_tematiques_bp.route('/paisos/<int:pais_id>/eliminar', methods=['POST'])
@admin_required
def eliminar_pais(pais_id):
    pais = Pais.query.get_or_404(pais_id)
    
    if pais.categories:
        flash(f'No es pot eliminar {pais.nom} perquè té categories associades', 'error')
        return redirect(url_for('admin_tematiques.llistar_paisos'))
    
    db.session.delete(pais)
    db.session.commit()
    
    flash(f'País {pais.nom} eliminat', 'success')
    return redirect(url_for('admin_tematiques.llistar_paisos'))

# ============== CATEGORIES ==============

@admin_tematiques_bp.route('/paisos/<int:pais_id>/categories')
@admin_required
def llistar_categories(pais_id):
    from models.tematiques import TemaExclusio
    
    pais = Pais.query.get_or_404(pais_id)
    categories = CategoriaTema.query.filter_by(pais_id=pais_id).order_by(CategoriaTema.ordre).all()
    
    # Obtenir IDs de temes exclosos
    exclusions_ids = [e.tema_id for e in TemaExclusio.query.filter_by(pais_id=pais_id).all()]
    
    # Obtenir temes globals NO exclosos
    if exclusions_ids:
        temes_globals = Tema.query.filter_by(aplicar_a_tots_paisos=True).filter(~Tema.id.in_(exclusions_ids)).all()
    else:
        temes_globals = Tema.query.filter_by(aplicar_a_tots_paisos=True).all()
    
    print(f"DEBUG: Brasil té {len(temes_globals)} temes globals")  # ← AFEGIR AIXÒ
    
    return render_template('admin/tematiques/categories.html', 
                         pais=pais, 
                         categories=categories,
                         temes_globals=temes_globals)

@admin_tematiques_bp.route('/paisos/<int:pais_id>/categories/afegir', methods=['GET', 'POST'])
@admin_required
def afegir_categoria(pais_id):
    pais = Pais.query.get_or_404(pais_id)
    
    if request.method == 'POST':
        nom = request.form.get('nom')
        ordre = request.form.get('ordre', 0)
        
        if not nom:
            flash('El nom és obligatori', 'error')
            return redirect(url_for('admin_tematiques.afegir_categoria', pais_id=pais_id))
        
        nova_categoria = CategoriaTema(pais_id=pais_id, nom=nom, ordre=ordre)
        db.session.add(nova_categoria)
        db.session.commit()
        
        flash(f'Categoria {nom} creada', 'success')
        return redirect(url_for('admin_tematiques.llistar_categories', pais_id=pais_id))
    
    return render_template('admin/tematiques/afegir_categoria.html', pais=pais)

@admin_tematiques_bp.route('/categories/<int:categoria_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_categoria(categoria_id):
    categoria = CategoriaTema.query.get_or_404(categoria_id)
    
    if request.method == 'POST':
        nom = request.form.get('nom')
        ordre = request.form.get('ordre', 0)
        
        if not nom:
            flash('El nom és obligatori', 'error')
            return redirect(url_for('admin_tematiques.editar_categoria', categoria_id=categoria_id))
        
        categoria.nom = nom
        categoria.ordre = ordre
        db.session.commit()
        
        flash(f'Categoria {nom} actualitzada', 'success')
        return redirect(url_for('admin_tematiques.llistar_categories', pais_id=categoria.pais_id))
    
    return render_template('admin/tematiques/editar_categoria.html', categoria=categoria)

@admin_tematiques_bp.route('/categories/<int:categoria_id>/eliminar', methods=['POST'])
@admin_required
def eliminar_categoria(categoria_id):
    categoria = CategoriaTema.query.get_or_404(categoria_id)
    pais_id = categoria.pais_id
    
    if categoria.temes:
        flash(f'No es pot eliminar {categoria.nom} perquè té temes associats', 'error')
        return redirect(url_for('admin_tematiques.llistar_categories', pais_id=pais_id))
    
    db.session.delete(categoria)
    db.session.commit()
    
    flash(f'Categoria {categoria.nom} eliminada', 'success')
    return redirect(url_for('admin_tematiques.llistar_categories', pais_id=pais_id))

# ============== TEMES ==============

@admin_tematiques_bp.route('/categories/<int:categoria_id>/temes')
@admin_required
def llistar_temes(categoria_id):
    categoria = CategoriaTema.query.get_or_404(categoria_id)
    temes = Tema.query.filter_by(categoria_id=categoria_id).order_by(Tema.ordre).all()
    return render_template('admin/tematiques/temes.html', categoria=categoria, temes=temes)

@admin_tematiques_bp.route('/categories/<int:categoria_id>/temes/afegir', methods=['GET', 'POST'])
@admin_required
def afegir_tema(categoria_id):
    categoria = CategoriaTema.query.get_or_404(categoria_id)
    
    if request.method == 'POST':
        nom = request.form.get('nom')
        ordre = request.form.get('ordre', 0)
        
        if not nom:
            flash('El nom és obligatori', 'error')
            return redirect(url_for('admin_tematiques.afegir_tema', categoria_id=categoria_id))
        
        nou_tema = Tema(categoria_id=categoria_id, nom=nom, ordre=ordre)
        db.session.add(nou_tema)
        db.session.commit()
        
        flash(f'Tema {nom} creat', 'success')
        return redirect(url_for('admin_tematiques.llistar_temes', categoria_id=categoria_id))
    
    return render_template('admin/tematiques/afegir_tema.html', categoria=categoria)

@admin_tematiques_bp.route('/temes/<int:tema_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_tema(tema_id):
    tema = Tema.query.get_or_404(tema_id)
    
    if request.method == 'POST':
        nom = request.form.get('nom')
        ordre = request.form.get('ordre', 0)
        
        if not nom:
            flash('El nom és obligatori', 'error')
            return redirect(url_for('admin_tematiques.editar_tema', tema_id=tema_id))
        
        tema.nom = nom
        tema.ordre = ordre
        db.session.commit()
        
        flash(f'Tema {nom} actualitzat', 'success')
        return redirect(url_for('admin_tematiques.llistar_temes', categoria_id=tema.categoria_id))
    
    return render_template('admin/tematiques/editar_tema.html', tema=tema)

@admin_tematiques_bp.route('/temes/<int:tema_id>/eliminar', methods=['POST'])
@admin_required
def eliminar_tema(tema_id):
    tema = Tema.query.get_or_404(tema_id)
    categoria_id = tema.categoria_id
    
    db.session.delete(tema)
    db.session.commit()
    
    flash(f'Tema {tema.nom} eliminat', 'success')
    return redirect(url_for('admin_tematiques.llistar_temes', categoria_id=categoria_id))

@admin_tematiques_bp.route('/tema-global/afegir', methods=['GET', 'POST'])
@admin_required
def afegir_tema_global():
    """Afegir tema que pot aplicar-se a tots els països o múltiples"""
    
    if request.method == 'POST':
        nom_tema = request.form.get('nom_tema')
        distribucio = request.form.get('distribucio')  # 'tots', 'copiar', 'compartit'
        categoria_id = request.form.get('categoria_id')
        nova_categoria = request.form.get('nova_categoria')
        
        if not nom_tema:
            flash('El nom del tema és obligatori', 'error')
            return redirect(url_for('admin_tematiques.afegir_tema_global'))
        
        # OPCIÓ 1: TOTS els països
        if distribucio == 'tots':
            # Crear o obtenir categoria (només per un país base, ex: Espanya)
            pais_base = Pais.query.filter_by(codi_iso='ES').first()
            if not pais_base:
                pais_base = Pais.query.first()  # Si no hi ha Espanya, agafa el primer
            
            if categoria_id:
                categoria = CategoriaTema.query.get(categoria_id)
            elif nova_categoria:
                # Crear categoria només un cop
                categoria = CategoriaTema.query.filter_by(
                    pais_id=pais_base.id,
                    nom=nova_categoria
                ).first()
                
                if not categoria:
                    categoria = CategoriaTema(
                        pais_id=pais_base.id,
                        nom=nova_categoria,
                        ordre=0
                    )
                    db.session.add(categoria)
                    db.session.flush()
            else:
                flash('Has de seleccionar o crear una categoria', 'error')
                return redirect(url_for('admin_tematiques.afegir_tema_global'))
            
            # Crear UN SOL tema global
            tema = Tema(
                categoria_id=categoria.id,
                nom=nom_tema,
                ordre=0,
                aplicar_a_tots_paisos=True
            )
            db.session.add(tema)
            db.session.commit()
            
            flash(f'Tema global "{nom_tema}" creat per a tots els països', 'success')
            return redirect(url_for('admin_tematiques.llistar_paisos'))
        
        # OPCIÓ 2: Copiar a seleccionats
        elif distribucio == 'copiar':
            paisos_ids = request.form.getlist('paisos_copiar')
            
            if not paisos_ids:
                flash('Has de seleccionar almenys un país', 'error')
                return redirect(url_for('admin_tematiques.afegir_tema_global'))
            
            for pais_id in paisos_ids:
                pais = Pais.query.get(pais_id)
                
                # Crear o obtenir categoria
                if nova_categoria:
                    categoria = CategoriaTema.query.filter_by(
                        pais_id=pais.id,
                        nom=nova_categoria
                    ).first()
                    
                    if not categoria:
                        categoria = CategoriaTema(
                            pais_id=pais.id,
                            nom=nova_categoria,
                            ordre=0
                        )
                        db.session.add(categoria)
                        db.session.flush()
                elif categoria_id:
                    categoria = CategoriaTema.query.get(categoria_id)
                else:
                    flash('Has de crear o seleccionar una categoria', 'error')
                    return redirect(url_for('admin_tematiques.afegir_tema_global'))
                
                # Crear tema (còpia independent, NO global)
                tema = Tema(
                    categoria_id=categoria.id,
                    nom=nom_tema,
                    ordre=0,
                    aplicar_a_tots_paisos=False
                )
                db.session.add(tema)
            
            db.session.commit()
            flash(f'Tema "{nom_tema}" copiat a {len(paisos_ids)} països', 'success')
            return redirect(url_for('admin_tematiques.llistar_paisos'))
        
        # OPCIÓ 3: Compartit
        elif distribucio == 'compartit':
            flash('Funcionalitat "Compartit" encara no implementada', 'warning')
            return redirect(url_for('admin_tematiques.afegir_tema_global'))
    
    # GET: Mostrar formulari
    paisos = Pais.query.order_by(Pais.nom_oficial_en).all()
    categories = CategoriaTema.query.all()
    
    return render_template('admin/tematiques/afegir_tema_global.html',
                         paisos=paisos,
                         categories=categories)

@admin_tematiques_bp.route('/temes/<int:tema_id>/excloure-de-pais/<int:pais_id>', methods=['POST'])
@admin_required
def excloure_tema_de_pais(tema_id, pais_id):
    """Exclou un tema global d'un país específic"""
    from models.tematiques import TemaExclusio
    
    tema = Tema.query.get_or_404(tema_id)
    pais = Pais.query.get_or_404(pais_id)
    
    if not tema.aplicar_a_tots_paisos:
        flash(f'"{tema.nom}" no és un tema global', 'error')
        return redirect(url_for('admin_tematiques.llistar_categories', pais_id=pais_id))
    
    # Comprovar si ja està exclòs
    exclusio_existent = TemaExclusio.query.filter_by(tema_id=tema_id, pais_id=pais_id).first()
    if exclusio_existent:
        flash(f'"{tema.nom}" ja està exclòs de {pais.nom}', 'warning')
        return redirect(url_for('admin_tematiques.llistar_categories', pais_id=pais_id))
    
    # Crear exclusió
    exclusio = TemaExclusio(tema_id=tema_id, pais_id=pais_id)
    db.session.add(exclusio)
    db.session.commit()
    
    flash(f'✓ Tema "{tema.nom}" exclòs de {pais.nom}', 'success')
    return redirect(url_for('admin_tematiques.llistar_categories', pais_id=pais_id))