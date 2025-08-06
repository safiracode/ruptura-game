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
VELOCIDADE_JOGADOR = 2
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
COBEL = os.path.join('ideias de imagens', 'cobel 3.png')
SPRITESHEET = os.path.join('ideias de imagens', 'spritesheet.png')
RUPTURA_START_LOGO = os.path.join('imagens', 'ruptura_logo.png')

FONTE = 'arial'