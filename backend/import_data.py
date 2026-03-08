"""
========================================
Import monuments depuis data.json vers SQLite
========================================
"""

import json
from database import SessionLocal, engine
from models import Base, Monument

def import_monuments_from_json(json_file_path: str):
    """Importer les monuments depuis le fichier JSON"""
    
    # Créer les tables si elles n'existent pas
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    
    # Session DB
    db = SessionLocal()
    
    try:
        # Lire le fichier JSON
        print(f"Lecture du fichier {json_file_path}...")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"{len(data)} monuments trouvés dans le JSON\n")
        
        # Supprimer les anciens monuments
        print("Suppression des anciens monuments...")
        db.query(Monument).delete()
        db.commit()
        
        # Insérer les nouveaux monuments
        print("Insertion des monuments...\n")
        success_count = 0
        error_count = 0
        
        for idx, item in enumerate(data, 1):
            try:
                print(f"--- [{idx}/{len(data)}] {item.get('NOM', 'Sans nom')} ---")
                
                monument = Monument(
                    nom=item.get('NOM', ''),
                    ville=item.get('VILLE', ''),
                    description=item.get('DESCRIPTION', ''),
                    localisation=item.get('LOCALISATION', ''),
                    images=item.get('IMAGE', [])  # CORRECT: JSON array
                )
                
                db.add(monument)
                
                # Afficher les infos
                print(f"   {item.get('NOM', 'Sans nom')}")
                print(f"   Ville: {item.get('VILLE', 'N/A')}")
                print(f"   {len(item.get('IMAGE', []))} image(s)")
                
                success_count += 1
                
                # Commit tous les 50 monuments
                if success_count % 50 == 0:
                    db.commit()
                    print(f"\n  {success_count} monuments sauvegardés...\n")
                
            except Exception as e:
                print(f" Erreur pour {item.get('NOM', 'Sans nom')}: {e}")
                error_count += 1
                db.rollback()
                continue
        
        # Commit final
        db.commit()
        
        print(f"\n{'='*60}")
        print(f"SUCCÈS: {success_count} monuments importés")
        print(f"ERREURS: {error_count} monuments échoués")
        print(f"{'='*60}")
        
        # Vérification
        total_in_db = db.query(Monument).count()
        print(f"\n Vérification: {total_in_db} monuments dans la base de données")
        
        # Afficher quelques exemples
        print("\n Exemples de monuments importés:")
        examples = db.query(Monument).limit(3).all()
        for monument in examples:
            print(f"   • {monument.nom} ({monument.ville}) - {len(monument.images or [])} images")
        
    except FileNotFoundError:
        print(f"\n Erreur: Le fichier '{json_file_path}' n'existe pas!")
        print("   Assurez-vous que data.json est dans le même dossier.")
    except json.JSONDecodeError as e:
        print(f"\n Erreur JSON: {e}")
        print("   Le fichier data.json n'est pas un JSON valide.")
    except Exception as e:
        print(f"\n Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()
        print("\n Connexion à la base de données fermée")


if __name__ == "__main__":
    # Chemin vers votre fichier JSON
    json_file = "data.json"
    
    print("=" * 60)
    print(" IMPORT MONUMENTS DANS LA BASE DE DONNÉES")
    print("=" * 60)
    print()
    
    import_monuments_from_json(json_file)
    
    print()
    print("=" * 60)
    print("TERMINÉ!")
    print("=" * 60)