from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status, Query
from pydantic import UUID4
from sqlalchemy import exc
from fastapi_pagination import paginate, Page
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.categorias.models import CategoriaModel

from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post(
    '/', 
    summary='Criar uma nova Categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency, 
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    
    try:
        db_session.add(categoria_model)
        await db_session.commit()
    except exc.IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe uma categoria cadastrada com o nome: {categoria_model.nome}'
        )

    return categoria_out


@router.get(
    '/', 
    summary='Consultar todas as Categorias',
    status_code=status.HTTP_200_OK,
    response_model=Page[CategoriaOut],
)
async def query(
    db_session: DatabaseDependency,
    limit: int = Query(10, description="Número de itens por página"),
    offset: int = Query(0, description="Número de itens a serem pulados"),
) -> Page[CategoriaOut]:
    categorias = await db_session.execute(select(CategoriaModel))
    
    return paginate(categorias, limit=limit, offset=offset)


@router.get(
    '/{id}', 
    summary='Consulta uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria não encontrada no id: {id}'
        )
    
    return categoria
