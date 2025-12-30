# CONTEXT: REFACTORITZACIÓ FRONTEND ADABIDA

## SITUACIÓ ACTUAL (Final Agost 2025)

### PROJECTE ADABIDA
- **Què és:** Arxiu digital de memòria oral (Flask app 700MB+)
- **Objectiu:** Preservació testimonis personals hospitals/residències 
- **Estats:** MVP sistema organitzacions 100% operatiu
- **Domini:** adabida.cat registrat, pendent migració

### ARQUITECTURA TÈCNICA
- **Framework:** Flask amb 26+ blueprints modulars
- **BD:** PostgreSQL + SQLAlchemy
- **Frontend:** HTML + CSS + JS (actualment pestanyes, volem enllaços)

---

## PROBLEMA A RESOLDRE

### Sistema actual (inici.html):
```html
<div class="pestanyes">
  <div class="pestanya activa" onclick="obreSeccio('inici')">Inici</div>
  <div class="pestanya" onclick="obreSeccio('galeria')">Galeria</div>
  <div class="pestanya" onclick="obreSeccio('blog')">Blog</div>
</div>
```

### Objectiu:
- Eliminar pestanyes JavaScript
- Crear navegació per enllaços directes a pàgines independents
- Grid visual modern amb targetes clicables

---

## PROGRÉS REALITZAT

### ✅ SECCIONS JA SEPARADES:

**1. Galeria (`/galeria`)**
- Template: `galeria.html` 
- Ruta: `@galeria_bp.route("/galeria")`
- JavaScript: `static/js/galeria.js`
- Funcional amb subpestanyes (destacades/exposicions)

**2. Blog (`/blog`)**  
- Template: `blog.html`
- Ruta: `@blog_bp.route("/blog")`
- Funcional amb arxiu i cerca

**3. Organitzacions (`/organitzacions`)**
- Ja existent i operatiu
- Sistema complet: crear, administrar, sol·licituds

---

## PENDENT DE FER

### 1. Modificar `inici.html`
- Eliminar codi pestanyes JavaScript
- Crear enllaços directes:
  - `{{ url_for('galeria.galeria') }}`
  - `{{ url_for('blog.blog') }}`
  - `{{ url_for('organitzacions.llistat') }}`

### 2. Crear grid visual (opcional)
- Targetes 2x3 amb icones
- CSS: `static/css/grid-navegacio.css`
- Efectes hover i transicions

### 3. Netejar codi sobrant
- Eliminar JavaScript pestanyes de `inici.html`
- Revisar CSS no utilitzat
- Optimitzar imports CSS

---

## ESTRUCTURA OBJECTIU

```
/ (index nou)
├── Targeta GALERIA → /galeria
├── Targeta BLOG → /blog  
├── Targeta ORGANITZACIONS → /organitzacions
├── Targeta PERFIL → /perfil (si loguejar)
└── Targeta LOGIN → modal (si no loguejar)
```

---

## FITXERS CLAU A MODIFICAR

### Templates:
- `templates/inici.html` (principal a canviar)
- Mantenir: `galeria.html`, `blog.html`

### Rutes:
- `routes/inici.py` - funcio `inici_pagina()`
- Mantenir: `routes/galeria.py`, `routes/blog.py`

### Assets:
- Crear: `static/css/grid-navegacio.css` (si grid visual)
- Netejar: JavaScript pestanyes sobrant

---

## SEGÜENTS PASSOS IMMEDIATS

1. **Crear enllaços bàsics** a `inici.html` 
2. **Eliminar sistema pestanyes** existent
3. **Provar navegació** entre seccions
4. **Decidir disseny** grid visual o enllaços simples
5. **Implementar millores estètiques**

---

## NOTES TÈCNIQUES

### Variables importants:
- `session.usuari_id` per lògica login/no-login
- `imatges_destacades`, `exposicions` per galeria
- `entrades_blog`, `mesos_disponibles` per blog

### Rutes funcionals verificades:
- `galeria.galeria` ✅
- `blog.blog` ✅  
- `organitzacions.llistat` ✅
- `perfil.perfil` (per verificar)

### JavaScript a conservar:
- `static/js/galeria.js` ✅
- `static/js/modal.js` ✅
- Eliminar: pestanyes de inici.html