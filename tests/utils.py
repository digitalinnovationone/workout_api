from math import ceil

from faker import Faker

fake_pt = Faker('pt_BR')


def corta(texto: str, limite=20) -> str:
    return texto[:limite]


def gerar_casos_paginacao(limite: int = 20) -> list[tuple[int, int, int, int]]:
    casos = []
    total_itens = [1, 10, 25, 70, 101]
    tamanhos_pagina = [5, 10, 15, 20]

    for qtd in total_itens:
        for size in tamanhos_pagina:
            pages = ceil(qtd / size)
            for page in range(1, pages + 1):
                casos.append((qtd, page, pages, size))
                if len(casos) >= limite:
                    return casos
    return casos
