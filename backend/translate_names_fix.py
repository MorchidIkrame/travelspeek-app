"""
Script pour traduire:
- NOMS des monuments: EN, AR, ES
- VILLES: AR seulement
"""
import sqlite3
from deep_translator import GoogleTranslator
import time

DB_PATH = r'C:\Users\HP\travelspeek_app\backend\travelspeek.db'

def translate_text(text, target_lang):
    try:
        translator = GoogleTranslator(source='fr', target=target_lang)
        return translator.translate(text)
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def main():
    print("\n" + "="*70)
    print("TRADUCTION DES NOMS ET VILLES")
    print("="*70)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Récupérer TOUS les monuments
    cursor.execute("SELECT id, nom, ville FROM monuments")
    monuments = cursor.fetchall()
    total = len(monuments)
    
    print(f"{total} monuments trouvés")
    print(f"Durée estimée: ~{total * 2} secondes (~{total * 2 // 60} minutes)")
    print("="*70)

    success = 0
    errors = 0

    for idx, (mid, nom, ville) in enumerate(monuments, 1):
        print(f"\n[{idx}/{total}] Monument #{mid}: {nom[:50]}...")
        
        updates = {}
        
        # ═══════════════════════════════════════════════════
        # TRADUIRE LE NOM EN 3 LANGUES (EN, AR, ES)
        # ═══════════════════════════════════════════════════
        for lang_code, lang_name in [('en', 'EN'), ('ar', 'AR'), ('es', 'ES')]:
            print(f"Nom → {lang_name}...", end=' ')
            nom_translated = translate_text(nom, lang_code)
            if nom_translated:
                updates[f'nom_{lang_code}'] = nom_translated
                print(f"✅ {nom_translated[:40]}")
            else:
                print("❌")
                errors += 1
            time.sleep(0.4)  # Pause pour éviter rate limit

        # ═══════════════════════════════════════════════════
        # TRADUIRE LA VILLE EN ARABE SEULEMENT
        # ═══════════════════════════════════════════════════
        print(f"Ville → AR...", end=' ')
        ville_ar = translate_text(ville, 'ar')
        if ville_ar:
            updates['ville_ar'] = ville_ar
            print(f"✅ {ville_ar}")
        else:
            print("❌")
            errors += 1
        time.sleep(0.4)

        # Sauvegarder en base
        if updates:
            cols = ', '.join([f"{k} = ?" for k in updates.keys()])
            vals = list(updates.values()) + [mid]
            cursor.execute(f"UPDATE monuments SET {cols} WHERE id = ?", vals)
            conn.commit()
            success += 1
        
        # Pause tous les 10 monuments
        if idx % 10 == 0:
            print(f"\n Sauvegarde... ({idx}/{total})")
            time.sleep(2)

    conn.close()

    print("\n" + "="*70)
    print("TRADUCTION TERMINÉE!")
    print("="*70)
    print(f" Monuments traduits : {success}/{total}")
    print(f" Erreurs            : {errors}")
    print("\n TESTEZ MAINTENANT:")
    print("   http://localhost:8000/monuments?lang=en")
    print("   http://localhost:8000/monuments?lang=ar")
    print("   http://localhost:8000/monuments?lang=es")
    print("="*70)

if __name__ == '__main__':
    print("\n IMPORTANT: Cette opération va prendre 8-12 minutes")
    print("Ne fermez pas la fenêtre pendant l'exécution!\n")
    response = input("Voulez-vous continuer? (o/n): ")
    if response.lower() == 'o':
        main()
    else:
        print("Annulé")