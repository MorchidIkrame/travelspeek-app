# ══════════════════════════════════════════════════════
# Script de vérification CORRIGÉ : backend/check_images.py
# ══════════════════════════════════════════════════════

import sqlite3
import json

def check_monument_images():
    """Vérifier les images des monuments"""
    
    conn = sqlite3.connect('travelspeek.db')
    cursor = conn.cursor()
    
    # D'abord, vérifier quelles colonnes existent
    cursor.execute("PRAGMA table_info(monuments)")
    columns = cursor.fetchall()
    
    print("=" * 80)
    print("COLONNES DISPONIBLES DANS LA TABLE MONUMENTS")
    print("=" * 80)
    for col in columns:
        print(f"   - {col[1]} ({col[2]})")
    print()
    
    # Construire la requête selon les colonnes disponibles
    column_names = [col[1] for col in columns]
    
    has_main_image = 'main_image' in column_names
    has_images = 'images' in column_names
    has_image_url = 'image_url' in column_names
    
    # Construire la requête SELECT
    select_columns = ['id', 'nom', 'ville']
    if has_main_image:
        select_columns.append('main_image')
    if has_images:
        select_columns.append('images')
    if has_image_url:
        select_columns.append('image_url')
    
    query = f"SELECT {', '.join(select_columns)} FROM monuments ORDER BY id"
    
    cursor.execute(query)
    monuments = cursor.fetchall()
    
    print("=" * 80)
    print("VÉRIFICATION DES IMAGES DES MONUMENTS")
    print("=" * 80)
    print(f"Total monuments: {len(monuments)}")
    print()
    
    problems = []
    
    for row in monuments:
        monument_id = row[0]
        nom = row[1]
        ville = row[2]
        
        print(f"Monument #{monument_id}: {nom} ({ville})")
        print("-" * 80)
        
        col_index = 3  # Commence après id, nom, ville
        
        # Vérifier main_image si elle existe
        if has_main_image:
            main_image = row[col_index]
            if main_image:
                print(f"main_image: {main_image[:80]}...")
            else:
                print(f"main_image: NULL")
                problems.append(f"Monument #{monument_id} ({nom}): Pas de main_image")
            col_index += 1
        
        # Vérifier images si elle existe
        if has_images:
            images_json = row[col_index]
            if images_json:
                try:
                    images = json.loads(images_json)
                    if isinstance(images, list):
                        print(f"images: {len(images)} image(s)")
                        for i, img in enumerate(images[:3]):  # Afficher les 3 premières
                            print(f"      [{i+1}] {img[:80]}...")
                    else:
                        print(f"images: Format incorrect (pas une liste)")
                        problems.append(f"Monument #{monument_id} ({nom}): images pas une liste")
                except json.JSONDecodeError:
                    print(f"images: Erreur JSON")
                    problems.append(f"Monument #{monument_id} ({nom}): Erreur JSON dans images")
            else:
                print(f"images: NULL")
                problems.append(f"Monument #{monument_id} ({nom}): Pas d'images")
            col_index += 1
        
        # Vérifier image_url si elle existe
        if has_image_url:
            image_url = row[col_index]
            if image_url:
                print(f"image_url: {image_url[:80]}...")
            else:
                print(f"image_url: NULL")
                problems.append(f"Monument #{monument_id} ({nom}): Pas de image_url")
        
        print()
    
    conn.close()
    
    # Résumé
    print("=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    print(f"Total monuments: {len(monuments)}")
    print(f"Problèmes détectés: {len(problems)}")
    
    if problems:
        print()
        print("PROBLÈMES:")
        for problem in problems:
            print(f"   - {problem}")
    else:
        print()
        print("Aucun problème détecté!")
    
    print()
    print("=" * 80)
    print("RECOMMANDATIONS")
    print("=" * 80)
    if not has_main_image:
        print("La colonne 'main_image' n'existe pas dans votre base de données.")
        print("   Vos images sont probablement stockées dans la colonne 'images' (JSON)")
    if not has_images:
        print("La colonne 'images' n'existe pas dans votre base de données.")
    
    print()
    print("Structure utilisée par votre app Flutter:")
    if has_images:
        print("Colonne 'images' (JSON array) → OK pour Flutter")
    if has_main_image:
        print("Colonne 'main_image' → OK pour Flutter")
    elif has_image_url:
        print("Colonne 'image_url' → Vérifier si Flutter utilise bien ce nom")

if __name__ == "__main__":
    check_monument_images()