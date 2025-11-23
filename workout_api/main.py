from fastapi import FastAPI
from app.routers import router
from app.database import Base, engine

# Cria todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Desafio DIO - Atletas",
    description="CRUD completo de atletas, categorias e centros de treinamento",
    version="1.0.0"
)

# Inclui todos os endpoints
app.include_router(router)

