from typing import Annotated, Optional

from fastapi import Depends, Query
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession

from workout_api.configs.database import get_session

ParamsDependency = Annotated[Params, Depends(Params)]
DatabaseDependency = Annotated[AsyncSession, Depends(get_session)]


class AtletaFiltroQuery:
    def __init__(
        self,
        nome: Optional[str] = Query(None, description='Filtro por nome'),
        cpf: Optional[str] = Query(None, description='Filtro por CPF'),
    ):
        self.nome = nome
        self.cpf = cpf
