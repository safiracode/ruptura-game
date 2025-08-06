# classes/mark.py
import pygame
import constants
import mapa
import os
import random

class Mark(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # Carrega a imagem do Mark
        self.sprites = { 
        'cima': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MARK_CIMA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
        'baixo': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MARK_BAIXO)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
        'esquerda': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MARK_ESQUERDA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
        'direita': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MARK_DIREITA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))}
        self.image = self.sprites['baixo']
        self.rect = self.image.get_rect()

        # Posição e Velocidade
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)
        self.velocidade = constants.VELOCIDADE_JOGADOR
        
        # Sistema de Fila de Comandos
        self.dx, self.dy = 0, 0  # ALTERADO: Direção ATUAL (começa PARADO)
        self.proximos_movimentos = []

    def adicionar_movimento(self, dx=0, dy=0):
        """Adiciona um novo movimento à fila com um carimbo de tempo."""
        timestamp = pygame.time.get_ticks()
        self.proximos_movimentos.append({'dx': dx, 'dy': dy, 'tempo': timestamp})

    def pode_mover(self, dx, dy):
        """Verifica se o próximo bloco na direção desejada é um piso."""
        proximo_x_grid = (self.rect.centerx // constants.TAMANHO_BLOCO) + dx
        proximo_y_grid = (self.rect.centery // constants.TAMANHO_BLOCO) + dy
        
        if 0 <= proximo_y_grid < mapa.ALTURA_GRADE and 0 <= proximo_x_grid < mapa.LARGURA_GRADE:
            if self.game.mapa_do_jogo[proximo_y_grid][proximo_x_grid] == mapa.PISO:
                return True
        return False

    def update(self):
        """Atualiza a posição e a lógica de movimento a cada frame."""
        agora = pygame.time.get_ticks()

        self.proximos_movimentos = [
            mov for mov in self.proximos_movimentos if agora - mov['tempo'] < constants.COMANDO_TIMEOUT
        ]

        esta_alinhado_x = self.rect.x % constants.TAMANHO_BLOCO == 0
        esta_alinhado_y = self.rect.y % constants.TAMANHO_BLOCO == 0

        if esta_alinhado_x and esta_alinhado_y:
            comando_executado = False
            for i, comando in enumerate(self.proximos_movimentos):
                if self.pode_mover(comando['dx'], comando['dy']):
                    self.dx = comando['dx']
                    self.dy = comando['dy']
                    self.proximos_movimentos = self.proximos_movimentos[i+1:]
                    comando_executado = True
                    break
            
            # Atualiza sprite conforme direção
            if self.dx == 1:
                self.image = self.sprites['direita']
            elif self.dx == -1:
                self.image = self.sprites['esquerda']
            elif self.dy == -1:
                self.image = self.sprites['cima']
            elif self.dy == 1:
                self.image = self.sprites['baixo']

            if not comando_executado:
                if not self.pode_mover(self.dx, self.dy):
                    self.dx, self.dy = 0, 0

        vx = self.dx * self.velocidade
        vy = self.dy * self.velocidade

        self.rect.x += vx
        self.rect.y += vy