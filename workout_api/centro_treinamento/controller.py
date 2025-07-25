from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import (
    CentroTreinamentoIn,
    CentroTreinamentoOut,
)
from workout_api.contrib.dependencies import (
    DatabaseDependency,
    ParamsDependency,
)

router = APIRouter()


@router.post(
    '/',
    summary='Criar um novo Centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(
        id=uuid4(), **centro_treinamento_in.model_dump()
    )
    centro_treinamento_model = CentroTreinamentoModel(
        **centro_treinamento_out.model_dump()
    )
    db_session.add(centro_treinamento_model)
    try:
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=(
                'Já existe uma categoria cadastrada'
                f' com o nome: {centro_treinamento_model.nome}'
            ),
        )

    return centro_treinamento_out


@router.get(
    '/',
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=Page[CentroTreinamentoOut],
)
async def query(
    db_session: DatabaseDependency, params: ParamsDependency
) -> Page[CentroTreinamentoOut]:
    stmt: Select = select(CentroTreinamentoModel)
    page = await paginate(db_session, stmt, params=params)
    return page


@router.get(
    '/{id}',
    summary='Consulta um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(
    id: UUID4, db_session: DatabaseDependency
) -> CentroTreinamentoOut:
    stmt: Select = select(CentroTreinamentoModel).filter_by(id=id)
    result_query = await db_session.execute(stmt)

    centro_treinamento: Optional[CentroTreinamentoModel] = (
        result_query.scalar_one_or_none()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento não encontrado no id: {id}',
        )
    centro_treinamento_out = CentroTreinamentoOut.model_validate(
        centro_treinamento
    )
    return centro_treinamento_out
