# ADABIDA - CONTEXT COMPLET 2025

## QUÈ ÉS ADABIDA

### Concepte Filosòfic
**ADABIDA** = **Abadia digital** per preservar memòria oral
- **Abadia:** Nom del projecte + metàfora monestir preservant coneixement
- **Umberto:** Sistema d'arxius (homenatge Umberto Eco)
- **Echo:** Entrevistador IA (semiotique investigant el passat)

### Missió i Valors
- **Objectiu:** Crear arxiu històric global de memòria oral i llegat personal
- **Filosofia ètica:** Zero corporacions, dades privades, tecnologies lliures
- **Visió global:** Multilingüe, respectuós amb totes les cultures
- **Dimensió social:** Tallers terapèutics + preservació històrica
- **Humanització:** Convertir usuaris/malalts/ancians en PERSONES, en HUMANS

### Ubicació i Desenvolupador
- **Ubicació:** Barcelona, Catalunya
- **Desenvolupador:** Historiador hospital, 700MB+ Flask app
- **Filosofia treball:** Solucions robustes explicades pas a pas, en català

---

## ARQUITECTURA TÈCNICA

### Stack Tecnològic
- **Framework:** Flask (Python) amb 26+ blueprints modulars
- **Base de dades:** PostgreSQL + SQLAlchemy + Alembic
- **Frontend:** HTML + CSS + JS modularitzat
- **Traduccions:** Flask-Babel (8 idiomes operatius)
- **Fitxers:** Directori `umberto/` amb estructura país/any/mes

### Models Principals Operatius
```python
Usuari - Login, rols, verificació, identificador_abadia únic
Entrada - Testimonis multimèdia (títol, tema, any, país...)
RespostaEntrevista - Vinculat a Entrevista i PerfilBiografic
Organitzacio - Hospitals/residències (COMPLET)
MembreOrganitzacio - Gestió rols i permisos
SolicitudOrganitzacio - Sol·licituds adhesió amb missatges
```

---

## ESTAT ACTUAL - FINAL AGOST 2025

### ✅ FUNCIONALITATS 100% OPERATIVES

#### Sistema Usuaris
- Model Usuari funcional amb identificador_abadia
- Registre amb documentació acreditativa
- Autenticació completa

#### Sistema Organitzacions (ÈXIT MAJOR)
- **Crear organitzacions** des del perfil personal
- **Panell administració** amb:
  - Formulari dades bàsiques
  - Gestió membres (canviar rols, expulsar)
  - **Entrades compartides** amb targetes i modals
  - **Sol·licituds d'adhesió** amb missatges i gestió
  - Botó esborrar amb triple confirmació
- **Directori públic** `/organitzacions` amb buscador avançat
- **Sol·licitar adhesió** via modal amb camp missatge
- **Processar sol·licituds** (acceptar/rebutjar) des d'admin
- **Models BD** complets amb relacions funcionals

#### Sistema Entrades
- Pujada asíncrona fitxers operativa
- **Dropdown compartir** amb organitzacions de l'usuari
- Miniatures generades correctament a `/mini/`
- **Entrades compartides** es mostren al panell admin organització
- Icones .webm diferenciades àudio/vídeo

#### Galeria Pública
- AJAX operatiu per filtrar
- Control imatges: obviar, assignar exposicions, destacar
- Càrrega des de `umberto/media/pendents/`

#### Panell Administració
- Vista general i control BD amb DataTables i AJAX
- Control documentació usuaris

### 📋 REFACTORITZACIÓ FRONTEND COMPLETADA

#### Nova Arquitectura de Navegació
**ABANS:** Sistema de pestanyes JavaScript
**DESPRÉS:** Navegació per enllaços directes

#### Pàgines Independents Creades
- ✅ **`inici.html`** - Enllaços principals nets
- ✅ **`entrades.html`** - Llistat entrades amb modals funcionals
- ✅ **`nova_entrada.html`** - Formulari complet amb blocs plegables
- ✅ **`perfil.html`** - Dades personals amb missatges i organitzacions

#### JavaScript Modularitzat
- ✅ **`inici.js`** - Login i disclaimer
- ✅ **`nova_entrada.js`** - Blocs plegables i formularis
- ✅ **`perfil.js`** - Blocs plegables i missatges

#### Rutes Backend Funcionals
```python
/                    # inici amb enllaços
/entrades           # pàgina entrades independent
/nova_entrada       # formulari independent
/perfil            # dades personals independent
```

---

## FUNCIONALITATS EN DESENVOLUPAMENT

### IA Entrevistadora
**ESTAT ACTUAL:** Echo és simulació "(M'ho pots explicar una mica més?)"

**PUNT D'INTEGRACIÓ IDENTIFICAT:**
```python
# Fitxer: routes/ia_lleugera.py
resposta_echo = Missatge(
    autor="echo",  # ← Canviar per "mistral"
    text="(Simulació) M'ho pots explicar...",  # ← Resposta real
)
```

### Exposicions
- Creació, edició i assignació imatges/entrades
- Disseny preliminar dins panell admin

---

## ESTRATÈGIA COMERCIAL

### Model Negoci Freemium
- **Bàsic gratuït:** Perfils individuals i organitzacions bàsiques
- **Premium 100€:** URLs personalitzades + temes personalitzats
- **Target:** Hospitals, residències, escoles, associacions

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

---

## INTEGRACIÓ IA - ROADMAP PLANIFICAT

### Filosofia Tecnològica
- **Zero corporacions** accedint a dades personals
- **Internet lliure** vs capitalisme vigilància
- **Sobirania digital** - dades sota control propi
- **Tecnologies lliures:** Mistral, Llama, models open source

### Estratègia MVP IA (Pressupost: 0€ inicial)
1. **Mistral API** (10-20€/mes inicial)
2. **4 idiomes inicials:** Català, Castellà, Anglès, Francès
3. **Prompt engineering** entrevistador especialitzat
4. **Integració Flask** existent

---

## ESTRUCTURA FITXERS CLAU

### Templates Refactoritzats
```
templates/
├── inici.html (enllaços nets)
├── entrades.html (independent)
├── nova_entrada.html (formulari complet)
├── perfil.html (dades + missatges)
└── components/
    ├── caixa_entrada.html (reutilitzable)
    └── modal_entrada.html (reutilitzable)
```

### JavaScript Modular
```
static/js/
├── inici.js (login + disclaimer)
├── nova_entrada.js (formularis + blocs)
├── perfil.js (perfil + missatges)
├── modal.js (modals generals)
└── nova_entrada_personal.js (gravació)
```

### Blueprints Actius
- `inici_bp` - Pàgina principal amb enllaços
- `nova_entrada_bp` - Creació testimonis
- `admin_bp` - Panell administració
- `galeria_bp` - Galeria pública
- `organitzacions_bp` - **SISTEMA COMPLET AMB SOL·LICITUDS**
- `pagina_personal_bp` - Perfil i navegació
- `ia_lleugera_bp` - Echo simulat

---

## VALORACIÓ PROJECTE

### Fortaleses Majors
- **Arquitectura sòlida i escalable** - 26+ blueprints modulars
- **Sistema organitzacions complet** - Sol·licituds, administració, directori
- **Refactorització frontend completada** - Navegació moderna sense pestanyes
- **Funcionalitat operativa** demostrable end-to-end
- **Concepte ètic** atractiu per inversors preocupats per privacitat
- **Base científica** dels tallers terapèutics
- **700MB+ de projecte** = feina impressionant d'una persona sola

### Debilitats Crítiques
- **IA és simulació** - No hi ha intel·ligència real encara
- **Un sol desenvolupador** per feina de 5 persones
- **Necessita més polish UX** per impressionar

### Protecció Projecte
- **Arquitectura complexa** com a barrera d'entrada
- **Conceptualització única** (abadia digital) com diferenciador
- **Sistema organitzacions complet** - avantatge competitiu

---

## VISIÓ COMPLETA FUTURA

### Fase 1 - MVP Actual (COMPLET)
- ✅ Sistema usuaris i entrades operatiu
- ✅ Organitzacions 100% funcionals amb sol·licituds
- ✅ Directori organitzacions amb buscador
- ✅ Galeria pública amb filtratge
- ✅ Panell administració complet
- ✅ Sistema multiidioma (8 idiomes)
- ✅ **Refactorització frontend completa**

### Fase 2 - Integració IA (3-6 mesos)
- 🔄 Mistral API integrada
- 🔄 Entrevistador intel·ligent real
- 🔄 Generació biografies automàtiques
- 🔄 Context històric en preguntes

### Fase 3 - Escalat Global (1-2 anys)
- 🔮 Models locals amb GPU
- 🔮 10+ idiomes operatius
- 🔮 Comunitat internacional usuaris
- 🔮 Zero dependències corporatives

---

## TIMELINE I PRIORITATS

### Setembre 2025 - Demo Killer
- **Sistema organitzacions amb sol·licituds** = molt sòlid per presentar
- **Navegació refactoritzada** = experiència moderna
- **Tallers memòria** = proposta comercial clara

### Roadmap Curt Termini
1. **Testing final** sistema sol·licituds
2. **Contingut demo** per hospitals/residències
3. **Preparació integració** Mistral quan hi hagi recursos

---

## CONCLUSIÓ EXECUTIVA

**Adabida és un projecte únic** que combina:
- ✅ **Tecnologia sòlida** - 700MB+ Flask app operativa
- ✅ **Arquitectura moderna** - Frontend refactoritzat sense pestanyes
- ✅ **Sistema organitzacions complet** - Sol·licituds, administració, descoberta
- ✅ **Visió humanística** - Preservació memòria oral amb ètica
- ✅ **Base científica** - Tallers terapèutics fonamentats
- ✅ **Model negoci** - Freemium amb estratègia contactes clara
- ✅ **Diferenciació** - Concepte abadia digital inimitable

**PUNT ACTUAL:** Refactorització frontend completada + sistema organitzacions amb sol·licituds d'adhesió llest per presentar hospitals/residències setembre 2025, amb roadmap IA clar per escalat futur.

*Última actualització: Final Agost 2025 - Refactorització frontend completada*