import sqlite3

DB_PATH = r'C:\Users\HP\travelspeek_app\backend\travelspeek.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Copier description → description_fr
cursor.execute("""
    UPDATE monuments 
    SET description_fr = description 
    WHERE description_fr IS NULL OR description_fr = ''
""")
conn.commit()
print(f'OK : {cursor.rowcount} monuments mis à jour')

# Vérification
cursor.execute("SELECT COUNT(*) FROM monuments WHERE description_fr IS NOT NULL AND description_fr != ''")
count = cursor.fetchone()[0]
print(f'Monuments avec description_fr : {count}')

conn.close()
