from itertools import permutations

from nucleo_aestrela import a_estrela
from constantes import (
    ALCANCE_RADAR,
    CUSTO_TERRENO,
    NUM_ESFERAS,
    POS_INICIAL,
    TAMANHO_MAPA,
)


class Agente:
    """Agente inteligente para exploração, coleta e retorno à base."""

    def __init__(self, mapa, esferas):
        self.mapa = mapa
        # Conjuntos usados para controlar o que o agente sabe e o que ja coletou.
        self.todas_esferas = set(esferas)
        self.esferas_conhecidas = set()
        self.coletadas = set()

        # Estado atual da execucao do agente.
        self.posicao = POS_INICIAL
        self.estado = "explorando"
        self.caminho = []

        # Estatisticas acumuladas durante a simulacao.
        self.custo_total = 0.0
        self.passos = 0

        # Lista de posicoes usadas para desenhar o rastro do agente.
        self.trilha = [POS_INICIAL]

        # Planeja pontos de observacao para cobrir o mapa de forma sistematica.
        self.pontos_observacao = self._montar_plano_exploracao()
        self.pontos_observacao_restantes = set(self.pontos_observacao)

        # Historico textual de eventos para exibicao na interface.
        self.registro = []

    def _montar_plano_exploracao(self):
        # Cria uma grade de pontos separada pelo alcance do radar.
        passo = ALCANCE_RADAR * 2 + 1
        linhas = list(range(ALCANCE_RADAR, TAMANHO_MAPA, passo))
        ultimo_centro = TAMANHO_MAPA - 1 - ALCANCE_RADAR
        if not linhas or linhas[-1] != ultimo_centro:
            linhas.append(ultimo_centro)
        colunas = list(range(ALCANCE_RADAR, TAMANHO_MAPA, passo))
        if not colunas or colunas[-1] != ultimo_centro:
            colunas.append(ultimo_centro)

        pontos = []
        for indice, linha in enumerate(linhas):
            # Varredura em serpentina para reduzir deslocamentos desnecessarios.
            colunas_varredura = colunas if indice % 2 == 0 else list(reversed(colunas))
            for coluna in colunas_varredura:
                pontos.append((linha, coluna))
        return pontos

    def _melhor_ponto_observacao(self):
        # Escolhe o ponto restante com menor custo de caminho ate ele.
        candidatos = [
            ponto for ponto in self.pontos_observacao if ponto in self.pontos_observacao_restantes
        ]
        if not candidatos:
            return None, []

        melhor_ponto = None
        melhor_caminho = []
        menor_custo = float("inf")

        for ponto in candidatos:
            caminho, custo = a_estrela(self.posicao, ponto, self.mapa)
            if caminho and custo < menor_custo:
                menor_custo = custo
                melhor_ponto = ponto
                melhor_caminho = caminho

        return melhor_ponto, melhor_caminho

    def _planejar_coleta_otima(self):
        # Testa todas as ordens possiveis das esferas conhecidas.
        candidatas = list(self.esferas_conhecidas - self.coletadas)
        if not candidatas:
            return None, []

        melhor_ordem = None
        melhor_caminho = []
        menor_custo = float("inf")

        for ordem in permutations(candidatas):
            posicao_atual = self.posicao
            custo_total = 0.0
            caminho_total = []
            rota_valida = True

            for indice, destino in enumerate(ordem):
                caminho, custo = a_estrela(posicao_atual, destino, self.mapa)
                if not caminho:
                    rota_valida = False
                    break

                custo_total += custo
                if indice == 0:
                    caminho_total = caminho
                else:
                    caminho_total.extend(caminho[1:])
                posicao_atual = destino

            if rota_valida and custo_total < menor_custo:
                menor_custo = custo_total
                melhor_ordem = list(ordem)
                melhor_caminho = caminho_total

        return melhor_ordem, melhor_caminho

    def escanear_radar(self):
        # Varre as celulas dentro do alcance do radar e atualiza o conhecimento.
        linha_base, coluna_base = self.posicao
        detectadas = []
        for d_linha in range(-ALCANCE_RADAR, ALCANCE_RADAR + 1):
            for d_coluna in range(-ALCANCE_RADAR, ALCANCE_RADAR + 1):
                if max(abs(d_linha), abs(d_coluna)) <= ALCANCE_RADAR:
                    nova_linha, nova_coluna = linha_base + d_linha, coluna_base + d_coluna
                    if 0 <= nova_linha < TAMANHO_MAPA and 0 <= nova_coluna < TAMANHO_MAPA:
                        posicao = (nova_linha, nova_coluna)
                        if (
                            posicao in self.todas_esferas
                            and posicao not in self.coletadas
                            and posicao not in self.esferas_conhecidas
                        ):
                            self.esferas_conhecidas.add(posicao)
                            detectadas.append(posicao)
        return detectadas

    def avancar(self):
        # Se a missao ja terminou, nao executa novos passos.
        if self.estado == "concluido":
            return False

        # O radar e consultado em todo turno antes da decisao de movimento.
        novas_detectadas = self.escanear_radar()
        if novas_detectadas:
            for esfera in novas_detectadas:
                self.registro.append(f"Esfera detectada em {esfera}")
            if self.estado == "coletando":
                self.caminho = []

        if self.estado == "explorando":
            # Se alguma esfera ja foi descoberta, o agente passa a coletar.
            disponiveis = self.esferas_conhecidas - self.coletadas
            if disponiveis:
                self.estado = "coletando"
                self.caminho = []
                self.registro.append("Mudando para COLETA")
                return True

            # Caso nao haja caminho ativo, escolhe um novo ponto de observacao.
            if not self.caminho:
                alvo, caminho = self._melhor_ponto_observacao()
                if alvo is not None:
                    self.pontos_observacao_restantes.discard(alvo)
                    self.caminho = caminho[1:] if len(caminho) > 1 else []
                else:
                    # Quando todos os pontos foram visitados, reinicia a lista.
                    self.pontos_observacao_restantes = set(self.pontos_observacao)
                    self.registro.append("Pontos de observacao reiniciados")
                    return True

            if self.caminho:
                proxima_posicao = self.caminho.pop(0)
                self.mover_para(proxima_posicao)

        elif self.estado == "coletando":
            # Define a melhor sequencia para pegar todas as esferas conhecidas.
            if not self.caminho:
                melhor_ordem, melhor_caminho = self._planejar_coleta_otima()
                if melhor_ordem is None:
                    self.estado = "explorando"
                    return True
                self.registro.append(
                    "Melhor sequencia conhecida: "
                    + " -> ".join(str(posicao) for posicao in melhor_ordem)
                )
                self.caminho = melhor_caminho[1:] if len(melhor_caminho) > 1 else []

            if self.caminho:
                proxima_posicao = self.caminho.pop(0)
                self.mover_para(proxima_posicao)

                # Se chegou a uma esfera ainda nao coletada, registra a coleta.
                if self.posicao in (self.esferas_conhecidas - self.coletadas):
                    self.coletadas.add(self.posicao)
                    self.registro.append(
                        f"Esfera coletada em {self.posicao} "
                        f"({len(self.coletadas)}/{NUM_ESFERAS})"
                    )
                    self.caminho = []

                    # Quando todas as esferas sao coletadas, volta para a base.
                    if len(self.coletadas) == NUM_ESFERAS:
                        self.estado = "retornando"
                        caminho, _ = a_estrela(self.posicao, POS_INICIAL, self.mapa)
                        self.caminho = caminho[1:] if len(caminho) > 1 else []
                        self.registro.append("TODAS AS ESFERAS COLETADAS! Retornando a base.")
            else:
                self.caminho = []

        elif self.estado == "retornando":
            # Garante um caminho valido ate a posicao inicial.
            if not self.caminho:
                caminho, _ = a_estrela(self.posicao, POS_INICIAL, self.mapa)
                self.caminho = caminho[1:] if len(caminho) > 1 else []

            if self.caminho:
                proxima_posicao = self.caminho.pop(0)
                self.mover_para(proxima_posicao)

                # Ao chegar na base, encerra a missao.
                if self.posicao == POS_INICIAL:
                    self.estado = "concluido"
                    self.registro.append(
                        f"MISSAO CONCLUIDA! Custo total: {self.custo_total:.1f} | "
                        f"Passos: {self.passos}"
                    )
                    return False
            else:
                if self.posicao == POS_INICIAL:
                    self.estado = "concluido"
                    return False

        return True

    def mover_para(self, nova_posicao):
        # Atualiza custo, passos, posicao atual e trilha visual.
        terreno = self.mapa[nova_posicao[0]][nova_posicao[1]]
        custo_movimento = CUSTO_TERRENO[terreno]
        self.custo_total += custo_movimento
        self.passos += 1
        self.posicao = nova_posicao
        self.trilha.append(nova_posicao)

        # Mantem apenas o trecho mais recente do rastro.
        if len(self.trilha) > 300:
            self.trilha = self.trilha[-300:]
