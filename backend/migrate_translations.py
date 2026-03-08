import sqlite3

print("=" * 80)
print("MIGRATION DES TRADUCTIONS")
print("=" * 80)
print()

conn = sqlite3.connect('travelspeek.db')
cursor = conn.cursor()

# Vérifier si les colonnes existent
cursor.execute("PRAGMA table_info(monuments)")
columns = [col[1] for col in cursor.fetchall()]

print("Colonnes actuelles dans monuments:")
for col in columns:
    print(f"  - {col}")
print()

# Ajouter les colonnes si elles n'existent pas
for lang in ['en', 'ar', 'es']:
    col_name = f'description_{lang}'
    if col_name not in columns:
        print(f"Ajout de la colonne {col_name}...")
        cursor.execute(f"ALTER TABLE monuments ADD COLUMN {col_name} TEXT")
        conn.commit()

# Migrer les traductions
print("\n Migration des traductions...")

cursor.execute("""
    SELECT monument_id, lang, description 
    FROM monument_translations
    WHERE lang IN ('en', 'ar', 'es')
""")

translations = cursor.fetchall()
total = len(translations)

for idx, (monument_id, lang, description) in enumerate(translations, 1):
    col_name = f'description_{lang}'
    
    cursor.execute(f"""
        UPDATE monuments 
        SET {col_name} = ? 
        WHERE id = ?
    """, (description, monument_id))
    
    if idx % 30 == 0:
        print(f" {idx}/{total} traductions migrées...")

conn.commit()
print(f"\n {total} traductions migrées avec succès !")

# Vérification
print("\n VÉRIFICATION:")
for lang in ['fr', 'en', 'ar', 'es']:
    col_name = f'description_{lang}' if lang != 'fr' else 'description'
    cursor.execute(f"SELECT COUNT(*) FROM monuments WHERE {col_name} IS NOT NULL AND {col_name} != ''")
    count = cursor.fetchone()[0]
    emoji = {'fr': '🇫🇷', 'en': '🇬🇧', 'ar': '🇸🇦', 'es': '🇪🇸'}[lang]
    print(f"  {emoji} {lang.upper()}: {count} monuments")

conn.close()

print("\n" + "=" * 80)
print("MIGRATION TERMINÉE !")
print("Votre backend est maintenant prêt pour le multilingue")
print("=" * 80)