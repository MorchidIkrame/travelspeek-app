import sqlite3
from datetime import datetime

def create_feedback_table():
    """
    Crée la table feedback dans la base de données
    """
    print("Création de la table feedback...")
    
    conn = sqlite3.connect('travelspeek.db')
    cursor = conn.cursor()
    
    # Créer la table feedback
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            category TEXT DEFAULT 'general',
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Créer un index pour la performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_feedback_user 
        ON feedback(user_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_feedback_rating 
        ON feedback(rating)
    """)
    
    conn.commit()
    
    # Vérifier
    cursor.execute("SELECT COUNT(*) FROM feedback")
    count = cursor.fetchone()[0]
    
    print(f"Table feedback créée avec succès !")
    print(f"Nombre de feedback : {count}")
    
    conn.close()
    print("\n Configuration terminée !\n")

if __name__ == "__main__":
    create_feedback_table()