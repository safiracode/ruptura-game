# classes/chave.py
import pygame
import constants

class ChaveParte(pygame.sprite.Sprite):
    # REPRESENTA UM PEDAÇO DA CHAVE
    def __init__(self, x, y, parte_index, imagem_da_parte):
        super().__init__()
        
        # Guarda qual parte da chave esta sprite representa (0, 1 ou 2)
        self.parte_index = parte_index
        
        # Usa a imagem que foi cortada e enviada pelo main.py
        self.image = imagem_da_parte
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)