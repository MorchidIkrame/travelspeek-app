from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    favoris = relationship("Favoris", back_populates="user")
    commentaires = relationship("Commentaire", back_populates="user")


class Monument(Base):
    __tablename__ = "monuments"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    ville = Column(String)
    description = Column(String)
    localisation = Column(String)
    images = Column(String)  # JSON كنص

    favoris = relationship("Favoris", back_populates="monument")
    commentaires = relationship("Commentaire", back_populates="monument")


class Favoris(Base):
    __tablename__ = "favoris"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    monument_id = Column(Integer, ForeignKey("monuments.id"))

    user = relationship("User", back_populates="favoris")
    monument = relationship("Monument", back_populates="favoris")


class Commentaire(Base):
    __tablename__ = "commentaires"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    monument_id = Column(Integer, ForeignKey("monuments.id"))
    texte = Column(String)

    user = relationship("User", back_populates="commentaires")
    monument = relationship("Monument", back_populates="commentaires")
