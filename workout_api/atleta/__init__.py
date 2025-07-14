from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import Atleta, AtletaBase
from models import Atleta as AtletaModel
from typing import List
from sqlalchemy import or_

router = APIRouter()

@router.get("/atletas", response_model=List[Atleta])
def get_atletas(
    nome: str = Query(None, description="Filtrar por nome"),
    cpf: str = Query(None, description="Filtrar por CPF"),
    db: Session = Depends(get_db)
):
    query = db.query(AtletaModel)
    if nome:
        query = query.filter(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
    return query.all()
