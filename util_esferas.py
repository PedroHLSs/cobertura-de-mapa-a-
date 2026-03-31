import random

from constantes import NUM_ESFERAS, POS_INICIAL, TAMANHO_MAPA


def gerar_esferas(mapa, quantidade=NUM_ESFERAS):
    """Distribui a quantidade de esferas em posicoes aleatorias do mapa."""
    del mapa

    esferas = set()
    while len(esferas) < quantidade:
        linha = random.randint(0, TAMANHO_MAPA - 1)
        coluna = random.randint(0, TAMANHO_MAPA - 1)
        posicao = (linha, coluna)
        if posicao != POS_INICIAL and posicao not in esferas:
            esferas.add(posicao)
    return esferas


def gerar_esferas_fixas(posicoes, mapa):
    """Valida e retorna as posicoes fixas como conjunto."""
    del mapa

    if len(posicoes) != NUM_ESFERAS:
        raise ValueError(
            f"Sao necessarias exatamente {NUM_ESFERAS} posicoes "
            f"(informadas: {len(posicoes)})."
        )

    posicoes_vistas = set()
    for posicao in posicoes:
        linha, coluna = posicao
        if not (0 <= linha < TAMANHO_MAPA and 0 <= coluna < TAMANHO_MAPA):
            raise ValueError(f"Posicao {posicao} esta fora do mapa (0-{TAMANHO_MAPA - 1}).")
        if posicao == POS_INICIAL:
            raise ValueError(f"Posicao {posicao} coincide com a base {POS_INICIAL}.")
        if posicao in posicoes_vistas:
            raise ValueError(f"Posicao {posicao} esta duplicada.")
        posicoes_vistas.add(posicao)

    return set(posicoes)
