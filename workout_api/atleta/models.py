from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from workout_api.contrib.models import BaseModel


class AtletaModel(BaseModel):
    __tablename__ = 'atletas'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    categoria: Mapped['CategoriaModel'] = relationship(  # noqa: F821 # type: ignore
        back_populates='atleta', lazy='selectin'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("timezone('utc', now())"),
        nullable=False,
    )
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.pk_id'))
    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(  # noqa: F821 # type: ignore
        back_populates='atleta', lazy='selectin'
    )
    centro_treinamento_id: Mapped[int] = mapped_column(
        ForeignKey('centros_treinamento.pk_id')
    )
