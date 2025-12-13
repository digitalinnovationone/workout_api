from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome do atleta",
            max_length=50,
            json_schema_extra={"example": "João"},
        )
    ]

    cpf: Annotated[
        str,
        Field(
            description="Cpf do atleta",
            max_length=11,
            json_schema_extra={"example": "43929900000"},
        )
    ]

    idade: Annotated[
        int,
        Field(description="Idade do atleta",
              json_schema_extra={"example": 20})
    ]

    peso: Annotated[
        PositiveFloat,
        Field(description="Peso", json_schema_extra={"example": 120})
    ]

    altura: Annotated[
        PositiveFloat,
        Field(description="Altura do atleta", json_schema_extra={"example": 1.95})
    ]

    sexo: Annotated[
        str,
        Field(description="Sexo do atleta", json_schema_extra={"example": "M"})
    ]

    categoria: Annotated[
        CategoriaIn,
        Field(description="Categoria do atleta")
    ]

    centro_treinamento: Annotated[
        CentroTreinamentoAtleta,
        Field(description="Centro de treinamento do atleta",
        json_schema_extra={"example": {"nome": "CT King"}})
    ]


class AtletaIn(Atleta):
    pass


class AtletaOut(AtletaIn, OutMixin):
    pass


class AtletaUpdate(BaseSchema):
    nome: Annotated[
        Optional[str],
        Field(
            None, description="Nome do atleta",
            max_length=50,
            json_schema_extra={"example": "João"},
        )
    ]

    idade: Annotated[
        Optional[int],
        Field(
            None, description="Idade do atleta",
            json_schema_extra={"example": 20})
    ]


class CategoriaSimples(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Iniciante', max_length=10)]

class CTSimples(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', example='CT Power', max_length=20)]


class AtletasSimples(OutMixin):

    nome: Annotated[str, Field(description='Nome do atleta', example='Joana', max_length=50)]
    

    centro_treinamento: CTSimples 
    categoria: CategoriaSimples