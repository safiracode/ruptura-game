import pygame
import os
import constants

class Mark(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tamanho_bloco):
        super().__init__()
        # caminho para a imagem do Mark
        caminho_imagem = os.path.join(constants.MARK)
        self.image = pygame.image.load(caminho_imagem).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tamanho_bloco, tamanho_bloco))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def mover(self, direcao, mapa, tamanho_bloco):
        dx, dy = 0, 0
        if direcao == 'esquerda':
            dx = -tamanho_bloco
        elif direcao == 'direita':
            dx = tamanho_bloco
        elif direcao == 'cima':
            dy = -tamanho_bloco
        elif direcao == 'baixo':
            dy = tamanho_bloco

        novo_x = self.rect.x + dx
        novo_y = self.rect.y + dy

        grid_x = novo_x // tamanho_bloco
        grid_y = novo_y // tamanho_bloco

        if 0 <= grid_y < len(mapa) and 0 <= grid_x < len(mapa[0]):
            if mapa[grid_y][grid_x] == 0:
                self.rect.x = novo_x
                self.rect.y = novo_y