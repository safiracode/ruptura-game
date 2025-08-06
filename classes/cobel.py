import pygame
import constants
import mapa
import os
import random

class Cobel(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # Carrega a imagem do Cobel
        self.image = pygame.image.load(os.path.join('imagens', constants.COBEL_BAIXO)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        self.rect = self.image.get_rect()

        # Posição inicial
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)
        
        # Velocidade de movimento (mais lenta que o jogador)
        self.velocidade = 1
        
        # Timer para movimento
        self.ultimo_movimento = pygame.time.get_ticks()
        self.intervalo_movimento = 500  # Move a cada 500ms

    def pode_mover(self, dx, dy):
        # VERIFICA SE PODE MOVER PARA POSIÇÃO ESPECIFICADA
        novo_x_grid = (self.rect.centerx // constants.TAMANHO_BLOCO) + dx
        novo_y_grid = (self.rect.centery // constants.TAMANHO_BLOCO) + dy
        
        if 0 <= novo_y_grid < mapa.ALTURA_GRADE and 0 <= novo_x_grid < mapa.LARGURA_GRADE:
            return self.game.mapa_do_jogo[novo_y_grid][novo_x_grid] == mapa.PISO
        return False

    def encontrar_direcao_para_jogador(self):
        # ENCONTRA A DIREÇÃO PARA SE MOVER EATÉ O JOGADOR
        jogador_x = self.game.jogador.rect.centerx // constants.TAMANHO_BLOCO
        jogador_y = self.game.jogador.rect.centery // constants.TAMANHO_BLOCO
        cobel_x = self.rect.centerx // constants.TAMANHO_BLOCO
        cobel_y = self.rect.centery // constants.TAMANHO_BLOCO

        # Lista de possíveis direções
        direcoes = []
        
        # Prioriza movimento horizontal se há diferença significativa
        if abs(jogador_x - cobel_x) > abs(jogador_y - cobel_y):
            if jogador_x > cobel_x and self.pode_mover(1, 0):
                direcoes.append((1, 0))
            elif jogador_x < cobel_x and self.pode_mover(-1, 0):
                direcoes.append((-1, 0))
        else:
            # Prioriza movimento vertical
            if jogador_y > cobel_y and self.pode_mover(0, 1):
                direcoes.append((0, 1))
            elif jogador_y < cobel_y and self.pode_mover(0, -1):
                direcoes.append((0, -1))

        # Se não conseguiu se mover na direção preferida, tenta outras
        if not direcoes:
            movimentos_possiveis = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in movimentos_possiveis:
                if self.pode_mover(dx, dy):
                    direcoes.append((dx, dy))

        return random.choice(direcoes) if direcoes else (0, 0)

    def update(self):
        # ATUALIZA O MOVIMENTO DA COBEL
        agora = pygame.time.get_ticks()
        
        # Move apenas a cada intervalo definido
        if agora - self.ultimo_movimento > self.intervalo_movimento:
            dx, dy = self.encontrar_direcao_para_jogador()
            
            if dx != 0 or dy != 0:
                self.rect.x += dx * constants.TAMANHO_BLOCO
                self.rect.y += dy * constants.TAMANHO_BLOCO
                
            self.ultimo_movimento = agora

    def causar_dano(self):
        # CAUSA DANO AO JOGADOR QUANDO HÁ COLISÃO
        self.game.vidas -= 2
        if self.game.vidas < 0:
            self.game.vidas = 0
        print(f"Cobel atacou! Vidas restantes: {self.game.vidas}")