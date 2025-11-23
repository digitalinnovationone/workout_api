from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import List, Optional

from app.atleta import models, schemas

def criar_atleta(db: Session, atleta: schemas.AtletaCreate) -> schemas.AtletaResponse:
    novo_atleta = models.Atleta(**atleta.dict())
    db.add(novo_atleta)
    try:
        db.commit()
        db.refresh(novo_atleta)
        return novo_atleta
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Atleta com este nome já existe.")

def listar_atletas(
    db: Session,
    nome: Optional[str] = None,
    idade: Optional[int] = None,
    categoria_id: Optional[int] = None,
    limit: int = 10,
    offset: int = 0
) -> List[schemas.AtletaResponse]:
    query = db.query(models.Atleta)
    if nome:
        query = query.filter(models.Atleta.nome.ilike(f"%{nome}%"))
    if idade is not None:
        query = query.filter(models.Atleta.idade == idade)
    if categoria_id:
        query = query.filter(models.Atleta.categoria_id == categoria_id)
    return query.offset(offset).limit(limit).all()

def obter_atleta(db: Session, atleta_id: int) -> schemas.AtletaResponse:
    atleta = db.query(models.Atleta).filter(models.Atleta.id == atleta_id).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado.")
    return atleta

def atualizar_atleta(db: Session, atleta_id: int, dados: schemas.AtletaUpdate) -> schemas.AtletaResponse:
    atleta = db.query(models.Atleta).filter(models.Atleta.id == atleta_id).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado.")
    
    for key, value in dados.dict(exclude_unset=True).items():
        setattr(atleta, key, value)
    
    try:
        db.commit()
        db.refresh(atleta)
        return atleta
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Atualização inválida (nome duplicado?).")

def deletar_atleta(db: Session, atleta_id: int) -> None:
    atleta = db.query(models.Atleta).filter(models.Atleta.id == atleta_id).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado.")
    db.delete(atleta)
    db.commit()

