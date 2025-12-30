# Com afegir un país nou amb regions i traduccions

## Context del sistema

Adabida té un sistema d'ubicacions intel·ligent que permet:
- Carregar dinàmicament països, regions i municipis
- Traduccions multiidioma (català, castellà, anglès, euskera, gallec...)
- Els usuaris poden afegir municipis nous automàticament
- Sistema escalable per afegir països segons demanda real

---

## Quan afegir un país nou?

Quan detectis que hi ha usuaris d'un país que encara no està a la BD:
- Mires els registres nous
- Si veus "Noruega", "Italia", "França" en camps de text lliure
- Llavors crees el JSON d'aquell país i l'importes

---

## PAS 1: Crear el fitxer JSON del país

### Exemple: `data/italia.json`

```json
{
  "pais": {
    "nom": "Italia",
    "codi_iso": "IT"
  },
  "regions": [
    {
      "nom": "Lombardia",
      "municipis": ["Milano", "Brescia", "Bergamo", "Monza"]
    },
    {
      "nom": "Lazio",
      "municipis": ["Roma", "Latina", "Frosinone"]
    },
    {
      "nom": "Campania",
      "municipis": ["Napoli", "Salerno", "Caserta"]
    }
  ]
}
```

**Estructura:**
- `pais.nom`: Nom del país en l'idioma original
- `pais.codi_iso`: Codi ISO de 2 lletres (IT, FR, NO, etc.)
- `regions`: Array de regions/províncies/estats
- `regions[].nom`: Nom de la regió
- `regions[].municipis`: Array de municipis principals (no cal posar-los tots, els usuaris els aniran afegint)

**On trobar les dades?**
- Wikipedia: https://ca.wikipedia.org/wiki/Llista_de_països
- Geonames: http://www.geonames.org/
- OpenStreetMap: https://www.openstreetmap.org/

---

## PAS 2: Executar el script d'importació

```bash
python scripts/importar_ubicacions.py
```

Aquest script:
1. Llegeix el fitxer JSON
2. Crea el país a la taula `paisos`
3. Crea les regions a la taula `regions`
4. Crea els municipis a la taula `municipis`

**IMPORTANT:** El script està preparat per importar qualsevol fitxer de `data/*.json`. Si el fitxer es diu `italia.json`, el script l'importarà automàticament.

---

## PAS 3: Afegir traduccions (opcional però recomanat)

### Crear script de traduccions: `scripts/afegir_traduccions_italia.py`

```python
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Pais, Regio, TraducioUbicacio

def afegir_traduccions_italia():
    """Afegeix traduccions en múltiples idiomes per Itàlia"""
    
    with app.app_context():
        # Buscar Itàlia
        italia = Pais.query.filter_by(codi_iso='IT').first()
        
        if not italia:
            print("❌ No s'ha trobat Itàlia a la BD")
            return
        
        print(f"✅ Trobat país: {italia.nom} (ID: {italia.id})")
        
        # Traducció del país
        traduccions_pais = [
            ('ca', 'Itàlia'),
            ('es', 'Italia'),
            ('en', 'Italy'),
            ('it', 'Italia'),
            ('fr', 'Italie')
        ]
        
        for idioma, nom in traduccions_pais:
            existe = TraducioUbicacio.query.filter_by(
                tipus='pais',
                element_id=italia.id,
                idioma=idioma
            ).first()
            
            if not existe:
                traduccio = TraducioUbicacio(
                    tipus='pais',
                    element_id=italia.id,
                    idioma=idioma,
                    nom=nom
                )
                db.session.add(traduccio)
                print(f"  📝 Afegida traducció [{idioma}]: {nom}")
        
        # Traduccions de regions (exemple)
        traduccions_regions = {
            'Lombardia': {
                'ca': 'Llombardia',
                'es': 'Lombardía',
                'en': 'Lombardy',
                'it': 'Lombardia'
            },
            'Lazio': {
                'ca': 'Laci',
                'es': 'Lacio',
                'en': 'Lazio',
                'it': 'Lazio'
            },
            'Campania': {
                'ca': 'Campània',
                'es': 'Campania',
                'en': 'Campania',
                'it': 'Campania'
            }
        }
        
        for nom_original, traduccions in traduccions_regions.items():
            regio = Regio.query.filter_by(nom=nom_original, pais_id=italia.id).first()
            
            if regio:
                for idioma, nom_traduit in traduccions.items():
                    existe = TraducioUbicacio.query.filter_by(
                        tipus='regio',
                        element_id=regio.id,
                        idioma=idioma
                    ).first()
                    
                    if not existe:
                        traduccio = TraducioUbicacio(
                            tipus='regio',
                            element_id=regio.id,
                            idioma=idioma,
                            nom=nom_traduit
                        )
                        db.session.add(traduccio)
                        print(f"    📍 {nom_original} [{idioma}]: {nom_traduit}")
        
        db.session.commit()
        print("\n🎉 Traduccions afegides correctament!")
        
        # Estadístiques
        total = TraducioUbicacio.query.filter_by(tipus='pais', element_id=italia.id).count()
        print(f"📊 Total traduccions del país: {total}")

if __name__ == '__main__':
    print("🌍 Afegint traduccions per Itàlia...\n")
    afegir_traduccions_italia()
```

### Executar:

```bash
python scripts/afegir_traduccions_italia.py
```

---

## PAS 4: Verificar que funciona

1. **Arrenca l'app:**
   ```bash
   python app.py
   ```

2. **Ves a crear entrada:**
   ```
   http://localhost:5000/nova_entrada_personal
   ```

3. **Comprova:**
   - Selecciona l'idioma català → Hauria de sortir "Itàlia"
   - Selecciona l'idioma castellà → Hauria de sortir "Italia"
   - Selecciona "Itàlia/Italia" → Carrega regions (Llombardia, Laci, Campània...)
   - Selecciona una regió → Carrega municipis

---

## Idiomes suportats actualment

Codis ISO 639-1 que fas servir:
- `ca` - Català
- `es` - Castellà
- `en` - Anglès
- `eu` - Euskera
- `gl` - Gallec
- `ast` - Asturià
- `it` - Italià (exemple)
- `fr` - Francès (exemple)
- `de` - Alemany (exemple)
- `pt` - Portuguès (exemple)

**Pots afegir qualsevol idioma seguint el mateix patró!**

---

## Consells

### 1. No cal posar TOTS els municipis
Posa només els 10-20 principals. Els usuaris aniran afegint la resta automàticament quan creïn entrades.

### 2. Prioritza traduccions de països i regions
Els municipis no cal traduir-los (massa feina i els noms solen ser iguals).

### 3. Ordre d'idiomes recomanat
1. Idioma original del país
2. Català (el teu idioma principal)
3. Castellà (mercat espanyol)
4. Anglès (internacional)
5. Altres idiomes segons demanda

### 4. On trobar traduccions?
- Wikipedia multiidioma
- Wikidata: https://www.wikidata.org/
- Google Translate (per verificar)

---

## Estructura de fitxers

```
adabida/
├── data/
│   ├── espanya.json          ✅ Ja fet
│   ├── italia.json           ⬜ Exemple a crear
│   ├── franca.json           ⬜ Futur
│   └── ...
├── scripts/
│   ├── importar_ubicacions.py                  ✅ Script genèric (serveix per tots)
│   ├── afegir_traduccions_espanya.py           ✅ Ja fet
│   ├── afegir_traduccions_italia.py            ⬜ Exemple a crear
│   └── afegir_traduccions_franca.py            ⬜ Futur
└── models/
    └── ubicacions.py         ✅ Models Pais, Regio, Municipi, TraducioUbicacio
```

---

## Flux complet (resum)

```bash
# 1. Crear JSON
vim data/italia.json

# 2. Importar dades
python scripts/importar_ubicacions.py

# 3. Crear script de traduccions
cp scripts/afegir_traduccions_espanya.py scripts/afegir_traduccions_italia.py
# Editar i adaptar per Itàlia

# 4. Executar traduccions
python scripts/afegir_traduccions_italia.py

# 5. Verificar a l'app
python app.py
# Anar a /nova_entrada_personal i provar
```

---

## Notes finals

- El sistema està dissenyat per **escalar orgànicament**
- **No cal tenir tots els països des del dia 1**
- Afegeix països **segons demanda real d'usuaris**
- Els usuaris t'ompliran els municipis automàticament
- El sistema funciona igual per **qualsevol país del món**

---

## Si tens problemes

1. Comprova que el JSON està ben format (https://jsonlint.com/)
2. Mira els logs de l'script d'importació
3. Verifica que el codi ISO del país no estigui duplicat
4. Comprova que les traduccions tenen el `tipus` correcte ('pais' o 'regio')

---

**Sistema creat el 2025-01-27**  
**Per: Ilan (Adabida)**  
**Amb ajuda de: Claude (Anthropic)** 😄
