from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Atleta(Base):
    __tablename__ = "atletas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    idade = Column(Integer, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    centro_id = Column(Integer, ForeignKey("centros_treinamento.id"), nullable=False)

    categoria = relationship("Categoria", back_populates="atletas")
    centro = relationship("CentroTreinamento", back_populates="atletas")
