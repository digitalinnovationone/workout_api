# criar_tabelas.py
import asyncio
from workout_api.configs.database import engine
from workout_api.atleta.models import Base

async def criar_tabelas():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    asyncio.run(criar_tabelas())
