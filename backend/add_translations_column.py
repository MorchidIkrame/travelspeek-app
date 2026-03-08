# ========================================
# add_translations_column.py
# Ajouter les colonnes de traduction à la table monuments
# ========================================

import sqlite3

def add_translation_columns():
    """Ajouter les colonnes description_en, description_ar, description_es"""
    
    conn = sqlite3.connect('travelspeek.db')
    cursor = conn.cursor()
    
    try:
        # Vérifier si les colonnes existent déjà
        cursor.execute("PRAGMA table_info(monuments)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Ajouter description_en si elle n'existe pas
        if 'description_en' not in columns:
            print(" Ajout de la colonne description_en...")
            cursor.execute("ALTER TABLE monuments ADD COLUMN description_en TEXT")
            print(" Colonne description_en ajoutée")
        else:
            print("  Colonne description_en existe déjà")
        
        # Ajouter description_ar
        if 'description_ar' not in columns:
            print(" Ajout de la colonne description_ar...")
            cursor.execute("ALTER TABLE monuments ADD COLUMN description_ar TEXT")
            print(" Colonne description_ar ajoutée")
        else:
            print("  Colonne description_ar existe déjà")
        
        # Ajouter description_es
        if 'description_es' not in columns:
            print(" Ajout de la colonne description_es...")
            cursor.execute("ALTER TABLE monuments ADD COLUMN description_es TEXT")
            print(" Colonne description_es ajoutée")
        else:
            print(" Colonne description_es existe déjà")
        
        # Copier description dans description_fr (si pas déjà fait)
        if 'description_fr' not in columns:
            print(" Ajout de la colonne description_fr...")
            cursor.execute("ALTER TABLE monuments ADD COLUMN description_fr TEXT")
            cursor.execute("UPDATE monuments SET description_fr = description")
            print(" Descriptions françaises copiées dans description_fr")
        
        conn.commit()
        print("\n Structure de la base de données mise à jour !")
        
        # Afficher le nombre de monuments
        cursor.execute("SELECT COUNT(*) FROM monuments")
        count = cursor.fetchone()[0]
        print(f" Nombre de monuments : {count}")
        
    except Exception as e:
        print(f" Erreur : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("Modification de la structure de la base de données...\n")
    add_translation_columns()