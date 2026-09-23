# Resum de la sessió – Arquitectura UX i jerarquia d’Adabida

## 1. Flux de registre i accés
- El registre crea l’usuari, envia correu de verificació i **no inicia sessió automàticament**.
- Després de validar l’email:
  - L’usuari torna a **Inici**.
  - Ha de fer **login manualment**.
- Decisió conscient i correcta a nivell de **seguretat** i **control del flux**.
- Un cop loguejat, l’usuari pot accedir a la **pàgina personal**, que és el seu espai de treball real.

---

## 2. Separació clara d’espais (arquitectura del projecte)

### Espais sense login (públics)
- **Adabida principal / Home**  
  Explicació teòrica del projecte, aparador, exploració de continguts.
- **Galeria i exposicions**
- **Blog**
- **Participació econòmica**
- **Exploració de testimonis i temes**

### Espais amb login obligatori
- **Espai personal**
- **Família**
- **Organitzacions**
- **Creació d’entrades**
- **Gestió de contingut propi**

👉 Aquesta separació és coherent i estable.

---

## 3. Concepte clau de la portada (Inici)

### Jerarquia funcional definida
- **Bloc central = CREAR**
  - Escriure
  - Enregistrar
  - Iniciar entrevistes
  - Crear temes
- **Columna dreta = LLEGIR / EXPLORAR**
  - Navegar per temes
  - Filtrar per país
  - Consultar contingut existent

👉 Regla d’or establerta:
> Crear al centre · Llegir al costat

---

## 4. Columna dreta (“Explora Temes”)
- Bona resolució visual i funcional.
- Risc identificat: **competència visual lleu** amb el bloc central.
- Decisió:
  - Mantenir-la com a **exploració**, mai com a acció principal.
  - Evitar CTAs de creació en aquest espai.
- Estat actual: **al límit correcte**, només cal vigilar futures ampliacions.

---

## 5. Sidebar esquerra (navegació)
- Es manté la sidebar.
- Es decideix **eliminar el títol “Navegació”**, però:
  - Es conserven tots els ítems.
  - Els ítems són necessaris i clars:
    - Adabida principal
    - Espai personal
    - Família
    - Organitzacions
    - Cultura popular
    - Galeria
    - Blog
    - Aportacions

👉 Decisió basada en intuïció + criteri: correcta.

---

## 6. Desplegables amb i sense login

### Família
- **Amb login**:
  - Crear espai familiar
  - Els meus espais
  - Arbre genealògic
  - Documents familiars
- **Sense login**:
  - Text explicatiu (què és i per a què serveix)
  - CTA: *Crear perfil personal* → modal disclaimer

### Organitzacions
- Mateix patró que Família:
  - Accions reals només amb login
  - Sense login → explicació + CTA a crear perfil

### Arxiu de cultura popular
- Amb login:
  - Accés directe a crear entrades temàtiques
- Sense login:
  - Missatge motivador
  - Redirecció a registre / login

👉 Patró unificat i coherent a tot el projecte.

---

## 7. Decisions de disseny i UX
- Es descarta fer pop-ups grans que trenquin la jerarquia.
- Es descarta fer “caixes que sobresurten” si trenquen l’ordre visual.
- Es prioritza:
  - Claredat
  - Jerarquia
  - Continuïtat visual
- Millor un sistema lleuger i estable que un efecte espectacular.

---

## 8. Conclusió general
- El projecte ha passat de “provar coses” a **dissenyar amb criteri**.
- La jerarquia CREAR / LLEGIR està clara i ben aplicada.
- Les decisions preses són:
  - coherents
  - defensables
  - escalables
- L’instint que has seguit **no és antic**: és arquitectura de la informació clàssica que funciona.

👉 Base sòlida per continuar sense haver de refer-ho tot més endavant.
