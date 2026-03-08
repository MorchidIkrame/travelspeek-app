"""
Script d'extraction et traduction automatique AMÉLIORÉ pour Flutter
Version 2.0 - Filtre les vraies chaînes uniquement
"""
import os
import re
from deep_translator import GoogleTranslator
import time

# Configuration
FLUTTER_PROJECT_PATH = r"C:\Users\HP\travelspeek_app\lib"
LANGUAGES = {
    'en': 'English',
    'fr': 'French', 
    'ar': 'Arabic',
    'es': 'Spanish'
}
OUTPUT_FILE = "app_translations_CLEAN.dart"

def is_valid_text(text):
    """Vérifie si c'est un vrai texte à traduire"""
    # Ignorer si trop court
    if len(text) < 3:
        return False
    
    # Ignorer si contient des variables Dart
    if '$' in text or '{' in text or '}' in text:
        return False
    
    # Ignorer si c'est juste des symboles
    if re.match(r'^[•\s\d\-\+\(\)]+$', text):
        return False
    
    # Ignorer les clés techniques (snake_case sans espaces)
    if '_' in text and ' ' not in text and text.islower():
        return False
    
    # Ignorer les URLs et emails
    if '@' in text or 'http' in text or '.com' in text:
        return False
    
    # Ignorer les noms de classes/fonctions
    if text[0].isupper() and '(' in text:
        return False
    
    return True

def extract_strings_from_dart(file_path):
    """Extrait SEULEMENT les vrais textes d'un fichier Dart"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    strings = []
    
    # Pattern 1: Text('...')
    pattern1 = r"Text\s*\(\s*['\"]([^'\"]+)['\"]"
    for match in re.finditer(pattern1, content):
        text = match.group(1)
        if is_valid_text(text):
            strings.append(text)
    
    # Pattern 2: hintText: '...'
    pattern2 = r"hintText:\s*['\"]([^'\"]+)['\"]"
    for match in re.finditer(pattern2, content):
        text = match.group(1)
        if is_valid_text(text):
            strings.append(text)
    
    # Pattern 3: return '...' (validations)
    pattern3 = r"return\s*['\"]([^'\"]+)['\"]"
    for match in re.finditer(pattern3, content):
        text = match.group(1)
        if is_valid_text(text):
            strings.append(text)
    
    # Pattern 4: content: Text('...')
    pattern4 = r"content:\s*(?:const\s+)?Text\s*\(\s*['\"]([^'\"]+)['\"]"
    for match in re.finditer(pattern4, content):
        text = match.group(1)
        if is_valid_text(text):
            strings.append(text)
    
    # Pattern 5: title: Text('...')
    pattern5 = r"title:\s*(?:const\s+)?Text\s*\(\s*['\"]([^'\"]+)['\"]"
    for match in re.finditer(pattern5, content):
        text = match.group(1)
        if is_valid_text(text):
            strings.append(text)
    
    # Pattern 6: 'text' (chaînes simples)
    pattern6 = r"['\"]([A-Z][^'\"]{10,})['\"]"
    for match in re.finditer(pattern6, content):
        text = match.group(1)
        if is_valid_text(text) and len(text) > 15:  # Phrases longues seulement
            strings.append(text)
    
    return list(set(strings))

def scan_dart_files(root_path):
    """Scanne tous les fichiers .dart"""
    all_strings = {}
    
    print("\n Scanning fichiers...")
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith('.dart'):
                file_path = os.path.join(root, file)
                strings = extract_strings_from_dart(file_path)
                
                if strings:
                    print(f" {file}: {len(strings)} textes")
                    all_strings[file] = strings
    
    return all_strings

def translate_string(text, target_lang):
    """Traduit un texte"""
    try:
        # Ne pas traduire si déjà dans la langue cible
        if target_lang == 'en' and text.replace('!', '').replace('?', '').isascii():
            return text
        
        translator = GoogleTranslator(source='auto', target=target_lang)
        result = translator.translate(text)
        time.sleep(0.3)
        return result
    except Exception as e:
        print(f"Erreur: {e}")
        return text

def generate_key(text):
    """Génère une clé propre"""
    # Nettoyer
    key = text.lower()
    key = re.sub(r'[^\w\s]', '', key)  # Enlever ponctuation
    key = re.sub(r'\s+', '_', key.strip())  # Espaces -> _
    key = key[:50]  # Limiter
    
    # Éviter les doublons
    if not key or key[0].isdigit():
        key = 'text_' + key
    
    return key

def create_translations_map(strings_by_file):
    """Crée les traductions"""
    print("\n" + "="*70)
    print("TRADUCTION EN COURS")
    print("="*70)
    
    # Collecter tous les textes
    all_strings = []
    for strings in strings_by_file.values():
        all_strings.extend(strings)
    
    # Dédupliquer et trier
    unique_strings = sorted(list(set(all_strings)))
    total = len(unique_strings)
    
    print(f"\n Textes uniques filtrés: {total}")
    print(f"Temps estimé: ~{int(total * 1.2)} secondes\n")
    
    translations_map = {}
    used_keys = set()
    
    for idx, text in enumerate(unique_strings, 1):
        # Générer clé unique
        base_key = generate_key(text)
        key = base_key
        counter = 1
        while key in used_keys:
            key = f"{base_key}_{counter}"
            counter += 1
        used_keys.add(key)
        
        print(f"[{idx}/{total}] {text[:50]}...")
        
        translations = {}
        
        # Traduire
        for lang_code, lang_name in LANGUAGES.items():
            print(f"   → {lang_name}...", end=' ')
            translated = translate_string(text, lang_code)
            translations[lang_code] = translated
            print(f"")
        
        translations_map[key] = translations
    
    return translations_map

def generate_dart_file(translations_map, output_file):
    """Génère le fichier Dart"""
    print("\n" + "="*70)
    print("GÉNÉRATION DU FICHIER")
    print("="*70)
    
    dart_code = """// ============================================================================
// AUTO-GENERATED FILE - CLEAN VERSION
// Generated by translate_flutter_clean.py
// ============================================================================

class AppTranslations {
  static const Map<String, Map<String, String>> translations = {
"""
    
    for key, translations in translations_map.items():
        dart_code += f"    '{key}': {{\n"
        for lang_code in ['en', 'fr', 'ar', 'es']:
            value = translations.get(lang_code, '').replace("'", "\\'")
            dart_code += f"      '{lang_code}': '{value}',\n"
        dart_code += "    },\n"
    
    dart_code += """  };

  /// Récupère une traduction
  static String get(String key, String languageCode) {
    return translations[key]?[languageCode] ?? key;
  }
}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(dart_code)
    
    print(f"\n Fichier généré: {output_file}")
    print(f" Total de clés: {len(translations_map)}")

def generate_replacement_guide(strings_by_file, translations_map):
    """Génère le guide"""
    guide_file = "REPLACEMENT_GUIDE_CLEAN.md"
    
    # Créer un mapping texte -> clé
    text_to_key = {}
    for key, translations in translations_map.items():
        text_to_key[translations['en']] = key
    
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write("# GUIDE DE REMPLACEMENT\n\n")
        
        for file, strings in strings_by_file.items():
            f.write(f"### {file}\n\n")
            f.write("```dart\n")
            f.write("// Import:\n")
            f.write("import '../../../core/l10n/string_extensions.dart';\n\n")
            
            for text in strings:
                # Trouver la clé
                key = None
                for k, trans in translations_map.items():
                    if trans['en'] == text or trans['fr'] == text:
                        key = k
                        break
                
                if key:
                    safe_text = text.replace("'", "\\'")
                    f.write(f"'{safe_text}' → '{key}'.tr(context)\n")
            
            f.write("```\n\n")
    
    print(f" Guide généré: {guide_file}")

def main():
    print("\n" + "="*70)
    print(" TRADUCTION AUTOMATIQUE FLUTTER - VERSION PROPRE")
    print("="*70)
    
    # Scanner
    print("\n ÉTAPE 1: Scanner les fichiers...")
    strings_by_file = scan_dart_files(FLUTTER_PROJECT_PATH)
    
    if not strings_by_file:
        print(" Aucun texte trouvé!")
        return
    
    print(f"\n Fichiers scannés: {len(strings_by_file)}")
    
    # Traduire
    print("\n ÉTAPE 2: Traduire...")
    translations_map = create_translations_map(strings_by_file)
    
    # Générer
    print("\n ÉTAPE 3: Générer les fichiers...")
    generate_dart_file(translations_map, OUTPUT_FILE)
    generate_replacement_guide(strings_by_file, translations_map)
    
    print("\n" + "="*70)
    print("🎉 TERMINÉ!")
    print("="*70)
    print(f"\n Fichiers générés:")
    print(f"   - {OUTPUT_FILE}")
    print(f"   - REPLACEMENT_GUIDE_CLEAN.md")

if __name__ == "__main__":
    main()