from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import List

from app.categorias import models, schemas

def criar_categoria(db: Session, categoria: schemas.CategoriaCreate) -> schemas.CategoriaResponse:
    nova_categoria = models.Categoria(**categoria.dict())
    db.add(nova_categoria)
    try:
        db.commit()
        db.refresh(nova_categoria)
        return nova_categoria
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Categoria com este nome já existe.")

def listar_categorias(db: Session) -> List[schemas.CategoriaResponse]:
    return db.query(models.Categoria).all()

def obter_categoria(db: Session, categoria_id: int) -> schemas.CategoriaResponse:
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return categoria

def atualizar_categoria(db: Session, categoria_id: int, dados: schemas.CategoriaUpdate) -> schemas.CategoriaResponse:
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    
    for key, value in dados.dict(exclude_unset=True).items():
        setattr(categoria, key, value)
    
    try:
        db.commit()
        db.refresh(categoria)
        return categoria
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Atualização inválida (nome duplicado?).")

def deletar_categoria(db: Session, categoria_id: int) -> None:
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    db.delete(categoria)
    db.commit()
