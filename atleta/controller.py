import datetime
from uuid import uuid4
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi_pagination import Page

from fastapi_pagination import Params 

from fastapi_pagination.ext.sqlalchemy import paginate 

from sqlalchemy.exc import IntegrityError 
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletasSimples
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DataBaseDependency

router = APIRouter()

@router.post(
    "/", 
    summary="Criar um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DataBaseDependency, 
    atleta_in: AtletaIn = Body(...)
):
    categoria_name = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_name)
    )).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"A categoria com {categoria_name} não foi encontrada")
    
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"O centro de treinamento {centro_treinamento_nome} não foi encontrado")

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.datetime.now(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
    
        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model)

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, 
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
        )

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao inserir os dados no banco")

    return AtletaOut.model_validate(atleta_model)


@router.get(
    "/", 
    summary="Consultar todos os atletas (com filtros e paginação eficiente)",
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletasSimples], 
)
async def query(
    db_session: DataBaseDependency,
    
    # requisito: Query parameters NOME e CPF
    nome: Optional[str] = None,
    cpf: Optional[str] = None, 
    
    pagination_params: Params = Depends(), 
) -> Page[AtletasSimples]:
    
    # 1. Monta a query com filtros--
    query = select(AtletaModel)
    
    if nome:
        query = query.filter(AtletaModel.nome.ilike(f'%{nome}%'))
    
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
    
    # 2. Usa o paginate da extensão SQLAlchemy, passando o params
    return await paginate(db_session, query, params=pagination_params) 


# == Endpoint GET ONE ==
@router.get(
    "/{id}", 
    summary="Consultar um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado pelo id: {id}")
    return atleta

# == Endpoint PATCH ==
@router.patch(
    "/{id}", 
    summary="Editar um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado pelo id: {id}")
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    await db_session.commit()
    await db_session.refresh(atleta)     
    return atleta

# == Endpoint DELETE ==
@router.delete(
    "/{id}", 
    summary="Deletar um atleta pelo id",
    status_code=status.HTTP_204_NO_CONTENT
)
async def query(id: UUID4, db_session: DataBaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado pelo id: {id}")
    
    await db_session.delete(atleta)
    await db_session.commit()

    #Implementação conforme o exercicio