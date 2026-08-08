# ADABIDA - LLISTA DE PENDENTS COMPLETA

**Última actualització:** 3 desembre 2024  
**Estat actual:** Fase 1 completada, començant Fase 2

---

## 🔥 PRIORITAT CRÍTICA - Funcionalitats Comunitat


###  Sistema "Cerquem testimonis sobre..." - EN CURS
- [ ] Crear blueprint `routes/comunitat/peticions.py`
- [ ] Template llista pública de peticions
- [ ] Formulari afegir nova petició
- [ ] Sistema de tracking (qui sol·licita, qui respon)
- [ ] Marcar petició com completada
- [ ] Enllaç al menú principal
inici ha de ser el "ganxo" per usuaris, s'ha de fer de al manera que la gent entengui rapidament el que hiha
temes, estem buscant per temes/subtemes
tembé temes oberts pot ser t'enterresa tema/subtema
 

### ⏳ Fase 3: Sistema de Denúncies - PENDENT
- [ ] Botó "Denunciar" a modals (només usuaris 🟢)
- [ ] Modal de denúncia amb categories
- [ ] Panel admin per revisar denúncies
- [ ] Sistema de notificacions
- [ ] Accions sobre denúncies

### ⏳ Fase 4: Fòrum de Discussió - PENDENT
- [ ] Pàgina principal fòrum
- [ ] Sistema categories/temes
- [ ] Botó "Discussió" a modals (només 🟢)
- [ ] Creació automàtica tema des de modal
- [ ] Sistema de moderació
- [ ] Regles del fòrum

---

## 🎨 PRIORITAT ALTA - Disseny i UX

### Distintius de Nivell d'Usuari
- [x] Header (completat)
- [ ] Perfil públic (al costat del nom)
- [ ] Modals d'entrada (autor)
- [ ] Caixes/targetes d'entrades (autor)
- [ ] Llistes d'usuaris
- [ ] Comentaris del fòrum (quan es creïn)

**Solució recomanada:** Crear un component/macro reutilitzable Jinja2





## ⚙️ PRIORITAT MITJANA - Correccions Tècniques

### Errors actuals
- [ ] **404**: `familia.png` no existeix → crear o canviar ruta
- [ ] **500**: API `/api/guardades/{usuari}` està petant
- [ ] **JavaScript**: `carregaEntradesGuardades()` busca element que no existeix
  - Revisar `pagina_personal.html` línia ~401


### Cerca i Duplicats
- [ ] Cerca en temps real per evitar duplicats al crear membres família
- [ ] Bucle infinit: des del formulari d'afegir, gestionar relacions del nou membre

---

## 📊 PRIORITAT BAIXA - Millores i Poliment

### Visualització Dades
- [ ] Aplicar `visualitzacio.css` a `veure_espai.html`
- [ ] Aplicar `visualitzacio.css` a `les_meves_families.html`
- [ ] Aplicar `visualitzacio.css` a pàgines organitzacions
- [ ] Visualització bàsica d'arbre genealògic
- [ ] Timeline familiar visual
- [ ] Mapa ubicacions família

### Sistema Espais Familiars
- [ ] Sistema permisos dins espais familiars
- [ ] Recalcular ubicacions actuals quan s'afegeixen membres
- [ ] Notificacions dins espais familiars
- [ ] Estadístiques espai familiar

### Funcionalitats Avançades
- [ ] Integrar documents amb sistema Umberto (seguretat)
- [ ] Export espai familiar a PDF
- [ ] Arbre genealògic visual avançat amb D3.js
- [ ] Sistema de cerca global millorat

---

## 📋 BACKLOG COMPLET - Tasques per organitzar

### Sistema d'Arxius i Documents
- [ ] **Escàner PDF integrat**: Funcionalitat per escanejar documents directament
- [ ] **Redirigir totes les pujades a Umberto**: Assegurar que tots els arxius/documents passen pel sistema Umberto
- [ ] **Límit temps àudio/vídeo**: Definir i implementar límits de durada per uploads multimèdia
  - Àudio: 30 min? 1 hora?
  - Vídeo: 15 min? 30 min?

### Administració
- [ ] **Polir pàgina administradors**: Acabar disseny i funcionalitats del panel admin
- [ ] **Estructura administradors**: Definir jerarquies i permisos diferents nivells admin
- [ ] **Panel de denúncies**: Revisió i gestió de reports

### Internacionalització
- [ ] **Acabar de traduir tots els .po**: Completar traduccions per tots els idiomes
  - Català (ca) - base
  - Castellà (es)
  - English (en)
  - Euskara (eu)
  - Français (fr)
  - Русский (ru)
  - Deutsch (de)
  - Українська (uk)
- [ ] **Revisar traduccions existents**: Coherència i qualitat
- [ ] **Sistema de detecció idioma automàtic**: Segons ubicació/navegador

### Pop-ups i Guies
- [ ] **Pop-up aportació**: Decidir on posar-lo estratègicament
  - Després de X temps a la plataforma?
  - Després de crear primera entrada?
  - Quan l'usuari té contingut de qualitat?
- [ ] **Pop-ups info-guia (i)**: Afegir més icones d'ajuda contextual
  - "Per què això i no allò?"
  - Explicacions de funcionalitats
  - Ajuda contextual per formularis complexos
  - Tooltips educatius

### Portada i Descobriment
- [ ] **Temes de portada**: Pàgina amb temes més comentats/populars
- [ ] **Secció "Cerquem testimonis" a portada**: Integrar a home/inici
- [ ] **Destacats de la comunitat**: Entrades més visitades/rellevants del mes
- [ ] **Timeline històrica**: Explorar esdeveniments per dècades
- [ ] **Explorar per temes**: Categorització intel·ligent

### Estadístiques i Visualitzacions
- [ ] **Visualitzacions privades per usuari**: 
  - L'usuari veu quantes visualitzacions tenen les seves entrades
  - Panel privat d'estadístiques personals
  - Sense likes ni gamificació pública
  - Gràfics d'evolució temporal
  - Dades demogràfiques agregades (qui veu el meu contingut)

### Mapa Interactiu
- [ ] **Mapa de testimonis**: Visualització geogràfica d'entrades
  - Per ubicació d'origen dels autors
  - Per ubicació dels esdeveniments narrats
  - Clústers per densitat
- [ ] **Filtres avançats del mapa**:
  - Per temes/categories
  - Per períodes temporals
  - Per tipus de contingut (àudio/vídeo/text)
- [ ] **Interactivitat**: Hover mostra resum, click obre entrada


### Sistema de Referències Acadèmiques 🔗
- [ ] **Sistema de citació automàtica**: 
  - Generar citació en múltiples formats (APA, Chicago, MLA, ISO 690)
  - Botó "Citar aquest testimoni"
  - Copiar al portapapers
- [ ] **Tracking de citacions**: 
  - Notificar usuari quan el seu testimoni és citat en publicacions
  - Registre de citacions acadèmiques
  - Enllaços a publicacions que citen
- [ ] **Badge "Citat en investigació"**: Distintiu per entrades citades
- [ ] **Export metadata**: Formats compatibles amb Zotero, Mendeley, etc.

### Validació Social d'Usuaris ✓
- [ ] **Sistema "Usuaris que coneixen aquest usuari"**:
  - X usuaris coneixen aquest usuari
  - NO és followers ni xarxa social
  - És validació de veracitat/existència
  - Similar a LinkedIn "endorsements"
- [ ] **Procés de validació**:
  - "Conec aquesta persona perquè..." (camp opcional)
  - Opció validació anònima vs pública
  - Límit de validacions per usuari/dia (evitar spam)
- [ ] **Visualització**:
  - Comptador simple al perfil
  - Sense llista pública de qui valida (privacitat)
  - Badge "Perfil validat per la comunitat" (si >X validacions)
- [ ] **Proteccions**:
  - Evitar gamificació excessiva
  - No convertir en xarxa social
  - Focus en credibilitat, no popularitat

- [ ] **Missatges motivacionals**:
  - Quan usuari crea primera entrada
  - Quan compleix fites (1 mes, 1 any, 10 entrades)
  - Quan la seva entrada és visualitzada X vegades

---

## 🔮 IDEES FUTURES - Backlog Llarg Termini

### Comunitat
- [ ] Gamificació subtil: badges per fites (sense punts ni rànkings)
- [ ] Sistema de mentoria: usuaris 🟢 ajuden usuaris 🔵
- [ ] Newsletters amb "destacats de la comunitat"
- [ ] Esdeveniments virtuals: xerrades, debats temàtics
- [ ] Programa ambaixadors: usuaris actius que promouent Adabida
- [ ] Col·laboracions amb associacions memòria històrica

### Tecnologia
- [ ] API pública per a investigadors (amb autenticació)
- [ ] Sistema de transcripció automàtica (Whisper) per àudios
- [ ] Reconeixement automàtic de llocs/dates en textos (NLP)
- [ ] Traducció automàtica entre idiomes plataforma
- [ ] App mòbil nativa (iOS/Android)
- [ ] Mode offline per consultar contingut descarregat

### Acadèmic
- [ ] Col·laboracions amb universitats
- [ ] Programa beques investigació
- [ ] Certificats d'autenticitat per testimonis
- [ ] Sistema de peer-review acadèmic (opcional)
- [ ] Repositori específic per investigadors

### Arxiu
- [ ] "Time capsule": Publicació diferida de contingut
- [ ] Herència digital: Què passa amb el compte quan mors
- [ ] Backup automàtic per usuaris
- [ ] Versioning de testimonis (edicions amb historial)

---

## 🤔 DECISIONS PENDENTS - Preguntes Obertes

### Pop-up Aportació
**Pregunta:** On col·locar-lo estratègicament?
- Opció A: Després de crear primera entrada de qualitat
- Opció B: Després de X minuts navegant la plataforma
- Opció C: Quan usuari té contingut popular (>100 visites)
- Opció D: Mai invasiu, només enllaç discret al footer/perfil

### Límits Multimèdia
**Pregunta:** Quins límits són raonables?
- Àudio: 30 min? 1 hora? Sense límit?
- Vídeo: 15 min? 30 min? (per cost servidor/storage)
- Diferents límits segons nivell usuari?
- Possibilitat de sol·licitar extensió per casos especials?

### Validació Social
**Pregunta:** Com evitar que es converteixi en xarxa social?
- Límit validacions per usuari: 10? 20? 50?
- Només visible recompte total (no qui valida)?
- Només admins veuen detalls de validacions?
- Requerir text obligatori "Per què coneixes aquesta persona"?

### Mapa de Testimonis
**Pregunta:** Quina informació mostrar públicament?
- Ubicació exacta o només regió/comarca?
- Mostrar foto/nom autor en hover o només títol entrada?
- Permetre usuari ocultar les seves entrades del mapa?
- Diferents capes: origen autors vs lloc esdeveniments

### Onboarding
**Pregunta:** Quin to utilitzar?
- Inspirador i emotiu?
- Seriós i acadèmic?
- Proper i càlid?
- Combinació segons context?

**Lemes candidats:**
- "La teva vida, la teva visió, el teu testimoni formen part de la història"
- "Cada record és un tresor. Cada testimoni, un llegat"
- "Tu ets història viva. Comparteix-la"
- "La memòria col·lectiva es construeix amb les teves paraules"

---

## 📝 NOTES DE DESENVOLUPAMENT

### Filosofia
- **Pas a pas**: No agobiar-se, anar implementant funcionalitat per funcionalitat
- **MVP primer**: Funcionalitat mínima viable, després millores
- **Testejar**: Provar amb usuaris reals abans de seguir
- **Flexibilitat**: Adaptar segons feedback
- **Ètica first**: Privacitat, accessibilitat, inclusivitat sempre

### Recordatoris
- Cada nova funcionalitat genera més coses a polir
- Millor 4 funcionalitats senzilles que 1 de complexa
- La comunitat creix quan se sent útil i escoltada
- Documentar decisions importants
- No perseguir la perfecció, perseguir el valor real

### Convencions
- Codi en català (`snake_case`)
- Templates heretant de `base.html`
- CSS específic per funcionalitat
- Blueprints organitzats per mòduls (`comunitat/`, `familia/`, etc.)
- Comentaris clars i descriptius
- Git commits descriptius

### Principis de Disseny Adabida
- **Pla i elegant**: Sense colors cridaners
- **Paleta consistent**: Blaus suaus, grisos
- **Tipografia clara**: Montserrat
- **Espaciats generosos**: Respirar
- **Responsive**: Funciona a mòbil, tablet, desktop
- **Accessible**: Contrast, mida text, navegació teclat
- **Professional però humà**: Calidesa sense ser infantil

---


---

## 💭 REFLEXIÓ FINAL

Adabida no és només una plataforma. És un **arxiu viu de la memòria humana**. Cada funcionalitat que implementem ha de servir aquest propòsit: preservar, dignificar i fer accessible la història personal que forma part de la Història col·lectiva.

Les decisions tècniques importants, però més important és mantenir sempre present el **per què** existeix Adabida: perquè cada vida mereix ser recordada, cada veu mereix ser escoltada, i cada testimoni aporta una peça única al mosaic de la nostra memòria col·lectiva.

---

**Document viu - s'actualitza contínuament**  
**Última actualització:** 3 desembre 2024 - LLISTA COMPLETA amb backlog expandit
