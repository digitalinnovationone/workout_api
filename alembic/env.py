import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.engine import Connection
from alembic import context
from workout_api.contrib.models import BaseModel
from workout_api.centro_treinamento.models import BaseModel
from workout_api.contrib.repository.models import *


target_metadata = BaseModel.metadata

# Configuração Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Rodar migrações em modo offline (sem conexão ao banco)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Executa migrações com uma conexão."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """Executa migrações assíncronas."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def run_migrations_online() -> None:
    """Rodar migrações em modo online (com conexão)."""
    asyncio.run(run_async_migrations())


# Rodar de acordo com o modo
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
