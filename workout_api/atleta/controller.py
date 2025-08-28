from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status, Query
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi_pagination import Page, add_pagination, paginate

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...),
):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome))
    ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada.'
        )
    
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )

    atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
    atleta_model.categoria_id = categoria.pk_id
    atleta_model.centro_treinamento_id = centro_treinamento.pk_id

    try:
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
        )

    return atleta_out


@router.get(
    '/',
    summary='Consultar todos os Atletas',
    response_model=Page[AtletaOut],
)
async def query(
    db_session: DatabaseDependency,
    nome: str | None = Query(None, description="Filtrar por nome"),
    cpf: str | None = Query(None, description="Filtrar por CPF"),
):
    query_stmt = select(AtletaModel)
    if nome:
        query_stmt = query_stmt.filter_by(nome=nome)
    if cpf:
        query_stmt = query_stmt.filter_by(cpf=cpf)

    atletas = (await db_session.execute(query_stmt)).scalars().all()
    return paginate(atletas)


@router.get(
    '/{id}',
    summary='Consulta um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )
    return atleta


@router.patch(
    '/{id}',
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    for key, value in atleta_up.model_dump(exclude_unset=True).items():
        setattr(atleta, key, value)

    try:
        await db_session.commit()
        await db_session.refresh(atleta)
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_up.cpf}"
        )

    return atleta


@router.delete(
    '/{id}',
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    await db_session.delete(atleta)
    await db_session.commit()


# Integrar paginação
add_pagination(router)
