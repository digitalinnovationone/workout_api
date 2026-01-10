from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from workout_api.configs.database import get_session

DataBaseDependency = Annotated[AsyncSession, Depends(get_session)]