# pyright: reportAttributeAccessIssue=false
# pyright: reportPrivateImportUsage=false

import factory
from utils import fake_pt

from tests.utils import corta
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn


class CentroTreinamentoBaseFactory(factory.Factory):
    nome = factory.Sequence(
        lambda n: corta(f'ct_{n} {fake_pt.company()[:44]}', 20)
    )

    endereco = factory.LazyAttribute(lambda _: corta(fake_pt.address(), 60))
    proprietario = factory.LazyAttribute(lambda _: corta(fake_pt.name(), 30))


class CentroTreinamentoSchemaFactory(CentroTreinamentoBaseFactory):
    class Meta:  # type: ignore[attr-defined]
        model = CentroTreinamentoIn


class CentroTreinamentoModelFactory(CentroTreinamentoBaseFactory):
    class Meta:  # type: ignore[attr-defined]
        model = CentroTreinamentoModel
