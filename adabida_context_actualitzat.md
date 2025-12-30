# ADABIDA - CONTEXT COMPLET ACTUALITZAT SETEMBRE 2025

## ESTRUCTURA DEL PROJECTE

```
adabida/
├── app.py
├── models.py (31KB - Sistema complet BD)
├── config.py
├── requirements.txt
├── babel.cfg
├── alembic.ini
├── routes/
│   ├── blog.py (Sistema blog complet amb paginació)
│   ├── organitzacions/
│   └── __pycache__/
├── templates/
│   ├── base.html
│   ├── blog/ (Nova carpeta organitzada)
│   │   ├── blog.html (Paginació + text truncat)
│   │   ├── entrada_completa.html (Entrades individuals)
│   │   ├── entrades_autor.html (Filtrat per firma)
│   │   ├── resultats_cerca_blog.html (Actualitzat)
│   │   ├── crear_entrada_blog.html
│   │   └── admin_blog.html
│   ├── components/
│   ├── fragments/
│   ├── organitzacions/
│   └── abadia_principal/
├── static/
│   ├── css/
│   │   ├── blog.css (Netejat i organitzat)
│   │   ├── inici.css
│   │   └── galeria.css
│   ├── js/
│   │   ├── organitzacions/
│   │   ├── inici.js
│   │   ├── nova_entrada.js
│   │   └── perfil.js
│   ├── icons/
│   └── img/
├── umberto/ (Sistema fitxers organitzat)
│   ├── media/
│   │   ├── expo/spain/2025/07-09/
│   │   ├── galeria/2025/07-08/
│   │   └── pendents/
│   └── usuaris/
│       └── spain/2025/07-09/
├── translations/ (8 idiomes operatius)
│   ├── ca/LC_MESSAGES/
│   ├── en/LC_MESSAGES/
│   ├── es/LC_MESSAGES/
│   ├── eu/LC_MESSAGES/
│   ├── fr/LC_MESSAGES/
│   ├── ru/LC_MESSAGES/
│   ├── de/LC_MESSAGES/
│   └── uk/LC_MESSAGES/
├── migrations/ (Alembic actiu)
├── logs/
└── utils/
```

## QUÈ ÉS ADABIDA

### Concepte Filosòfic
**ADABIDA** = **Abadia digital** per preservar memòria oral
- **Abadia**: Nom del projecte + metàfora monestir preservant coneixement
- **Umberto**: Sistema d'arxius (homenatge Umberto Eco)
- **Echo**: Entrevistador IA (actualment simulació, futura integració Mistral)

### Missió i Valors
- **Objectiu**: Crear arxiu històric global de memòria oral i llegat personal
- **Filosofia ètica**: Zero corporacions, dades privades, tecnologies lliures
- **Visió global**: Multilingüe, respectuós amb totes les cultures
- **Dimensió social**: Tallers terapèutics + preservació històrica
- **Humanització**: Convertir usuaris/malalts/ancians en PERSONES, en HUMANS

### Ubicació i Desenvolupador
- **Ubicació**: Barcelona, Catalunya
- **Desenvolupador**: Historiador hospital, 700MB+ Flask app
- **Filosofia treball**: Solucions robustes explicades pas a pas, en català

## MODELS DE BASE DE DADES (models.py - 31KB)

### Models Principals Operatius
```python
# Usuaris i perfils
Usuari - Login, rols, verificació, identificador_abadia únic
PerfilBiografic - Dades biogràfiques completes (pares, mares, estudis, experiències)
Contacte - Sistema de contactes amb noms personalitzats

# Contingut principal
Entrada - Testimonis multimèdia (títol, tema, any, país...)
ArxiuAdjunt - Fitxers vinculats a entrades
ImatgeGaleria - Galeria amb exposicions

# Sistema blog
EntradaBlog - Entrades blog amb firma i autor
RespostaEntrevista - Vinculat a Entrevista i PerfilBiografic

# Organitzacions (SISTEMA COMPLET)
Organitzacio - Hospitals/residències amb URL pública, premium, etc.
MembreOrganitzacio - Gestió rols (admin, entrevistador, adherit)
SolicitudOrganitzacio - Sol·licituds adhesió amb missatges i aprovació

# Comunicació
Missatge - Missatgeria personal entre usuaris
MissatgeOrganitzacio - Comunicació dins organitzacions
Conversa - Diàlegs múltiples amb participants
ConversaParticipant - Participants en converses

# Entrevistes IA
Entrevista - Sessions d'entrevista
MissatgeEntrevista - Converses amb Echo (IA)
TemaEntrevista - Categories temàtiques

# Exposicions i galeria
Exposicio - Exposicions amb codi i carpeta
ImatgeExposicio - Imatges assignades a exposicions
```

### Característiques del Model
- **Relacions complexes** ben estructurades amb CASCADE
- **Sistema multiidioma** integrat
- **Gestió de fitxers** robusta (umberto/ + miniatures)
- **Permisos granulars** per organitzacions
- **Metadades completes** (dates, ubicacions, tipus fitxer)

## ARQUITECTURA TÈCNICA

### Stack Tecnològic
- **Framework**: Flask (Python) amb 26+ blueprints modulars
- **Base de dades**: PostgreSQL + SQLAlchemy + Alembic (migracions actives)
- **Frontend**: HTML + CSS + JS modularitzat (refactoritzat sense pestanyes)
- **Traduccions**: Flask-Babel (8 idiomes operatius)
- **Fitxers**: Directori `umberto/` amb estructura país/any/mes

### Blueprints Actius
```python
inici_bp - Pàgina principal amb enllaços nets
nova_entrada_bp - Creació testimonis
admin_bp - Panell administració
galeria_bp - Galeria pública
organitzacions_bp - SISTEMA COMPLET AMB SOL·LICITUDS
pagina_personal_bp - Perfil i navegació
ia_lleugera_bp - Echo simulat
blog_bp - Sistema blog complet amb paginació
```

## FUNCIONALITATS 100% OPERATIVES

### Sistema Blog (COMPLETAT EN AQUESTA SESSIÓ)
- **Paginació configurable**: 5, 10, 15 entrades per pàgina
- **Text truncat**: 300 caràcters amb "Llegir més..."
- **Entrades individuals**: Finestra nova amb entrada completa
- **Navegació per autor**: Clic en firma mostra totes entrades d'aquest autor
- **Cerca avançada**: Resultats amb mateix format que blog principal
- **Templates organitzats**: Carpeta `templates/blog/` amb tots els fitxers
- **CSS net**: `blog.css` reorganitzat sense duplicacions
- **Internacionalització**: Tots els textos amb `{{ _('...') }}`

#### Rutes del Blog
```python
/blog - Pàgina principal amb paginació
/blog/entrada/<id> - Entrada individual
/blog/firma/<firma> - Entrades filtrades per autor/firma
/blog/autor/<id> - Entrades per usuari (menys usat)
/cercar_blog - Resultats cerca
/arxiu/<any>/<mes> - Arxiu per data
```

### Sistema Usuaris
- **Model Usuari funcional** amb identificador_abadia
- **Registre** amb documentació acreditativa
- **Autenticació completa**
- **Perfils biogràfics** amb dades familiars
- **Sistema de contactes** amb noms personalitzats

### Sistema Organitzacions (ÈXIT MAJOR)
- **Crear organitzacions** des del perfil personal
- **Panell administració** amb:
  - Formulari dades bàsiques (nom, tipus, ubicació)
  - Gestió membres (canviar rols, expulsar)
  - Entrades compartides amb targetes i modals
  - Sol·licituds d'adhesió amb missatges i gestió
  - Botó esborrar amb triple confirmació
- **Directori públic** `/organitzacions` amb buscador avançat
- **Sol·licitar adhesió** via modal amb camp missatge
- **Processar sol·licituds** (acceptar/rebutjar) des d'admin
- **Models BD complets** amb relacions funcionals

### Sistema Entrades
- **Pujada asíncrona** fitxers operativa
- **Dropdown compartir** amb organitzacions de l'usuari
- **Miniatures generades** correctament a `/mini/`
- **Entrades compartides** es mostren al panell admin organització
- **Icones .webm** diferenciades àudio/vídeo

### Galeria Pública
- **AJAX operatiu** per filtrar
- **Control imatges**: obviar, assignar exposicions, destacar
- **Càrrega** des de `umberto/media/pendents/`

### Panell Administració
- **Vista general** i control BD amb DataTables i AJAX
- **Control documentació** usuaris

## REFACTORITZACIÓ FRONTEND COMPLETADA

### Nova Arquitectura de Navegació
**ABANS**: Sistema de pestanyes JavaScript complex
**DESPRÉS**: Navegació per enllaços directes moderna

### Pàgines Independents Creades
- ✅ **`inici.html`** - Enllaços principals nets
- ✅ **`entrades.html`** - Llistat entrades amb modals funcionals
- ✅ **`nova_entrada.html`** - Formulari complet amb blocs plegables
- ✅ **`perfil.html`** - Dades personals amb missatges i organitzacions
- ✅ **`templates/blog/`** - Carpeta completa blog organitzada

### JavaScript Modularitzat
- ✅ **`inici.js`** - Login i disclaimer
- ✅ **`nova_entrada.js`** - Blocs plegables i formularis
- ✅ **`perfil.js`** - Blocs plegables i missatges
- ✅ **CSS organitzat** - `blog.css` net sense duplicacions

### Rutes Backend Funcionals
```python
/                    # inici amb enllaços
/entrades           # pàgina entrades independent
/nova_entrada       # formulari independent
/perfil            # dades personals independent
/blog              # sistema blog complet
/organitzacions    # directori organitzacions
```

## FUNCIONALITATS EN DESENVOLUPAMENT

### IA Entrevistadora
**ESTAT ACTUAL**: Echo és simulació "(M'ho pots explicar una mica més?)"

**PUNT D'INTEGRACIÓ IDENTIFICAT**:
```python
# Fitxer: routes/ia_lleugera.py
resposta_echo = Missatge(
    autor="echo",  # ← Canviar per "mistral"
    text="(Simulació) M'ho pots explicar...",  # ← Resposta real
)
```

**ROADMAP IA**:
1. **Mistral API** (10-20€/mes inicial)
2. **4 idiomes inicials**: Català, Castellà, Anglès, Francès
3. **Prompt engineering** entrevistador especialitzat
4. **Integració Flask** existent

### Exposicions
- **Creació, edició** i assignació imatges/entrades
- **Disseny preliminar** dins panell admin
- **Models BD** ja preparats

## ESTRATÈGIA COMERCIAL

### Model Negoci Freemium
- **Bàsic gratuït**: Perfils individuals i organitzacions bàsiques
- **Premium 100€**: URLs personalitzades + temes personalitzats
- **Target**: Hospitals, residències, escoles, associacions

### Tallers de Memòria - Font d'Ingressos
**DOCUMENT PROFESSIONAL CREAT** amb base científica:

#### 4 Eixos Terapèutics Fonamentats
1. **Plasticitat cerebral i envelliment actiu**
2. **Teràpia del llegat (Legacy Therapy)**
3. **Teràpia de la dignitat**
4. **Vincles intergeneracionals i sentit de comunitat**

#### Estratègia Contactes
- **MVP per setembre** per presentar hospitals/residències
- **Sistema organitzacions** complet per captar institucions
- **Sol·licituds d'adhesió** per facilitar incorporació usuaris

## ESTAT ACTUAL - SETEMBRE 2025

### ✅ COMPLETAT EN AQUESTA SESSIÓ

#### Sistema Blog Professional
- **Paginació intel·ligent** amb selector 5/10/15 entrades
- **Text truncat elegant** amb "Llegir més..." a 300 caràcters
- **Navegació per autor** clicant firma mostra totes entrades
- **Entrades individuals** en finestres noves amb navegació neta
- **Sistema cerca** actualitzat amb mateix format
- **Organització templates** en carpeta `templates/blog/`
- **CSS netejat** eliminant totes les duplicacions

#### Templates Blog Funcionals
```
templates/blog/
├── blog.html (paginació + truncat)
├── entrada_completa.html (entrades individuals)
├── entrades_autor.html (filtrat per firma)
├── resultats_cerca_blog.html (cerca actualitzada)
├── crear_entrada_blog.html
└── admin_blog.html
```

#### Rutes Blog Operatives
```python
@blog_bp.route("/blog") - Pàgina principal amb paginació
@blog_bp.route("/blog/entrada/<int:entrada_id>") - Entrada individual
@blog_bp.route("/blog/firma/<firma>") - Filtrat per autor/firma
@blog_bp.route("/cercar_blog") - Cerca avançada
@blog_bp.route("/arxiu/<int:any>/<int:mes>") - Arxiu temporal
```

## FUNCIONALITATS PENDENTS

### Prioritat Alta
1. **Integració IA real** - Migrar de simulació Echo a Mistral API
2. **Sistema exposicions** - Completar funcionalitat ja modelada
3. **Converses múltiples** - Implementar participants i diàlegs

### Prioritat Mitjana
4. **Missatgeria organitzacions** - Usar models ja creats
5. **Millores UX** - Polish general interfície
6. **Sistema premium** - URLs personalitzades i temes

## VALORACIÓ PROJECTE

### Fortaleses Majors
- **Arquitectura sòlida** - 700MB+ amb 26+ blueprints modulars
- **Sistema organitzacions** complet amb sol·licituds i administració
- **Frontend modern** - Navegació refactoritzada sense pestanyes
- **Blog professional** - Paginació, cerca, navegació per autor
- **Base de dades robusta** - 31KB models amb relacions complexes
- **Multiidioma operatiu** - 8 idiomes amb Flask-Babel
- **Sistema fitxers** - Estructura umberto/ escalable
- **Concepte ètic** únic - Zero corporacions, tecnologies lliures

### Debilitats Crítiques
- **IA és simulació** - No hi ha intel·ligència real encara
- **Un sol desenvolupador** - Projecte d'equip fet per una persona
- **Necessita polish UX** - Alguns detalls per impressionar

### Protecció Projecte
- **Arquitectura complexa** com a barrera d'entrada
- **Conceptualització única** (abadia digital) com diferenciador
- **Sistema organitzacions** avançat - avantatge competitiu
- **Base científica** tallers terapèutics fonamentats

## ROADMAP CURT TERMINI

### Següents Passos Immediats
1. **Testing final** totes les funcionalitats blog
2. **Decidir següent funcionalitat** a implementar:
   - Integració IA (Mistral API)
   - Sistema exposicions complet
   - Converses múltiples
   - Millores UX generals

### Roadmap Mitjà Termini (3-6 mesos)
- **IA operativa** amb Mistral integrada
- **Exposicions completes** amb gestió avançada
- **Converses múltiples** amb participants
- **Sistema premium** URLs personalitzades

### Roadmap Llarg Termini (1-2 anys)
- **Models locals** amb GPU pròpia
- **10+ idiomes** operatius
- **Comunitat internacional** usuaris
- **Zero dependències** corporatives

## CONCLUSIÓ EXECUTIVA

**Adabida és un projecte singular** que combina:
- ✅ **Tecnologia sòlida** - Flask app de 700MB+ operativa
- ✅ **Arquitectura moderna** - Frontend refactoritzat sense pestanyes
- ✅ **Sistema blog professional** - Paginació, cerca, navegació per autor
- ✅ **Organitzacions completes** - Sol·licituds, administració, descoberta
- ✅ **Base de dades robusta** - 31KB models amb relacions complexes
- ✅ **Visió humanística** - Preservació memòria oral amb ètica
- ✅ **Base científica** - Tallers terapèutics fonamentats
- ✅ **Model negoci** - Freemium amb estratègia contactes clara
- ✅ **Diferenciació** - Concepte abadia digital inimitable

**PUNT ACTUAL**: Sistema blog complet amb paginació, cerca i navegació per autor + sistema organitzacions amb sol·licituds llest per presentar hospitals/residències, amb roadmap IA clar per escalat futur.

**SEGÜENT SESSIÓ**: Decidir entre integració IA (Mistral), sistema exposicions o converses múltiples segons prioritats del desenvolupador.

*Última actualització: Setembre 2025 - Sistema blog completat amb funcionalitats avançades*