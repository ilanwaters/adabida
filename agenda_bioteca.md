## Dínamo Pendents – Projecte Abadia

### Millores generals i funcionalitats pendents

* Millorar la **recerca** del repositori (formulari, filtres, resultats)

* Millorar els **camps de la modal** (filtres clicables: ubicació, any, autor, tema)

* Activar sistema d’**exposicions públiques**

* Definir i publicar el **codi ètic** del projecte

* Crear una secció de **tema legal / avisos legals**

* Preparar la **portada** amb:

  * Temes destacats
  * Bloc “Coneixes algú?”
  * Secció de **pàgines amigues**

* Millorar el sistema de **localització d’entrades** i crear un **mapa interactiu**

* Millorar el sistema de **localització al registre**:

  * Quan s’introdueixi un país, carregar automàticament les divisions administratives d’aquell país (ex: províncies i ciutats d’Espanya, departaments i municipis de França, etc.)
  * Sistema escalable per a futura expansió internacional
  * Crear sistema genèric per a països sense dades (inputs lliures: regió / ciutat)

* Definir com a **objectiu estratègic final** la creació d’un **mapa mundial interactiu** de les entrades:

  * Geolocalització per coordenades (manual o automàtica)
  * Visualització amb Leaflet.js o Mapbox
  * Filtres per país, any, tema, etc.

* Treballar la **webapp** per a ús mòbil + gestió de **vídeo, càmera i micròfon**

* **Mail d’avís** a l’usuari si la seva imatge es publica a una exposició

* **Enllaços entre usuaris** (famílies, grups, vincles socials)

* Crear un **panell de control d’usuari-perfil** (editar, vincles, activitats, etc.)

* Traduir el projecte a **neerlandès**

### Errors o incoherències a corregir

* No es veu el **missatge de l’exposició** si la imatge no està assignada a galeria
* Una **imatge pot anar a una exposició** encara que hagi estat obviada
* La **primera entrada d’un nou usuari no es guarda**, probablement per tema de carpeta temporal

### Validació d’usuari

* Protocol complet de **validació d’usuari** (document pujat → avís a admin → verificació humana → distintiu verd)
* Crear **filtres** d’usuaris verificats/desverificats
* Informar **clarament a l’usuari** del procés: “Vols ser usuari verd?” etc.

### Administració i dades

* Crear HTML d’**anàlisi de dades** (admin\_analisi\_dades.html)
* Fer **visibles les miniatures dels documents acreditatius** per a l’usuari\_admin
* Activar les **relacions encara que siguin enllaços cecs** (ex: entrades vinculades a documents encara que no siguin públics)

### Altres idees obertes

* Permetre que els usuaris es **puguin enviar missatges entre ells** (amb control ètic)
* Aclarir tema de **majors de 18 anys** (autoria, consentiment, límits legals)

Afegit a Dínamo Pendents (08/07/2025):

🧾 **Nou model de perfils, estructuració visual i governança de perfils (juliol 2025)**

1. **Disseny modular amb pestanyes**: la pàgina personal adopta el mateix model visual que la pàgina d'inici, amb pestanyes separades (Biografia, Entrevista, Nova entrada personal, Entrades). Aquest patró s’aplicarà també a les pàgines d’organitzacions i famílies.

2. **Principi base del sistema de perfils**: cada login equival a un perfil real i documentable. No hi haurà usuaris "anònims" o tècnics. Tots els perfils han de ser rastrejables històricament.

3. **Regles específiques per a cada tipus de perfil**:
   - Perfils **familiars**: només es poden crear des d’un perfil personal existent. És obligatori que una persona real (familiar) gestioni la creació del perfil col·lectiu.
   - Perfils **d’organització**: poden registrar-se directament, però hauran de fer servir un **correu corporatiu verificable**. Es pot requerir validació administrativa abans d’activar el compte.

4. **Traçabilitat i autoria**: tot perfil ha de tenir origen clar i responsable documentat. Això reforça el rigor del projecte i la seva naturalesa d’arxiu històric.

5. **Arbre genealògic visual** (previst per a més endavant): es crearà un arbre interactiu escalable (zoom, pan, clics) utilitzant D3.js, vinculat a perfils familiars. Cada node serà un perfil amb nom i vincles. El sistema s’activarà quan la base familiar estigui madura.

Aquestes normes fonamenten la governança i expansió futura del sistema de perfils a Bioteca.

Revisar els models Usuari, Entrada i ImatgeGaleria per eliminar relacions duplicades o solapades, i afegir overlaps="..." si cal, per evitar conflictes de SQLAlchemy i garantir coherència ORM

Afegir navegació esquerra/dreta dins la modal de la vista exposicio_imatges.html, només en mode públic, sense afectar les altres vistes compartides amb login
Inici:


Repositori de recepte de cuina, cançons, dites populars, etc, 

“Unificar Entrada.imatges / Entrada.imatges_galeria i ImatgeGaleria.entrada / entrada_rel (back_populates únic)”

treballar la possibulitrat de que lusari crei una entad que no es publiqui fins adaqui vint anys o alguna cosa aixi

podem fer el filtre a la ruta de la galeria perquè mai arribi a la plantilla una imatge sense entrada_id. Així desapareixerà el missatge d’alerta i tot estarà vinculat sempre.

millorar el menu idiomes aparença

¿como ho farem per crear usuaris sense email? f.i. residents de llars de gent gran?

