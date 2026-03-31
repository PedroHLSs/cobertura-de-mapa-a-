#Implementação do algoritmo A* (A-Estrela) para encontrar o caminho mais curto em um mapa 2D.
#Biblioteca usada para filas de prioridade. Utilizada para manter os nós a serem explorados ordenados pelo custo total estimado (f = g + h).
import heapq

from constantes import CUSTO_TERRENO, TAMANHO_MAPA


class No:
    """Representa um nó na busca A*."""

    def __init__(self, posicao, g=0.0, h=0.0, pai=None):
        # g = custo real acumulado; h = estimativa até o objetivo; f = soma dos dois.
        self.posicao = posicao
        self.g = g
        self.h = h
        self.f = g + h
        #refere-se ao nó pai para reconstrução do caminho quando o objetivo for alcançado.
        self.pai = pai
    # Serve para comparação da fila de prioridade com base em f
    def __lt__(self, outro):
        return self.f < outro.f
    # Serve para comparar se a posição do nó é igual a de outro nó
    def __eq__(self, outro):
        return self.posicao == outro.posicao
    # Dois nós na mesma posição terão o mesmo valor
    def __hash__(self):
        return hash(self.posicao)

def distancia_manhattan(origem, destino):
    """Heurística de distância de Manhattan."""
    return abs(origem[0] - destino[0]) + abs(origem[1] - destino[1])

# Usado para definir quais são os movimentos possíveis 
def obter_vizinhos(posicao, mapa):
    del mapa

    linha, coluna = posicao
    # Movimentos possíveis: cima, baixo, esquerda, direita.
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    vizinhos = []
    for d_linha, d_coluna in direcoes:
        nova_linha, nova_coluna = linha + d_linha, coluna + d_coluna
        if 0 <= nova_linha < TAMANHO_MAPA and 0 <= nova_coluna < TAMANHO_MAPA:
            vizinhos.append((nova_linha, nova_coluna))
    return vizinhos

#Implementação para que o algoritimo descubra o caminho mais curto entre o ponto inicial e final, considerando os custos.
def a_estrela(inicio, objetivo, mapa):
    """Implementação do algoritmo A* (A-Estrela)."""
    if inicio == objetivo:
        return [inicio], 0.0

    # O primeiro nó nasce com custo zero e heurística calculada até o objetivo.
    no_inicial = No(
        posicao=inicio,
        g=0.0,
        h=distancia_manhattan(inicio, objetivo),
        pai=None,
    )

    # A fila de prioridade mantém os nós com menor f na frente.
    lista_aberta = []
    heapq.heappush(lista_aberta, no_inicial)
    custos_abertos = {inicio: no_inicial.g}
    conjunto_fechado = set()

    while lista_aberta:
        no_atual = heapq.heappop(lista_aberta)

        # Entradas antigas podem permanecer no heap; ignoramos nós já processados.
        if no_atual.posicao in conjunto_fechado:
            continue

        conjunto_fechado.add(no_atual.posicao)

        # Quando o objetivo é removido da fila, o caminho ótimo foi encontrado.
        if no_atual.posicao == objetivo:
            caminho = []
            no_cursor = no_atual
            while no_cursor is not None:
                caminho.append(no_cursor.posicao)
                no_cursor = no_cursor.pai
            caminho.reverse()
            return caminho, no_atual.g

        for posicao_vizinha in obter_vizinhos(no_atual.posicao, mapa):
            if posicao_vizinha in conjunto_fechado:
                continue

            # O custo real depende do terreno da célula vizinha.
            terreno = mapa[posicao_vizinha[0]][posicao_vizinha[1]]
            custo_movimento = CUSTO_TERRENO[terreno]
            novo_g = no_atual.g + custo_movimento

            # Se já existe um caminho melhor para essa posição, não vale reprocessar.
            if posicao_vizinha in custos_abertos and custos_abertos[posicao_vizinha] <= novo_g:
                continue

            novo_h = distancia_manhattan(posicao_vizinha, objetivo)
            no_filho = No(posicao=posicao_vizinha, g=novo_g, h=novo_h, pai=no_atual)
            heapq.heappush(lista_aberta, no_filho)
            custos_abertos[posicao_vizinha] = novo_g

    return [], float("inf")
