# Inicia o uvicorn para rodar o FastAPI
run:
	@uvicorn workout_api.main:app --reload


# Cria o banco de dados postgres
run-docker:
	@docker-compose up -d

# Cria as migrações do banco de dados postgres
create-migrations:
	@cmd /C "set PYTHONPATH=%cd% && alembic revision --autogenerate -m $(d)"

# Executa as migrações do banco de dados postgres
run-migrations:
	@cmd /C "set PYTHONPATH=%cd% && alembic upgrade head"