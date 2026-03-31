# Configurações principais do mapa, terrenos, cores e parâmetros visuais para o jogo de coleta de esferas. 

# Dimensões do mapa
TAMANHO_MAPA = 42

# Tipos de terreno e seus custos de movimento
GRAMA = 0
AGUA = 1
MONTANHA = 2

CUSTO_TERRENO = {
    GRAMA: 1,
    AGUA: 10,
    MONTANHA: 60,
}

# Cores para cada terreno (RGB)
COR_TERRENO = {
    GRAMA: (34, 139, 34),
    AGUA: (30, 144, 255),
    MONTANHA: (112, 128, 144),
}

# Parâmetros visuais
TAMANHO_CELULA = 16
LARGURA_INFO = 320
LARGURA_TELA = TAMANHO_MAPA * TAMANHO_CELULA + LARGURA_INFO
ALTURA_TELA = TAMANHO_MAPA * TAMANHO_CELULA
FPS = 60

# Cores de interface
COR_FUNDO = (15, 15, 25)
COR_PAINEL = (20, 20, 35)
COR_TEXTO = (220, 220, 240)
COR_TEXTO_DIM = (120, 120, 140)
COR_AGENTE = (255, 215, 0)
COR_ESFERA = (180, 0, 255)
COR_ESFERA_COL = (80, 255, 120)
COR_BASE = (255, 80, 80)
COR_TRILHA = (255, 200, 0)
COR_RADAR = (255, 255, 0)
COR_DESTAQUE = (255, 255, 100)

# Raio do radar do agente (em células)
ALCANCE_RADAR = 3

# Número de esferas no mapa
NUM_ESFERAS = 7

# Posição inicial do agente (centro do mapa)
POS_INICIAL = (TAMANHO_MAPA // 2, TAMANHO_MAPA // 2)

# Velocidade de animação (menor = mais rápido)
ATRASO_MOVIMENTO = 0.04

# Posições padrão usadas no modo fixo
POSICOES_FIXAS_PADRAO = [
    (3, 38),
    (5, 16),
    (11, 14),
    (15, 8),
    (24, 33),
    (34, 5),
    (38, 30),
]
