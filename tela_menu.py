import sys

import pygame

from constantes import (
    TAMANHO_CELULA,
    POSICOES_FIXAS_PADRAO,
    FPS,
    GRAMA,
    LARGURA_INFO,
    TAMANHO_MAPA,
    MONTANHA,
    NUM_ESFERAS,
    ALTURA_TELA,
    LARGURA_TELA,
    POS_INICIAL,
    COR_TERRENO,
    AGUA,
)
from util_esferas import gerar_esferas_fixas


class TelaMenu:
    """Tela exibida antes do inicio da simulacao."""

    C_BG = (10, 12, 28)
    C_PANEL = (18, 20, 40)
    C_BORDER = (50, 60, 100)
    C_TITLE = (255, 215, 0)
    C_TEXT = (220, 220, 240)
    C_DIM = (110, 115, 145)
    C_BTN_A = (30, 120, 60)
    C_BTN_A_HV = (40, 160, 80)
    C_BTN_F = (40, 80, 180)
    C_BTN_F_HV = (60, 110, 220)
    C_BTN_OK = (180, 40, 40)
    C_BTN_OK_HV = (220, 60, 60)
    C_BTN_CLR = (80, 50, 20)
    C_BTN_CLR_HV = (110, 75, 30)
    C_PLACED = (180, 0, 255)
    C_HOVER = (255, 255, 100)
    C_BASE_MK = (255, 80, 80)

    def __init__(self, mapa):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Agente A* - Configuracao Inicial")
        self.relogio = pygame.time.Clock()

        self.fonte_xl = pygame.font.SysFont("monospace", 22, bold=True)
        self.fonte_grd = pygame.font.SysFont("monospace", 15, bold=True)
        self.fonte_med = pygame.font.SysFont("monospace", 13, bold=True)
        self.fonte_peq = pygame.font.SysFont("monospace", 11)

        self.mapa = mapa
        self.estado = "selecao_modo"
        self.modo_esferas = None
        self.posicionadas = []
        self.celula_hover = None
        self.mensagem_erro = ""
        self.temporizador_erro = 0

        self.superficie_terreno = self._pre_renderizar_terreno()

    def _pre_renderizar_terreno(self):
        superficie = pygame.Surface((TAMANHO_MAPA * TAMANHO_CELULA, TAMANHO_MAPA * TAMANHO_CELULA))
        for linha in range(TAMANHO_MAPA):
            for coluna in range(TAMANHO_MAPA):
                cor = COR_TERRENO[self.mapa[linha][coluna]]
                retangulo = pygame.Rect(
                    coluna * TAMANHO_CELULA,
                    linha * TAMANHO_CELULA,
                    TAMANHO_CELULA,
                    TAMANHO_CELULA,
                )
                pygame.draw.rect(superficie, cor, retangulo)
                pygame.draw.rect(superficie, (0, 0, 0), retangulo, 1)
        return superficie

    def _desenhar_botao(self, retangulo, rotulo, cor_base, cor_hover, posicao_mouse, sub_rotulo=None):
        esta_sobre = retangulo.collidepoint(posicao_mouse)
        cor = cor_hover if esta_sobre else cor_base
        pygame.draw.rect(self.tela, cor, retangulo, border_radius=6)
        pygame.draw.rect(self.tela, (255, 255, 255, 60), retangulo, width=2, border_radius=6)
        txt = self.fonte_grd.render(rotulo, True, (255, 255, 255))
        self.tela.blit(
            txt,
            (
                retangulo.centerx - txt.get_width() // 2,
                retangulo.centery - txt.get_height() // 2 - (8 if sub_rotulo else 0),
            ),
        )
        if sub_rotulo:
            sub = self.fonte_peq.render(sub_rotulo, True, (200, 200, 200))
            self.tela.blit(sub, (retangulo.centerx - sub.get_width() // 2, retangulo.centery + 6))
        return esta_sobre

    def _retangulo_painel(self):
        return pygame.Rect(TAMANHO_MAPA * TAMANHO_CELULA, 0, LARGURA_INFO, ALTURA_TELA)

    def _desenhar_fundo_painel(self):
        pygame.draw.rect(self.tela, self.C_PANEL, self._retangulo_painel())
        pygame.draw.line(
            self.tela,
            self.C_BORDER,
            (TAMANHO_MAPA * TAMANHO_CELULA, 0),
            (TAMANHO_MAPA * TAMANHO_CELULA, ALTURA_TELA),
            2,
        )

    def _texto(self, superficie, texto, fonte, cor, centro_x, y, centralizado=True):
        texto_renderizado = fonte.render(texto, True, cor)
        pos_x = centro_x - texto_renderizado.get_width() // 2 if centralizado else centro_x
        superficie.blit(texto_renderizado, (pos_x, y))
        return texto_renderizado.get_height()

    def _desenhar_selecao_modo(self, posicao_mouse):
        self.tela.fill(self.C_BG)
        self.tela.blit(self.superficie_terreno, (0, 0))

        overlay = pygame.Surface((TAMANHO_MAPA * TAMANHO_CELULA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        self.tela.blit(overlay, (0, 0))

        self._desenhar_fundo_painel()
        px = TAMANHO_MAPA * TAMANHO_CELULA + 16
        py = 30

        py += self._texto(self.tela, "AGENTE A*", self.fonte_xl, self.C_TITLE, px + (LARGURA_INFO - 32) // 2, py) + 6
        py += self._texto(self.tela, "Esferas do Dragao", self.fonte_med, self.C_DIM, px + (LARGURA_INFO - 32) // 2, py) + 24

        pygame.draw.line(self.tela, self.C_BORDER, (px, py), (px + LARGURA_INFO - 32, py))
        py += 20

        py += self._texto(self.tela, "MODO DE JOGO", self.fonte_grd, self.C_TEXT, px + (LARGURA_INFO - 32) // 2, py) + 16

        bw, bh = LARGURA_INFO - 40, 58
        bx = TAMANHO_MAPA * TAMANHO_CELULA + 20

        btn_rand = pygame.Rect(bx, py, bw, bh)
        self._desenhar_botao(btn_rand, "ALEATORIO", self.C_BTN_A, self.C_BTN_A_HV, posicao_mouse, "Esferas em posicoes sorteadas")
        py += bh + 14

        btn_fix = pygame.Rect(bx, py, bw, bh)
        self._desenhar_botao(btn_fix, "POSICOES FIXAS", self.C_BTN_F, self.C_BTN_F_HV, posicao_mouse, "Voce escolhe onde ficam")
        py += bh + 30

        pygame.draw.line(self.tela, self.C_BORDER, (px, py), (px + LARGURA_INFO - 32, py))
        py += 16

        py += self._texto(self.tela, "Legenda do mapa:", self.fonte_med, self.C_DIM, px, py, centralizado=False) + 10
        for color, label in [
            (COR_TERRENO[GRAMA], "Grama   (custo 1)"),
            (COR_TERRENO[AGUA], "Agua    (custo 10)"),
            (COR_TERRENO[MONTANHA], "Montanha (custo 60)"),
            (self.C_BASE_MK, "Base do agente"),
        ]:
            pygame.draw.circle(self.tela, color, (px + 7, py + 6), 5)
            self._texto(self.tela, label, self.fonte_peq, self.C_DIM, px + 18, py, centralizado=False)
            py += 18

        br, bc = POS_INICIAL
        pygame.draw.rect(self.tela, self.C_BASE_MK, (bc * TAMANHO_CELULA + 2, br * TAMANHO_CELULA + 2, TAMANHO_CELULA - 4, TAMANHO_CELULA - 4), 2)

        title_surf = self.fonte_xl.render("ESCOLHA O MODO", True, self.C_TITLE)
        tx = (TAMANHO_MAPA * TAMANHO_CELULA) // 2 - title_surf.get_width() // 2
        self.tela.blit(title_surf, (tx, ALTURA_TELA // 2 - 50))
        hint = self.fonte_med.render("Clique em um botao no painel ->", True, self.C_DIM)
        self.tela.blit(hint, ((TAMANHO_MAPA * TAMANHO_CELULA) // 2 - hint.get_width() // 2, ALTURA_TELA // 2 - 10))

        return btn_rand, btn_fix

    def _desenhar_posicionamento_esferas(self, posicao_mouse):
        self.tela.fill(self.C_BG)
        self.tela.blit(self.superficie_terreno, (0, 0))

        if self.celula_hover:
            hr, hc = self.celula_hover
            s = pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA), pygame.SRCALPHA)
            s.fill((255, 255, 100, 90))
            self.tela.blit(s, (hc * TAMANHO_CELULA, hr * TAMANHO_CELULA))
            pygame.draw.rect(self.tela, self.C_HOVER, (hc * TAMANHO_CELULA, hr * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA), 2)

        for idx, pos in enumerate(self.posicionadas):
            pr, pc = pos
            cx = pc * TAMANHO_CELULA + TAMANHO_CELULA // 2
            cy = pr * TAMANHO_CELULA + TAMANHO_CELULA // 2
            pygame.draw.circle(self.tela, self.C_PLACED, (cx, cy), 6)
            pygame.draw.circle(self.tela, (255, 255, 255), (cx, cy), 6, 1)
            num = self.fonte_peq.render(str(idx + 1), True, (255, 255, 255))
            self.tela.blit(num, (cx - num.get_width() // 2, cy - num.get_height() // 2))

        br, bc = POS_INICIAL
        pygame.draw.rect(self.tela, self.C_BASE_MK, (bc * TAMANHO_CELULA + 1, br * TAMANHO_CELULA + 1, TAMANHO_CELULA - 2, TAMANHO_CELULA - 2), 2)

        self._desenhar_fundo_painel()
        px = TAMANHO_MAPA * TAMANHO_CELULA + 16
        py = 20
        w = LARGURA_INFO - 32

        py += self._texto(self.tela, "POSICOES FIXAS", self.fonte_xl, self.C_TITLE, px + w // 2, py) + 4
        py += self._texto(self.tela, "Clique no mapa para", self.fonte_peq, self.C_DIM, px + w // 2, py) + 2
        py += self._texto(self.tela, "posicionar as esferas", self.fonte_peq, self.C_DIM, px + w // 2, py) + 16

        pygame.draw.line(self.tela, self.C_BORDER, (px, py), (px + w, py))
        py += 12

        remaining = NUM_ESFERAS - len(self.posicionadas)
        prog_color = (100, 255, 100) if remaining == 0 else self.C_TITLE
        py += self._texto(self.tela, f"Esferas: {len(self.posicionadas)}/{NUM_ESFERAS}", self.fonte_grd, prog_color, px + w // 2, py) + 6

        bar_w = w
        bar_h = 10
        pygame.draw.rect(self.tela, (40, 40, 70), (px, py, bar_w, bar_h))
        filled = int(bar_w * len(self.posicionadas) / NUM_ESFERAS)
        pygame.draw.rect(self.tela, prog_color, (px, py, filled, bar_h))
        pygame.draw.rect(self.tela, self.C_BORDER, (px, py, bar_w, bar_h), 1)
        py += bar_h + 14

        for i in range(NUM_ESFERAS):
            if i < len(self.posicionadas):
                r, c = self.posicionadas[i]
                ter = self.mapa[r][c]
                ter_sym = {GRAMA: "G", AGUA: "A", MONTANHA: "M"}[ter]
                ter_col = COR_TERRENO[ter]
                line = f"  {i + 1}. ({r:2d},{c:2d}) [{ter_sym}]"
                ls = self.fonte_peq.render(line, True, self.C_TEXT)
                tc = pygame.Surface((8, 8))
                tc.fill(ter_col)
                self.tela.blit(tc, (px + 2, py + 2))
                self.tela.blit(ls, (px + 12, py))
            else:
                ls = self.fonte_peq.render(f"  {i + 1}. ---", True, self.C_DIM)
                self.tela.blit(ls, (px, py))
            py += 16

        py += 10
        pygame.draw.line(self.tela, self.C_BORDER, (px, py), (px + w, py))
        py += 12

        if self.celula_hover:
            hr, hc = self.celula_hover
            ter = self.mapa[hr][hc]
            ter_name = {GRAMA: "Grama(1)", AGUA: "Agua(10)", MONTANHA: "Mont.(60)"}[ter]
            self._texto(self.tela, f"Cursor: ({hr},{hc})", self.fonte_peq, self.C_DIM, px, py, centralizado=False)
            py += 14
            self._texto(self.tela, f"Terreno: {ter_name}", self.fonte_peq, COR_TERRENO[ter], px, py, centralizado=False)
            py += 18
        else:
            py += 32

        if self.mensagem_erro and self.temporizador_erro > 0:
            self._texto(self.tela, self.mensagem_erro, self.fonte_peq, (255, 80, 80), px + w // 2, py)
            self.temporizador_erro -= 1
        py += 18

        bw, bh = w, 40
        btn_clr = pygame.Rect(TAMANHO_MAPA * TAMANHO_CELULA + 20, ALTURA_TELA - bh * 2 - 20, bw, bh)
        self._desenhar_botao(btn_clr, "LIMPAR TUDO", self.C_BTN_CLR, self.C_BTN_CLR_HV, posicao_mouse)

        btn_ok = pygame.Rect(TAMANHO_MAPA * TAMANHO_CELULA + 20, ALTURA_TELA - bh - 10, bw, bh)
        ok_base = self.C_BTN_OK if len(self.posicionadas) == NUM_ESFERAS else (50, 50, 70)
        ok_hover = self.C_BTN_OK_HV if len(self.posicionadas) == NUM_ESFERAS else (50, 50, 70)
        sub_ok = "Clique para iniciar!" if len(self.posicionadas) == NUM_ESFERAS else f"Faltam {remaining} esfera(s)"
        self._desenhar_botao(btn_ok, "INICIAR", ok_base, ok_hover, posicao_mouse, sub_ok)

        if remaining > 0:
            msg = f"Clique para posicionar esfera {len(self.posicionadas) + 1}"
            ms = self.fonte_med.render(msg, True, self.C_TITLE)
            self.tela.blit(ms, (8, ALTURA_TELA - 22))

        return btn_clr, btn_ok

    def executar(self):
        """Executa o loop do menu ate o usuario confirmar ou sair."""
        while True:
            posicao_mouse = pygame.mouse.get_pos()

            if posicao_mouse[0] < TAMANHO_MAPA * TAMANHO_CELULA:
                self.celula_hover = (posicao_mouse[1] // TAMANHO_CELULA, posicao_mouse[0] // TAMANHO_CELULA)
            else:
                self.celula_hover = None

            if self.estado == "selecao_modo":
                btn_rand, btn_fix = self._desenhar_selecao_modo(posicao_mouse)
            else:
                btn_clr, btn_ok = self._desenhar_posicionamento_esferas(posicao_mouse)

            pygame.display.flip()
            self.relogio.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.estado == "posicionar_esferas":
                            self.estado = "selecao_modo"
                            self.posicionadas = []
                        else:
                            pygame.quit()
                            sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.estado == "selecao_modo":
                        if btn_rand.collidepoint(posicao_mouse):
                            return "aleatorio", None
                        if btn_fix.collidepoint(posicao_mouse):
                            self.estado = "posicionar_esferas"
                            self.posicionadas = list(POSICOES_FIXAS_PADRAO)

                    elif self.estado == "posicionar_esferas":
                        if btn_clr.collidepoint(posicao_mouse):
                            self.posicionadas = []
                            self.mensagem_erro = ""
                            continue

                        if btn_ok.collidepoint(posicao_mouse):
                            if len(self.posicionadas) == NUM_ESFERAS:
                                try:
                                    sp = gerar_esferas_fixas(self.posicionadas, self.mapa)
                                    return "fixo", sp
                                except ValueError as e:
                                    self.mensagem_erro = str(e)[:38]
                                    self.temporizador_erro = 180
                            else:
                                self.mensagem_erro = f"Faltam {NUM_ESFERAS - len(self.posicionadas)} esfera(s)!"
                                self.temporizador_erro = 180
                            continue

                        if self.celula_hover:
                            pos = self.celula_hover
                            if pos == POS_INICIAL:
                                self.mensagem_erro = "Essa e a base do agente!"
                                self.temporizador_erro = 150
                            elif pos in self.posicionadas:
                                self.posicionadas.remove(pos)
                                self.mensagem_erro = ""
                            elif len(self.posicionadas) < NUM_ESFERAS:
                                self.posicionadas.append(pos)
                                self.mensagem_erro = ""
                            else:
                                self.mensagem_erro = "Ja tem 7 esferas! Limpe para refazer."
                                self.temporizador_erro = 180


