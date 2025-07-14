from fastapi import FastAPI
from workout_api.routers import api_router
from fastapi import FastAPI
from fastapi_pagination import add_pagination

app = FastAPI()

# seus includes de routers...
add_pagination(app)

app = FastAPI(title='WorkoutApi')
app.include_router(api_router)
