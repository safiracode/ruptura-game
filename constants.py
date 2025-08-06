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
BALAO = 'baloes_att.png'
CAFE = 'cafe_att.png'
PAREDE = 'parede3.png'
MARK_IMG = 'mark_frente.png'
COBEL = 'cobel_frente.png'
SPRITESHEET = os.path.join('ideias de imagens', 'spritesheet.png') # checar uso
RUPTURA_START_LOGO = 'ruptura_logo.png'

FONTE = 'arial'