
# Utilitário para carregar e validar o mapa a partir de um arquivo TXT.
from constantes import GRAMA, POS_INICIAL, TAMANHO_MAPA

#
def carregar_mapa_de_txt(caminho_arquivo):
    """Carrega o mapa a partir de um arquivo TXT."""
    try:
        with open(caminho_arquivo, "r") as arquivo:
            linhas = arquivo.readlines()

        mapa = []
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue

            if "," in linha:
                linha_mapa = [int(valor) for valor in linha.split(",")]
            else:
                linha_mapa = [int(caractere) for caractere in linha if caractere.isdigit()]

            mapa.append(linha_mapa)

        if mapa[POS_INICIAL[0]][POS_INICIAL[1]] != GRAMA:
            print(
                f"[AVISO] Posicao inicial {POS_INICIAL} nao e grama "
                f"(era {mapa[POS_INICIAL[0]][POS_INICIAL[1]]}), ajustando apenas essa celula..."
            )
            mapa[POS_INICIAL[0]][POS_INICIAL[1]] = GRAMA

        print(f"[INFO] Mapa carregado com sucesso do TXT: {caminho_arquivo}")
        return mapa
    except Exception as erro:
        print(f"[ERRO] Falha ao ler o arquivo TXT: {erro}")
        return None


def validar_mapa(mapa):
    """Valida se o mapa possui dimensões e estrutura corretas."""
    if not mapa:
        print("[ERRO] Mapa vazio!")
        return False

    if len(mapa) != TAMANHO_MAPA:
        print(f"[ERRO] Numero de linhas incorreto: {len(mapa)} (esperado: {TAMANHO_MAPA})")
        return False

    for indice, linha_mapa in enumerate(mapa):
        if len(linha_mapa) != TAMANHO_MAPA:
            print(
                f"[ERRO] Linha {indice} tem {len(linha_mapa)} colunas "
                f"(esperado: {TAMANHO_MAPA})"
            )
            return False

    print(f"[INFO] Mapa validado: {TAMANHO_MAPA}x{TAMANHO_MAPA} celulas")
    return True
