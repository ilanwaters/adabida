# ADABIDA - CONTEXT COMPLET ACTUALITZAT 22 NOVEMBRE 2025

## ESTRUCTURA DEL PROJECTE

```
adabida/
├── .env (NOU - Variables d'entorn protegides)
├── .gitignore (NOU - Protecció fitxers sensibles)
├── app.py (actualitzat - Flask-Mail integrat)
├── models.py (actualitzat - camps verificació email)
├── config.py (ACTUALITZAT - Llegeix des de .env)
├── requirements.txt (Flask-Mail + python-dotenv afegits)
├── babel.cfg
├── alembic.ini
├── routes/
│   ├── blog.py (Sistema blog complet amb paginació)
│   ├── organitzacions/
│   ├── registre_individual.py (ACTUALITZAT - Pàgina confirmació)
│   ├── auth.py (Verificació i reset password)
│   ├── login.py (ACTUALITZAT - Bloqueig sense verificació)
│   └── __pycache__/
├── templates/
│   ├── base.html
│   ├── blog/
│   │   ├── blog.html (Paginació + text truncat + índex lateral)
│   │   ├── entrada_completa.html
│   │   ├── entrades_autor.html
│   │   ├── resultats_cerca_blog.html
│   │   ├── crear_entrada_blog.html
│   │   └── admin_blog.html
│   ├── auth/
│   │   ├── recuperar_contrasenya.html
│   │   ├── reset_password.html
│   │   ├── reenviar_verificacio.html
│   │   └── registre_complet.html (NOU - Confirmació registre)
│   ├── emails/
│   │   ├── verificacio_email.html
│   │   ├── reset_password.html
│   │   └── confirmacio_canvi_password.html
│   ├── components/
│   ├── fragments/
│   ├── organitzacions/
│   │   ├── organitzacions.html (estil sobri)
│   │   └── seccio_home.html (estil sobri)
│   ├── abadia_principal/
│   │   ├── avis_legal.html (RGPD compliant)
│   │   └── manifest_etic.html (secció finançament)
│   ├── inici.html (Cards modernes)
│   ├── home.html (NOU - Pàgina institucional amb índex lateral)
│   └── aportacions.html (model Wikipedia)
├── static/
│   ├── css/
│   │   ├── blog.css (Estil editorial elegant)
│   │   ├── home.css (NOU - Mateix estil que blog)
│   │   ├── inici.css (Cards modernes reutilitzable)
│   │   ├── galeria.css
│   │   ├── estils_abadia.css (CSS global amb sticky fix)
│   │   └── organitzacio_seccio_sobri.css (estil tanatori)
│   ├── js/
│   │   ├── organitzacions/
│   │   ├── inici.js
│   │   ├── nova_entrada.js
│   │   └── perfil.js
│   ├── icons/
│   └── img/
├── utils/
│   └── email.py (Sistema enviament emails)
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
└── logs/
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
- **Contacte**: contacte@adabida.cat, noreply@adabida.cat
- **Filosofia treball**: Solucions robustes explicades pas a pas, en català

## MODELS DE BASE DE DADES (models.py)

### Models Principals Operatius
```python
# Usuaris i perfils
Usuari - Login, rols, verificació EMAIL, identificador_abadia únic
  ├── email_verificat - Boolean per verificació
  ├── token_verificacio - Token únic verificació
  ├── data_token - Data creació token
  ├── token_reset_password - Token reset contrasenya
  └── data_token_reset - Data creació token reset

PerfilBiografic - Dades biogràfiques completes
Contacte - Sistema de contactes amb noms personalitzats

# Contingut principal
Entrada - Testimonis multimèdia
ArxiuAdjunt - Fitxers vinculats a entrades
ImatgeGaleria - Galeria amb exposicions

# Sistema blog
EntradaBlog - Entrades blog amb firma i autor
RespostaEntrevista - Vinculat a Entrevista i PerfilBiografic

# Organitzacions
Organitzacio - Hospitals/residències
MembreOrganitzacio - Gestió rols
SolicitudOrganitzacio - Sol·licituds adhesió

# Comunicació
Missatge - Missatgeria personal
MissatgeOrganitzacio - Comunicació dins organitzacions
Conversa - Diàlegs múltiples
ConversaParticipant - Participants en converses

# Entrevistes IA
Entrevista - Sessions d'entrevista
MissatgeEntrevista - Converses amb Echo (IA)
TemaEntrevista - Categories temàtiques

# Exposicions i galeria
Exposicio - Exposicions amb codi i carpeta
ImatgeExposicio - Imatges assignades a exposicions
```

### Mètodes del model Usuari
```python
generar_token_verificacio() - Crea token únic verificació
generar_token_reset_password() - Crea token reset contrasenya
verificar_token(token, tipus) - Verifica validesa i expiració
eliminar_token_verificacio() - Neteja token després d'usar
eliminar_token_reset() - Neteja token reset després d'usar
```

## ARQUITECTURA TÈCNICA

### Stack Tecnològic
- **Framework**: Flask (Python) amb 27+ blueprints modulars
- **Base de dades**: PostgreSQL + SQLAlchemy + Alembic (migracions actives)
- **Frontend**: HTML + CSS + JS modularitzat
- **Traduccions**: Flask-Babel (8 idiomes operatius)
- **Fitxers**: Directori `umberto/` amb estructura país/any/mes
- **Disseny**: Estil sobri i minimalista ("tanatori elegant")
- **Email**: Flask-Mail + SMTP Gandi
- **Seguretat**: Variables d'entorn amb python-dotenv

### Configuració Seguretat (NOU - 22 NOV 2025)
```python
# .env (protegit amb .gitignore)
SECRET_KEY=clau-secreta-abadia
DATABASE_URL=postgresql://postgres:1234@localhost/bioteca
FLASK_ENV=development
FLASK_APP=app.py
MAIL_PASSWORD=Cimbaline.1968
BASE_URL=http://localhost:5000
TOKEN_EXPIRATION_HOURS=24
```

```python
# config.py (llegeix des de .env)
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
    # ... resta de configuració
```

### Blueprints Actius
```python
inici_bp - Pàgina principal amb cards modernes
home_bp - Pàgina institucional amb índex lateral (ACTUALITZAT)
nova_entrada_bp - Creació testimonis
admin_bp - Panell administració
galeria_bp - Galeria pública
organitzacions_bp - Sistema complet amb sol·licituds
pagina_personal_bp - Perfil i navegació
ia_lleugera_bp - Echo simulat
blog_bp - Sistema blog complet amb paginació i índex lateral
registre_individual_bp - Registre + pàgina confirmació (ACTUALITZAT)
aportacions_bp - Pàgina finançament ètic
auth_bp - Verificació email i reset password
login_bp - Login amb bloqueig sense verificació (ACTUALITZAT)
```

## SISTEMA DE VERIFICACIÓ PER EMAIL (COMPLETAT I FUNCIONAL)

### Funcionalitats Implementades
✅ **Verificació obligatòria** en registrar-se
✅ **Email automàtic** amb enllaç de verificació (24h validesa)
✅ **Pàgina confirmació** professio després del registre (NOU)
✅ **Bloqueig de login** sense verificar (NOU)
✅ **Reenviar verificació** si no arriba o expira
✅ **Recuperació contrasenya** per email
✅ **Reset contrasenya** amb token segur
✅ **Confirmació canvi** contrasenya per email
✅ **Templates HTML professionals** amb disseny Adabida
✅ **Enviament asíncron** (no bloqueja l'app)

### Flux de Registre Actualitzat (22 NOV 2025)
1. Usuari omple formulari registre
2. Sistema crea compte amb `email_verificat = False`
3. Genera token únic verificació amb `nou.generar_token_verificacio()`
4. Envia email amb enllaç
5. **Mostra pàgina de confirmació professional** (NOU)
6. Usuari clica enllaç email
7. Sistema verifica token i marca `email_verificat = True`
8. Usuari intenta fer login
9. **Sistema comprova verificació abans de permetre accés** (NOU)
10. Si verificat → Login correcte
11. Si no verificat → Redirigeix a reenviar verificació

### Templates i Rutes Noves
```python
# Template nou
templates/auth/registre_complet.html - Pàgina confirmació després registre

# Rutes actualitzades
/registre_individual - Mostra pàgina confirmació en comptes de redirect
/login - Comprova email_verificat abans de permetre login
```

## DISSENY I UX - ESTIL CONSOLIDAT

### Filosofia Visual: "Tanatori Elegant"
Decisió de disseny: Estil sobri, net i professional

#### Principis de Disseny
- ✅ Paleta neutra: Grisos, blancs, turquesa (#14d8ce), blau (#007bff)
- ✅ Tipografia clara: Georgia (contingut), Sans-serif (UI)
- ✅ Espais generosos: Padding ampli, gaps 2-3rem
- ✅ Boxes simples: Fons #fafafa, vores #e5e5e5
- ✅ Zero ornamentació: Sense gradients excessius
- ✅ Icons minimalistes: Emojis simples o fletxes

### Layout 2 Columnes (Blog i Home)
```
┌────────────────┬──────────────────────────────┐
│                │                              │
│   ÍNDEX/LATERAL│      CONTINGUT PRINCIPAL     │
│   (300px fix)  │      (flex: 2)               │
│   sticky top   │                              │
│   #f8f9fa      │                              │
│                │                              │
└────────────────┴──────────────────────────────┘
```

**Característiques:**
- Índex lateral sticky (es manté fix en scroll)
- Responsive: En mòbil, índex va a dalt
- Mateixos colors i tipografia
- Scroll suau amb ancoratges (#seccio)

## PÀGINA HOME INSTITUCIONAL (NOU - 22 NOV 2025)

### Estructura i Contingut
Pàgina amb índex lateral fix i 7 seccions principals:

1. **Qui som**
   - Què és Adabida
   - La nostra missió
   - Internet dels Elevats

2. **Com funciona**
   - Testimonis multimèdia
   - Perfil biogràfic
   - Galeria personal
   - Echo (IA)
   - Tallers terapèutics

3. **Manifest ètic**
   - Zero dependències corporatives
   - Les teves dades són teves
   - No som un producte
   - Tecnologies lliures
   - Accessibilitat universal
   - Respecte i dignitat

4. **Finançament transparent**
   - Model Wikipedia
   - Taula de costos anuals (850-1.500€)
   - Compromisos públics
   - Enllaç a pàgina d'aportacions

5. **Advertència important**
   - Box destacat en groc (#fff3cd)
   - Testimonis autèntics però NO verificats
   - Responsabilitat de l'usuari
   - Valor històric dels testimonis

6. **Documentació legal**
   - Avís legal i RGPD
   - Dret a l'oblit
   - Propietat intel·lectual
   - Limitacions fase DEMO

7. **Contacte**
   - Email, ubicació, responsable
   - Col·laboracions possibles

### Estil CSS
- Fitxer: `static/css/home.css`
- Layout idèntic al blog per continuïtat
- Índex lateral sticky amb `position: sticky; top: 2rem;`
- Ancoratges amb `scroll-behavior: smooth`
- Responsive adaptatiu

## FUNCIONALITATS COMPLETADES

### ✅ Sistema Usuaris i Autenticació
- **Registre** amb pàgina de confirmació professional
- **Verificació obligatòria** per email abans de login
- **Bloqueig de login** sense verificar
- **Recuperació contrasenya** per email
- **Perfils biogràfics** amb dades familiars
- **Sistema de contactes**

### ✅ Sistema Organitzacions
- Crear organitzacions des del perfil personal
- Pàgina pública amb cards modernes
- Seccions internes amb estil sobri
- Panell administració complet
- Directori públic amb buscador
- Sol·licitar adhesió via modal
- Models BD complets

### ✅ Sistema Entrades
- Pujada asíncrona fitxers
- Dropdown compartir amb organitzacions
- Miniatures generades
- Entrades compartides
- Icones .webm diferenciades

### ✅ Sistema Blog
- Paginació professional
- Índex lateral amb arxiu per mesos
- Cercador integrat
- Entrades per autor
- Text truncat amb "Llegir més"
- Estil editorial elegant

### ✅ Galeria Pública
- AJAX operatiu per filtrar
- Control imatges
- Càrrega des de `umberto/media/pendents/`

### ✅ Pàgina Home Institucional (NOU)
- 7 seccions amb contingut complet
- Índex lateral navegable
- Ancoratges funcionals
- Estil coherent amb blog
- Responsive

### ✅ Seguretat i Configuració
- Variables d'entorn amb `.env`
- Contrasenyes protegides
- `.gitignore` configurat
- python-dotenv instal·lat

## DOCUMENTS LEGALS I ÈTICS

### 1. Avís Legal DEMO
Ruta: `/avis-legal`
- RGPD compliant
- Transparent sobre limitacions fase DEMO
- Dret a l'oblit explicat
- Enllaç a pàgina d'aportacions

### 2. Pàgina d'Aportacions
Ruta: `/aportacions`
- Model finançament 100% gratuït
- Transparència financera amb taula costos
- Compromisos públics
- Estil sobri

### 3. Manifest Ètic
- Valors del projecte
- "Internet dels Elevats"
- Secció finançament integrada
- Ara també a la pàgina HOME

## ESTRATÈGIA COMERCIAL

### Model de Finançament: Aportacions Voluntàries
**Model Wikipedia**: 100% gratuït + aportacions voluntàries

#### Raons Ètiques
1. Independència: No dependre de corporacions
2. Privacitat: Dades no són producte
3. Accessibilitat universal
4. Dignitat: Records no són mercaderia
5. Comunitat: Projecte de tots

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

## ESTAT ACTUAL - 22 NOVEMBRE 2025

### ✅ COMPLETAT EN AQUESTA SESSIÓ (22 NOVEMBRE 2025)

#### 1. Sistema de Verificació Email - ARREGLAT I FUNCIONAL
**Problema detectat**: Els comptes es creaven sense verificar
**Solució implementada**:
- ✅ Afegit `email_verificat=False` al crear usuari
- ✅ Afegit `nou.generar_token_verificacio()` després de crear compte
- ✅ Creat template `registre_complet.html` per confirmació
- ✅ Modificat `registre_individual.py` per mostrar pàgina confirmació
- ✅ Modificat `login.py` per bloquejar login sense verificar
- ✅ **TESTAT I FUNCIONA AL 100%** ✅

#### 2. Sistema de Variables d'Entorn - IMPLEMENTAT
**Objectiu**: Protegir contrasenyes i dades sensibles
**Solució implementada**:
- ✅ Instal·lat `python-dotenv`
- ✅ Creat fitxer `.env` amb variables sensibles
- ✅ Modificat `config.py` per llegir des de `.env`
- ✅ Creat `.gitignore` per protegir fitxers
- ✅ Contrasenyes fora del codi → Seguretat millorada

#### 3. Pàgina HOME Institucional - CREADA
**Objectiu**: Pàgina informativa amb contingut complet
**Solució implementada**:
- ✅ Creat `home.html` amb 7 seccions
- ✅ Creat `home.css` amb estil idèntic al blog
- ✅ Índex lateral sticky funcional
- ✅ Ancoratges amb scroll suau
- ✅ Responsive adaptatiu
- ✅ Contingut complet: Qui som, Manifest, Finançament, Advertència, etc.

### 🎯 RESUM TÈCNIC AVUI
```
✅ registre_individual.py - Pàgina confirmació + email_verificat=False
✅ login.py - Bloqueig login sense verificar
✅ templates/auth/registre_complet.html - Template confirmació
✅ .env - Variables d'entorn
✅ .gitignore - Protecció fitxers
✅ config.py - Lectura des de .env
✅ templates/home.html - Pàgina institucional
✅ static/css/home.css - Estil home amb sticky
✅ static/css/estils_abadia.css - CSS global amb sticky fix
```

## FUNCIONALITATS PENDENTS

### Prioritat Alta
1. **Testing exhaustiu** amb usuaris reals
2. **Configurar SPF/DKIM** a Gandi (emails van a SPAM)
3. **Traduir templates nous** als 8 idiomes
4. **Integració IA real** - Migrar Echo a Mistral API
5. **Sistema exposicions** - Completar funcionalitat

### Prioritat Mitjana
6. **Missatgeria organitzacions** - Usar models creats
7. **PWA per mòbil** - Gravadora ràpida amb icona a inici
8. **Converses múltiples** - Implementar participants
9. **Millores UX** - Polish general interfície
10. **Mètodes pagament** - Activar Bizum/transferència per aportacions

### Fase Llançament Oficial
11. **Sortir de DEMO** - Hosting definitiu, backup professional
12. **Constituir associació** - Entitat legal
13. **Informe transparència** - Primer informe financer
14. **10+ idiomes** - Expansió internacional

## PROBLEMES CONEGUTS I SOLUCIONS

### 1. Emails van a SPAM
**Problema**: Els emails de verificació arriben a la carpeta de spam
**Causa**: Domini nou sense reputació, falta SPF/DKIM
**Solució**:
- Configurar SPF/DKIM a Gandi
- Warming del domini (enviar emails gradualment)
- Millorar contingut email (menys emojis, text clar)
- Considerar SendGrid/Mailgun en futur
- Demanar als usuaris que marquin "No és spam"

### 2. Disseny en constant revisió
**Problema**: Tendència a canviar disseny constantment
**Solució acordada**: 
- Congelar disseny actual durant 3 mesos
- Prioritzar funcionalitats i testing
- Deixar feedback usuaris reals decidir canvis
- Filosofia: "Un projecte acabat imperfecte > un projecte perfecte inacabat"

## VALORACIÓ PROJECTE

### Fortaleses Majors
- **Arquitectura sòlida** - 700MB+ amb 27+ blueprints
- **Sistema organitzacions** complet
- **Frontend modern** - Disseny sobri consolidat
- **Blog professional** - Paginació, cerca, índex lateral
- **Base de dades robusta** - 31KB models
- **Multiidioma operatiu** - 8 idiomes
- **Documents legals** - RGPD compliant
- **Sistema email** - Verificació i reset complets i FUNCIONALS
- **Seguretat** - Variables d'entorn implementades
- **Pàgina HOME** - Contingut institucional complet
- **Model finançament ètic** - Aportacions voluntàries
- **Concepte únic** - Internet dels Elevats

### Debilitats Crítiques
- **IA és simulació** - No hi ha intel·ligència real
- **Un sol desenvolupador** - Projecte complex
- **Fase DEMO** - Sense garanties producció
- **Emails a SPAM** - Cal configurar SPF/DKIM
- **Testing pendent** - Cal usuaris reals

### Protecció Projecte
- **Arquitectura complexa** com a barrera
- **Conceptualització única** com diferenciador
- **Sistema organitzacions** avançat
- **Base científica** tallers terapèutics
- **Ètica radical** - Diferenciador total

## ROADMAP ACTUALITZAT

### Curt Termini (1-3 setmanes)
1. **Configurar SPF/DKIM** a Gandi (1 hora)
2. **Testing exhaustiu** amb 5-10 comptes de prova (2 dies)
3. **Traduir templates nous** als 8 idiomes (1 dia)
4. **Activar mètodes pagament** - Bizum, IBAN (2 dies)
5. **Feedback loop** - Millorar UX segons testing

### Mitjà Termini (1-2 mesos)
- **PWA + Gravadora ràpida** - User-friendly mòbil
- **Integrar IA real** - Mistral API
- **Sistema exposicions complet**
- **Sortir de DEMO** - Llançament oficial v1.0
- **Hosting professional** - Servidor dedicat
- **Primer informe transparència**

### Llarg Termini (6-12 mesos)
- **Constituir associació** - "Associació Cultural Adabida"
- **IA local** - Models propis amb GPU
- **10+ idiomes** - Expansió internacional
- **Comunitat consolidada** - Usuaris actius
- **Tallers operatius** - Font ingressos
- **Zero dependències corporatives**

## DECISIÓ ESTRATÈGICA: CAMÍ DE CONSOLIDACIÓ

**Decisió presa**: Seguir el **Camí de Consolidació** abans d'afegir noves funcionalitats

### Filosofia
- **No afegir res nou** durant 2-3 setmanes
- **Només arreglar, testejar, documentar**
- **Quan tot funcioni al 100%** → llavors afegir coses noves

### Raons
✅ Tens **MOLTA feina feta** i és molt bona
✅ Millor tenir **10 coses que funcionin** que 20 a mitges
✅ Quan tot estigui sòlid, **afegir coses noves serà més fàcil**
✅ Els usuaris prefereixen **poc però que funcioni** que molt però buggy

### Pròxims Passos Immediats
1. ✅ Verificació email → **ARREGLAT**
2. ✅ Variables d'entorn → **IMPLEMENTAT**
3. ✅ Pàgina HOME → **CREADA**
4. ⬜ SPF/DKIM → PENDENT (30 min)
5. ⬜ Testing complet → PENDENT (2 dies)

## CONCLUSIÓ EXECUTIVA

**Adabida és un projecte singular** que combina:
- ✅ **Tecnologia sòlida** - Flask app de 700MB+ operativa
- ✅ **Arquitectura moderna** - Frontend consolidat
- ✅ **Sistema blog professional** - Layout 2 columnes elegant
- ✅ **Pàgina HOME completa** - Contingut institucional (NOU)
- ✅ **Organitzacions completes** - Sol·licituds, administració
- ✅ **Base de dades robusta** - 31KB models
- ✅ **Documents legals** - RGPD compliant
- ✅ **Sistema email complet** - Verificació FUNCIONAL al 100%
- ✅ **Seguretat implementada** - Variables d'entorn protegides
- ✅ **Model finançament ètic** - Aportacions voluntàries
- ✅ **Visió humanística** - Ètica radical
- ✅ **Base científica** - Tallers fonamentats
- ✅ **Diferenciació única** - Internet dels Elevats

### Punt Actual (22 Novembre 2025 - Final del dia)

**FASE**: DEMO amb funcionalitats core operatives

**COMPLETAT AVUI** (Sessió 22 NOV):
- ✅ Sistema verificació email → **ARREGLAT I FUNCIONAL**
- ✅ Variables d'entorn → **IMPLEMENTAT**
- ✅ Pàgina HOME institucional → **CREADA**
- ✅ Templates confirmació registre → **CREATS**
- ✅ Bloqueig login sense verificar → **IMPLEMENTAT**
- ✅ CSS home amb continuïtat blog → **CREAT**
- ✅ Índex lateral sticky → **FUNCIONAL**

**PENDENT PRIORITARI**:
1. Configurar SPF/DKIM a Gandi
2. Testing amb usuaris reals
3. Traduir templates nous

**VISIÓ PROJECTE**: 
Un arxiu històric de memòria oral **gratuït, ètic i respectuós**, finançat per la comunitat, amb **sistema de verificació segur i funcional**, **pàgina institucional completa**, **seguretat implementada**, sense corporacions, sense vendre dades, sense publicitat. Una fortalesa digital per preservar la memòria col·lectiva amb dignitat.

---

*Última actualització: 22 Novembre 2025 - 21:00h*  
*Sessió: Verificació email arreglada + Variables d'entorn + Pàgina HOME*  
*Següent prioritat: SPF/DKIM + Testing exhaustiu*  
*Hores dedicades aquesta sessió: ~4-5h*
*Estat general: MOLT POSITIU - Funcionalitats core operatives al 100%*
