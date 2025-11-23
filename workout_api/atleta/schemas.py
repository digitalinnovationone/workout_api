from pydantic import BaseModel
from typing import Optional

class AtletaBase(BaseModel):
    nome: str
    idade: int
    categoria_id: int
    centro_id: int

class AtletaCreate(AtletaBase):
    pass

class AtletaUpdate(BaseModel):
    nome: Optional[str] = None
    idade: Optional[int] = None
    categoria_id: Optional[int] = None
    centro_id: Optional[int] = None

class AtletaResponse(AtletaBase):
    id: int

    class Config:
        orm_mode = True
