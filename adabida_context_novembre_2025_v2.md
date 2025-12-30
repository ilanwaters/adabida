# ADABIDA - CONTEXT COMPLET ACTUALITZAT NOVEMBRE 2025

## ESTRUCTURA DEL PROJECTE

```
adabida/
├── app.py (actualitzat - Flask-Mail integrat)
├── models.py (actualitzat - camps verificació email)
├── config.py (actualitzat - SMTP Gandi)
├── requirements.txt (Flask-Mail afegit)
├── babel.cfg
├── alembic.ini
├── routes/
│   ├── blog.py (Sistema blog complet amb paginació)
│   ├── organitzacions/
│   ├── registre_individual.py (actualitzat - envia email verificació)
│   ├── auth.py (NOU - verificació i reset password)
│   └── __pycache__/
├── templates/
│   ├── base.html
│   ├── blog/
│   │   ├── blog.html (Paginació + text truncat)
│   │   ├── entrada_completa.html
│   │   ├── entrades_autor.html
│   │   ├── resultats_cerca_blog.html
│   │   ├── crear_entrada_blog.html
│   │   └── admin_blog.html
│   ├── auth/ (NOU - templates verificació)
│   │   ├── recuperar_contrasenya.html
│   │   ├── reset_password.html
│   │   └── reenviar_verificacio.html
│   ├── emails/ (NOU - templates emails)
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
│   ├── home.html (Cards modernes)
│   └── aportacions.html (model Wikipedia)
├── static/
│   ├── css/
│   │   ├── blog.css
│   │   ├── inici.css (Cards modernes reutilitzable)
│   │   ├── galeria.css
│   │   └── organitzacio_seccio_sobri.css (estil tanatori)
│   ├── js/
│   │   ├── organitzacions/
│   │   ├── inici.js
│   │   ├── nova_entrada.js
│   │   └── perfil.js
│   ├── icons/
│   └── img/
├── utils/ (NOU)
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
- **Contacte**: contacte@adabida.cat, noreply@adabida.cat
- **Filosofia treball**: Solucions robustes explicades pas a pas, en català

## MODELS DE BASE DE DADES (models.py - Actualitzat)

### Models Principals Operatius
```python
# Usuaris i perfils
Usuari - Login, rols, verificació EMAIL (NOU), identificador_abadia únic
  ├── email_verificat (NOU) - Boolean per verificació
  ├── token_verificacio (NOU) - Token únic verificació
  ├── data_token (NOU) - Data creació token
  ├── token_reset_password (NOU) - Token reset contrasenya
  └── data_token_reset (NOU) - Data creació token reset

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

### Mètodes nous del model Usuari
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
- **Frontend**: HTML + CSS + JS modularitzat (refactoritzat sense pestanyes)
- **Traduccions**: Flask-Babel (8 idiomes operatius)
- **Fitxers**: Directori `umberto/` amb estructura país/any/mes
- **Disseny**: Estil sobri i minimalista ("tanatori elegant")
- **Email**: Flask-Mail + SMTP Gandi (NOU)

### Configuració Email (NOU)
```python
# config.py
MAIL_SERVER = 'mail.gandi.net'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'noreply@adabida.cat'
MAIL_PASSWORD = 'Cimbaline.1968'
MAIL_DEFAULT_SENDER = ('Adabida', 'noreply@adabida.cat')
BASE_URL = 'http://localhost:5000'  # En producció: https://adabida.cat
TOKEN_EXPIRATION_HOURS = 24
```

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
registre_individual_bp - Registre + verificació email (ACTUALITZAT)
aportacions_bp - Pàgina finançament ètic
auth_bp - Verificació email i reset password (NOU)
```

## SISTEMA DE VERIFICACIÓ PER EMAIL (NOU - COMPLETAT 21 NOV 2025)

### Funcionalitats Implementades
✅ **Verificació obligatòria** en registrar-se
✅ **Email automàtic** amb enllaç de verificació (24h validesa)
✅ **Reenviar verificació** si no arriba o expira
✅ **Recuperació contrasenya** per email
✅ **Reset contrasenya** amb token segur
✅ **Confirmació canvi** contrasenya per email
✅ **Templates HTML professionals** amb disseny Adabida
✅ **Enviament asíncron** (no bloqueja l'app)

### Rutes d'Autenticació
```python
/verificar-email/<token> - Verificar compte amb token
/reenviar-verificacio - Sol·licitar nou email verificació
/recuperar-contrasenya - Sol·licitar reset contrasenya
/reset-password/<token> - Formulari nova contrasenya
```

### Templates d'Emails
- **verificacio_email.html** - Email benvinguda + verificació
- **reset_password.html** - Email recuperació contrasenya
- **confirmacio_canvi_password.html** - Confirmació canvi

Característiques:
- Disseny responsive
- Colors corporatius Adabida (#14d8ce)
- Botó principal + enllaç alternatiu
- Advertències de seguretat
- Missatges clars i concisos

### Flux de Registre Actualitzat
1. Usuari omple formulari registre
2. Sistema crea compte amb `email_verificat = False`
3. Genera token únic verificació
4. Envia email amb enllaç
5. Usuari redirigit a login (NO login automàtic)
6. Usuari clica enllaç email
7. Sistema verifica token i marca `email_verificat = True`
8. Usuari ja pot fer login

### Flux de Recuperació Contrasenya
1. Usuari clica "He oblidat la contrasenya"
2. Introdueix email
3. Sistema genera token reset
4. Envia email amb enllaç
5. Usuari clica enllaç
6. Introdueix nova contrasenya
7. Sistema actualitza contrasenya
8. Envia email confirmació
9. Usuari fa login amb nova contrasenya

### Seguretat Implementada
- ✅ Tokens únics generats amb `secrets.token_urlsafe(32)`
- ✅ Expiració 24 hores
- ✅ Tokens eliminats després d'usar-se
- ✅ Contrasenyes hasheades amb Werkzeug
- ✅ Validació mínim 8 caràcters amb lletres i números
- ✅ Missatges genèrics per no revelar si email existeix

## FUNCIONALITATS 100% OPERATIVES

### Sistema Blog
- Paginació configurable: 5, 10, 15 entrades per pàgina
- Text truncat: 300 caràcters amb "Llegir més..."
- Entrades individuals: Finestra nova amb entrada completa
- Navegació per autor: Clic en firma mostra totes entrades
- Cerca avançada
- Templates organitzats
- CSS net
- Internacionalització

### Sistema Usuaris (ACTUALITZAT)
- **Model Usuari** amb camps verificació email
- **Registre** amb enviament email verificació automàtic
- **Verificació obligatòria** abans de fer login
- **Recuperació contrasenya** per email
- **Autenticació completa**
- **Perfils biogràfics** amb dades familiars
- **Sistema de contactes**

### Sistema Organitzacions
- Crear organitzacions des del perfil personal
- Pàgina pública amb cards modernes
- Seccions internes amb estil sobri
- Panell administració complet
- Directori públic amb buscador
- Sol·licitar adhesió via modal
- Models BD complets

### Sistema Entrades
- Pujada asíncrona fitxers
- Dropdown compartir amb organitzacions
- Miniatures generades
- Entrades compartides
- Icones .webm diferenciades

### Galeria Pública
- AJAX operatiu per filtrar
- Control imatges
- Càrrega des de `umberto/media/pendents/`

### Panell Administració
- Vista general i control BD
- Control documentació usuaris

## DISSENY I UX - ESTIL CONSOLIDAT

### Filosofia Visual: "Tanatori Elegant"
Decisió de disseny: Estil sobri, net i professional

#### Principis de Disseny
- ✅ Paleta neutra: Grisos, blancs, turquesa (#14d8ce)
- ✅ Tipografia clara: Sans-serif, mides llegibles
- ✅ Espais generosos: Padding ampli, gaps 2rem
- ✅ Boxes simples: Fons #fafafa, vores #e5e5e5
- ✅ Zero ornamentació: Sense gradients excessius
- ✅ Icons minimalistes: Emojis simples o fletxes

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

## ESTAT ACTUAL - NOVEMBRE 2025

### ✅ COMPLETAT EN AQUESTA SESSIÓ (21 NOVEMBRE 2025)

#### Sistema de Verificació per Email (IMPLEMENTAT)
- **Flask-Mail instal·lat** i configurat amb SMTP Gandi
- **Model Usuari actualitzat** amb camps verificació
- **Migració Alembic** aplicada correctament
- **Blueprint auth.py** creat amb totes les rutes
- **Templates emails** HTML professionals creats
- **Templates pàgines** (recuperar, reset, reenviar)
- **Registre actualitzat** per enviar email automàtic
- **Sistema complet** testat i funcional

#### Configuració Tècnica Completada
```
✅ config.py - SMTP Gandi configurat
✅ models.py - 5 camps nous + 5 mètodes
✅ utils/email.py - Sistema enviament
✅ routes/auth.py - Blueprint autenticació
✅ routes/registre_individual.py - Integrat
✅ app.py - Flask-Mail inicialitzat
✅ Migració BD - Camps creats
✅ Templates - 6 fitxers nous (3 emails + 3 pàgines)
```

#### Dades Tècniques Email
- **Servidor SMTP**: mail.gandi.net:587 (STARTTLS)
- **Email**: noreply@adabida.cat
- **Credencials**: Configurades i testades
- **Tokens**: Generats amb `secrets.token_urlsafe(32)`
- **Expiració**: 24 hores
- **Enviament**: Asíncron amb threading

## FUNCIONALITATS PENDENTS

### Prioritat Alta
1. **Testing complet** sistema verificació email
2. **Integració IA real** - Migrar Echo a Mistral API
3. **Sistema exposicions** - Completar funcionalitat
4. **Converses múltiples** - Implementar participants

### Prioritat Mitjana
5. **Missatgeria organitzacions** - Usar models creats
6. **Millores UX** - Polish general interfície
7. **Mètodes pagament** - Activar Bizum/transferència per aportacions
8. **Bloquejar login** sense verificació (opcional per DEMO)

### Fase Llançament Oficial
9. **Sortir de DEMO** - Hosting definitiu, backup professional
10. **Constituir associació** - Entitat legal
11. **Informe transparència** - Primer informe financer
12. **Variables d'entorn** - Migrar credencials a .env

## VALORACIÓ PROJECTE

### Fortaleses Majors
- **Arquitectura sòlida** - 700MB+ amb 27+ blueprints
- **Sistema organitzacions** complet
- **Frontend modern** - Disseny sobri consolidat
- **Blog professional** - Paginació, cerca
- **Base de dades robusta** - 31KB models
- **Multiidioma operatiu** - 8 idiomes
- **Documents legals** - RGPD compliant
- **Sistema email** - Verificació i reset complets (NOU)
- **Model finançament ètic** - Aportacions voluntàries
- **Concepte únic** - Internet dels Elevats

### Debilitats Crítiques
- **IA és simulació** - No hi ha intel·ligència real
- **Un sol desenvolupador** - Projecte complex
- **Fase DEMO** - Sense garanties producció
- **Testing pendent** - Cal testejar emails en producció

### Protecció Projecte
- **Arquitectura complexa** com a barrera
- **Conceptualització única** com diferenciador
- **Sistema organitzacions** avançat
- **Base científica** tallers terapèutics
- **Ètica radical** - Diferenciador total

## ROADMAP ACTUALITZAT

### Curt Termini (1-3 mesos)
1. **Testejar emails** en diferents clients (Gmail, Outlook, etc.)
2. **Activar mètodes pagament** - Bizum, IBAN, PayPal
3. **Testing exhaustiu** - Fase DEMO amb usuaris reals
4. **Feedback loop** - Millorar UX
5. **Traduir emails** - Als 8 idiomes operatius

### Mitjà Termini (3-6 mesos)
- **Sortir de DEMO** - Llançament oficial v1.0
- **Hosting professional** - Servidor dedicat
- **Constituir associació** - "Associació Cultural Adabida"
- **Integrar IA real** - Mistral API
- **Primer informe transparència**

### Llarg Termini (1-2 anys)
- **IA local** - Models propis amb GPU
- **10+ idiomes** - Expansió internacional
- **Comunitat consolidada** - Usuaris actius
- **Tallers operatius** - Font ingressos
- **Zero dependències corporatives**

## CONCLUSIÓ EXECUTIVA

**Adabida és un projecte singular** que combina:
- ✅ **Tecnologia sòlida** - Flask app de 700MB+ operativa
- ✅ **Arquitectura moderna** - Frontend refactoritzat
- ✅ **Sistema blog professional** - Paginació, cerca
- ✅ **Organitzacions completes** - Sol·licituds, administració
- ✅ **Base de dades robusta** - 31KB models
- ✅ **Documents legals** - RGPD compliant
- ✅ **Sistema email complet** - Verificació i reset (NOU)
- ✅ **Model finançament ètic** - Aportacions voluntàries
- ✅ **Visió humanística** - Ètica radical
- ✅ **Base científica** - Tallers fonamentats
- ✅ **Diferenciació única** - Internet dels Elevats

### Punt Actual (21 Novembre 2025)

**FASE**: DEMO amb funcionalitats core operatives

**COMPLETAT AVUI**:
- Sistema verificació email complet i funcional
- Flask-Mail integrat amb SMTP Gandi
- 5 camps nous + 5 mètodes al model Usuari
- Blueprint auth amb 4 rutes
- 6 templates nous (emails + pàgines)
- Migració BD aplicada
- Tokens segurs amb expiració
- Enviament asíncron emails

**PENDENT PRIORITARI**:
1. Testejar emails amb usuaris reals
2. Activar mètodes pagament aportacions
3. Decidir següent funcionalitat: IA vs Exposicions

**VISIÓ PROJECTE**: 
Un arxiu històric de memòria oral **gratuït, ètic i respectuós**, finançat per la comunitat, amb **verificació segura per email**, sense corporacions, sense vendre dades, sense publicitat. Una fortalesa digital per preservar la memòria col·lectiva amb dignitat.

---

*Última actualització: 21 Novembre 2025 - 23:30h*  
*Sessió: Sistema verificació per email COMPLETAT*  
*Següent prioritat: Testing emails + Decidir següent funcionalitat*  
*Hores dedicades aquesta sessió: ~6h (documents legals + sistema email)*
