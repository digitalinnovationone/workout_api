import random
from http import HTTPStatus
from typing import Any, Dict, List, cast
from uuid import UUID, uuid4

import httpx

# import ipdb
import pytest
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factory.atleta import AtletaModelFactory, AtletaSchemaFactory
from tests.factory.categoria import CategoriaModelFactory
from tests.factory.centro_treinamento import CentroTreinamentoModelFactory
from tests.utils import gerar_casos_paginacao
from workout_api.atleta.schemas import get_filtro_query
from workout_api.contrib.dependencies import AtletaFiltroQuery


@pytest.mark.asyncio
async def test_post_atleta_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    categoria = CategoriaModelFactory.build()
    centro = CentroTreinamentoModelFactory.build()
    session.add_all([categoria, centro])
    await session.commit()

    atleta_payload = AtletaSchemaFactory(
        categoria={'nome': categoria.nome},
        centro_treinamento={'nome': centro.nome},
    ).model_dump()

    response = await client.post('/atletas/', json=atleta_payload)
    data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert data['nome'] == atleta_payload['nome']
    assert UUID(data['id'])


@pytest.mark.asyncio
async def test_post_atleta_categoria_not_found(
    client: httpx.AsyncClient, session: AsyncSession
):
    categoria = CategoriaModelFactory.build()
    centro = CentroTreinamentoModelFactory.build()
    session.add_all([categoria, centro])
    await session.commit()
    atleta_payload = AtletaSchemaFactory(
        categoria={'nome': 'inexiste'},
        centro_treinamento={'nome': centro.nome},
    ).model_dump()

    response = await client.post('/atletas/', json=atleta_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'não foi encontrada' in response.json()['detail'].lower()


@pytest.mark.asyncio
async def test_post_atleta_centro_treinamento_not_found(
    client: httpx.AsyncClient, session: AsyncSession
):
    categoria = CategoriaModelFactory.build()
    centro = CentroTreinamentoModelFactory.build()
    session.add_all([categoria, centro])
    await session.commit()
    atleta_payload = AtletaSchemaFactory(
        categoria={'nome': categoria.nome},
        centro_treinamento={'nome': 'ct inexistente'},
    ).model_dump()

    response = await client.post('/atletas/', json=atleta_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'não foi encontrado' in response.json()['detail'].lower()


@pytest.mark.asyncio
async def test_post_atleta_ja_existente(
    client: httpx.AsyncClient, session: AsyncSession
):
    categoria0 = CategoriaModelFactory.build()
    centro_treinamento0 = CentroTreinamentoModelFactory.build()
    categoria1 = CategoriaModelFactory.build()
    centro_treinamento1 = CentroTreinamentoModelFactory.build()
    session.add_all([
        categoria0,
        centro_treinamento0,
        categoria1,
        centro_treinamento1,
    ])
    await session.flush()

    atleta = AtletaModelFactory.create(
        categoria_id=categoria0.pk_id,
        centro_treinamento_id=centro_treinamento0.pk_id,
    )
    await session.commit()

    atleta_payload = AtletaSchemaFactory.build(
        cpf=atleta.cpf,  # Usa o mesmo CPF
        categoria__nome=categoria1.nome,
        centro_treinamento__nome=centro_treinamento1.nome,
    ).model_dump()

    response = await client.post('/atletas/', json=atleta_payload)
    cpf_atleta = atleta_payload['cpf']

    assert response.status_code == HTTPStatus.SEE_OTHER

    assert (
        response.json()['detail'].lower()
        == f'Já existe um atleta cadastrado com o cpf: {cpf_atleta}'.lower()
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ('qtd', 'page', 'total_pages', 'size'), gerar_casos_paginacao(55)
)
async def test_get_atletas_success(  # noqa: PLR0913, PLR0917
    client: httpx.AsyncClient,
    session: AsyncSession,
    qtd,
    page,
    total_pages,
    size,
):
    categorias = [CategoriaModelFactory.build() for _ in range(qtd)]
    centros_treinamento = [
        CentroTreinamentoModelFactory.build() for _ in range(qtd)
    ]
    session.add_all([
        *categorias,
        *centros_treinamento,
    ])
    await session.flush()
    atletas = []
    for cat, ct in zip(categorias, centros_treinamento):
        atleta = AtletaModelFactory.create(
            categoria=cat,
            centro_treinamento_id=ct,
        )
        atletas.append(atleta)
    session.add_all(atletas)
    await session.commit()

    response = await client.get(
        '/atletas/', params={'page': page, 'size': size}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['items']
    assert data['total'] == qtd
    assert data['page'] == page
    assert data['pages'] == total_pages
    assert data['size'] == size


@pytest.mark.asyncio
async def test_get_atletas_by_cpf_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    qtd = 2
    atletas = []

    for _ in range(qtd):
        atleta = AtletaModelFactory.create()
        await session.flush()
        atletas.append(atleta)
    await session.commit()

    atleta = random.choice(atletas)
    cpf_atleta = atleta.cpf

    response = await client.get(f'/atletas/?cpf={cpf_atleta}')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    # ipdb.set_trace()
    assert data['total'] == 1
    assert data['items'][0]['cpf'] == cpf_atleta


@pytest.mark.asyncio
async def test_get_atleta_by_id_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    atleta = AtletaModelFactory.create()
    await session.commit()

    response = await client.get(f'/atletas/{atleta.id}')
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == str(atleta.id)


@pytest.mark.asyncio
async def test_get_atleta_by_id_not_found(client: httpx.AsyncClient):
    id_errado = str(uuid4())
    response = await client.get(f'/atletas/{id_errado}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'não encontrado' in response.json()['detail']


@pytest.mark.asyncio
async def test_patch_atleta_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    atleta = AtletaModelFactory.create()
    await session.commit()
    patch_data = {'nome': 'Nome Atualizado'}
    response = await client.patch(
        f'/atletas/{str(atleta.id)}', json=patch_data
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['nome'] == patch_data['nome']


@pytest.mark.asyncio
async def test_patch_atleta_not_found(client: httpx.AsyncClient):
    patch_data = {'nome': 'Nome Atualizado'}
    id_errado = str(uuid4())
    response = await client.patch(
        f'/atletas/{str(id_errado)}', json=patch_data
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_atleta_success(client, session):
    atleta = AtletaModelFactory.create()
    await session.commit()

    response = await client.delete(f'/atletas/{atleta.id}')
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_atleta_not_found(client: httpx.AsyncClient):
    id_errado = uuid4()
    response = await client.delete(f'/atletas/{id_errado}')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_filtro_atletas(
    client: httpx.AsyncClient, session: AsyncSession
):
    # Cria dados de teste
    categoria = CategoriaModelFactory.create(nome='Categoria Teste')
    centro = CentroTreinamentoModelFactory.create(nome='CT Teste')
    atleta1 = AtletaModelFactory.create(  # noqa: F841
        nome='João Silva',
        cpf='11122233344',
        categoria=categoria,
        centro_treinamento=centro,
    )
    atleta2 = AtletaModelFactory.create(  # noqa: F841
        nome='Maria Souza',
        cpf='55566677788',
        categoria=categoria,
        centro_treinamento=centro,
    )
    await session.commit()

    # Teste 1: Sem filtros - deve retornar todos
    response = await client.get('/atletas/', params={'page': 1, 'size': 10})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['total'] >= 2  # noqa: PLR2004

    # Teste 2: Filtro por nome
    response = await client.get(
        '/atletas/', params={'page': 1, 'size': 10, 'nome': 'João'}
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['total'] == 1
    assert data['items'][0]['nome'] == 'João Silva'

    # Teste 3: Filtro por CPF
    response = await client.get(
        '/atletas/', params={'page': 1, 'size': 10, 'cpf': '55566677788'}
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['total'] == 1
    assert data['items'][0]['cpf'] == '55566677788'

    # Teste 4: Filtro combinado (deve retornar vazio)
    response = await client.get(
        '/atletas/',
        params={'page': 1, 'size': 10, 'nome': 'João', 'cpf': '55566677788'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['total'] == 0


@pytest.mark.asyncio
async def test_filtro_cpf_formato_invalido(client: httpx.AsyncClient):
    response = await client.get(
        '/atletas/',
        params={
            'page': 1,
            'size': 10,
            'cpf': '111',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    error_data = response.json()
    errors = error_data.get('detail', [])

    assert any(error['type'] == 'string_pattern_mismatch' for error in errors)


@pytest.mark.asyncio
async def test_filtro_cpf_valor_invalido(client: httpx.AsyncClient):
    response = await client.get(
        '/atletas/',
        params={
            'page': 1,
            'size': 10,
            'cpf': '11111111111',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    error_data = response.json()
    errors = error_data.get('detail', [])
    if errors:
        error = errors[0]
        assert error['type'] == 'value_error'
        assert (
            'CPF não pode ter todos os dígitos iguais'.lower()
            in error['msg'].lower()
        )
    # ipdb.set_trace()


@pytest.mark.asyncio
async def test_get_filtro_query_cpf_invalido():
    with pytest.raises(HTTPException) as exc_info:
        get_filtro_query(cpf='11111111111')

    assert exc_info.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    errors: List[Dict[str, Any]] = cast(
        List[Dict[str, Any]], exc_info.value.detail
    )
    assert any(
        error['type'] == 'value_error'
        and error['msg']
        == 'Value error, CPF não pode ter todos os dígitos iguais'
        for error in errors
    )


@pytest.mark.asyncio
async def test_filtro_cpf_valido(client: httpx.AsyncClient):
    response = await client.get(
        '/atletas/',
        params={
            'page': 1,
            'size': 10,
            'cpf': '12345678901',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)


@pytest.mark.asyncio
async def test_filtro_nome_valido(client: httpx.AsyncClient):
    response = await client.get(
        '/atletas/',
        params={
            'page': 1,
            'size': 10,
            'nome': 'Joao',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)


@pytest.mark.asyncio
async def test_filtro_sem_parametros(client: httpx.AsyncClient):
    response = await client.get(
        '/atletas/',
        params={
            'page': 1,
            'size': 10,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)


def test_atleta_filtro_query_instantiation():
    filtro = AtletaFiltroQuery(nome='Joao', cpf='12345678901')
    assert filtro.nome == 'Joao'
    assert filtro.cpf == '12345678901'
