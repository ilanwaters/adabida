# ADABIDA - CONTEXT COMPLET ACTUALITZAT NOVEMBRE 2025

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
│   ├── registre_individual.py (+ ruta avís legal)
│   ├── aportacions.py (NOVA - finançament ètic)
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
│   │   ├── organitzacions.html (ACTUALITZAT - estil sobri)
│   │   └── seccio_home.html (ACTUALITZAT - estil sobri)
│   ├── abadia_principal/
│   │   ├── avis_legal.html (NOU - RGPD compliant)
│   │   └── manifest_etic.html (ACTUALITZAT - secció finançament)
│   ├── inici.html (Cards modernes)
│   ├── home.html (Cards modernes)
│   └── aportacions.html (NOVA - model Wikipedia)
├── static/
│   ├── css/
│   │   ├── blog.css (Netejat i organitzat)
│   │   ├── inici.css (Cards modernes reutilitzable)
│   │   ├── galeria.css
│   │   └── organitzacio_seccio_sobri.css (NOU - estil tanatori elegant)
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
- **Model finançament**: 100% gratuït, finançat per aportacions voluntàries (model Wikipedia)

### Ubicació i Desenvolupador
- **Ubicació**: Barcelona, Catalunya
- **Responsable**: Ilan Sánchez, historiador
- **Contacte**: contacte@adabida.cat
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
Organitzacio - Hospitals/residències amb URL pública, etc.
MembreOrganitzacio - Gestió rols (admin, entrevistador, adherit)
SolicitudOrganitzacio - Sol·licituds adhesió amb missatges i aprovació

# Comunicació
Missatge - Missatgeria personal entre usuaris
MissatgeOrganitzacio - Comunicació dins organitzacions
Conversa - Diàlegs múltiples amb participants
ConversaParticipant - Participants en converses

# Entrevistes IA (obsolet/no implementat/)
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
- **Disseny**: Estil sobri i minimalista ("tanatori elegant") - coherent i professional

### Blueprints Actius
```python
inici_bp - Pàgina principal amb cards modernes
home_bp - Adabida principal amb cards
nova_entrada_bp - Creació testimonis
admin_bp - Panell administració
galeria_bp - Galeria pública
organitzacions_bp - Sistema complet amb sol·licituds
pagina_personal_bp - Perfil i navegació
ia_lleugera_bp - Echo simulat
blog_bp - Sistema blog complet amb paginació
registre_individual_bp - Registre + avís legal
aportacions_bp - Pàgina finançament ètic (NOU)
```

## FUNCIONALITATS 100% OPERATIVES

### Sistema Blog
- **Paginació configurable**: 5, 10, 15 entrades per pàgina
- **Text truncat**: 300 caràcters amb "Llegir més..."
- **Entrades individuals**: Finestra nova amb entrada completa
- **Navegació per autor**: Clic en firma mostra totes entrades d'aquest autor
- **Cerca avançada**: Resultats amb mateix format que blog principal
- **Templates organitzats**: Carpeta `templates/blog/` amb tots els fitxers
- **CSS net**: `blog.css` reorganitzat sense duplicacions
- **Internacionalització**: Tots els textos amb `{{ _('...') }}`

### Sistema Usuaris
- **Model Usuari funcional** amb identificador_abadia
- **Registre** amb documentació acreditativa i acceptació termes ètics
- **Autenticació completa**
- **Perfils biogràfics** amb dades familiars
- **Sistema de contactes** amb noms personalitzats

### Sistema Organitzacions (ÈXIT MAJOR)
- **Crear organitzacions** des del perfil personal
- **Pàgina pública** amb cards modernes (estil actualitzat)
- **Seccions internes** amb estil sobri i espaiós
- **Panell administració** amb:
  - Formulari dades bàsiques (nom, tipus, ubicació)
  - Gestió membres (canviar rols, expulsar)
  - Entrades compartides amb targetes i modals
  - Sol·licituds d'adhesió amb missatges i gestió
  - Botó esborrar amb triple confirmació
- **Directori públic** `/organitzacions` amb buscador avançat
- **Sol·licitar adhesió** via modal amb camp missatge
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

## DISSENY I UX - ESTIL CONSOLIDAT

### Filosofia Visual: "Tanatori Elegant"
**Decisió de disseny**: Estil sobri, net i professional sense colors cridaners

#### Principis de Disseny
- ✅ **Paleta neutra**: Grisos, blancs, turquesa (#14d8ce) només per accents
- ✅ **Tipografia clara**: Sans-serif, mides llegibles, interlineat generós
- ✅ **Espais generosos**: Padding ampli, gaps de 2rem, max-width 800-1100px
- ✅ **Boxes simples**: Fons #fafafa, vores subtils #e5e5e5
- ✅ **Zero ornamentació**: Sense gradients, ombres o animacions excessives
- ✅ **Icons minimalistes**: Emojis simples o fletxes en text (← →)

#### Sistema de Cards Modernes (Reutilitzable)
**Fitxer CSS**: `inici.css`

Estructura estàndard per a pàgines principals:
```html
<div class="cards-grid">
  <a href="..." class="card">
    <div class="card-image" style="background-image: url('...');">
      <div class="card-overlay"></div>
    </div>
    <div class="card-content">
      <h3>Títol</h3>
      <p>Descripció breu</p>
    </div>
  </a>
</div>
```

Usat en:
- `inici.html` - Pàgina principal
- `home.html` - Adabida principal
- `organitzacions.html` - Pàgina organitzacions

#### CSS per Seccions Internes
**Fitxer CSS**: `organitzacio_seccio_sobri.css`

Característiques:
- Max-width 1100px (més espai que abans)
- Gaps de 2rem entre seccions
- Boxes amb padding 2rem
- Grid responsive automàtic
- Estadístiques destacades amb números grans
- Activitat recent amb icones emoji

## DOCUMENTS LEGALS I ÈTICS (COMPLETAT NOVEMBRE 2025)

### 1. Avís Legal DEMO
**Ruta**: `/avis-legal`  
**Template**: `templates/abadia_principal/avis_legal.html`

Contingut:
- ✅ Identificació del projecte (fase DEMO)
- ✅ Naturalesa experimental amb advertències
- ✅ Objectiu: arxiu històric públic
- ✅ Dret a l'oblit i eliminació total de dades
- ✅ Propietat intel·lectual (usuari conserva drets)
- ✅ Compartició amb organitzacions
- ✅ Compromisos ètics (transparència, tecnologies lliures, dades privades)
- ✅ **Secció finançament**: Model aportacions voluntàries
- ✅ Protecció de dades (RGPD compliant)
- ✅ Contacte i suport

**Característiques**:
- RGPD compliant
- Transparent sobre limitacions fase DEMO
- Enllaç a pàgina d'aportacions
- Text clar i entenedor (no legalès)

### 2. Pàgina d'Aportacions Voluntàries
**Ruta**: `/aportacions`  
**Template**: `templates/aportacions.html`  
**Blueprint**: `routes/aportacions.py`

**Model de finançament**: 100% gratuït + aportacions voluntàries (estil Wikipedia)

Contingut:
- ✅ **Per què aportacions voluntàries**: Raons ètiques (independència, privacitat, accessibilitat, dignitat)
- ✅ **Transparència financera**: Taula de costos detallada (servidors, hosting, domini, IA futura...)
- ✅ **Compromisos**: Mai cobrar, mai vendre dades, mai publicitat
- ✅ **Com aportar**: Bizum, transferència, targeta (pendent activació fase oficial)
- ✅ **Altres maneres d'ajudar**: Difusió, traduccions, disseny, desenvolupament
- ✅ **FAQs**: Gestió, transparència, avantatges (NO hi ha avantatges de pagament)

**Disseny**: Estil sobri amb taula de costos, boxes neutres, zero "Hollywood"

Enllaçat des de:
- Avís legal
- Manifest ètic
- Footer (recomanat)

### 3. Manifest Ètic (Actualitzat)
**Template**: `templates/abadia_principal/manifest_etic.html`

Contingut original mantingut:
- Prioritat testimonis vius, quotidians i plurals
- Continguts voluntaris i modificables
- No compartim dades personals amb tercers
- Valor històric de cada història
- **"Internet dels Elevats"**: Filosofia del projecte

**Secció afegida**:
- ✅ **El finançament d'aquesta trinxera**: Explicació model aportacions voluntàries
- ✅ Enllaç a pàgina d'aportacions
- ✅ Missatge: "Els teus records són part de la història"

**Disseny**: Minimalista amb interlineat 1.8, secció finançament amb línia separadora

## ESTRATÈGIA COMERCIAL ACTUALITZADA

### Model de Finançament: Aportacions Voluntàries
**DECISIÓ CLAU**: Canvi de model freemium a **100% gratuït finançat per la comunitat**

#### Model Wikipedia
- ✅ **Tot gratuït** per a tothom (individuals i organitzacions)
- ✅ **Zero funcionalitats de pagament** ni premium
- ✅ **Aportacions voluntàries** dels usuaris que valoren el projecte
- ✅ **Transparència total** sobre costos i despeses

#### Raons Ètiques
1. **Independència**: No dependre de corporacions
2. **Privacitat**: Dades no són producte
3. **Accessibilitat universal**: Memòria accessible a tothom
4. **Dignitat**: Records no són mercaderia
5. **Comunitat**: Projecte de tots, no d'una empresa

#### Costos Estimats Anuals
- Servidor i hosting: 500-800€
- Domini i SSL: 50-100€
- Còpies de seguretat: 100-200€
- Desenvolupament: Variable
- IA entrevistes (futur): 200-400€
- **TOTAL**: 850-1.500€/any inicial

#### Compromisos Públics
- ✅ Mai cobrar per l'accés
- ✅ Mai vendre dades
- ✅ Mai publicitat
- ✅ Publicar informe financer anual
- ✅ Tecnologies lliures
- ✅ Dret eliminació total

### Tallers de Memòria
**DOCUMENT PROFESSIONAL CREAT** amb base científica

#### 4 Eixos Terapèutics Fonamentats
1. **Plasticitat cerebral i envelliment actiu**
2. **Teràpia del llegat (Legacy Therapy)**
3. **Teràpia de la dignitat**
4. **Vincles intergeneracionals i sentit de comunitat**

#### Font d'Ingressos Complementària
- Tallers poden generar ingressos sense comprometre gratuïtat plataforma
- Target: Hospitals, residències, escoles, associacions
- No és el model principal, però complement sostenible

## ESTAT ACTUAL - NOVEMBRE 2025

### ✅ COMPLETAT EN AQUESTA SESSIÓ (21 NOVEMBRE 2025)

#### 1. Documents Legals i Ètics Complets
- **Avís Legal DEMO**: RGPD compliant, transparent, fase experimental
- **Pàgina Aportacions**: Model Wikipedia, transparència financera
- **Manifest Ètic actualitzat**: Secció finançament integrada
- **Blueprint aportacions**: Ruta `/aportacions` operativa

#### 2. Consolidació Estil Visual Sobri
- **home.html**: Adaptat a cards modernes (eliminats SVG)
- **organitzacions.html**: Adaptat a cards modernes
- **seccio_home.html**: CSS sobri amb més espai
- **CSS nou**: `organitzacio_seccio_sobri.css` - "tanatori elegant"
- **Eliminades dependències**: Zero FontAwesome, només emojis/text

#### 3. Model de Negoci Definit
- **Decisió estratègica**: Abandonat model freemium
- **Nou model**: 100% gratuït + aportacions voluntàries
- **Transparència**: Costos públics, compromisos clars
- **Ètica reforçada**: Mai vendre dades, mai publicitat

#### Fitxers Creats/Actualitzats Avui
```
templates/
├── abadia_principal/
│   ├── avis_legal.html (NOU)
│   └── manifest_etic.html (ACTUALITZAT)
├── aportacions.html (NOU)
├── home.html (ACTUALITZAT - cards)
└── organitzacions/
    ├── organitzacions.html (ACTUALITZAT - cards)
    └── seccio_home.html (ACTUALITZAT - estil sobri)

static/css/
└── organitzacio_seccio_sobri.css (NOU)

routes/
├── registre_individual.py (ACTUALITZAT - ruta avís legal)
└── aportacions.py (NOU)
```

## FUNCIONALITATS PENDENTS

### Prioritat Alta
2. **Sistema exposicions** - Completar funcionalitat ja modelada
3. **Converses múltiples** - Implementar participants i diàlegs

### Prioritat Mitjana
4. **Missatgeria organitzacions** - Usar models ja creats
5. **Millores UX** - Polish general interfície
6. **Mètodes pagament**: Activar Bizum/transferència/targeta per aportacions

### Fase Llançament Oficial
7. **Sortir de DEMO**: Activar hosting definitiu, backup professional
8. **Constituir associació**: Passar de persona física a entitat legal
9. **Informe transparència**: Primer informe financer públic
10. **URLs personalitzades**: Opcional per organitzacions (si hi ha demanda)

## VALORACIÓ PROJECTE

### Fortaleses Majors
- **Arquitectura sòlida** - 700MB+ amb 26+ blueprints modulars
- **Sistema organitzacions** complet amb sol·licituds i administració
- **Frontend modern** - Navegació refactoritzada, disseny sobri consolidat
- **Blog professional** - Paginació, cerca, navegació per autor
- **Base de dades robusta** - 31KB models amb relacions complexes
- **Multiidioma operatiu** - 8 idiomes amb Flask-Babel
- **Documents legals** - RGPD compliant, transparents, ètics
- **Model finançament ètic** - Aportacions voluntàries, zero vendes dades
- **Concepte únic** - Abadia digital, Internet dels Elevats
- **Disseny coherent** - Estil sobri i professional consolidat

### Debilitats Crítiques
- **Un sol desenvolupador** - Projecte d'equip fet per una persona
- **Fase DEMO** - Sense garanties producció completes
- **Mètodes pagament pendents** - Aportacions no activades encara

### Protecció Projecte
- **Arquitectura complexa** com a barrera d'entrada
- **Conceptualització única** (abadia digital) com diferenciador
- **Sistema organitzacions** avançat - avantatge competitiu
- **Base científica** tallers terapèutics fonamentats
- **Ètica radical** - Diferenciador total del mercat

## ROADMAP ACTUALITZAT

### Curt Termini (1-3 mesos)
1. **Activar mètodes pagament** - Bizum, IBAN, PayPal/Stripe per aportacions
2. **Testing exhaustiu** - Fase DEMO amb usuaris reals
3. **Feedback loop** - Millorar UX segons testers
4. **Traduir documents legals** - Als 8 idiomes operatius

### Mitjà Termini (3-6 mesos)
- **Sortir de DEMO** - Llançament oficial v1.0
- **Hosting professional** - Servidor dedicat amb backups
- **Constituir associació** - "Associació Cultural Adabida"
- **Integrar IA real** - Mistral API per entrevistes
- **Primer informe transparència** - Costos i ingressos públics

### Llarg Termini (1-2 anys)
- **IA local** - Models propis amb GPU
- **10+ idiomes** - Expansió internacional
- **Comunitat consolidada** - Usuaris actius aportant
- **Tallers operatius** - Font ingressos complementària
- **Zero dependències corporatives** - Sobirania digital total

## CONCLUSIÓ EXECUTIVA

**Adabida és un projecte singular** que combina:
- ✅ **Tecnologia sòlida** - Flask app de 700MB+ operativa
- ✅ **Arquitectura moderna** - Frontend refactoritzat, disseny sobri consolidat
- ✅ **Sistema blog professional** - Paginació, cerca, navegació per autor
- ✅ **Organitzacions completes** - Sol·licituds, administració, descoberta
- ✅ **Base de dades robusta** - 31KB models amb relacions complexes
- ✅ **Documents legals** - RGPD compliant, transparents, accessibles
- ✅ **Model finançament ètic** - Aportacions voluntàries, model Wikipedia
- ✅ **Visió humanística** - Preservació memòria oral amb ètica radical
- ✅ **Base científica** - Tallers terapèutics fonamentats
- ✅ **Diferenciació única** - Internet dels Elevats, abadia digital

### Punt Actual (21 Novembre 2025)

**FASE**: DEMO amb funcionalitats core operatives

**COMPLETAT**:
- Sistema blog amb paginació i cerca
- Organitzacions amb sol·licituds i administració
- Documents legals (Avís Legal + Aportacions + Manifest Ètic)
- Disseny sobri consolidat ("tanatori elegant")
- Model finançament definit (aportacions voluntàries)

**PENDENT PRIORITARI**:
1. Activar mètodes pagament per aportacions
2. Testing amb usuaris reals
3. Decidir següent gran funcionalitat: IA real vs Exposicions

**VISIÓ PROJECTE**: 
Un arxiu històric de memòria oral **gratuït, ètic i respectuós**, finançat per la comunitat que el valora, sense corporacions, sense vendre dades, sense publicitat. Una fortalesa digital per preservar la memòria col·lectiva amb dignitat.

---

*Última actualització: 21 Novembre 2025*  
*Sessió: Documents legals + Disseny sobri + Model finançament ètic*  
*Següent prioritat: Activar pagaments + Testing DEMO*
