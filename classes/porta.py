# porta.py
import pygame
import constants

class Porta(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.x = x * constants.TAMANHO_BLOCO
        self.rect.y = y * constants.TAMANHO_BLOCO