from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from fastapi import APIRouter, Body, HTTPException, status, Query
from pydantic import UUID4

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from fastapi_pagination import Page, paginate

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

# -----------------------------
# POST: Criar um novo atleta
# -----------------------------
@router.post(
    '/', 
    summary='Criar um novo atleta',
@@ -23,6 +29,10 @@ async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn = Body(...)
):
    """
    Cria um novo atleta. Valida se categoria e centro de treinamento existem.
    Trata duplicidade de CPF com status 303.
    """
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

@@ -45,43 +55,70 @@ async def post(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        

        db_session.add(atleta_model)
        await db_session.commit()

    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
        )
    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Ocorreu um erro ao inserir os dados no banco'
        )

    return atleta_out


# -----------------------------
# GET: Listar atletas com filtro
# -----------------------------
@router.get(
    '/', 
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
    '/',
    summary='Consultar todos os atletas com filtros e paginação',
    response_model=Page[AtletaOut]
)
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
async def query(
    db_session: DatabaseDependency,
    nome: str | None = Query(None, description="Filtrar atletas pelo nome"),
    cpf: str | None = Query(None, description="Filtrar atletas pelo CPF")
):
    """
    Retorna lista de atletas com filtros opcionais e paginação (limit e offset automáticos).
    """
    query_base = select(AtletaModel)

    if nome:
        query_base = query_base.filter(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        query_base = query_base.filter_by(cpf=cpf)

    return [AtletaOut.model_validate(atleta) for atleta in atletas]

    atletas: list[AtletaOut] = (await db_session.execute(query_base)).scalars().all()
    return paginate([AtletaOut.model_validate(a) for a in atletas])

# -----------------------------
# GET: Consultar atleta por id
# -----------------------------
@router.get(
    '/{id}', 
    summary='Consulta um Atleta pelo id',
    summary='Consultar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    """
    Retorna um atleta específico pelo ID.
    """
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
@@ -94,14 +131,23 @@ async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:

    return atleta


# -----------------------------
# PATCH: Atualizar atleta pelo id
# -----------------------------
@router.patch(
    '/{id}', 
    summary='Editar um Atleta pelo id',
    summary='Editar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
async def patch(
    id: UUID4, 
    db_session: DatabaseDependency, 
    atleta_up: AtletaUpdate = Body(...)
) -> AtletaOut:
    """
    Atualiza os campos fornecidos de um atleta específico.
    """
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
@@ -121,13 +167,18 @@ async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpda

    return atleta


# -----------------------------
# DELETE: Deletar atleta pelo id
# -----------------------------
@router.delete(
    '/{id}', 
    summary='Deletar um Atleta pelo id',
    summary='Deletar um atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    """
    Remove um atleta específico do banco.
    """
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()