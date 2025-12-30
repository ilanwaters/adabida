# Sistema d'Aportacions - Adabida

## Base de dades

**Taula: `aportacions`**
```sql
- id (SERIAL PRIMARY KEY)
- usuari_id (FK → usuaris.id, nullable)
- quantitat (NUMERIC(10,2), NOT NULL)
- data (TIMESTAMP, NOT NULL)
- metode_pagament (VARCHAR(50), nullable)
- estat (VARCHAR(20), NOT NULL, default='confirmada')
- notes (TEXT, nullable)
- pais (VARCHAR(100), nullable)
- referit_per (FK → usuaris.id, nullable)
- comissio_percentatge (NUMERIC(5,2), nullable)
- comissio_pagada (BOOLEAN, NOT NULL, default=false)
```

## Model

**Fitxer:** `models/aportacio.py`

```python
class Aportacio(db.Model):
    # Camps bàsics
    id, usuari_id, quantitat, data, metode_pagament, estat, notes
    
    # Tracking de referits
    pais, referit_per, comissio_percentatge, comissio_pagada
    
    # Relacions
    usuari = relationship('Usuari', foreign_keys=[usuari_id])
    referidor = relationship('Usuari', foreign_keys=[referit_per])
```

## Routes

**Fitxer:** `routes/admin/aportacions.py`

**Blueprint:** `admin_aportacions_bp` (prefix: `/admin`)

**Rutes:**
- `GET /admin/aportacions` → Llista totes les aportacions + estadístiques
- `GET/POST /admin/aportacions/nova` → Formulari per registrar aportació

**Funcions:**
- `aportacions()` - Visualització amb total recaptat
- `nova_aportacio()` - Registre manual d'aportacions

## Templates

**templates/admin/aportacions.html**
- Taula amb totes les aportacions
- Estadístiques: total recaptat, nombre d'aportacions
- Botó per crear nova aportació

**templates/admin/nova_aportacio.html**
- Formulari amb tots els camps
- Dropdown d'usuaris
- Camps de referit i comissió per col·laboradors

## Funcionalitat

### Actual
- Registre manual d'aportacions per admin
- Tracking de país d'origen
- Sistema de comissions per col·laboradors (referits)
- Assignació opcional a usuari
- Estadístiques bàsiques

### Casos d'ús
1. Aportació anònima: usuari_id = NULL
2. Aportació amb referit: es registra qui l'ha aconseguit + comissió
3. Tracking per país: permet veure d'on arriben aportacions

### Estats possibles
- `confirmada` (default)
- `pendent`
- `cancel·lada`

### Mètodes de pagament
- Transferència
- Bizum
- PayPal
- Targeta

## Importació a app.py

```python
from routes.admin.aportacions import admin_aportacions_bp
app.register_blueprint(admin_aportacions_bp)
```

## Enllaç al menú admin

```html
<li><a href="{{ url_for('admin_aportacions.aportacions') }}">Gestió d'aportacions</a></li>
```

## Notes tècniques

- NO hi ha integració de pagament automàtic
- Registre 100% manual per l'admin
- Pensat per escalar a múltiples col·laboradors per país
- Sistema de comissions per incentivar col·laboradors
