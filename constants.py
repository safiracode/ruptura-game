# constants.py
import os

# Dimensões da tela
LARGURA = 480
ALTURA = 600
TAMANHO_BLOCO = 24

# Título do jogo
TITULO_JOGO = 'Ruptura'

# FPS
FPS = 60 # Aumentei o FPS para um movimento mais suave

VIDAS_INICIAIS = 5

# --- JOGADOR ---
VELOCIDADE_JOGADOR = 3 # Velocidade do Mark em pixels por frame
COR_JOGADOR = (255, 255, 0) # Amarelo (para testes)

# --- CORES EM RGB ---
PRETO = (0, 0, 0)
VERDE = (35, 115, 80)
BRANCO = (255, 255, 255)

# --- ARQUIVOS ---
# (Caminhos dos arquivos de imagem)
BALAO = 'balão.png'
CAFE = 'café.png'
PAREDE = 'parede3.png'
MARK_IMG = os.path.join('ideias de imagens', 'mark-head.png') # Renomeado para clareza

FONTE = 'arial'