# ADABIDA - CONTEXT COMPLET ACTUALITZAT 23 NOVEMBRE 2025

## RESUM SESSIÓ 23 NOVEMBRE 2025

### Tasques completades:

1. **Sistema Espais Familiars - Base implementada**
   * Blueprint `familia_bp` creat i registrat a `app.py`
   * Ruta `/familia/` funcional amb hub base
   * Card "Família" a pàgina personal enllaçada correctament

2. **Formulari Crear Espai Familiar**
   * Template `crear_espai_familiar.html` amb estil Adabida
   * Camps implementats:
     - Nom família (obligatori)
     - Motiu/sobrenom familiar (opcional) - "Els Raboses", "Ca la Maria"
     - Descripció i context (opcional)
     - **Múltiples ubicacions d'origen** amb botó [+ Afegir altra ubicació d'origen]
     - **Múltiples ubicacions actuals provisionals** amb botó [+ Afegir altra ubicació actual]
     - Període de referència (opcional)
     - Upload heràldica/escut (opcional)
   * JavaScript per afegir/eliminar ubicacions dinàmicament
   * Capçalera centrada amb subtítol

3. **Models Base de Dades - Espais Familiars**
   * Model `EspaiFamiliar` actualitzat amb:
     - Camps bàsics: nom, motiu, descripció, periode_referencia, heraldica_fitxer
     - Property `ubicacions_principals_calculades` per calcular top 3 ubicacions dels membres
     - Property `ubicacions_mostrar` que retorna provisionals o calculades segons membres
   * Model `UbicacioOrigenFamilia` (nou):
     - Taula per múltiples llocs d'origen
     - Camps: pais, regio, municipi, ordre
     - Relació many-to-one amb EspaiFamiliar
   * Model `UbicacioActualFamilia` (nou):
     - Taula per ubicacions actuals provisionals
     - Camps: pais, regio, municipi, ordre, es_provisional
     - Es substitueixen automàticament quan s'afegeixen membres amb ubicacions
   * Model `MembreFamilia` mantingut amb camps ubicació actual

4. **Rutes Família**
   * `familia.hub()` - Pàgina principal gestió familiar
   * `familia.crear()` - GET: mostra formulari / POST: processa múltiples ubicacions
   * `familia.veure(familia_id)` - Veure detalls espai (pendent template)
   * `familia.les_meves()` - Llistar espais de l'usuari (pendent template)

5. **Migracions Base de Dades**
   * Migració creada i executada per taules `ubicacions_origen_familia` i `ubicacions_actuals_familia`
   * Carpeta `static/heraldica/` creada per guardar escuts familiars

### Filosofia ubicacions:

**Ubicacions d'origen:** Múltiples per reflectir diferents orígens de la família

**Ubicacions actuals:** 
- Provisionals afegides manualment al crear espai
- Permeten que la família aparegui en cerques des del principi
- Diferencien famílies amb mateix cognom però ubicacions diferents
- Exemple: "García López de Tordera/Barcelona/Ardales" vs "García López de Vic/Tetuan/Michigan"
- Es recalculen automàticament quan s'afegeixen membres amb ubicacions reals

### Fitxers modificats/creats:

**Nous:**
* `routes/familia/familia.py` - Blueprint complet amb rutes
* `templates/familia/crear_espai_familiar.html` - Formulari amb múltiples ubicacions
* `static/heraldica/` - Carpeta per escuts familiars
* Models: `UbicacioOrigenFamilia`, `UbicacioActualFamilia`

**Actualitzats:**
* `models.py` - Models EspaiFamiliar ampliat amb properties + 2 models nous
* `app.py` - Blueprint familia_bp registrat
* `templates/pagina_personal/pagina_personal.html` - Card Família amb enllaç correcte

### Estat actual:

✅ Crear espai familiar funcional amb múltiples ubicacions
✅ Blueprint registrat i funcionant
✅ Models i migracions executades
⬜ Template visualització espai familiar (veure_espai.html) pendent
⬜ Template llistat espais (les_meves_families.html) pendent
⬜ Sistema afegir membres a espai familiar pendent
⬜ Gestió relacions de parentiu pendent
⬜ Buscador de famílies pendent

---

## ESTRUCTURA DEL PROJECTE

```
adabida/
├── .env (Variables d'entorn protegides)
├── .gitignore (Protecció fitxers sensibles)
├── app.py (Flask-Mail integrat + Blueprint familia registrat)
├── models.py (Models Espais Familiars + Ubicacions)
├── config.py (Llegeix des de .env)
├── requirements.txt (Flask-Mail + python-dotenv)
├── babel.cfg
├── alembic.ini
├── routes/
│   ├── blog.py (Sistema blog complet)
│   ├── familia/
│   │   └── familia.py (NOU - Blueprint espais familiars)
│   ├── organitzacions/
│   │   ├── xorganitzacions.py (Many-to-many compartició)
│   │   └── ...
│   ├── registre_individual.py
│   ├── auth.py
│   ├── login.py
│   └── __pycache__/
├── templates/
│   ├── base.html (Badge missatges nous al nav)
│   ├── blog/
│   ├── familia/
│   │   ├── familia.html (Hub base)
│   │   └── crear_espai_familiar.html (NOU - Formulari múltiples ubicacions)
│   ├── auth/
│   ├── emails/
│   ├── organitzacions/
│   ├── pagina_personal/
│   │   ├── pagina_personal.html (Card Família afegida)
│   │   └── nova_entrada.html (Checkboxes múltiples organitzacions)
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   ├── heraldica/ (NOU - Escuts familiars)
│   └── ...
├── translations/ (català, castellà, anglès)
├── umberto/ (Sistema arxiu digital amb estructura jeràrquica)
└── migrations/ (Control versions BD)
```

---

## MODELS BASE DE DADES

### Model EspaiFamiliar (actualitzat)
```python
class EspaiFamiliar(db.Model):
    id, nom, motiu, descripcio
    periode_referencia, heraldica_fitxer
    data_creacio, creat_per_id, activa
    
    # Relacions:
    creador → Usuari
    membres → [MembreFamilia]
    ubicacions_origen → [UbicacioOrigenFamilia]
    ubicacions_actuals → [UbicacioActualFamilia]
    
    # Properties:
    @property ubicacions_principals_calculades  # Top 3 dels membres
    @property ubicacions_mostrar  # Provisionals o calculades
    @property nombre_membres
```

### Model UbicacioOrigenFamilia (nou)
```python
class UbicacioOrigenFamilia(db.Model):
    id, espai_familiar_id
    pais, regio, municipi, ordre
    
    # Relació:
    espai_familiar → EspaiFamiliar
```

### Model UbicacioActualFamilia (nou)
```python
class UbicacioActualFamilia(db.Model):
    id, espai_familiar_id
    pais, regio, municipi, ordre
    es_provisional  # Bool: True si manual, False si calculat
    
    # Relació:
    espai_familiar → EspaiFamiliar
```

### Model MembreFamilia (existent)
```python
class MembreFamilia(db.Model):
    id, usuari_id, espai_familiar_id
    rol  # 'administrador' o 'membre'
    data_adhesio
    pais_actual, regio_actual, municipi_actual
    
    # Relacions:
    usuari → Usuari
    espai_familiar → EspaiFamiliar
```

### Model Usuari (selecció camps rellevants)
```python
class Usuari(db.Model, UserMixin):
    # Bàsic
    id, nom_login, contrasenya_hash, email, rol
    nom, primer_cognom, segon_cognom
    
    # Ubicació
    municipi_naixement, regio_naixement, pais_naixement
    pais_residencia, data_naixement
    
    # Sistema
    es_admin, identificador_abadia, idioma
    email_verificat, token_verificacio, data_token
    token_reset_password, data_token_reset
    rebre_missatges
    
    # Relacions
    perfil → PerfilBiografic
    entrades → [Entrada]
    families_creades → [EspaiFamiliar]  # NOU
    membresies_families → [MembreFamilia]  # NOU
```

### Model Entrada (many-to-many compartició)
```python
class Entrada(db.Model):
    # Camps principals
    id, usuari_id, titol, tema, any_text, contingut
    pais, regio, municipi, data_creacio
    
    # Imatge
    titol_imatge, descripcio_imatge, any_imatge
    pais_imatge, regio_imatge, municipi_imatge
    referencia, nom_fitxer, tipus_fitxer, tipus_media
    
    # Visibilitat
    visible_publicament, es_publica, timestamp
    
    # Relacions many-to-many (NOU)
    organitzacions_compartides → [EntradaOrganitzacio]
    families_compartides → [EntradaFamilia]
    
    # Relacions antigues
    usuari → Usuari
    arxius_adjuntats → [ArxiuAdjunt]
    imatges → [ImatgeGaleria]
    exposicions → [Exposicio]
```

### Taula intermèdia EntradaOrganitzacio (nou)
```python
class EntradaOrganitzacio(db.Model):
    id, entrada_id, organitzacio_id, data_compartit
    
    # Relacions:
    entrada → Entrada
    organitzacio → Organitzacio
```

### Taula intermèdia EntradaFamilia (nou)
```python
class EntradaFamilia(db.Model):
    id, entrada_id, espai_familiar_id, data_compartit
    
    # Relacions:
    entrada → Entrada
    espai_familiar → EspaiFamiliar
```

### Model Organitzacio (many-to-many membres)
```python
class Organitzacio(db.Model):
    # Bàsic
    id, nom, tipus, descripcio
    pais, regio, municipi, codi_postal
    
    # Web
    url_publica, url_personalitzada
    color_primary, logo_fitxer
    
    # Premium
    es_premium, data_premium
    
    # Contacte
    email_adabida, email_extern, telefon_contacte, adresa
    
    # Meta
    data_creacio, creat_per_id, activa
    
    # Relacions
    creador → Usuari
    membres → [MembreOrganitzacio]
    solicituds → [SolicitudOrganitzacio]
    
    # Properties
    @property slug  # Àlies url_publica
    @property solicituds_pendents
    @property entrades_totals
    @property entrades  # De tots els membres
```

---

## FUNCIONALITATS IMPLEMENTADES

### Sistema Missatges
* Badge vermell amb comptador missatges nous al nav
* Context processor `inject_missatges_nous()` a app.py
* Icona sobre blanc SVG a base.html

### Sistema Compartició Múltiple (Many-to-Many)
* Models: EntradaOrganitzacio, EntradaFamilia
* Eliminat camp obsolet `organitzacio_compartida_id`
* Checkboxes múltiples a nova_entrada.html
* xorganitzacions.py actualitzat per relacions many-to-many

### Sistema Verificació Email
* Token únic generat amb secrets.token_urlsafe(32)
* Expiració 24h configurable
* Plantilles HTML professionals per emails
* Bloqueig login sense verificació
* Pàgina confirmació "registre_complet.html"
* Sistema reenviar verificació
* Reset password amb token similar

### Blog Institucional
* Paginació amb Flask-Paginate
* Truncat de text amb "Llegir més..."
* Índex lateral sticky amb scroll actiu
* Cerca per títol/contingut
* Filtre per autor
* Sistema admin per crear/editar/eliminar

### Pàgina Institucional HOME
* Secció institucional `/home`
* Índex lateral sticky amb navegació
* Estil editorial sobri
* Contingut en català amb traduccions

### Organitzacions
* Sistema crear organitzacions
* URL pública personalitzable (/o/nom-org)
* Email automàtic @adabida.cat
* Sistema membres amb rols (admin/entrevistador/adherit)
* Sol·licituds adhesió
* Pàgines públiques organitzacions
* Sistema compartir entrades amb múltiples orgs

### Espais Familiars (NOU)
* Crear espai amb nom, motiu, descripció
* Múltiples ubicacions d'origen
* Múltiples ubicacions actuals provisionals
* Upload heràldica/escut familiar
* Període de referència
* Sistema membres amb rols (administrador/membre)
* Compartir entrades amb famílies
* Ubicacions calculades automàticament dels membres

---

## SEGURETAT I BONES PRÀCTIQUES

### Variables d'entorn (.env)
```
MAIL_USERNAME=adabida.official@gmail.com
MAIL_PASSWORD=xxxx_xxxx_xxxx_xxxx
SECRET_KEY=clau-secreta-generada
DATABASE_URL=sqlite:///adabida.db
```

### .gitignore actualitzat
```
.env
__pycache__/
*.pyc
instance/
.DS_Store
migrations/versions/*.pyc
```

### Tokens segurs
* secrets.token_urlsafe(32) per verificació
* Expiració temporal configurable
* Hash bcrypt per contrasenyes
* Validació email amb regex

---

## TRADUCCIONS MULTIIDIOMA

### Idiomes disponibles:
* Català (ca) - per defecte
* Castellà (es)
* Anglès (en)

### Sistema Flask-Babel configurat
* Detecció automàtica idioma navegador
* Selector manual idioma
* Traduccions .po compilades
* Funcions _() per textos traduïbles

---

## PENDENTS / BACKLOG

### Prioritat Alta
1. Template visualització espai familiar (`veure_espai.html`)
2. Template llistat espais (`les_meves_families.html`)
3. Sistema afegir membres a espai familiar
4. Formulari dades membre (nom, dates, parentiu, ubicació)
5. Vinculació membres amb usuaris Adabida existents
6. Buscador de famílies per nom/ubicació

### Prioritat Mitjana
7. Gestió relacions de parentiu (pare/mare/fill/germà)
8. Arbre genealògic visual (opcional)
9. Disclaimer confirmació compartir entrades
10. Sistema permisos dins espais familiars
11. Recalcular ubicacions actuals quan s'afegeixen membres
12. Notificacions dins espais familiars

### Prioritat Baixa
13. Export espai familiar a PDF
14. Timeline familiar visual
15. Mapa ubicacions família
16. Estadístiques espai familiar
17. Sistema jeràrquic divisions administratives per país (per becari futur! 😄)

---

## NOTES TÈCNIQUES

### Stack tecnològic:
* Flask 3.x
* SQLAlchemy + Alembic
* Flask-Login
* Flask-Mail
* Flask-Babel
* PostgreSQL (producció) / SQLite (dev)
* Jinja2 templates
* Python 3.13

### Estructura URLs:
* `/` - Pàgina pública inici
* `/home` - Pàgina institucional
* `/blog` - Blog institucional
* `/o/<slug>` - Pàgines públiques organitzacions
* `/familia/` - Hub espais familiars (NOU)
* `/familia/crear` - Crear espai familiar (NOU)
* `/familia/<id>` - Veure espai familiar (NOU)
* `/familia/les-meves` - Llistar meus espais (NOU)
* `/pagina_personal` - Àrea privada usuari
* `/auth/*` - Login, registre, recuperació

### Convencions codi:
* Noms variables/funcions en català
* Comentaris en català
* Templates en català amb traduccions _()
* Models en CamelCase
* Routes en snake_case
* Commits descriptius en català

---

## FILOSOFIA DEL PROJECTE

**Adabida és un arxiu digital de memòria oral i testimonis personals amb vocació acadèmica i rigor històric, però amb una interfície accessible i amigable per a tots els usuaris.**

**Espais Familiars:** Permet a les famílies crear el seu propi arxiu familiar professional, preservar memòria, localitzar-se geogràficament i diferenciar-se d'altres famílies amb cognoms similars. És com crear la "Casa" o "Saga" familiar amb rigor arxivístic però amb calidesa humana.

---

*Document actualitzat: 23 novembre 2025 22:30h*
*Sessió durada: ~3 hores*
*"En els detalls radica l'excel·lència" - Ilan*
