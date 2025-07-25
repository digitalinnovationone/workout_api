# pyright: reportAttributeAccessIssue=false
# pyright: reportPrivateImportUsage=false


import factory
from utils import fake_pt

from tests.factory.categoria import CategoriaModelFactory
from tests.factory.centro_treinamento import CentroTreinamentoModelFactory
from tests.utils import corta
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn


class AtletaBaseFactory(factory.Factory):
    nome = factory.Sequence(lambda n: corta(f'{fake_pt.name()}_{n}', 50))
    cpf = factory.LazyFunction(
        lambda: fake_pt.cpf().replace('.', '').replace('-', '')
    )
    idade = factory.LazyFunction(lambda: fake_pt.random_int(min=10, max=80))
    peso = factory.LazyFunction(
        lambda: round(fake_pt.pyfloat(min_value=40, max_value=120), 1)
    )
    altura = factory.LazyFunction(
        lambda: round(fake_pt.pyfloat(min_value=1.40, max_value=2.10), 2)
    )
    sexo = factory.LazyFunction(
        lambda: fake_pt.random_element(elements=['M', 'F'])
    )


class AtletaSchemaFactory(AtletaBaseFactory):
    categoria = factory.SubFactory(
        'tests.factory.categoria.CategoriaSchemaFactory'
    )
    centro_treinamento = factory.SubFactory(
        'tests.factory.centro_treinamento.CentroTreinamentoSchemaFactory'
    )

    class Meta:  # type: ignore[attr-defined]
        model = AtletaIn


class AtletaModelFactory(
    factory.alchemy.SQLAlchemyModelFactory, AtletaBaseFactory
):
    categoria = factory.SubFactory(CategoriaModelFactory)
    categoria_id = factory.SelfAttribute('categoria.pk_id')

    centro_treinamento = factory.SubFactory(CentroTreinamentoModelFactory)
    centro_treinamento_id = factory.SelfAttribute('centro_treinamento.pk_id')

    class Meta:  # type: ignore[attr-defined]
        model = AtletaModel
        sqlalchemy_session = None  # será setado no teste
        sqlalchemy_session_persistence = 'flush'
