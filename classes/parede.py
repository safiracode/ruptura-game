import pygame
import constants

class Parede(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # A parede para colisão não precisa de uma imagem,
        # apenas de um retângulo (rect) na posição correta.
        self.rect = pygame.Rect(x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO,
                                constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)