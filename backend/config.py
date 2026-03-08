import os

# Configuration sécurité
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "SUPER_SECRET_CHANGE_ME")
ALGORITHM = "HS256"

# Tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

# ✅ En local → SQLite | En production (Railway) → PostgreSQL automatiquement
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'travelspeek.db')}"
)

# ✅ Railway donne une URL qui commence par "postgres://" → SQLAlchemy veut "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Base de données : {DATABASE_URL}")