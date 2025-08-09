import pygame
import constants
import os

class Balao(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Passo 1: Inicia a classe "Sprite" original do Pygame
        super().__init__()
        
        caminho_imagem = os.path.join('imagens', constants.BALAO)
        # Carrega a imagem e mantém a transparência
        self.image = pygame.image.load(caminho_imagem).convert_alpha()

        # Passo 3: Define a posição e o tamanho (self.rect)
        # Cria um retângulo com as dimensões da imagem
        self.rect = self.image.get_rect()
        # Posiciona o canto superior esquerdo do retângulo na coordenada de pixel correta
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)