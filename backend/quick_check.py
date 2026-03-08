"""
Vérification rapide - Est-ce que les traductions sont dans la base?
"""
import sqlite3

DB_PATH = r'C:\Users\HP\travelspeek_app\backend\travelspeek.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n" + "="*70)
print("VÉRIFICATION RAPIDE")
print("="*70)

# Monument ID=1
cursor.execute("SELECT nom, description_fr, description_en, description_ar, description_es FROM monuments WHERE id=1")
result = cursor.fetchone()

if result:
    nom, fr, en, ar, es = result
    print(f"\nMonument: {nom}\n")
    print(f"FR: {fr[:100] if fr else ' VIDE'}...")
    print(f"EN: {en[:100] if en else ' VIDE'}...")
    print(f"AR: {ar[:100] if ar else ' VIDE'}...")
    print(f"ES: {es[:100] if es else ' VIDE'}...")

# Compter
cursor.execute("SELECT COUNT(*) FROM monuments WHERE description_en IS NOT NULL AND description_en != ''")
en_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM monuments WHERE description_ar IS NOT NULL AND description_ar != ''")
ar_count = cursor.fetchone()[0]

print(f"\n RÉSUMÉ:")
print(f"  EN: {en_count}/120")
print(f"  AR: {ar_count}/120")

conn.close()

if en_count > 0 and ar_count > 0:
    print("\n TRADUCTIONS PRÉSENTES DANS LA BASE!")
    print("\n Si l'API retourne toujours du français, le problème est dans main.py")
else:
    print("\n TRADUCTIONS MANQUANTES DANS LA BASE!")
    print("\n Le script de traduction n'a pas fonctionné correctement")

print("="*70 + "\n")