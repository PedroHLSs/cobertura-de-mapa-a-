import os
import sys
import time

import pygame

from logica_agente import Agente
from constantes import ATRASO_MOVIMENTO, FPS, NUM_ESFERAS, POS_INICIAL
from util_mapa import carregar_mapa_de_txt, validar_mapa
from tela_menu import TelaMenu
from util_esferas import gerar_esferas
from visualizador import Visualizador


def principal():
    """Função principal da simulação."""
    # Apresenta um resumo inicial no terminal antes de abrir a interface gráfica.
    print("=" * 70)
    print("AGENTE INTELIGENTE COM BUSCA HEURÍSTICA A* (A-Estrela)".center(70))
    print("=" * 70)
    print()

    # O mapa base fica no mesmo diretório do executável principal.
    caminho_mapa = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapa.txt")
    mapa = carregar_mapa_de_txt(caminho_mapa)

    if mapa is None:
        print("[ERRO] Falha ao carregar o mapa! Encerrando...")
        sys.exit(1)

    if not validar_mapa(mapa):
        print("[ERRO] Mapa inválido! Encerrando...")
        sys.exit(1)

    tela_menu = TelaMenu(mapa)
    modo_esferas, esferas_fixas = tela_menu.executar()

    # O usuário escolhe entre posições fixas ou geração aleatória das esferas.
    if modo_esferas == "fixo":
        esferas = esferas_fixas
        print("[INFO] Modo POSIÇÕES FIXAS")
    else:
        esferas = gerar_esferas(mapa)
        print("[INFO] Modo ALEATÓRIO")

    print(f"[INFO] Posição inicial do agente: {POS_INICIAL}")
    print(f"[INFO] Esferas em: {sorted(esferas)}")
    print()
    print("Controles durante a simulação:")
    print("  ESPAÇO      - Pausar/Retomar")
    print("  ↑ (UP)      - Acelerar")
    print("  ↓ (DOWN)    - Desacelerar")
    print("  ESC         - Sair")
    print("=" * 70)
    print()

    pygame.display.set_caption("Agente A* — Busca e Coleta de Esferas")

    agente = Agente(mapa, esferas)
    visualizador = Visualizador(mapa, esferas)

    ultimo_tempo_passo = time.time()
    atraso_movimento = ATRASO_MOVIMENTO

    em_execucao = True
    pausado = False

    while em_execucao:
        # Processa eventos do teclado e da janela em cada ciclo da simulação.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                em_execucao = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    em_execucao = False
                elif event.key == pygame.K_SPACE:
                    pausado = not pausado
                elif event.key == pygame.K_UP:
                    atraso_movimento = max(0.005, atraso_movimento - 0.01)
                elif event.key == pygame.K_DOWN:
                    atraso_movimento = min(0.5, atraso_movimento + 0.01)

        agora = time.time()
        # O agente só avança quando não está pausado e quando já passou o atraso configurado.
        if not pausado and agente.estado != "concluido":
            if agora - ultimo_tempo_passo >= atraso_movimento:
                agente.avancar()
                ultimo_tempo_passo = agora

        # Redesenha toda a cena a cada frame.
        visualizador.desenhar(agente)
        visualizador.relogio.tick(FPS)

    print("\n" + "=" * 60)
    print("MISSÃO CONCLUÍDA" if agente.estado == "concluido" else "SIMULAÇÃO ENCERRADA")
    print("=" * 60)
    print(f"  Esferas coletadas : {len(agente.coletadas)}/{NUM_ESFERAS}")
    print(f"  Custo total       : {agente.custo_total:,.1f}")
    print(f"  Número de passos  : {agente.passos}")
    print(f"  Posição final     : {agente.posicao}")
    print("=" * 60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    principal()
