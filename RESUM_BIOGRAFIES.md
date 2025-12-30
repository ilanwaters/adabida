# 📖 RESUM: Sistema de Biografies Adabida

**Data:** 29 novembre 2025  
**Estat:** ✅ FUNCIONANT

---

## 🎯 Què hem implementat

Un sistema complet d'**edició de biografies** amb TinyMCE que permet als usuaris escriure la seva història personal amb un editor de text ric (format, imatges, enllaços a entrades).

**Funciona per:**
- 👤 Perfils personals → "La meva biografia"
- 👨‍👩‍👧‍👦 Famílies → "Història de la família" (pendent adaptar)
- 🏛️ Organitzacions → "Història de l'organització" (pendent adaptar)

---

## 🎨 Disseny visual

```
┌─────────────────────────────────────────┐
│  El meu espai › Biografia               │
│                                          │
│  📖 La meva biografia                   │
│  La meva història, els meus orígens     │
├─────────────────────────────────────────┤
│                                          │
│  👁️ BIOGRAFIA PUBLICADA                 │
│  ┌────────────────────────────────────┐ │
│  │ [Text renderitzat amb HTML]        │ │
│  │ - Format (negreta, cursiva...)     │ │
│  │ - Imatges                          │ │
│  │ - Enllaços a entrades              │ │
│  └────────────────────────────────────┘ │
│                                          │
├─────────────────────────────────────────┤
│                                          │
│  ✏️ EDITAR BIOGRAFIA                     │
│  ┌────────────────────────────────────┐ │
│  │ [Editor TinyMCE]                   │ │
│  │ - Toolbar amb format               │ │
│  │ - Botó pujar imatges               │ │
│  │ - Botó enllaçar entrades           │ │
│  └────────────────────────────────────┘ │
│                                          │
│  [Cancel·lar]  [💾 Guardar biografia]   │
│                                          │
│  [← Tornar]                              │
└─────────────────────────────────────────┘
```

**Filosofia de disseny:**
- **Part superior:** Text renderitzat (llegir primer)
- **Part inferior:** Editor (editar després)

---

## ✅ Tasques completades

### 1. Base de dades
- [x] Executat: `flask db migrate -m "Afegir camp biografia a usuari"`
- [x] Executat: `flask db upgrade`
- [x] Camp `biografia` (TEXT) afegit al model `Usuari`

### 2. Estructura de carpetes
```
routes/
└── pagina_personal/
    ├── __init__.py              (nou - imports dels blueprints)
    ├── pagina_personal.py       (existent - mogut dins carpeta)
    └── personal_biografia.py    (nou - 4 rutes biografia)
```

### 3. Rutes Python implementades

**Fitxer:** `routes/pagina_personal/personal_biografia.py`

```python
# 4 rutes creades:

@personal_biografia_bp.route('/biografia')
def biografia():
    # Mostra pàgina biografia

@personal_biografia_bp.route('/biografia/guardar', methods=['POST'])
def guardar_biografia():
    # Guarda biografia (AJAX)

@personal_biografia_bp.route('/biografia/pujar-imatge', methods=['POST'])
def pujar_imatge_biografia():
    # Puja imatges (PENDENT - decidir on guardar)

@personal_biografia_bp.route('/biografia/llistar-entrades')
def llistar_entrades_biografia():
    # Llista entrades per enllaçar
```

### 4. Templates

**Fitxer:** `templates/pagina_personal/personal_biografia.html`

Característiques:
- ✅ Visor de text renderitzat (part superior)
- ✅ Editor TinyMCE (part inferior)
- ✅ Formulari AJAX per guardar
- ✅ Botó cancel·lar amb confirmació
- ✅ Breadcrumb navegació
- ✅ Missatge si no hi ha biografia escrita

### 5. TinyMCE en local (sense API, sense CDN)

**Ubicació:** `static/js/tinymce/`

**Avantatges:**
- ✅ Zero dependències externes
- ✅ Cap API key necessària
- ✅ 100% privat (no envia dades a tercers)
- ✅ Funciona offline
- ✅ Més ràpid
- ✅ Total control del codi

**Canvi al template:**
```html
<!-- ABANS (CDN amb API key): -->
<script src="https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js"></script>

<!-- DESPRÉS (local sense API): -->
<script src="{{ url_for('static', filename='js/tinymce/tinymce.min.js') }}"></script>
```

### 6. CSS

**Fitxer:** `static/css/biografia.css`

Característiques:
- ✅ Disseny responsive
- ✅ Cards amb gradients
- ✅ Animacions suaus
- ✅ Colors coherents amb Adabida (#14d8ce)
- ✅ Tipografia llegible

### 7. Component modal

**Fitxer:** `templates/components/modal_seleccionar_entrada.html`

Per enllaçar entrades a la biografia:
- ✅ Llista entrades de l'usuari
- ✅ Cercador en temps real
- ✅ Radio buttons per seleccionar
- ✅ Insereix enllaç a TinyMCE

### 8. Blueprint registrat

**Fitxer:** `app.py`

```python
from routes.pagina_personal import pagina_personal_bp, personal_biografia_bp

app.register_blueprint(pagina_personal_bp)
app.register_blueprint(personal_biografia_bp)
```

### 9. Card al dashboard

Al dashboard personal s'ha afegit:

```html
<a href="{{ url_for('personal_biografia.biografia') }}" class="card">
  <div class="card-image" style="background-image: url('{{ url_for('static', filename='img/personal.png') }}');">
    <div class="card-overlay"></div>
  </div>
  <div class="card-content">
    <h3>{{ _('Biografia') }}</h3>
  </div>
</a>
```

---

## 📁 Fitxers creats/modificats

### Nous fitxers:
```
routes/pagina_personal/__init__.py
routes/pagina_personal/personal_biografia.py
templates/pagina_personal/personal_biografia.html
templates/components/modal_seleccionar_entrada.html
static/css/biografia.css
static/js/tinymce/ (carpeta sencera)
```

### Fitxers modificats:
```
app.py (registre blueprints)
models.py (camp biografia afegit)
templates/pagina_personal/pagina_personal.html (card biografia afegit)
```

---

## 🎨 Funcionalitats implementades

✅ **Editor de text ric:**
- Format: negreta, cursiva, subratllat
- Llistes ordenades/desordenades
- Alineació text
- Enllaços
- Imatges (pujada pendent implementar)
- Taules
- Codi
- Ajuda integrada

✅ **Visor:**
- HTML renderitzat amb format
- Imatges responsive
- Enllaços estilitzats
- Missatge elegant si buit

✅ **Guardar:**
- AJAX (sense recarregar pàgina)
- Confirmació d'èxit
- Gestió d'errors

✅ **Modal entrades:**
- Llista totes les entrades
- Cercador funcional
- Inserció automàtica d'enllaç

---

## ⚠️ Tasques pendents

### Crítica (abans de producció):
- [ ] **Implementar pujar imatges** (decidir ubicació: NO static)
- [ ] **Provar modal enllaçar entrades** amb dades reals
- [ ] **Validació i sanitització** d'HTML (seguretat)

### Mitjà termini:
- [ ] Adaptar sistema per **famílies** (història familiar)
- [ ] Adaptar sistema per **organitzacions** (història org)
- [ ] Sistema de **capítols** (dividir biografia en seccions)
- [ ] Control de **visibilitat** (públic/privat/família)
- [ ] **Exportar a PDF**

### Llarg termini:
- [ ] Col·laboració (familiars poden comentar)
- [ ] Versionat (historial de canvis)
- [ ] Timeline interactiva
- [ ] Estadístiques (paraules, temps dedicat)
- [ ] Traducció automàtica

---

## 🔧 Configuració TinyMCE

```javascript
tinymce.init({
  selector: '#editor-biografia',
  height: 500,
  menubar: false,
  language: 'ca', // Multilingual
  
  plugins: [
    'advlist', 'autolink', 'lists', 'link', 'image', 
    'charmap', 'preview', 'anchor', 'searchreplace',
    'visualblocks', 'code', 'fullscreen', 'insertdatetime',
    'media', 'table', 'help', 'wordcount'
  ],
  
  toolbar: 'undo redo | blocks | bold italic underline | ' +
           'alignleft aligncenter alignright | ' +
           'bullist numlist | link image | custom_entrada | ' +
           'removeformat | help',
  
  // Pujar imatges (URL pendent implementar)
  images_upload_url: '/perfil/biografia/pujar-imatge',
  automatic_uploads: true,
  
  // Botó personalitzat enllaçar entrades
  setup: function(editor) {
    editor.ui.registry.addButton('custom_entrada', {
      text: '📄 Entrada',
      tooltip: 'Enllaçar una entrada',
      onAction: function() {
        obrirModalEntrades();
      }
    });
  }
});
```

---

## 💾 Model de dades

```python
class Usuari(db.Model, UserMixin):
    # ... camps existents ...
    biografia = db.Column(db.Text, nullable=True)
```

**Capacitat:** PostgreSQL TEXT pot emmagatzemar fins a 1 GB de text (~150 milions de paraules).

---

## 🔒 Decisions ètiques preses

### TinyMCE:
✅ **Descarregat i hostatjat localment**
- Zero dependències externes
- Cap API key
- Cap connexió a tiny.cloud
- 100% privat
- Coherent amb filosofia Adabida

✅ **Watermark de TinyMCE mantingut**
- Reconeixement just al creador
- Programari lliure MIT
- Petit i discret

### Imatges (pendent):
⚠️ **NO es guardaran a /static**
- Per protecció de privacitat
- Ubicació a decidir:
  - Base de dades (BLOB)?
  - Carpeta separada fora static?
  - Sistema actual d'entrades?

---

## 🎯 Possibilitats futures

Aquest sistema és la **base** per:

📚 **Capítols:**
- Dividir biografia en seccions editables
- Reordenar capítols
- Índex automàtic

👁️ **Visibilitat:**
- Biografia pública/privada
- Capítols amb permisos diferents
- Compartir amb persones específiques

📊 **Estadístiques:**
- Paraules escrites
- Temps dedicat
- Progrés

📖 **Exportació:**
- PDF amb format
- ePub (llibre electrònic)
- Versió imprimible

🤝 **Col·laboració:**
- Familiars poden comentar
- Biografies col·lectives
- Suggeriments de correccions

🎤 **Multimèdia:**
- Àudios de relats orals
- Vídeos incrustats
- Galeries de fotos

---

## 📊 Comparativa amb competència

### StoryWorth (competidor comercial):
- ❌ Tancat i propietari
- ❌ 99$/any
- ❌ Només anglès
- ❌ Depens d'ells
- ❌ Les dades són seves

### Adabida (nosaltres):
- ✅ Codi lliure (privat ara, públic en futur?)
- ✅ Gratuït / Aportacions voluntàries
- ✅ 8 idiomes
- ✅ Control total
- ✅ Les dades són dels usuaris
- ✅ **Programari lliure i ètic**

---

## 🚀 Pròxims passos recomanats

### 1. Implementar pujar imatges (prioritat alta)
Decidir ubicació i implementar ruta `pujar_imatge_biografia()`

### 2. Provar amb dades reals
Escriure una biografia de prova completa per detectar errors

### 3. Adaptar per família
Copiar sistema i adaptar per "Història familiar"

### 4. Adaptar per organització
Copiar sistema i adaptar per "Història de l'organització"

### 5. Sistema de capítols
Permetre dividir biografies llargues en seccions

---

## 📚 Documentació útil

- **TinyMCE Docs:** https://www.tiny.cloud/docs/
- **Flask-Migrate:** https://flask-migrate.readthedocs.io/
- **Jinja2 Templates:** https://jinja.palletsprojects.com/

---

## ✨ Conclusió

**Sistema de biografies FUNCIONANT i OPERATIU!** 🎉

- ✅ Editor professional de text ric
- ✅ 100% privat i local
- ✅ Zero dependències externes
- ✅ Coherent amb filosofia Adabida
- ✅ Base sòlida per funcionalitats futures

**Pròxim repte:** Implementar pujar imatges i adaptar per família/organització.

---

**Data última actualització:** 29 novembre 2025  
**Estat del projecte:** MVP en desenvolupament  
**Sistema biografia:** ✅ Operatiu

---

🌟 **Adabida - Arxiu internacional de memòria oral**  
*Preservant històries amb dignitat i respecte*
