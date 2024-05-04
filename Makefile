run:
	@uvicorn workout_api.main:app --reload

run-docker:
	docker compose up --detach

stop-docker:
	docker compose down
	
create-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic revision --autogenerate -m $(d)

run-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic upgrade head