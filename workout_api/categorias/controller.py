from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy import Select, select

from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import (
    DatabaseDependency,
    ParamsDependency,
)

router = APIRouter()


@router.post(
    '/',
    summary='Criar uma nova Categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out


@router.get(
    '/',
    summary='Consultar todas as Categorias',
    status_code=status.HTTP_200_OK,
    response_model=Page[CategoriaOut],
)
async def query(
    db_session: DatabaseDependency, params: ParamsDependency
) -> Page[CategoriaOut]:
    stmt: Select = select(CategoriaModel)
    page = await paginate(db_session, stmt, params=params)
    return page


@router.get(
    '/{id}',
    summary='Consulta uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    stmt: Select = select(CategoriaModel).filter_by(id=id)
    query_result = await db_session.execute(stmt)
    categoria: Optional[CategoriaOut] = query_result.scalar()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria não encontrada no id: {id}',
        )

    return categoria
