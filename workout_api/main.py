from fastapi import FastAPI
from workout_api.routers import api_router
from fastapi_pagination import add_pagination  # ⬅️ Import necessário

app = FastAPI(title='WorkoutApi')
app.include_router(api_router)

add_pagination(app)  # ⬅️ Ativa a paginação global
