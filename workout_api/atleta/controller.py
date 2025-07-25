import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import (
    AtletaIn,
    AtletaListagemOut,
    AtletaOut,
    AtletaUpdate,
    get_filtro_query,
)
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import (
    AtletaFiltroQuery,
    DatabaseDependency,
    ParamsDependency,
)

router = APIRouter()


@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)
):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    stmt: Select = select(CategoriaModel).filter_by(nome=categoria_nome)
    categoria = (await db_session.execute(stmt)).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada.',
        )
    stmt: Select = select(CentroTreinamentoModel).filter_by(
        nome=centro_treinamento_nome
    )
    centro_treinamento = (await db_session.execute(stmt)).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_nome}'
            ' não foi encontrado.',
        )
    cpf_atleta: str = atleta_in.cpf
    try:
        atleta_out = AtletaOut(
            id=uuid4(),
            created_at=datetime.datetime.now(datetime.timezone.utc),
            **atleta_in.model_dump(),
        )
        atleta_model = AtletaModel(
            **atleta_out.model_dump(
                exclude={'categoria', 'centro_treinamento'}
            )
        )

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o cpf: {cpf_atleta}',
        )

    return atleta_out


@router.get(
    '/',
    summary='Filtra atleta por nome ou CPF',
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaListagemOut],
)
async def query(
    db_session: DatabaseDependency,
    params: ParamsDependency,
    filtro: AtletaFiltroQuery = Depends(get_filtro_query),
) -> Page[AtletaListagemOut]:
    stmt: Select = select(AtletaModel).options(
        selectinload(AtletaModel.categoria),
        selectinload(AtletaModel.centro_treinamento),
    )
    if filtro:
        if filtro.cpf:
            stmt = stmt.where(AtletaModel.cpf == filtro.cpf)
        if filtro.nome:
            stmt = stmt.where(AtletaModel.nome.ilike(f'%{filtro.nome}%'))

    page = await paginate(db_session, stmt, params=params)
    return page


@router.get(
    '/{id}',
    summary='Consulta um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    stmt: Select = select(AtletaModel).filter_by(id=id)
    query_result = await db_session.execute(stmt)
    atleta: Optional[AtletaOut] = query_result.scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}',
        )

    return atleta


@router.patch(
    '/{id}',
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(
    id: UUID4,
    db_session: DatabaseDependency,
    atleta_up: AtletaUpdate = Body(...),
) -> AtletaOut:
    stmt = select(AtletaModel).filter_by(id=id)
    query_result = await db_session.execute(stmt)
    atleta: Optional[AtletaModel] = query_result.scalars().first()
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}',
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return AtletaOut.model_validate(atleta)


@router.delete(
    '/{id}',
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    stmt: Select = select(AtletaModel).filter_by(id=id)
    query_result = await db_session.execute(stmt)
    atleta: Optional[AtletaModel] = query_result.scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}',
        )

    await db_session.delete(atleta)
    await db_session.commit()
