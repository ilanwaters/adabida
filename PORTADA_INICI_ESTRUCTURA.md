# ESTRUCTURA PORTADA INICI - Adabida

**Data:** 9 desembre 2024

---

## LAYOUT GENERAL

```
┌──────────────┬────────────────────────────────┐
│              │                                │
│  BARRA       │  CONTINGUT PRINCIPAL           │
│  LATERAL     │                                │
│              │  • Caixa 1: Explica'ns sobre   │
│  (fixa)      │  • Caixa 2: Últims testimonis  │
│              │                                │
└──────────────┴────────────────────────────────┘
```

---

## 1. BARRA LATERAL (fixa, esquerra)

### Dos botons toggle a dalt:
- **[TEMA]** (actiu per defecte)
- **[PAÍS]**

### Mode TEMA (per defecte):
Llista de **categories** amb scroll:
- 🗳️ Política
- ⚔️ Conflictes
- 🎨 Cultura
- ⚽ Esports
- etc.

**Clic categoria →** Filtra repositori per categoria

### Mode PAÍS:
Llista de **països** amb scroll (ordre alfabètic):
- 🇪🇸 España
- 🇩🇪 Alemanya
- 🇻🇳 Vietnam
- etc.

**Clic país →** Canvia a vista de temes d'aquest país:
```
← España
─────────────
Guerra Civil
ETA
Transició
Pandèmia
...
```

**Clic tema →** Filtra repositori per tema del país

---

## 2. CAIXA 1: "Explica'ns sobre..."

**Dropdown països:** `[España ▼]`

**Grid de temes** (dinàmic segons país seleccionat):
- Temes globals (aplicar_a_tots_paisos=True)
- Temes específics del país

**9 temes visibles + botó "Més"**

**Clic tema →** `/nova_entrada_personal?titol=NomTema`

---

## 3. CAIXA 2: "Últims testimonis compartits"

**Grid 6-9 entrades recents** (globals, sense filtrar):
- Component `caixa_entrada.html` (reutilitzable)
- Títol, resum, ubicació, autor, data
- **Amb bandereta** de l'usuari (acabat d'implementar)

**Query:** `Entrada.query.order_by(Entrada.data.desc()).limit(9).all()`

**Sense traduccions**, surten en l'idioma original.

---

## IMPLEMENTAT AVUI

✅ Sistema de banderes per usuari:
- Camp `bandera_preferida` a BD
- Selector modal amb 260+ banderes
- Bandereta visible a:
  - Perfil personal (al costat del nom)
  - Caixes d'entrada (metadades)

---

## PENDENT

- [ ] Barra lateral dinàmica (TEMA/PAÍS toggle)
- [ ] Caixa 1 amb temes per país
- [ ] Caixa 2 amb últims testimonis
- [ ] Sistema categories/temes/subtemes (jerarquia 3 nivells)

---

**Nota:** Les banderes **SÍ es mostren** a les caixes d'entrada (component `caixa_entrada.html`). Això permet al visitant saber d'on ve l'autor del testimoni. Discreta (16x11px) però visible.
