import pygame
import constants
import os

class Cafe(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        
        # Carrega a imagem do café
        caminho_imagem = os.path.join('imagens', constants.CAFE)
        self.image = pygame.image.load(caminho_imagem).convert_alpha()
        
        # Redimensiona a imagem para o tamanho de um bloco do mapa
        self.image = pygame.transform.scale(self.image, (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)

        #carrega o som do café
        caminho_som= os.path.join('audios', 'som_café.mp3')
        self.som_cafe= pygame.mixer.Sound(caminho_som)