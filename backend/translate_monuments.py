import sqlite3
import time
from deep_translator import GoogleTranslator

# Configuration
DB_PATH = 'travelspeek.db'
LANGUAGES = {
    'en': 'english',
    'ar': 'arabic',
    'es': 'spanish'
}

def translate_text(text, target_lang):
    """Traduit un texte vers la langue cible"""
    try:
        if not text or len(text.strip()) == 0:
            return ""
        
        # Limite à 4500 caractères (limite de Google Translate)
        if len(text) > 4500:
            text = text[:4500]
        
        translator = GoogleTranslator(source='fr', target=target_lang)
        result = translator.translate(text)
        time.sleep(0.5)  # Pause pour éviter rate limit
        return result
    except Exception as e:
        print(f"Erreur de traduction ({target_lang}): {e}")
        return ""

def main():
    print("=" * 70)
    print("TRADUCTION FORCÉE DES MONUMENTS")
    print("=" * 70)
    
    # Connexion à la base
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Récupérer TOUS les monuments
    cursor.execute("SELECT id, nom, description FROM monuments")
    monuments = cursor.fetchall()
    
    total = len(monuments)
    print(f"{total} monuments trouvés")
    print(f"Durée estimée: {total * 3} secondes (~{total * 3 // 60} minutes)")
    print("=" * 70)
    
    success_count = 0
    error_count = 0
    
    for i, (monument_id, nom, description_fr) in enumerate(monuments, 1):
        print(f"\n[{i}/{total}] Monument #{monument_id}: {nom[:40]}...")
        
        if not description_fr or len(description_fr.strip()) == 0:
            print("Pas de description française - ignoré")
            continue
        
        try:
            # Traduire en anglais
            print("Traduction EN...", end=" ")
            desc_en = translate_text(description_fr, 'en')
            if desc_en:
                cursor.execute(
                    "UPDATE monuments SET description_en = ? WHERE id = ?",
                    (desc_en, monument_id)
                )
                print("✅")
            else:
                print("❌")
                error_count += 1
            
            # Traduire en arabe
            print("Traduction AR...", end=" ")
            desc_ar = translate_text(description_fr, 'ar')
            if desc_ar:
                cursor.execute(
                    "UPDATE monuments SET description_ar = ? WHERE id = ?",
                    (desc_ar, monument_id)
                )
                print("✅")
            else:
                print("❌")
                error_count += 1
            
            # Traduire en espagnol
            print("Traduction ES...", end=" ")
            desc_es = translate_text(description_fr, 'es')
            if desc_es:
                cursor.execute(
                    "UPDATE monuments SET description_es = ? WHERE id = ?",
                    (desc_es, monument_id)
                )
                print("✅")
            else:
                print("❌")
                error_count += 1
            
            conn.commit()
            success_count += 1
            
            # Pause tous les 10 monuments
            if i % 10 == 0:
                print(f"\n Sauvegarde... ({i}/{total})")
                time.sleep(2)
        
        except Exception as e:
            print(f"ERREUR: {e}")
            error_count += 1
            continue
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("TRADUCTION TERMINÉE!")
    print("=" * 70)
    print(f"Monuments traduits : {success_count}/{total}")
    print(f"Erreurs            : {error_count}")
    print("\n TESTEZ MAINTENANT:")
    print("   http://localhost:8000/monuments?lang=en")
    print("   http://localhost:8000/monuments?lang=ar")
    print("   http://localhost:8000/monuments?lang=es")
    print("=" * 70)

if __name__ == "__main__":
    main()