from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import HTTPException, Query
from pydantic import (
    BaseModel,
    Field,
    PositiveFloat,
    StringConstraints,
    ValidationError,
    field_validator,
    model_validator,
)

from workout_api.atleta.models import AtletaModel
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[
        str,
        Field(description='Nome do atleta', examples=['Joao'], max_length=50),
    ]
    cpf: Annotated[
        str,
        Field(
            description='CPF do atleta',
            examples=['12345678900'],
            max_length=11,
        ),
    ]
    idade: Annotated[int, Field(description='Idade do atleta', examples=[25])]
    peso: Annotated[
        PositiveFloat, Field(description='Peso do atleta', examples=[75.5])
    ]
    altura: Annotated[
        PositiveFloat, Field(description='Altura do atleta', examples=[1.70])
    ]
    sexo: Annotated[
        str, Field(description='Sexo do atleta', examples=['M'], max_length=1)
    ]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[
        CentroTreinamentoAtleta,
        Field(description='Centro de treinamento do atleta'),
    ]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixin):
    pass


class AtletaListagemOut(OutMixin):
    nome: str
    cpf: str
    categoria: str
    centro_treinamento: str

    @model_validator(mode='before')
    @classmethod
    def validate_model(cls, data):
        if isinstance(data, AtletaModel):
            return {
                'id': data.id,
                'created_at': data.created_at,
                'nome': data.nome,
                'cpf': data.cpf,
                'categoria': data.categoria.nome,
                'centro_treinamento': data.centro_treinamento.nome,
            }


class AtletaUpdate(BaseSchema):
    nome: Annotated[
        Optional[str],
        Field(
            None,
            description='Nome do atleta',
            examples=['Joao'],
            max_length=50,
        ),
    ]
    idade: Annotated[
        Optional[int],
        Field(None, description='Idade do atleta', examples=[25]),
    ]


class AtletaFiltroSchema(BaseModel):
    nome: Optional[
        Annotated[
            str,
            StringConstraints(strip_whitespace=True, max_length=50),
        ]
    ] = None
    cpf: Optional[
        Annotated[
            str, StringConstraints(strip_whitespace=True, pattern=r'^\d{11}$')
        ]
    ] = None

    @field_validator('cpf')
    def validar_cpf(cls, v):
        if v is not None and len(set(v)) == 1:
            raise ValueError('CPF não pode ter todos os dígitos iguais')
        return v


def get_filtro_query(
    nome: Optional[str] = Query(None),
    cpf: Optional[str] = Query(None),
) -> Optional[AtletaFiltroSchema]:
    try:
        if nome is None and cpf is None:
            return None
        return AtletaFiltroSchema(nome=nome, cpf=cpf)
    except ValidationError as e:
        formatted_errors = [
            {
                'loc': error['loc'],
                'msg': error['msg'],
                'type': error['type'],
            }
            for error in e.errors()
        ]
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=formatted_errors,
        )
