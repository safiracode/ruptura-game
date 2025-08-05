# classes/mark.py (Versão com movimento contínuo)
import pygame
import constants
import os

class Mark(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game # Referência à classe principal do jogo

        # Carrega a imagem do Mark
        self.image = pygame.image.load(constants.MARK_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        self.rect = self.image.get_rect()

        # Define a posição inicial e a velocidade (parado)
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)
        self.vx, self.vy = 0, 0
        self.velocidade = constants.VELOCIDADE_JOGADOR

    def mudar_direcao(self, dx=0, dy=0):
        """Muda a velocidade do jogador para a nova direção."""
        self.vx = dx * self.velocidade
        self.vy = dy * self.velocidade

    def checar_colisao_e_parar(self, direcao):
        """Verifica colisões com as paredes e para o movimento se necessário."""
        colisoes = pygame.sprite.spritecollide(self, self.game.grupo_paredes, False)
        if colisoes:
            if direcao == 'x':
                if self.vx > 0: self.rect.right = colisoes[0].rect.left
                if self.vx < 0: self.rect.left = colisoes[0].rect.right
                self.vx = 0 # Para o movimento horizontal
            if direcao == 'y':
                if self.vy > 0: self.rect.bottom = colisoes[0].rect.top
                if self.vy < 0: self.rect.top = colisoes[0].rect.bottom
                self.vy = 0 # Para o movimento vertical
    
    def update(self):
        """Atualiza a posição do jogador a cada frame, gerenciando o movimento contínuo."""
        # Move e checa colisão no eixo X
        self.rect.x += self.vx
        self.checar_colisao_e_parar('x')
        
        # Move e checa colisão no eixo Y
        self.rect.y += self.vy
        self.checar_colisao_e_parar('y')