"""
Script pour trouver les clés de traduction manquantes
"""
import os
import re
from pathlib import Path

# ===================================
# CONFIGURATION
# ===================================

FLUTTER_PROJECT_PATH = r"C:\Users\HP\travelspeek_app\lib"
TRANSLATIONS_FILE = r"C:\Users\HP\travelspeek_app\lib\core\l10n\app_translations.dart"

# ===================================
# FONCTIONS
# ===================================

def extract_tr_calls_from_dart(file_path):
    """Extrait toutes les clés .tr(context) d'un fichier Dart"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    # Pattern: 'key'.tr(context)
    pattern = r"'([^']+)'\.tr\(context\)"
    keys = re.findall(pattern, content)
    
    return keys

def extract_keys_from_translations_file(file_path):
    """Extrait toutes les clés définies dans app_translations.dart"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return set()
    
    # Pattern: 'key': {
    pattern = r"'([^']+)':\s*\{"
    keys = re.findall(pattern, content)
    
    return set(keys)

def scan_all_dart_files(root_path):
    """Scanne tous les fichiers Dart et extrait les clés .tr()"""
    print("\n SCANNING FLUTTER PROJECT...")
    
    all_keys = {}
    
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith('.dart'):
                file_path = os.path.join(root, file)
                keys = extract_tr_calls_from_dart(file_path)
                
                if keys:
                    relative_path = os.path.relpath(file_path, root_path)
                    all_keys[relative_path] = keys
                    print(f"{file}: {len(keys)} clés trouvées")
    
    return all_keys

def main():
    print("\n" + "="*70)
    print("VÉRIFICATION DES TRADUCTIONS MANQUANTES")
    print("="*70)
    
    # 1. Scanner les fichiers Dart
    dart_keys_by_file = scan_all_dart_files(FLUTTER_PROJECT_PATH)
    
    # 2. Extraire toutes les clés uniques utilisées
    all_used_keys = set()
    for keys in dart_keys_by_file.values():
        all_used_keys.update(keys)
    
    print(f"\n Total de clés UTILISÉES dans le code: {len(all_used_keys)}")
    
    # 3. Extraire les clés définies dans app_translations.dart
    if not os.path.exists(TRANSLATIONS_FILE):
        print(f"\n ERREUR: {TRANSLATIONS_FILE} n'existe pas!")
        return
    
    defined_keys = extract_keys_from_translations_file(TRANSLATIONS_FILE)
    print(f"Total de clés DÉFINIES dans app_translations.dart: {len(defined_keys)}")
    
    # 4. Trouver les clés manquantes
    missing_keys = all_used_keys - defined_keys
    
    print("\n" + "="*70)
    print("RÉSULTAT")
    print("="*70)
    
    if not missing_keys:
        print("\n PARFAIT ! Toutes les clés sont définies !")
    else:
        print(f"\n ATTENTION ! {len(missing_keys)} clés MANQUANTES :\n")
        
        for key in sorted(missing_keys):
            print(f" '{key}'")
        
        # Afficher dans quels fichiers elles sont utilisées
        print("\n" + "-"*70)
        print("FICHIERS CONCERNÉS :")
        print("-"*70 + "\n")
        
        for file_path, keys in dart_keys_by_file.items():
            missing_in_file = [k for k in keys if k in missing_keys]
            if missing_in_file:
                print(f"\n {file_path}:")
                for key in missing_in_file:
                    print(f"'{key}'")
        
        # Générer un fichier avec les clés à ajouter
        print("\n" + "="*70)
        print("GÉNÉRATION DU FICHIER DE CORRECTION")
        print("="*70)
        
        output_file = "MISSING_TRANSLATIONS.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("// ===================================\n")
            f.write("// CLÉS MANQUANTES À AJOUTER\n")
            f.write("// ===================================\n\n")
            
            for key in sorted(missing_keys):
                f.write(f"    '{key}': {{\n")
                f.write(f"      'en': '{key}',\n")
                f.write(f"      'fr': '{key}',\n")
                f.write(f"      'ar': '{key}',\n")
                f.write(f"      'es': '{key}',\n")
                f.write(f"    }},\n\n")
        
        print(f"\n Fichier généré: {output_file}")
        print("   → Copiez le contenu dans app_translations.dart")
        print("   → Puis traduisez manuellement chaque clé\n")
    
    # 5. Statistiques
    print("\n" + "="*70)
    print("STATISTIQUES")
    print("="*70)
    print(f"   Clés utilisées dans le code : {len(all_used_keys)}")
    print(f"   Clés définies dans app_translations.dart : {len(defined_keys)}")
    print(f"   Clés manquantes : {len(missing_keys)}")
    print(f"   Couverture : {(len(defined_keys) / len(all_used_keys) * 100):.1f}%")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()