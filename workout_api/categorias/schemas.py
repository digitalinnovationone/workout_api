from typing import Annotated, Optional

from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=50)]


class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]


class CategoriaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome da categoria', example='Scale', max_length=50)]
