from pydantic import BaseModel
from typing import Optional

class CentroTreinamentoBase(BaseModel):
    nome: str
    localizacao: Optional[str] = None

class CentroTreinamentoCreate(CentroTreinamentoBase):
    pass

class CentroTreinamentoUpdate(BaseModel):
    nome: Optional[str] = None
    localizacao: Optional[str] = None

class CentroTreinamentoResponse(CentroTreinamentoBase):
    id: int

    class Config:
        orm_mode = True
