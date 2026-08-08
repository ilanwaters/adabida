# 📋 RESUM SESSIÓ 10 GENER 2026 - PROJECTE ADABIDA

**Durada:** ~3 hores  
**Focus:** Banner cookies, pàgina web projecte, documentació

---

## ✅ COMPLETAT AVUI

### 1. Sistema Legal de Cookies ✅
**Temps:** ~1h 15min

**Implementat:**
- ✅ Pàgina "Política de Cookies" (`/legal/politica-cookies`)
- ✅ Banner informatiu (apareix primera vegada, guarda cookie)
- ✅ Enllaç "Política de Cookies" al footer
- ✅ Traduccions banner als 8 idiomes
- ✅ Sistema templates legals amb detecció idioma + fallback
- ✅ CSS legal separat i net (sense duplicitats)
- ✅ Compliment RGPD (només cookies essencials)

**Fitxers creats/modificats:**
- `routes/legal.py` (funció `render_legal_template()` amb fallback)
- `templates/legal/politica_cookies_ca.html`
- `static/css/legal.css` (CSS unificat)
- `templates/base.html` (banner + JavaScript + CSS)
- Traduccions als 8 `.po` (ca, es, en, fr, de, ru, uk, eu)

**Estat:** ✅ OPERATIU EN PRODUCCIÓ

---

### 2. Pàgina Web del Projecte (Començada) 🚧
**Temps:** ~1h

**Implementat:**
- ✅ Blueprint `routes/projecte.py` amb 6 rutes
- ✅ Pàgina principal `/projecte/` (home del projecte)
  - Hero amb tagline
  - Què és Adabida
  - Els 3 pilars (Plataforma, Metodologia, Tallers)
  - Per a qui és
  - CTA buttons
- ✅ Pàgina `/projecte/contacte/`
  - 3 cards (Organitzacions, Consultes, Col·laboracions)
  - Emails de contacte
  - Responsive
- ✅ CSS compartit `static/css/projecte.css`
- ✅ Traduccions preparades per Babel (tots els textos amb `{{ _('...') }}`)
- ✅ Traduccions al castellà afegides

**Fitxers creats:**
- `routes/projecte.py`
- `templates/projecte/index.html`
- `templates/projecte/contacte.html`
- `static/css/projecte.css`
- Registrat a `app.py`

**Estat:** ✅ FUNCIONAL (pendent pujar a producció)

---

### 3. Documentació Crítica del Projecte 📄
**Temps:** 30min

**Creat:**
- ✅ Document `NOTES_PROJECTE_ADABIDA.md` amb:
  - Accés servidor (IP, SSH, credencials)
  - Bases de dades (producció i local)
  - Dominis configurats
  - Estructura directoris
  - Comandes útils (rsync, restart, logs, backups)
  - Procediment deployment complet
  - Troubleshooting
  - Checklist post-deployment
  - Manteniment regular

**Estat:** ✅ DOCUMENT CREAT (pendent guardar localment i afegir contrasenyes)

---

## 🚧 PENDENT / EN CURS

### 1. Pàgina Web Projecte - COMPLETAR ⏳
**Temps estimat:** 3-4 hores

**Falta crear:**
- [ ] `/projecte/metodologia/` → Explicar mètode entrevista
  - 6 perfils d'entrevistador
  - 4 eixos terapèutics
  - Validació acadèmica
  - Document PDF descargable
- [ ] `/projecte/tallers/` → Informació tallers
  - Properes dates
  - Com inscriure's
  - Fotos tallers (quan n'hi hagi)
  - Testimonis participants
- [ ] `/projecte/faq/` → Preguntes freqüents
  - Què és / Per què existeix
  - És gratuït?
  - Qui pot participar?
  - Seguretat dades
  - Diferència amb xarxes socials
- [ ] `/projecte/documents/` → Centre descàrregues
  - Guia participants taller (PDF)
  - Metodologia completa (PDF)
  - Dossier organitzacions (PDF)
  - Infografies
- [ ] Enllaç "El Projecte" al menú principal del web

**Traduccions:**
- [ ] Completar traduccions templates projecte (7 idiomes)
- [ ] Templates legals a ES i EN (prioritat)

---

### 2. Documents Corporatius 📚
**Temps estimat:** Variable (depèn contingut)

**Documents a crear:**
1. **Dossier complet projecte** (per organitzadors tallers)
   - Què és Adabida
   - Metodologia detallada
   - Com organitzar un taller
   - Requisits
   - Materials necessaris
   
2. **Document metodologia** (per validació acadèmica)
   - Marc teòric
   - 6 perfils d'entrevistador explicats
   - 4 eixos terapèutics amb fonamentació
   - Bibliografia
   - Per enviar a psicòlegs/historiadors
   
3. **Guies participants** (per assistents tallers)
   - Guia breu: Què esperar
   - Com preparar-se
   - Després del taller

**Estat:** ❌ PENDENT (PRIORITAT ALTA per llançar tallers)

---

### 3. Desenvolupament Tècnic ⚙️

#### PRIORITAT ALTA 🔥
- [ ] **PWA - Botó pantalla inici mòbil** (2-3h)
  - `manifest.json`
  - Service Worker
  - Meta tags
  - Prompt instal·lació

- [ ] **Sistema Codis Entrada Automàtics** (3-4h)
  - Format: `ESP-2024-12-JG-2025-01-001`
  - Reorganitzar estructura carpetes `umberto/`
  - Camp `codi_entrada` a BD

#### PRIORITAT MITJANA ⚙️
- [ ] **Completar Traduccions**
  - Acabar tots els `.po` (8 idiomes)
  - Templates legals (prioritzar ES, EN)

- [ ] **Arbre Genealògic** (99% operatiu)
  - Últims poliments

#### FUNCIONALITATS COMUNITAT 📋
- [x] Fase 1: Validació Usuaris - ✅ COMPLETADA
- [ ] Fase 2: "Cerquem testimonis sobre..." - 🚧 PROPERA
- [ ] Fase 3: Sistema Denúncies
- [ ] Fase 4: Fòrum Discussió

#### BACKLOG 🎯
- Escàner PDF integrat
- Mapa interactiu testimonis
- Sistema referències acadèmiques
- Límits temps àudio/vídeo
- Afegir Ucraïna com a país
- Pop-ups estratègics
- Visualitzacions privades per usuari

---

## 📊 ESTAT GENERAL DEL PROJECTE

### Plataforma Tècnica: 99% ✅
- ✅ Aplicació web funcional
- ✅ Sistema usuaris i autenticació
- ✅ Repositori testimonis
- ✅ Sistema famílies
- ✅ Sistema organitzacions
- ✅ Multiidioma (8 idiomes)
- ✅ Sistema aportacions/donacions
- ✅ Email verificació
- ✅ Deployment producció operatiu
- ✅ SSL/HTTPS
- ✅ Backups automàtics
- ✅ Sistema legal (cookies, privacitat)

### Contingut i Comunicació: 40% 🚧
- ✅ Pàgina principal projecte
- ✅ Contacte
- 🚧 Metodologia (pendent)
- 🚧 Tallers (pendent)
- 🚧 FAQ (pendent)
- 🚧 Documents descargables (pendent)
- ❌ Dossiers corporatius (pendent crear)

### Validació i Tracció: 0% ❌
- ❌ Metodologia validada per professionals
- ❌ Taller pilot realitzat
- ❌ Testimonis reals d'usuaris
- ❌ Fotos/vídeos tallers
- ❌ Casos d'ús documentats

---

## 🎯 ROADMAP RECOMANAT

### FASE 1: PREPARACIÓ PRE-LLANÇAMENT (2-3 setmanes)
**Objectiu:** Tenir tot el material necessari abans de fer públic

1. **Setmana 1: Documents corporatius**
   - Crear dossier complet projecte
   - Crear document metodologia per validació
   - Crear guies participants

2. **Setmana 2: Web projecte completa**
   - Acabar `/projecte/metodologia/`
   - Acabar `/projecte/tallers/`
   - Acabar `/projecte/faq/`
   - Afegir enllaç menú principal

3. **Setmana 3: Validació acadèmica**
   - Enviar metodologia a 2-3 professionals
   - Incorporar feedback
   - Obtenir avals (si cal)

### FASE 2: TALLER PILOT (1 setmana)
**Objectiu:** Provar metodologia amb públic de confiança

1. Organitzar taller pilot (5-10 persones)
2. Documentar amb fotos
3. Recollir feedback honest
4. Ajustar metodologia si cal

### FASE 3: LLANÇAMENT PÚBLIC (ongoing)
**Objectiu:** Començar tracció real

1. Publicar fotos/testimonis taller pilot
2. Oferir tallers a organitzacions
3. Començar comunicació (xarxes? blog?)
4. Iterar segons feedback

---

## 💭 REFLEXIONS SESSIÓ

### Moments clau:
- 🎉 Sistema cookies completat i operatiu
- 🚀 Pàgina projecte començada amb estructura clara
- 😰 Moment "he esborrat les notes" → Solucionat amb document complet
- 💡 Definició clara: "Adabida és un projecte d'arxiu de memòria oral..."
- 🤔 Por/dubtes sobre fase següent (tallers públics) → Normal i esperat

### Aprenentatges:
- Tens un projecte **tècnicament sòlid** (99% acabat)
- Ara arriba la part **exposició pública** (més vulnerable)
- **Validació acadèmica** és clau abans de tallers públics
- No cal convèncer tothom, només trobar el primer grup petit
- Pots començar molt a poc a poc (taller pilot 5 persones)

### Decisió important:
**Crear pàgina `/projecte/` dins adabida.cat** (no domini separat)
- Millor SEO
- Gestió més simple
- Zero cost extra
- És l'estàndard

---

## 📝 TASQUES PROPERA SESSIÓ

**Opcions (a triar):**

**A) Continuar pàgina projecte**
- Crear `/projecte/metodologia/`
- Crear `/projecte/faq/`
- Afegir enllaç menú

**B) Documents corporatius**
- Dossier complet projecte (DOCX/PDF)
- Document metodologia per validació (DOCX/PDF)

**C) Funcionalitat comunitat**
- Fase 2: "Cerquem testimonis sobre..."

**D) PWA mòbil**
- Botó "Afegir a pantalla d'inici"

---

## 🔧 PROBLEMES TÈCNICS DETECTATS

### Entorn virtual duplicat
- **Situació:** 2 projectes Adabida al mateix ordinador
  - `/home/ilan/projectes/adabida/` (sense venv)
  - `/mnt/c/Users/ilanw/Desktop/adabida/` (amb venv)
- **Recomanació:** Decidir quin usar i eliminar/actualitzar l'altre

---

## ✅ CHECKLIST ABANS DE TANCAR SESSIÓ

- [x] Banner cookies operatiu en producció
- [x] Pàgina projecte creada i funcional localment
- [x] Document notes crític generat
- [ ] Pàgina projecte pujada a producció (pendent sincronitzar)
- [ ] Document notes guardat localment amb contrasenyes
- [ ] Decidir quin directori projecte usar (Linux vs Windows)

---

## 📞 CONTACTE I SUPORT

Si necessites ajuda:
- Consulta `NOTES_PROJECTE_ADABIDA.md` per info tècnica
- Revisa documentació al Project Knowledge
- Roadmap: `ROADMAP_PRIORITATS_2025.md`

---

**Document viu - actualitzar després de cada sessió**  
**Última actualització:** 10 gener 2026 - 23:00h
