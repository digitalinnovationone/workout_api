from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            max_length=50,
            json_schema_extra={"example": "CT King"}
        )
    ]

    endereco: Annotated[
        str,
        Field(
            description="Endereço",
            max_length=100,
            json_schema_extra={"example": "Rua X, 002"}
        )
    ]

    proprietario: Annotated[
        str,
        Field(
            description="Proprietário do centro",
            max_length=50,
            json_schema_extra={"example": "Davidson"}
        )
    ]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            max_length=20,
            json_schema_extra={"example": "Ct"}
        )
    ]


class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[
        UUID4,
        Field(description="Identificador do centro de treinamento")
    ]
