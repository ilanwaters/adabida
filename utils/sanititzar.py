import bleach

ETIQUETES_PERMESES = [
    'p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'h3', 'h4'
]
ATRIBUTS_PERMESOS = {
    'a': ['href', 'title', 'target']
}

def neteja_html(contingut):
    if not contingut:
        return contingut
    return bleach.clean(
        contingut,
        tags=ETIQUETES_PERMESES,
        attributes=ATRIBUTS_PERMESOS,
        strip=True
    )