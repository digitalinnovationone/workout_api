from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta

from workout_api.contrib.schemas import BaseSchema, OutMixin


class AtletaUpdate(BaseSchema):
    nome: Optional[str] = Field(None, description='Nome do atleta', example='Joao', max_length=50)
    cpf: Optional[str] = Field(None, description='CPF do atleta', example='12345678900', max_length=11)
    idade: Optional[int] = Field(None, description='Idade do atleta', example=25)
    peso: Optional[PositiveFloat] = Field(None, description='Peso do atleta', example=75.5)
    altura: Optional[PositiveFloat] = Field(None, description='Altura do atleta', example=1.70)
    sexo: Optional[str] = Field(None, description='Sexo do atleta', example='M', max_length=1)
    categoria: Optional[CategoriaIn] = Field(None, description='Categoria do atleta')
    centro_treinamento: Optional[CentroTreinamentoAtleta] = Field(None, description='Centro de treinamento do atleta')


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]