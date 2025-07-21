from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut, CentroTreinamentoUpdate
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo Centro de Treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    ct_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    try:
        ct_out = CentroTreinamentoOut(id=uuid4(), **ct_in.model_dump())
        ct_model = CentroTreinamentoModel(**ct_out.model_dump())
        db_session.add(ct_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um centro de treinamento cadastrado com o nome: {ct_in.nome}"
        )
    return ct_out

@router.get(
    '/',
    summary='Consultar todos os Centros de Treinamento',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[CentroTreinamentoOut],
)
async def query(
    db_session: DatabaseDependency,
    nome: Optional[str] = Query(None, description="Nome do centro de treinamento para filtrar")
) -> LimitOffsetPage[CentroTreinamentoOut]:
    query = select(CentroTreinamentoModel)
    if nome:
        query = query.filter(CentroTreinamentoModel.nome == nome)
    return await paginate(db_session, query)

@router.get(
    '/{id}',
    summary='Consulta um Centro de Treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    ct: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()
    if not ct:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de Treinamento não encontrado no id: {id}'
        )
    return ct


@router.patch(
    '/{id}',
    summary='Editar um Centro de Treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, ct_up: CentroTreinamentoUpdate = Body(...)) -> CentroTreinamentoOut:
    ct: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not ct:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de Treinamento não encontrado no id: {id}'
        )
    
    ct_update = ct_up.model_dump(exclude_unset=True)
    for key, value in ct_update.items():
        setattr(ct, key, value)

    try:
        await db_session.commit()
        await db_session.refresh(ct)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um centro de treinamento cadastrado com o nome: {ct_up.nome}"
        )

    return ct


@router.delete(
    '/{id}',
    summary='Deletar um Centro de Treinamento pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    ct: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not ct:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de Treinamento não encontrado no id: {id}'
        )
    
    await db_session.delete(ct)
    await db_session.commit()