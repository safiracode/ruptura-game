import pygame
import constants
import os

class Balao(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Passo 1: Inicia a classe "Sprite" original do Pygame
        super().__init__()
        
        # Passo 2: Define a aparência (self.image)
        # Constrói o caminho completo para o arquivo de imagem
        caminho_imagem = os.path.join('imagens', constants.BALAO)
        # Carrega a imagem e mantém a transparência
        self.image = pygame.image.load(caminho_imagem).convert_alpha()
        # Redimensiona a imagem para ter o mesmo tamanho de um bloco do mapa
        self.image = pygame.transform.scale(self.image, (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))

        # Passo 3: Define a posição e o tamanho (self.rect)
        # Cria um retângulo com as dimensões da imagem
        self.rect = self.image.get_rect()
        # Posiciona o canto superior esquerdo do retângulo na coordenada de pixel correta
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)