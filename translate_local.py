#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script per traduir fitxers .po usant Argos Translate (100% local, sense enviar dades a internet)
"""

import os
from pathlib import Path

try:
    import argostranslate.package
    import argostranslate.translate
    print("✓ argostranslate està instal·lat")
except ImportError:
    print("❌ Cal instal·lar argostranslate:")
    print("   pip install argostranslate")
    exit(1)

# Configuració
TRANSLATIONS_DIR = "translations"
SOURCE_LANG = "ca"  # Català

# Mapa d'idiomes
LANG_MAP = {
    'en': 'en',  # Anglès
    'es': 'es',  # Castellà
    'fr': 'fr',  # Francès
    'de': 'de',  # Alemany
    'eu': 'eu',  # Basc
    'ru': 'ru',  # Rus
    'uk': 'uk',  # Ucraïnès
}

def download_language_packages():
    """Descarrega els paquets de traducció necessaris"""
    print("\n📦 Comprovant paquets d'idiomes...")
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    
    for lang_code in LANG_MAP.values():
        # Busca el paquet ca -> lang_code
        package = next(
            (p for p in available_packages 
             if p.from_code == SOURCE_LANG and p.to_code == lang_code),
            None
        )
        
        if package:
            if not package.is_installed():
                print(f"   Descarregant paquet {SOURCE_LANG} -> {lang_code}...")
                argostranslate.package.install_from_path(package.download())
            else:
                print(f"   ✓ Paquet {SOURCE_LANG} -> {lang_code} ja instal·lat")

def extract_entries(po_content):
    """Extreu les entrades msgid/msgstr del fitxer .po"""
    entries = []
    lines = po_content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('msgid "') and not line.startswith('msgid ""'):
            msgid = line[7:-1]
            
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('msgstr'):
                i += 1
            
            if i < len(lines):
                msgstr_line = lines[i].strip()
                msgstr = msgstr_line[8:-1] if msgstr_line.startswith('msgstr "') else ""
                is_fuzzy = (i > 0 and lines[i-2].strip().startswith('#, fuzzy'))
                
                entries.append({
                    'msgid': msgid,
                    'msgstr': msgstr,
                    'line_num': i,
                    'is_empty': msgstr == "",
                    'is_fuzzy': is_fuzzy
                })
        
        i += 1
    
    return entries

def translate_po_file(po_path, target_lang):
    """Tradueix un fitxer .po localment"""
    print(f"\n📝 Processant: {po_path}")
    
    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = extract_entries(content)
    empty_count = sum(1 for e in entries if e['is_empty'])
    
    print(f"   Entrades buides: {empty_count}")
    
    if empty_count == 0:
        print("   ✓ No cal traduir res!")
        return False
    
    # Carrega el traductor local
    try:
        translation = argostranslate.translate.get_translation_from_codes(SOURCE_LANG, target_lang)
        if not translation:
            print(f"   ❌ No s'ha trobat el paquet de traducció {SOURCE_LANG} -> {target_lang}")
            return False
    except Exception as e:
        print(f"   ❌ Error carregant traductor: {e}")
        return False
    
    lines = content.split('\n')
    modified = False
    translated_count = 0
    
    for entry in entries:
        if entry['is_empty'] and entry['msgid']:
            try:
                # Tradueix localment (sense enviar res a internet)
                translated_text = translation.translate(entry['msgid'])
                
                if translated_text:
                    lines[entry['line_num']] = f'msgstr "{translated_text}"'
                    modified = True
                    translated_count += 1
                    print(f"   ✓ '{entry['msgid'][:40]}...' -> '{translated_text[:40]}...'")
                
            except Exception as e:
                print(f"   ❌ Error traduint '{entry['msgid'][:30]}...': {e}")
    
    # Elimina marques fuzzy
    lines = [line for line in lines if not line.strip().startswith('#, fuzzy')]
    
    if modified:
        with open(po_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"   ✅ Traduïdes {translated_count} entrades")
        return True
    
    return False

def main():
    """Funció principal"""
    print("🔒 Traductor LOCAL de fitxers .po (sense enviar dades a internet)")
    print("=" * 70)
    
    # Descarrega paquets necessaris
    try:
        download_language_packages()
    except Exception as e:
        print(f"❌ Error descarregant paquets: {e}")
        return
    
    if not os.path.exists(TRANSLATIONS_DIR):
        print(f"❌ No es troba la carpeta '{TRANSLATIONS_DIR}'")
        return
    
    print("\nIdiomes disponibles:")
    for code in LANG_MAP.keys():
        print(f"  - {code}")
    
    choice = input("\nTraduir tots els idiomes? (s/n): ").lower()
    
    if choice == 's':
        langs_to_process = list(LANG_MAP.keys())
    else:
        lang = input("Quin idioma? (en/es/fr/de/eu/ru/uk): ").lower()
        if lang not in LANG_MAP:
            print("❌ Idioma no vàlid")
            return
        langs_to_process = [lang]
    
    total_modified = 0
    for lang_code in langs_to_process:
        po_file = Path(TRANSLATIONS_DIR) / lang_code / "LC_MESSAGES" / "messages.po"
        
        if not po_file.exists():
            print(f"⚠️  No existeix: {po_file}")
            continue
        
        if translate_po_file(po_file, LANG_MAP[lang_code]):
            total_modified += 1
    
    print("\n" + "=" * 70)
    print(f"✅ Procés completat! Fitxers modificats: {total_modified}")
    print("\n⚠️  Revisa les traduccions abans de compilar!")
    print("\n📦 Compila amb:")
    print("   pybabel compile -d translations")

if __name__ == "__main__":
    main()