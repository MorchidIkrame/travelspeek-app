from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Monument, Favoris, Commentaire
from pydantic import BaseModel
import json

app = FastAPI(title="Travelspeek Backend")

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

# ----------------------
# DB Dependency
# ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------
# Load monuments عند startup
# ----------------------
@app.on_event("startup")
def startup_event():
    db = next(get_db())

    with open("../assets/data.json", "r", encoding="utf-8") as f:
        monuments_data = json.load(f)

    for m in monuments_data:
        nom = m.get("NOM", "")
        ville = m.get("VILLE", "")
        description = m.get("DESCRIPTION", "")
        localisation = m.get("LOCALISATION", "")
        images = json.dumps(m.get("IMAGE", []))  # ✅ الحل هنا

        exists = db.query(Monument).filter(Monument.nom == nom).first()
        if not exists:
            monument = Monument(
                nom=nom,
                ville=ville,
                description=description,
                localisation=localisation,
                images=images
            )
            db.add(monument)

    db.commit()

# ----------------------
# Users
# ----------------------
class UserCreate(BaseModel):
    username: str
    email: str

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# ----------------------
# Monuments
# ----------------------
@app.get("/monuments/")
def get_monuments(db: Session = Depends(get_db)):
    monuments = db.query(Monument).all()

    # نرجعو images كـ list
    result = []
    for m in monuments:
        result.append({
            "id": m.id,
            "nom": m.nom,
            "ville": m.ville,
            "description": m.description,
            "localisation": m.localisation,
            "images": json.loads(m.images)
        })
    return result

# ----------------------
# Favoris
# ----------------------
class FavorisCreate(BaseModel):
    user_id: int
    monument_id: int

@app.post("/favoris/")
def add_favoris(fav: FavorisCreate, db: Session = Depends(get_db)):
    db_fav = Favoris(user_id=fav.user_id, monument_id=fav.monument_id)
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav

@app.get("/favoris/{user_id}")
def get_user_favoris(user_id: int, db: Session = Depends(get_db)):
    return db.query(Favoris).filter(Favoris.user_id == user_id).all()

# ----------------------
# Commentaires
# ----------------------
class CommentaireCreate(BaseModel):
    user_id: int
    monument_id: int
    content: str

@app.post("/commentaires/")
def add_comment(comment: CommentaireCreate, db: Session = Depends(get_db)):
    db_comment = Commentaire(
        user_id=comment.user_id,
        monument_id=comment.monument_id,
        texte=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.get("/commentaires/{monument_id}")
def get_monument_comments(monument_id: int, db: Session = Depends(get_db)):
    return db.query(Commentaire).filter(Commentaire.monument_id == monument_id).all()
