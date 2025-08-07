import pygame
import constants
import mapa
import os
import random

class Mark(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # Carrega as imagens do Mark
        self.sprites = { 
        'cima': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MARK_CIMA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
        'baixo': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MARK_BAIXO)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
        'esquerda': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MARK_ESQUERDA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
        'direita': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MARK_DIREITA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))}
        
        self.image_base = self.sprites['baixo'] # Guarda a imagem original da direção
        self.image = self.image_base.copy() # A imagem que será desenhada
        self.rect = self.image.get_rect()

        # Posição e Velocidade
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)
        self.velocidade = constants.VELOCIDADE_JOGADOR
        self.x = float(self.rect.x); self.y = float(self.rect.y)
        
        # Sistema de Fila de Comandos
        self.dx, self.dy = 0, 0
        self.proximos_movimentos = []

        # Estado do jogador
        self.invencivel = False
        self.timer_efeito_cafe = 0

    def adicionar_movimento(self, dx=0, dy=0):
        timestamp = pygame.time.get_ticks()
        self.proximos_movimentos.append({'dx': dx, 'dy': dy, 'tempo': timestamp})

    def pode_mover(self, dx, dy):
        proximo_x_grid = (self.rect.centerx // constants.TAMANHO_BLOCO) + dx
        proximo_y_grid = (self.rect.centery // constants.TAMANHO_BLOCO) + dy
        if 0 <= proximo_y_grid < mapa.ALTURA_GRADE and 0 <= proximo_x_grid < mapa.LARGURA_GRADE:
            if self.game.mapa_do_jogo[proximo_y_grid][proximo_x_grid] == mapa.PISO:
                return True
        return False

    def update(self):
        agora = pygame.time.get_ticks()
        self.proximos_movimentos = [mov for mov in self.proximos_movimentos if agora - mov['tempo'] < constants.COMANDO_TIMEOUT]

        esta_alinhado_x = self.rect.x % constants.TAMANHO_BLOCO == 0
        esta_alinhado_y = self.rect.y % constants.TAMANHO_BLOCO == 0

        if esta_alinhado_x and esta_alinhado_y:
            comando_executado = False
            for i, comando in enumerate(self.proximos_movimentos):
                if self.pode_mover(comando['dx'], comando['dy']):
                    self.dx = comando['dx']; self.dy = comando['dy']
                    self.proximos_movimentos = self.proximos_movimentos[i+1:]
                    comando_executado = True
                    break
            if not comando_executado and not self.pode_mover(self.dx, self.dy):
                self.dx, self.dy = 0, 0

        # Atualiza a imagem base do Mark de acordo com a direção
        if self.dx == 1: self.image_base = self.sprites['direita']
        elif self.dx == -1: self.image_base = self.sprites['esquerda']
        elif self.dy == -1: self.image_base = self.sprites['cima']
        elif self.dy == 1: self.image_base = self.sprites['baixo']

        # Efeito de brilho se estiver invencível
        if self.invencivel:
            self.image = self.image_base.copy()
            # Pisca a cada 200ms
            if (agora // 200) % 2 == 0:
                self.image.set_alpha(150) # Deixa semi-transparente
            else:
                self.image.set_alpha(255) # Opacidade normal
        else:
            self.image = self.image_base

        vx = self.dx * self.velocidade; vy = self.dy * self.velocidade
        self.x += vx; self.y += vy
        self.rect.x = round(self.x); self.rect.y = round(self.y)