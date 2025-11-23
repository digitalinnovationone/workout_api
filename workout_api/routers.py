from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.atleta import controller as atleta_ctrl, schemas as atleta_schemas
from app.categorias import controller as cat_ctrl, schemas as cat_schemas
from app.centro_treinamento import controller as centro_ctrl, schemas as centro_schemas

router = APIRouter()

# ------------------ Atletas ------------------ #
@router.post("/atletas/", response_model=atleta_schemas.AtletaResponse)
def criar_atleta(atleta: atleta_schemas.AtletaCreate, db: Session = Depends(get_db)):
    return atleta_ctrl.criar_atleta(db, atleta)

@router.get("/atletas/", response_model=List[atleta_schemas.AtletaResponse])
def listar_atletas(
    nome: Optional[str] = None,
    idade: Optional[int] = None,
    categoria_id: Optional[int] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return atleta_ctrl.listar_atletas(db, nome, idade, categoria_id, limit, offset)

@router.get("/atletas/{atleta_id}", response_model=atleta_schemas.AtletaResponse)
def obter_atleta(atleta_id: int, db: Session = Depends(get_db)):
    return atleta_ctrl.obter_atleta(db, atleta_id)

@router.put("/atletas/{atleta_id}", response_model=atleta_schemas.AtletaResponse)
def atualizar_atleta(atleta_id: int, dados: atleta_schemas.AtletaUpdate, db: Session = Depends(get_db)):
    return atleta_ctrl.atualizar_atleta(db, atleta_id, dados)

@router.delete("/atletas/{atleta_id}")
def deletar_atleta(atleta_id: int, db: Session = Depends(get_db)):
    atleta_ctrl.deletar_atleta(db, atleta_id)
    return {"detail": "Atleta deletado com sucesso."}

# ------------------ Categorias ------------------ #
@router.post("/categorias/", response_model=cat_schemas.CategoriaResponse)
def criar_categoria(categoria: cat_schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return cat_ctrl.criar_categoria(db, categoria)

@router.get("/categorias/", response_model=List[cat_schemas.CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return cat_ctrl.listar_categorias(db)

@router.get("/categorias/{categoria_id}", response_model=cat_schemas.CategoriaResponse)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    return cat_ctrl.obter_categoria(db, categoria_id)

@router.put("/categorias/{categoria_id}", response_model=cat_schemas.CategoriaResponse)
def atualizar_categoria(categoria_id: int, dados: cat_schemas.CategoriaUpdate, db: Session = Depends(get_db)):
    return cat_ctrl.atualizar_categoria(db, categoria_id, dados)

@router.delete("/categorias/{categoria_id}")
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    cat_ctrl.deletar_categoria(db, categoria_id)
    return {"detail": "Categoria deletada com sucesso."}

# ------------------ Centros de Treinamento ------------------ #
@router.post("/centros/", response_model=centro_schemas.CentroTreinamentoResponse)
def criar_centro(centro: centro_schemas.CentroTreinamentoCreate, db: Session = Depends(get_db)):
    return centro_ctrl.criar_centro(db, centro)

@router.get("/centros/", response_model=List[centro_schemas.CentroTreinamentoResponse])
def listar_centros(db: Session = Depends(get_db)):
    return centro_ctrl.listar_centros(db)

@router.get("/centros/{centro_id}", response_model=centro_schemas.CentroTreinamentoResponse)
def obter_centro(centro_id: int, db: Session = Depends(get_db)):
    return centro_ctrl.obter_centro(db, centro_id)

@router.put("/centros/{centro_id}", response_model=centro_schemas.CentroTreinamentoResponse)
def atualizar_centro(centro_id: int, dados: centro_schemas.CentroTreinamentoUpdate, db: Session = Depends(get_db)):
    return centro_ctrl.atualizar_centro(db, centro_id, dados)

@router.delete("/centros/{centro_id}")
def deletar_centro(centro_id: int, db: Session = Depends(get_db)):
    centro_ctrl.deletar_centro(db, centro_id)
    return {"detail": "Centro deletado com sucesso."}
