"""Detecta traduccions repetides per a molts textos diferents (restes de fuzzy matching)."""
from collections import defaultdict
from pathlib import Path

from babel.messages.pofile import read_po

LLINDAR = 3  # mateixa traducció per a 3 o més textos diferents

for po in sorted(Path('translations').glob('*/LC_MESSAGES/messages.po')):
    idioma = po.parts[1]
    if idioma == 'ca':
        continue
    with open(po, 'rb') as f:
        cataleg = read_po(f)

    per_traduccio = defaultdict(list)
    for m in cataleg:
        if m.id and isinstance(m.string, str) and m.string:
            per_traduccio[m.string].append(m.id)

    sospitoses = {t: ids for t, ids in per_traduccio.items() if len(ids) >= LLINDAR}
    total = sum(len(ids) for ids in sospitoses.values())
    print(f'\n=== {idioma}: {total} entrades sospitoses ===')
    for traduccio, ids in list(sospitoses.items())[:5]:
        print(f'  "{traduccio}" <- {ids[:4]}')