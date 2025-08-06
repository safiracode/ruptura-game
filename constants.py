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
VELOCIDADE_JOGADOR = 1.5
COR_JOGADOR = (255, 255, 0)
COMANDO_TIMEOUT = 3000 # 3 segundos em milissegundos

# --- CORES EM RGB ---
PRETO = (0, 0, 0)
VERDE = (35, 115, 80)
BRANCO = (255, 255, 255)

# --- ARQUIVOS ---
CHAVE = 'chave.png'
NUMERO_PARTES_CHAVE = 3
BALAO = 'baloes_att.png'
CAFE = 'cafe_att.png'
PAREDE = 'parede3.png'


MARK_BAIXO = 'mark_baixo.png'
MARK_CIMA = 'mark_cima.png'
MARK_ESQUERDA = 'mark_esquerda.png'
MARK_DIREITA = 'mark_direita.png'
COBEL_BAIXO = 'cobel_baixo.png'
COBEL_CIMA = 'cobel_cima.png'
COBEL_ESQUERDA = 'cobel_esquerda.png'
COBEL_DIREITA = 'cobel_direita.png'
MILCHICK_BAIXO = 'milchick_baixo.png'
MILCHICK_CIMA = 'milchick_cima.png'
MILCHICK_ESQUERDA = 'milchick_esquerda.png'
MILCHICK_DIREITA = 'milchick_direita.png'
DRUMMOND_BAIXO = 'drummond_baixo.png'
DRUMMOND_CIMA = 'drummond_cima.png'
DRUMMOND_ESQUERDA = 'drummond_esquerda.png'
DRUMMOND_DIREITA = 'drummond_direita.png'
MAUER_BAIXO = 'mauer_baixo.png'
MAUER_CIMA = 'mauer_cima.png'
MAUER_ESQUERDA = 'mauer_esquerda.png'
MAUER_DIREITA = 'mauer_direita.png'
HUANG_BAIXO = 'huang_baixo.png'
HUANG_CIMA = 'huang_cima.png'
HUANG_ESQUERDA = 'huang_esquerda.png'
HUANG_DIREITA = 'huang_direita.png'

SPRITESHEET = os.path.join('ideias de imagens', 'spritesheet.png') # checar uso
RUPTURA_START_LOGO = 'ruptura_logo.png'
GAME_OVER_IMG = 'game_over_vertical.png'

FONTE = 'arial'