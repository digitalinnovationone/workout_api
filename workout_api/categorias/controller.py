from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate

from workout_api.categorias.schemas import CategoriaIn, CategoriaOut, CategoriaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.contrib.dependencies import DatabaseDependency

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

    db_session.add(categoria_model)
    try:
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria '{categoria_in.nome}' já existe."
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
    nome: str | None = Query(None, description="Filtrar categorias pelo nome"),
) -> Page[CategoriaOut]:
    query = select(CategoriaModel)

    if nome:
        query = query.filter(CategoriaModel.nome.ilike(f"%{nome}%"))

    categorias = (await db_session.execute(query)).scalars().all()

    return paginate([CategoriaOut.model_validate(c) for c in categorias])


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
    
    return CategoriaOut.model_validate(categoria)


@router.patch(
    '/{id}', 
    summary='Editar uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def patch(
    id: UUID4,
    db_session: DatabaseDependency,
    categoria_up: CategoriaUpdate = Body(...),
) -> CategoriaOut:
    categoria = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria não encontrada no id: {id}'
        )

    for key, value in categoria_up.model_dump(exclude_unset=True).items():
        setattr(categoria, key, value)

    await db_session.commit()
    await db_session.refresh(categoria)

    return CategoriaOut.model_validate(categoria)


@router.delete(
    '/{id}', 
    summary='Deletar uma Categoria pelo id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    categoria = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria não encontrada no id: {id}'
        )

    await db_session.delete(categoria)
    await db_session.commit()
