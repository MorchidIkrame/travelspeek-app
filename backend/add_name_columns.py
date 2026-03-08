"""
Script pour ajouter les colonnes de traduction des NOMS et VILLES
"""
import sqlite3

DB_PATH = r'C:\Users\HP\travelspeek_app\backend\travelspeek.db'

print("\n" + "="*70)
print("AJOUT DES COLONNES POUR NOMS TRADUITS")
print("="*70)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Colonnes à ajouter
columns_to_add = [
    ('nom_en', 'TEXT'),
    ('nom_ar', 'TEXT'),
    ('nom_es', 'TEXT'),
    ('ville_en', 'TEXT'),
    ('ville_ar', 'TEXT'),
    ('ville_es', 'TEXT'),
]

print("\n Ajout des colonnes...")

for column_name, column_type in columns_to_add:
    try:
        cursor.execute(f"ALTER TABLE monuments ADD COLUMN {column_name} {column_type}")
        print(f"Colonne {column_name} ajoutée")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"Colonne {column_name} existe déjà")
        else:
            print(f"Erreur pour {column_name}: {e}")

conn.commit()

# Vérifier
cursor.execute("PRAGMA table_info(monuments)")
columns = [col[1] for col in cursor.fetchall()]

print("\n Colonnes disponibles:")
for col in ['nom', 'nom_en', 'nom_ar', 'nom_es', 'ville', 'ville_en', 'ville_ar', 'ville_es']:
    status = '' if col in columns else ''
    print(f"  {status} {col}")

conn.close()

print("\n" + "="*70)
print("TERMINÉ!")
print("="*70 + "\n")