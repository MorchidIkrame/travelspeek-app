"""
========================================
Import monuments depuis data.json vers SQLite
========================================
"""

import json
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Monument

def import_monuments_from_json(json_file_path: str):
    """Importer les monuments depuis le fichier JSON"""
    
    # Créer les tables
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    
    # Session DB
    db = SessionLocal()
    
    try:
        # Lire le fichier JSON
        print(f"Lecture du fichier {json_file_path}...")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"{len(data)} monuments trouvés dans le JSON")
        
        # Supprimer les anciens monuments
        print("Suppression des anciens monuments...")
        db.query(Monument).delete()
        db.commit()
        
        # Insérer les nouveaux monuments
        print("Insertion des monuments...")
        count = 0
        
        for item in data:
            monument = Monument(
                nom=item.get('NOM', ''),
                ville=item.get('VILLE', ''),
                description=item.get('DESCRIPTION', ''),
                localisation=item.get('LOCALISATION', ''),
                images=item.get('IMAGE', [])  # JSON array
            )
            db.add(monument)
            count += 1
            
            # Commit tous les 50 monuments
            if count % 50 == 0:
                db.commit()
                print(f"   → {count} monuments importés...")
        
        # Commit final
        db.commit()
        print(f"\n {count} monuments importés avec succès!")
        
        # Vérification
        total_in_db = db.query(Monument).count()
        print(f"Vérification: {total_in_db} monuments dans la base de données")
        
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{json_file_path}' n'existe pas!")
        print("   Assurez-vous que data.json est dans le même dossier que ce script.")
    except json.JSONDecodeError as e:
        print(f"Erreur JSON: {e}")
        print("   Le fichier data.json n'est pas un JSON valide.")
    except Exception as e:
        print(f"Erreur: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Chemin vers votre fichier JSON
    json_file = "data.json"
    
    print("=" * 50)
    print("IMPORT MONUMENTS DANS LA BASE DE DONNÉES")
    print("=" * 50)
    print()
    
    import_monuments_from_json(json_file)
    
    print()
    print("=" * 50)
    print("TERMINÉ!")
    print("=" * 50)