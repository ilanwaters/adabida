# SESSIÓ 4 DESEMBRE 2024 - Adabida
## Arquitectura Internacional de Països i Temes

**Durada:** ~4 hores  
**Focus principal:** Sistema de països amb temes històrics per país + Disseny portada estil Wikipedia

---

## 🎯 OBJECTIU INICIAL

Crear un sistema on:
- Usuaris puguin **seleccionar un país**
- Cada país tingui els seus **temes històrics específics**
- Exemple: España → Guerra Civil, ETA / Alemanya → Reunificació, Mur de Berlín / Perú → Sendero Luminoso
- Sistema **escalable** per afegir nous països manualment
- Preparar terreny per **traducció automàtica futura** (LibreTranslate en local)

---

## ✅ TASQUES COMPLETADES

### 1. **Disseny Portada Estil Wikipedia**
- Layout en dues columnes: menú lateral (250px) + contingut dreta
- Quadre de benvinguda centrat amb lema potent
- Menú lateral amb desplegables de Família i Organitzacions
- Grid de temes 3x3 amb botó "Més/Menys" funcional
- Estil sobri: fons gris clar, borders subtils, sense colors cridaners

### 2. **Sistema de Temes en Grid**
- 18 temes totals: 9 visibles + 9 ocults (desplegable)
- Grid responsive (3 columnes desktop, 2 tablet, 1 mòbil)
- Botó "Pots parlar-nos de qualsevol tema aquí" al final
- Usuaris logejats → enllaços a `/nova_entrada_personal?titol=NomTema`
- Usuaris NO logejats → modal motivadora

### 3. **Modal Motivadora per Usuaris No Logejats**
- Modal centrada amb overlay
- Contingut: "No tens perfil?" + explicació preservació rigorosa
- Botons: "Crear perfil" (obre disclaimer) + "Iniciar sessió"
- Tots els textos amb `{{ _() }}` per Babel
- Tancament: clic fora o botó ×

### 4. **Menú Lateral Desplegable**
- Desplegables funcionals per Família i Organitzacions
- JavaScript `toggleSubmenu()` per obrir/tancar
- Només un desplegable obert a la vegada
- Fletxa animada (▼ → ▲)
- Enllaços condicionals segons usuari logejat o no

### 5. **Títol Pre-omplert en Nova Entrada**
- Ruta `nova_entrada_personal()` modificada per acceptar `?titol=`
- Paràmetre `titol_preomplert` passat al template
- Camp títol amb `value="{{ titol_preomplert if titol_preomplert else ... }}"`
- Funcional per usuaris logejats

### 6. **Discussió Estratègica: LibreTranslate**
- Exploració de traducció automàtica **local** (open source, gratis)
- +100 idiomes suportats
- Cost €0, privacitat total, alineat amb filosofia Adabida
- **DECISIÓ:** Deixar per últim pas de producció (backlog)
- De moment: només arquitectura de països/temes

---

## 🚧 TASQUES INCOMPLETES / PROBLEMES ACTUALS

### ❌ Selector de País - BLOCAT

**Objectiu:** Selector discret "Tria un país: [España ▼]" amb camp manual per afegir nous països

**Estat actual:** 
- HTML creat correctament
- CSS creat amb múltiples versions (discret, inline, z-index)
- JavaScript `canviarPais()`, `guardarPaisNou()`, `cancelarPaisManual()` implementat
- **PROBLEMA PERSISTENT:** No s'ha aconseguit un funcionament estable

**Problemes trobats durant la sessió:**
1. ✅ Grid duplicat (dos `<div class="grid-temes">` niats) → Resolt
2. ✅ Selector massa llarg → Ajustat amb max-width
3. ✅ Camp manual no apareixia a sota → Reestructurat HTML
4. ✅ Estil "Hollywood" (massa cridaner) → Simplificat a discret
5. ⚠️ "Tria un país" i selector en línies separades → Parcialment resolt amb flex
6. ⚠️ Selector torna a ser massa llarg → Afegit max-width amb !important
7. ❌ **Camp manual no apareix o no es pot escriure** → NO RESOLT

**Última versió de fitxers creats:**
- `html_selector_final.html` - HTML del selector
- `css_amb_zindex.css` - CSS amb z-index per capes
- `js_selector_final.js` - JavaScript amb funcions

**Diagnòstic pendent:**
- Test amb `document.getElementById('pais-manual-container').style.display = 'flex'` per determinar si és problema CSS o JS
- Possible conflicte amb altres CSS del projecte
- Possible problema amb l'ordre de càrrega de scripts

---

## 📁 FITXERS GENERATS DURANT LA SESSIÓ

### HTML
- `caixa_temes_amb_selector.html` - Caixa temes amb selector inicial
- `html_selector_final.html` - HTML selector versió final
- `selector_pais_correcte.html` - HTML amb camp manual a sota

### CSS
- `css_selector_pais.css` - Primera versió CSS selector
- `selector_inline.css` - CSS per selector inline
- `inici_discret.css` - CSS discret i elegant
- `css_selector_final.css` - CSS final abans z-index
- `css_selector_discret.css` - Versió discreta (blanc)
- `fix_grid_ample.css` - Fix per grid ample complet
- `css_amb_zindex.css` - **VERSIÓ FINAL** amb z-index

### JavaScript
- `js_selector_pais.js` - Primera versió JS
- `js_selector_final.js` - **VERSIÓ FINAL** amb guardat provisional

### Altres
- `nova_entrada_modificat.py` - Backend per títol pre-omplert
- Múltiples versions de `inici.html` (no guardades, només snippets)

---

## 🗂️ ARQUITECTURA PLANEJADA (NO IMPLEMENTADA)

### Models de Base de Dades

```python
class Pais(db.Model):
    __tablename__ = 'paisos'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))  # "España", "Perú"
    codi = db.Column(db.String(2), unique=True)  # "ES", "PE"
    actiu = db.Column(db.Boolean, default=True)
    
    # Relacions
    categories = db.relationship('CategoriaTema', backref='pais')


class CategoriaTema(db.Model):
    __tablename__ = 'categories_tema'
    
    id = db.Column(db.Integer, primary_key=True)
    pais_id = db.Column(db.Integer, db.ForeignKey('paisos.id'))
    nom = db.Column(db.String(100))  # "Política", "Conflictes armats"
    ordre = db.Column(db.Integer, default=0)
    
    # Relacions
    temes = db.relationship('Tema', backref='categoria')


class Tema(db.Model):
    __tablename__ = 'temes'
    
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categories_tema.id'))
    nom = db.Column(db.String(100))  # "Guerra Civil", "Sendero Luminoso"
    ordre = db.Column(db.Integer, default=0)
```

### Jerarquia Prevista

```
País: España
  ├─ Categoria: Política
  │    ├─ Tema: Guerra Civil
  │    ├─ Tema: Dictadura Franco
  │    └─ Tema: Transició
  │
  ├─ Categoria: Conflictes armats
  │    ├─ Tema: ETA
  │    └─ Tema: GRAPO
  │
  └─ Categoria: Societat
       ├─ Tema: Migració
       └─ Tema: Feminisme

País: Perú
  ├─ Categoria: Conflictes armats
  │    ├─ Tema: Sendero Luminoso
  │    └─ Tema: MRTA
  │
  └─ Categoria: Política
       └─ Tema: Dictadura Fujimori
```

### Rutes API Planejades

```python
# POST /api/pais/crear
# Body: { "nom": "Perú" }
# Response: { "success": true, "codi": "PE", "id": 5 }

# GET /api/temes-pais/<codi>
# Response: {
#   "pais": "España",
#   "categories": [
#     {
#       "nom": "Política",
#       "temes": ["Guerra Civil", "Dictadura Franco", "Transició"]
#     },
#     {
#       "nom": "Conflictes armats",
#       "temes": ["ETA", "GRAPO"]
#     }
#   ]
# }
```

---

## 💡 DECISIONS ESTRATÈGIQUES PRESES

### 1. Internacionalització
- **Adabida = Arxiu MUNDIAL** (no només català)
- Cada país amb temes històrics específics
- Usuari pot navegar entre països
- Usuari pot contribuir a qualsevol país (no limitat per ubicació)

**Casos d'ús identificats:**
- Català a Alemanya → comparteix experiència sobre reunificació
- Alemany a Argentina → documenta vivències de Videla
- Palestí a Palestina → veu temes en àrab (futur amb traducció)

### 2. Traducció Automàtica
- **LibreTranslate** en local (última fase producció)
- NO queda obsolet Babel (`.po` per interfície)
- Babel = tradueix **interfície** (botons, menús)
- LibreTranslate = tradueix **contingut** (entrades usuaris)
- Les dues tecnologies són **complementàries**

**Filosofia:**
- Fase inicial: LibreTranslate local (€0)
- Si creix: més recursos servidor
- Si molt èxit: considerar DeepL API (amb ingressos)

### 3. Sistema de Països Manual
- Dropdown amb països predefinits + opció "Un altre país..."
- Camp manual per escriure país nou
- Es guarda a BD via API
- S'afegeix automàticament al dropdown
- Admin pot gestionar països i temes posteriorment

### 4. Disseny Visual
- **Estil Wikipedia**: sobri, professional, funcional
- Sense colors cridaners (blaus suaus, grisos)
- Tipografia clara (Montserrat)
- Espaciats generosos
- Grid responsive
- Menú lateral fix amb desplegables

---

## 🎨 ESTAT VISUAL ACTUAL

### Portada (funcionant)
```
┌────────────────────────────────────────────┐
│  BENVINGUTS A ADABIDA                      │
│  La teva vida, la teva visió...            │
└────────────────────────────────────────────┘

┌──────────┬─────────────────────────────────┐
│ Navega:  │  Explica'ns sobre...            │
│          │                                 │
│ • Adabida│  Tria un país: [España ▼]      │
│ • Espai  │                                 │
│          │  [Guerra] [Pandèmia] [Green.]   │
│ ▼ Família│  [Dicta.] [Cultura]  [Femin.]   │
│   Crear  │  [Exilis] [Migració] [Drets]    │
│   Arbre  │  [▼ Més]                        │
│          │                                 │
│ ▼ Orgs   │  [Pots parlar de qualsevol...]  │
│   Crear  │                                 │
│          │  Altres persones ens han...     │
│ • Galeria│  [En desenvolupament]           │
│ • Blog   │                                 │
└──────────┴─────────────────────────────────┘
```

### Selector País (problemàtic)
**Intent 1-5:** Massa llarg, no alineat, estil Hollywood
**Intent 6-8:** Discret però camp manual no funciona
**Estat actual:** BLOCAT - cal debugging

---

## 📋 PRÒXIMS PASSOS RECOMANATS

### OPCIÓ A - Continuar amb Selector (debugging profund)
1. Test JavaScript a consola per veure si camp apareix
2. Revisar conflictes CSS amb altres fitxers del projecte
3. Simplificar: eliminar tot el CSS del selector i començar de zero
4. Provar amb un HTML mínim aïllat

### OPCIÓ B - Deixar Selector per Després (avançar funcionalitat)
1. **Hardcodejar** "España" de moment
2. Implementar **backend**: models BD (Pais, Categoria, Tema)
3. Crear **panel admin** per gestionar països i temes
4. Implementar **carrega dinàmica** de temes des de BD
5. Tornar al selector quan hi hagi backend funcionant

**RECOMANACIÓ:** **Opció B** - Avançar amb backend i tornar al selector després

### Tasques Backend (Prioritat Alta)
```python
# 1. Crear models (30 min)
# 2. Migració BD (5 min)
# 3. Script seed inicial amb España i 18 temes (15 min)
# 4. Ruta GET /api/temes-pais/<codi> (20 min)
# 5. JavaScript actualitzarGridTemes() (30 min)
# 6. Provar amb España hardcoded (10 min)
# 7. Implementar selector un cop funciona (20 min)
```

**Total estimat:** ~2h per tenir sistema complet funcionant

---

## 🔍 APRENENTATGES DE LA SESSIÓ

### Tècnics
- Els `<select>` tenen comportament especial amb amplada
- `display: flex` no sempre funciona sense `!important` si hi ha conflictes CSS
- Niuar `<div>` amb mateix ID/class causa problemes imprevisibles
- El z-index només funciona amb `position: relative/absolute/fixed`

### Metodològics
- ⚠️ **Passar massa temps en CSS/visual sense backend = frustració**
- ✅ Millor: **MVP backend primer, després polir visual**
- ⚠️ Fer canvis incrementals sense testejar = efecte dominó
- ✅ Millor: **Testejar cada canvi abans de seguir**

### Estratègics
- 🎯 La visió d'Adabida internacional és **molt potent**
- 💡 LibreTranslate local és **perfecte** per filosofia del projecte
- 🌍 Sistema de països escalable pot **multiplicar usuaris x10**
- 📈 Diferenciador clar vs altres plataformes de testimonis

---

## 💭 REFLEXIÓ FINAL

Hem avançat molt en **conceptualització i estratègia**:
- Visió clara d'Adabida internacional
- Arquitectura de BD ben pensada
- Decisions de tecnologia (LibreTranslate) intel·ligents
- Disseny portada estil Wikipedia funcional

Però hem quedat **bloquejats en detall CSS/JS** del selector.

**Proposta per propera sessió:**
1. Deixar selector de banda temporalment
2. Implementar backend (models + API)
3. Fer funcionar carrega dinàmica de temes
4. Tornar al selector amb backend funcionant

Això donarà **motivació** i **context real** per acabar el selector!

---

## 📊 RESUM SESSIÓ

| Aspecte | Estat |
|---------|-------|
| **Disseny portada** | ✅ Completat |
| **Grid temes** | ✅ Funcional |
| **Modal motivadora** | ✅ Funcional |
| **Menú desplegable** | ✅ Funcional |
| **Títol pre-omplert** | ✅ Funcional |
| **Selector país** | ❌ Blocat |
| **Backend països/temes** | ⏳ Pendent |
| **Carrega dinàmica** | ⏳ Pendent |
| **Panel admin** | ⏳ Pendent |

**Temps invertit:** ~4 hores  
**Funcionalitats completades:** 5/9  
**Bloquejos actuals:** 1 (selector)  
**Propera sessió:** Backend + API

---

*"A vegades cal fer un pas enrere per poder avançar millor" - Ilan & Claude, 4 desembre 2024*

---

## 🎯 CHECKLIST PROPERA SESSIÓ

### Backend (2h estimades)
- [ ] Crear models `Pais`, `CategoriaTema`, `Tema`
- [ ] Migració BD
- [ ] Script seed amb España + 18 temes
- [ ] Ruta `GET /api/temes-pais/<codi>`
- [ ] JavaScript `actualitzarGridTemes()`
- [ ] Provar amb España hardcoded
- [ ] Si funciona → Implementar selector de país

### Alternatiu (si hi ha temps)
- [ ] Panel admin bàsic per gestionar països
- [ ] Panel admin per gestionar temes
- [ ] Començar sistema de categories

---

**Document creat:** 4 desembre 2024 - 21:20h  
**Projecte:** Adabida - Arxiu internacional de memòria oral  
**Sessió:** Arquitectura de països i temes històrics
