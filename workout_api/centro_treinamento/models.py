from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class CentroTreinamento(Base):
    __tablename__ = "centros_treinamento"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    localizacao = Column(String(200), nullable=True)

    atletas = relationship("Atleta", back_populates="centro")
