# pyright: reportAttributeAccessIssue=false
# pyright: reportPrivateImportUsage=false
import factory

from tests.utils import corta, fake_pt
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn


class CategoriaBaseFactory(factory.Factory):
    nome = factory.Sequence(
        lambda n: corta(f'cat_{n}_{max(fake_pt.words(25, unique=True))}', 10)
    )


class CategoriaSchemaFactory(CategoriaBaseFactory):
    class Meta:  # type: ignore[attr-defined]
        model = CategoriaIn


class CategoriaModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:  # type: ignore[attr-defined]
        model = CategoriaModel
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'flush'

    nome = factory.Sequence(
        lambda n: corta(f'cat_{n}_{max(fake_pt.words(25, unique=True))}', 10)
    )
