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
MARK_BAIXO = 'mark_baixo.png'
MARK_CIMA = 'mark_bxx.png'
MARK_ESQUERDA = 'mark_esquerda.png'
MARK_DIREITA = 'mark_direita.png'
COBEL = 'cobel_baixo.png'
MILCHICK = 'milchick_baixo.png'
DRUMMOND = 'drummond_baixo.png'
CHAVE_INTEIRA = 'chave_inteira.png'
CHAVE_PARTE1 = 'chave_parte_1.png'
CHAVE_PARTE2 = 'chave_parte_2.png'
CHAVE_PARTE3 = 'chave_parte_3.png'
SPRITESHEET = os.path.join('ideias de imagens', 'spritesheet.png') # checar uso
RUPTURA_START_LOGO = 'ruptura_logo.png'

FONTE = 'arial'