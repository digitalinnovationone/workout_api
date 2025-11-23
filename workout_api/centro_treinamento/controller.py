from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import List

from app.centro_treinamento import models, schemas

def criar_centro(db: Session, centro: schemas.CentroTreinamentoCreate) -> schemas.CentroTreinamentoResponse:
    novo_centro = models.CentroTreinamento(**centro.dict())
    db.add(novo_centro)
    try:
        db.commit()
        db.refresh(novo_centro)
        return novo_centro
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Centro com este nome já existe.")

def listar_centros(db: Session) -> List[schemas.CentroTreinamentoResponse]:
    return db.query(models.CentroTreinamento).all()

def obter_centro(db: Session, centro_id: int) -> schemas.CentroTreinamentoResponse:
    centro = db.query(models.CentroTreinamento).filter(models.CentroTreinamento.id == centro_id).first()
    if not centro:
        raise HTTPException(status_code=404, detail="Centro não encontrado.")
    return centro

def atualizar_centro(db: Session, centro_id: int, dados: schemas.CentroTreinamentoUpdate) -> schemas.CentroTreinamentoResponse:
    centro = db.query(models.CentroTreinamento).filter(models.CentroTreinamento.id == centro_id).first()
    if not centro:
        raise HTTPException(status_code=404, detail="Centro não encontrado.")
    
    for key, value in dados.dict(exclude_unset=True).items():
        setattr(centro, key, value)
    
    try:
        db.commit()
        db.refresh(centro)
        return centro
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Atualização inválida (nome duplicado?).")

def deletar_centro(db: Session, centro_id: int) -> None:
    centro = db.query(models.CentroTreinamento).filter(models.CentroTreinamento.id == centro_id).first()
    if not centro:
        raise HTTPException(status_code=404, detail="Centro não encontrado.")
    db.delete(centro)
    db.commit()
