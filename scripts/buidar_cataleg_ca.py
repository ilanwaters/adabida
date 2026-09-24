"""Buida totes les traduccions del català (idioma original del codi)."""
from babel.messages.pofile import read_po, write_po

RUTA = 'translations/ca/LC_MESSAGES/messages.po'

with open(RUTA, 'rb') as f:
    cataleg = read_po(f)

for missatge in cataleg:
    if missatge.id:
        if isinstance(missatge.string, tuple):
            missatge.string = ('',) * len(missatge.string)
        else:
            missatge.string = ''
        missatge.flags.discard('fuzzy')

with open(RUTA, 'wb') as f:
    write_po(f, cataleg, width=0)

print('Català buidat')