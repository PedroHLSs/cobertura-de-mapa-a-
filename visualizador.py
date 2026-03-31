import math
import time

import pygame

from constantes import (
    AGUA,
    ALCANCE_RADAR,
    ALTURA_TELA,
    COR_AGENTE,
    COR_BASE,
    COR_ESFERA,
    COR_ESFERA_COL,
    COR_FUNDO,
    COR_PAINEL,
    COR_RADAR,
    COR_TERRENO,
    COR_TEXTO,
    COR_TEXTO_DIM,
    COR_TRILHA,
    FPS,
    GRAMA,
    LARGURA_INFO,
    LARGURA_TELA,
    MONTANHA,
    NUM_ESFERAS,
    POS_INICIAL,
    TAMANHO_CELULA,
    TAMANHO_MAPA,
)


class Visualizador:
    """Gerencia toda a renderização gráfica usando Pygame."""

    def __init__(self, mapa, esferas):
        pygame.init()
        pygame.display.set_caption("Agente A* — Busca e Coleta de Esferas")

        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.relogio = pygame.time.Clock()
        self.fonte_peq = pygame.font.SysFont("monospace", 11)
        self.fonte_med = pygame.font.SysFont("monospace", 13, bold=True)
        self.fonte_grd = pygame.font.SysFont("monospace", 16, bold=True)
        self.fonte_xgr = pygame.font.SysFont("monospace", 20, bold=True)

        self.mapa = mapa
        self.esferas = esferas

        self.superficie_terreno = self._pre_renderizar_terreno()
        self.superficie_radar = pygame.Surface(
            (TAMANHO_MAPA * TAMANHO_CELULA, TAMANHO_MAPA * TAMANHO_CELULA),
            pygame.SRCALPHA,
        )

    def _pre_renderizar_terreno(self):
        superficie = pygame.Surface((TAMANHO_MAPA * TAMANHO_CELULA, TAMANHO_MAPA * TAMANHO_CELULA))
        for linha in range(TAMANHO_MAPA):
            for coluna in range(TAMANHO_MAPA):
                terreno = self.mapa[linha][coluna]
                cor = COR_TERRENO[terreno]
                retangulo = pygame.Rect(
                    coluna * TAMANHO_CELULA,
                    linha * TAMANHO_CELULA,
                    TAMANHO_CELULA,
                    TAMANHO_CELULA,
                )
                pygame.draw.rect(superficie, cor, retangulo)
                pygame.draw.rect(superficie, (0, 0, 0, 30), retangulo, 1)
        return superficie

    def desenhar(self, agente):
        self.tela.fill(COR_FUNDO)
        self.tela.blit(self.superficie_terreno, (0, 0))

        for indice, posicao in enumerate(agente.trilha):
            px_linha = posicao[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2
            px_coluna = posicao[1] * TAMANHO_CELULA + TAMANHO_CELULA // 2
            cor = (
                min(255, COR_TRILHA[0]),
                min(255, int(COR_TRILHA[1] * (indice / max(len(agente.trilha), 1)))),
                0,
            )
            pygame.draw.circle(self.tela, cor, (px_coluna, px_linha), 2)

        self.superficie_radar.fill((0, 0, 0, 0))
        agente_linha, agente_coluna = agente.posicao
        for d_linha in range(-ALCANCE_RADAR, ALCANCE_RADAR + 1):
            for d_coluna in range(-ALCANCE_RADAR, ALCANCE_RADAR + 1):
                if max(abs(d_linha), abs(d_coluna)) <= ALCANCE_RADAR:
                    nova_linha, nova_coluna = agente_linha + d_linha, agente_coluna + d_coluna
                    if 0 <= nova_linha < TAMANHO_MAPA and 0 <= nova_coluna < TAMANHO_MAPA:
                        retangulo = pygame.Rect(
                            nova_coluna * TAMANHO_CELULA,
                            nova_linha * TAMANHO_CELULA,
                            TAMANHO_CELULA,
                            TAMANHO_CELULA,
                        )
                        pygame.draw.rect(self.superficie_radar, (255, 255, 100, 35), retangulo)
        self.tela.blit(self.superficie_radar, (0, 0))

        radar_px = ALCANCE_RADAR * TAMANHO_CELULA
        agente_px_x = agente_coluna * TAMANHO_CELULA
        agente_px_y = agente_linha * TAMANHO_CELULA
        pygame.draw.rect(
            self.tela,
            COR_RADAR,
            (
                agente_px_x - radar_px,
                agente_px_y - radar_px,
                (ALCANCE_RADAR * 2 + 1) * TAMANHO_CELULA,
                (ALCANCE_RADAR * 2 + 1) * TAMANHO_CELULA,
            ),
            1,
        )

        for esfera in self.esferas:
            linha_esfera, coluna_esfera = esfera
            centro_x = coluna_esfera * TAMANHO_CELULA + TAMANHO_CELULA // 2
            centro_y = linha_esfera * TAMANHO_CELULA + TAMANHO_CELULA // 2

            if esfera in agente.coletadas:
                pygame.draw.circle(self.tela, COR_ESFERA_COL, (centro_x, centro_y), 4)
                pygame.draw.circle(self.tela, (255, 255, 255), (centro_x, centro_y), 4, 1)
            elif esfera in agente.esferas_conhecidas:
                pygame.draw.circle(self.tela, COR_ESFERA, (centro_x, centro_y), 5)
                pygame.draw.circle(self.tela, (255, 255, 255), (centro_x, centro_y), 5, 1)
                pulso = int(abs(math.sin(time.time() * 4)) * 80)
                brilho = pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA), pygame.SRCALPHA)
                pygame.draw.circle(
                    brilho,
                    (180, 0, 255, pulso),
                    (TAMANHO_CELULA // 2, TAMANHO_CELULA // 2),
                    TAMANHO_CELULA // 2,
                )
                self.tela.blit(brilho, (coluna_esfera * TAMANHO_CELULA, linha_esfera * TAMANHO_CELULA))
            else:
                pygame.draw.circle(self.tela, (200, 200, 210), (centro_x, centro_y), 4)
                pygame.draw.circle(self.tela, (120, 120, 140), (centro_x, centro_y), 4, 1)

        linha_base, coluna_base = POS_INICIAL
        base_centro_x = coluna_base * TAMANHO_CELULA + TAMANHO_CELULA // 2
        base_centro_y = linha_base * TAMANHO_CELULA + TAMANHO_CELULA // 2
        pygame.draw.rect(
            self.tela,
            COR_BASE,
            (
                coluna_base * TAMANHO_CELULA + 2,
                linha_base * TAMANHO_CELULA + 2,
                TAMANHO_CELULA - 4,
                TAMANHO_CELULA - 4,
            ),
            2,
        )
        pygame.draw.circle(self.tela, COR_BASE, (base_centro_x, base_centro_y), 4)

        centro_agente_x = agente_coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2
        centro_agente_y = agente_linha * TAMANHO_CELULA + TAMANHO_CELULA // 2
        pygame.draw.circle(self.tela, (0, 0, 0), (centro_agente_x, centro_agente_y), 7)
        pygame.draw.circle(self.tela, COR_AGENTE, (centro_agente_x, centro_agente_y), 6)
        pygame.draw.circle(self.tela, (255, 255, 255), (centro_agente_x, centro_agente_y), 6, 1)

        self._desenhar_painel(agente)
        pygame.display.flip()

    def _desenhar_painel(self, agente):
        painel_x = TAMANHO_MAPA * TAMANHO_CELULA
        pygame.draw.rect(self.tela, COR_PAINEL, (painel_x, 0, LARGURA_INFO, ALTURA_TELA))
        pygame.draw.line(self.tela, (50, 50, 80), (painel_x, 0), (painel_x, ALTURA_TELA), 2)

        x = painel_x + 12
        y = 12
        dy = 22

        titulo = self.fonte_xgr.render("AGENTE A*", True, COR_AGENTE)
        self.tela.blit(titulo, (x, y))
        y += 30

        subtitulo = self.fonte_peq.render("Busca Heuristica e Coleta", True, COR_TEXTO_DIM)
        self.tela.blit(subtitulo, (x, y))
        y += 28

        pygame.draw.line(self.tela, (50, 50, 80), (x, y), (x + LARGURA_INFO - 24, y))
        y += 10

        rotulos_estado = {
            "explorando": ("EXPLORANDO", (100, 200, 255)),
            "coletando": ("COLETANDO", (255, 180, 0)),
            "retornando": ("RETORNANDO", (100, 255, 100)),
            "concluido": ("CONCLUIDO", (80, 255, 80)),
        }
        rotulo, cor = rotulos_estado.get(agente.estado, ("?", COR_TEXTO))
        estado_surf = self.fonte_grd.render(f"Estado: {rotulo}", True, cor)
        self.tela.blit(estado_surf, (x, y))
        y += dy + 4

        texto_posicao = self.fonte_med.render(
            f"Posicao: ({agente.posicao[0]:2d}, {agente.posicao[1]:2d})",
            True,
            COR_TEXTO,
        )
        self.tela.blit(texto_posicao, (x, y))
        y += dy

        nomes_terreno = {
            GRAMA: "Grama (x1)",
            AGUA: "Agua (x10)",
            MONTANHA: "Montanha (x60)",
        }
        terreno = self.mapa[agente.posicao[0]][agente.posicao[1]]
        terreno_surf = self.fonte_med.render(
            f"Terreno: {nomes_terreno[terreno]}",
            True,
            COR_TERRENO[terreno],
        )
        self.tela.blit(terreno_surf, (x, y))
        y += dy

        custo_surf = self.fonte_med.render(f"Custo acum.: {agente.custo_total:,.1f}", True, COR_TEXTO)
        self.tela.blit(custo_surf, (x, y))
        y += dy

        passos_surf = self.fonte_med.render(f"Passos: {agente.passos}", True, COR_TEXTO)
        self.tela.blit(passos_surf, (x, y))
        y += dy + 4

        pygame.draw.line(self.tela, (50, 50, 80), (x, y), (x + LARGURA_INFO - 24, y))
        y += 10

        titulo_esferas = self.fonte_med.render("Esferas:", True, COR_TEXTO)
        self.tela.blit(titulo_esferas, (x, y))
        y += dy

        total_coletadas = len(agente.coletadas)
        total_conhecidas = len(agente.esferas_conhecidas)

        largura_barra = LARGURA_INFO - 30
        altura_barra = 14
        preenchido = int(largura_barra * total_coletadas / NUM_ESFERAS)
        pygame.draw.rect(self.tela, (40, 40, 60), (x, y, largura_barra, altura_barra))
        pygame.draw.rect(self.tela, COR_ESFERA_COL, (x, y, preenchido, altura_barra))
        pygame.draw.rect(self.tela, (80, 80, 100), (x, y, largura_barra, altura_barra), 1)
        texto_progresso = self.fonte_peq.render(
            f"  {total_coletadas}/{NUM_ESFERAS} coletadas",
            True,
            (255, 255, 255),
        )
        self.tela.blit(texto_progresso, (x, y))
        y += altura_barra + 6

        detectadas_surf = self.fonte_peq.render(
            f"  Detectadas pelo radar: {total_conhecidas}",
            True,
            COR_TEXTO_DIM,
        )
        self.tela.blit(detectadas_surf, (x, y))
        y += dy

        pygame.draw.line(self.tela, (50, 50, 80), (x, y), (x + LARGURA_INFO - 24, y))
        y += 10

        titulo_legenda = self.fonte_med.render("Legenda:", True, COR_TEXTO)
        self.tela.blit(titulo_legenda, (x, y))
        y += dy

        legenda_itens = [
            (COR_AGENTE, "Agente (Goku)"),
            ((200, 200, 210), "Esfera (nao detectada)"),
            (COR_ESFERA, "Esfera (no radar)"),
            (COR_ESFERA_COL, "Esfera (coletada)"),
            (COR_BASE, "Base / Ilha Kame"),
            (COR_TRILHA, "Trilha do agente"),
            (COR_RADAR, "Radar (alcance 3)"),
            (COR_TERRENO[GRAMA], "Grama  (custo 1)"),
            (COR_TERRENO[AGUA], "Agua   (custo 10)"),
            (COR_TERRENO[MONTANHA], "Montanha (custo 60)"),
        ]
        for cor, texto in legenda_itens:
            pygame.draw.circle(self.tela, cor, (x + 6, y + 6), 5)
            texto_surf = self.fonte_peq.render(texto, True, COR_TEXTO_DIM)
            self.tela.blit(texto_surf, (x + 16, y))
            y += 18

        y += 4
        pygame.draw.line(self.tela, (50, 50, 80), (x, y), (x + LARGURA_INFO - 24, y))
        y += 8

        titulo_log = self.fonte_med.render("Log de eventos:", True, COR_TEXTO)
        self.tela.blit(titulo_log, (x, y))
        y += dy

        max_linhas_log = (ALTURA_TELA - y - 10) // 16
        trecho_log = agente.registro[-max_linhas_log:]
        for linha in trecho_log:
            linha_surf = self.fonte_peq.render(linha[:36], True, COR_TEXTO_DIM)
            self.tela.blit(linha_surf, (x, y))
            y += 16

        if agente.estado == "concluido":
            self._desenhar_sobreposicao_conclusao(agente)

    def _desenhar_sobreposicao_conclusao(self, agente):
        sobreposicao = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        sobreposicao.fill((0, 0, 0, 160))
        self.tela.blit(sobreposicao, (0, 0))

        centro_x, centro_y = LARGURA_TELA // 2, ALTURA_TELA // 2 - 60

        titulo = self.fonte_xgr.render("🎉 MISSAO CONCLUIDA!", True, COR_AGENTE)
        self.tela.blit(titulo, (centro_x - titulo.get_width() // 2, centro_y))
        centro_y += 40

        linhas = [
            f"Todas as {NUM_ESFERAS} esferas foram coletadas!",
            f"Custo total do percurso: {agente.custo_total:,.1f}",
            f"Numero total de passos:  {agente.passos}",
            "",
            "Pressione ESC ou feche para sair.",
        ]
        for linha in linhas:
            superficie = self.fonte_med.render(linha, True, COR_TEXTO)
            self.tela.blit(superficie, (centro_x - superficie.get_width() // 2, centro_y))
            centro_y += 26
