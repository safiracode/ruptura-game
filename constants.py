# constants.py
import os

# Dimensões da tela
LARGURA = 480
ALTURA = 600
TAMANHO_BLOCO = 24

# Título do jogo
TITULO_JOGO = 'Ruptura'

# FPS
FPS = 60

VIDAS_INICIAIS = 5

# --- JOGADOR ---
VELOCIDADE_JOGADOR = 3
COR_JOGADOR = (255, 255, 0)
COMANDO_TIMEOUT = 3000 # 3 segundos em milissegundos

# --- CORES EM RGB ---
PRETO = (0, 0, 0)
VERDE = (35, 115, 80)
BRANCO = (255, 255, 255)

# --- ARQUIVOS ---
BALAO = 'balão.png'
CAFE = 'café.png'
PAREDE = 'parede3.png'
MARK_IMG = os.path.join('ideias de imagens', 'mark-head.png')

FONTE = 'arial'