from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status, Query
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from fastapi_pagination import Page, add_pagination, paginate

from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency

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

    try:
        db_session.add(centro_treinamento_model)
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um centro de treinamento cadastrado com o nome: {centro_treinamento_in.nome}",
        )

    return centro_treinamento_out


@router.get(
    '/',
    summary='Consultar todos os centros de treinamento',
    response_model=Page[CentroTreinamentoOut],
)
async def query(
    db_session: DatabaseDependency,
    nome: str | None = Query(None, description="Filtrar por nome"),
    endereco: str | None = Query(None, description="Filtrar por endereço"),
):
    query_stmt = select(CentroTreinamentoModel)
    
    if nome:
        query_stmt = query_stmt.filter_by(nome=nome)
    if endereco:
        query_stmt = query_stmt.filter_by(endereco=endereco)

    centros = (await db_session.execute(query_stmt)).scalars().all()
    return paginate(centros)


@router.get(
    '/{id}',
    summary='Consulta um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento não encontrado no id: {id}',
        )
    return centro


@router.patch(
    '/{id}',
    summary='Editar um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def patch(
    id: UUID4,
    db_session: DatabaseDependency,
    centro_up: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:
    centro = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento não encontrado no id: {id}',
        )

    for key, value in centro_up.model_dump(exclude_unset=True).items():
        setattr(centro, key, value)

    try:
        await db_session.commit()
        await db_session.refresh(centro)
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um centro de treinamento cadastrado com o nome: {centro_up.nome}",
        )

    return centro


@router.delete(
    '/{id}',
    summary='Deletar um centro de treinamento pelo id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    centro = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento não encontrado no id: {id}',
        )

    await db_session.delete(centro)
    await db_session.commit()


# Integrar paginação
add_pagination(router)
