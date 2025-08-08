# classes/porta.py
import pygame
import constants
import os

class Porta(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        caminho_imagem = os.path.join('imagens', constants.PORTA_SAIDA)
        self.image = pygame.image.load(caminho_imagem).convert_alpha()
        # Garante que a imagem tenha o tamanho correto
        self.image = pygame.transform.scale(self.image, (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        
        self.rect = self.image.get_rect()
        self.rect.x = x * constants.TAMANHO_BLOCO
        self.rect.y = y * constants.TAMANHO_BLOCO