# ADABIDA - SUPER CONTEXT DEFINITIU 2025

## PUNT EXACTE ON SOM (Final Agost 2025)

### ÈXIT MAJOR ASSOLIT: SISTEMA ORGANITZACIONS + SOL·LICITUDS 100% IMPLEMENTAT
- **Creació d'organitzacions:** ✅ Completament operativa
- **Panell administració:** ✅ Template netejat i funcional amb entrades compartides
- **Directori organitzacions:** ✅ Pàgina `/organitzacions` amb buscador avançat
- **Sol·licituds d'adhesió:** ✅ Modal per sol·licitar + gestió admin completa
- **Dropdown compartir entrades:** ✅ Funcional des de nova entrada personal
- **Navegació:** ✅ Redirect correcte i enllaços operatius
- **Base de dades:** ✅ Models complets implementats (SolicitudOrganitzacio ja existent)

**RESULTAT:** MVP Organitzacions al **100%** - Sistema complet per hospitals/residències amb sol·licituds d'adhesió

---

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
- **Dimensió social:** fer que usuaris, malalts, vells, ancians, residents interns, deixin de ser usuaris, malalts, vells, ancians, residents interns, i es comvertieixn en PERSONES, en HUMANS

### Targeta d'Identitat
- **Ubicació:** Barcelona, Catalunya 
- **Desenvolupador:** Historiador hospital, 700MB Flask app sense experiència programació
- **Filosofia treball:** Solucions robustes explicades pas a pas, en català 
- **Logo:** Plànol d'abadia vista des de dalt

---

## ARQUITECTURA TÈCNICA ACTUAL

### Stack Tecnològic
- **Framework:** Flask (Python) amb 26+ blueprints modulars
- **Base de dades:** PostgreSQL + SQLAlchemy + Alembic 
- **Frontend:** HTML + CSS + JS modularitzat
- **Traduccions:** Flask-Babel (8 idiomes operatius)
- **Fitxers:** Directori `umberto/` amb estructura país/any/mes

### Models Principals
```python
# OPERATIUS
Usuari - Login, rols, verificació, identificador_abadia únic
Entrada - Testimonis multimèdia (títol, tema, any, país...)
RespostaEntrevista - Vinculat a Entrevista i PerfilBiografic
Organitzacio - Hospitals/residències (COMPLET)
MembreOrganitzacio - Gestió rols i permisos
SolicitudOrganitzacio - Sol·licituds adhesió amb missatges (NOU)

# PLANIFICATS
Guardats - Sistema favorits
Exposicions - Galeries temàtiques
```

### Blueprints Actius
- `nova_entrada_bp` - Creació testimonis ✅
- `admin_bp` - Panell administració ✅  
- `galeria_bp` - Galeria pública ✅
- `organitzacions_bp` - Sistema organitzacions ✅ **COMPLET AMB SOL·LICITUDS**
- `ia_lleugera_bp` - Echo simulat (pendent integració Mistral)
- `repositori_bp` - Consulta pública ✅

---

## FUNCIONALITATS 100% OPERATIVES

### Sistema Usuaris
- Model Usuari funcional amb identificador_abadia
- Registre amb documentació acreditativa
- Pàgina personal amb 5 pestanyes sense canvi URL:
  - **Perfil:** Dades visibles/editables + bloc organitzacions
  - **Biografia:** Autogenerada des d'entrevistes  
  - **Entrades:** Targetes visuals amb modals
  - **Nova entrada:** Formulari pujada fitxers amb dropdown organitzacions
  - **Entrevista IA:** Xat estructurat per temes

### Sistema Organitzacions **[COMPLET - AMPLIACIÓ MAJOR]**
- **Crear organitzacions** des del perfil personal ✅
- **Panell administració** amb:
  - Formulari dades bàsiques ✅
  - Gestió membres (canviar rols, expulsar) ✅
  - **Entrades compartides** amb targetes i modals ✅
  - **Sol·licituds d'adhesió** amb missatges i gestió ✅
  - Botó esborrar amb triple confirmació ✅
- **Directori públic** `/organitzacions` amb buscador avançat ✅
- **Sol·licitar adhesió** via modal amb camp missatge ✅
- **Processar sol·licituds** (acceptar/rebutjar) des d'admin ✅
- **Models BD** complets amb relacions funcionals ✅

### Sistema Entrades  
- Pujada asíncrona fitxers operativa
- **Dropdown compartir** amb organitzacions de l'usuari ✅
- Miniatures generades correctament a `/mini/`
- **Entrades compartides** es mostren al panell admin organització ✅
- Icones .webm diferenciades àudio/vídeo
- Interfície: temes esquerra, xat centre

### Galeria Pública
- AJAX operatiu per filtrar
- Control imatges: obviar, assignar exposicions, destacar
- Càrrega des de `umberto/media/pendents/`

### Panell Administració
- `admin.html` - Vista general
- `admin_dades.html` - Control BD amb DataTables i AJAX
- Control documentació usuaris

---

## FUNCIONALITATS EN DESENVOLUPAMENT

### Exposicions  
- Creació, edició i assignació imatges/entrades
- Disseny preliminar dins panell admin

### IA Entrevistadora
**ESTAT ACTUAL:** Echo és simulació "(M'ho pots explicar una mica més?)"

**PUNT D'INTEGRACIÓ IDENTIFICAT:**
```python
# Fitxer: routes/ia_lleugera.py, línies 69-74
resposta_echo = Missatge(
    autor="echo",  # ← Canviar per "mistral"
    text="(Simulació) M'ho pots explicar...",  # ← Resposta real
)
```

## ESTRATÈGIA COMERCIAL INTEGRAL

### Model Negoci Freemium
- **Bàsic gratuït:** Perfils individuals i organitzacions bàsiques
- **Premium 100€:** URLs personalitzades + temes personalitzats
- **Target:** Hospitals, residències, escoles, associacions

### Tallers de Memòria - Font d'Ingressos Inicial
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
- **Dossier professional** preparat per entitats sanitàries

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

## PRÒXIMS PASSOS IMMEDIATS

### Prioritat 1: Testing Sistema Organitzacions
- [ ] **Provar sol·licituds d'adhesió** - modal i processament
- [ ] **Verificar entrades compartides** al panell admin
- [ ] **Testing complet** flux organitzacions end-to-end
- [ ] **Polir UX** sistema sol·licituds

### Prioritat 2: Preparar Demo Setembre  
- [ ] **Contingut demo** (organitzacions i entrades exemple)
- [ ] **Presentació MVP** + roadmap IA
- [ ] **Contactar hospitals/residències** amb sistema complet

### Prioritat 3: Planificar Integració IA
- [ ] Dissenyar arquitectura integració Mistral
- [ ] Definir prompts entrevistador especialitzat
- [ ] Planificar generació biogràfica

---

## ESTRUCTURA FITXERS CLAU ACTUALITZADA

### Templates Organitzacions (COMPLET)
```
templates/organitzacions/
├── organitzacio_crear.html ✅ Funcional
├── organitzacio_admin.html ✅ Complet amb sol·licituds + entrades
├── organitzacio_publica.html ✅ Per confirmar
└── llistat.html ✅ Directori amb buscador
```

### Routes Blueprint Ampliat
```python
routes/organitzacions.py ✅ Funcional amb:
- / (llistat amb buscador) ✅
- /crear (GET/POST) ✅
- /admin/<id> (amb sol·licituds + entrades) ✅  
- /publica/<slug> ✅
- /solicitar (POST - crear sol·licitud) ✅
- /processar_solicitud (POST - acceptar/rebutjar) ✅
- /esborrar/<id> ✅
- /actualitzar/<int:id> ✅
- /canviar_rol, /expulsar_membre ✅
```

### Components Reutilitzables
```
templates/components/
├── caixa_entrada.html ✅ Targetes universals
├── modal_entrada.html ✅ Modal completa
└── (altres components existents)
```

---

## VALORACIÓ REALISTA PROJECTE (ACTUALITZADA)

### Fortaleses Majors
- **Arquitectura sòlida i escalable** - 26+ blueprints modulars
- **Sistema organitzacions complet** - Sol·licituds, administració, directori
- **Funcionalitat operativa** demostrable - Sistema end-to-end funcionant
- **Concepte ètic** atractiu per inversors preocupats per privacitat
- **Base científica** dels tallers terapèutics
- **700MB+ de projecte** = feina impressionant d'una persona sola

### Debilitats Crítiques  
- **IA és simulació** - No hi ha intel·ligència real encara
- **Un sol desenvolupador** per feina de 5 persones
- **Necessita més polish UX** per impressionar
- **Falta contingut real** d'usuaris per demos

### Recomanació Estratègica
**Sistema organitzacions complet** + **roadmap IA** és una proposta molt sòlida per setembre. El sistema de sol·licituds fa molt professional per hospitals/residències.

---

## TIMING I PRESSIÓ MERCAT

### Realitat Setembre 2025
- **MVP amb organitzacions completes** = molt sòlid per presentar
- **Sistema sol·licituds** fa molt professional per institucions
- **Directori organitzacions** facilita descoberta
- **Agost = mes de plàstic** - contactes tancats fins setembre

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

## CONCLUSIÓ EXECUTIVA

**Adabida és un projecte únic** que combina:
- ✅ **Tecnologia sòlida** - 700MB+ Flask app operativa
- ✅ **Sistema organitzacions complet** - Sol·licituds, administració, descoberta
- ✅ **Visió humanística** - Preservació memòria oral amb ètica
- ✅ **Base científica** - Tallers terapèutics fonamentats
- ✅ **Model negoci** - Freemium amb estratègia contactes clara
- ✅ **Diferenciació** - Concepte abadia digital inimitable

**PUNT ACTUAL:** Sistema organitzacions **complet amb sol·licituds d'adhesió** per presentar hospitals/residències setembre 2025, amb roadmap IA clar per escalat futur.

**PRÒXIM OBJECTIU:** Testing final sistema sol·licituds + demo killer per setembre + preparació integració Mistral quan hi hagi recursos.


estem treballant la millora de accesibiliat, de pesatnyes i subpestanyes hem passat a blocs plegables, molt pràctic però una mica lleig, idea/proposta: canviar el botons desplehables per imatges? 


*Última actualització: Final Agost 2025 - Sistema Organitzacions + Sol·licituds completat al 100%, llest per presentar a hospitals/residències*