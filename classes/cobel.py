import pygame
import constants
import mapa
import os
import random
#import mark

class Cobel(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # Carrega a imagem do Cobel
        self.sprites = { 
        'cima': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_CIMA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
        'baixo': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_BAIXO)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
        'esquerda': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_ESQUERDA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
        'direita': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_DIREITA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))}
        self.image = self.sprites['baixo']
        self.rect = self.image.get_rect()

        # Posição inicial
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)
        
        # Velocidade de movimento (mais lenta que o jogador)
        self.velocidade = constants.VELOCIDADE_COBEL
        
        # Timer para movimento
        self.ultimo_movimento = pygame.time.get_ticks()
        self.intervalo_movimento = 300  # Move a cada 300ms

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

        direcoes = []

        # Movimentos possíveis
        movimentos = [
            (1, 0),   # direita
            (-1, 0),  # esquerda
            (0, 1),   # baixo
            (0, -1),  # cima
        ]

        # Calcula distância para o Mark em cada direção
        opcoes = []
        for dx, dy in movimentos:
            nx, ny = cobel_x + dx, cobel_y + dy
            if self.pode_mover(dx, dy):
                distancia = abs(jogador_x - nx) + abs(jogador_y - ny)
                opcoes.append(((dx, dy), distancia))

        # Prioriza a direção que mais aproxima do Mark
        if opcoes:
            opcoes.sort(key=lambda x: x[1])
            return opcoes[0][0]  # Retorna o movimento que mais aproxima
        else:
            return (0, 0)  # Fica parado se não pode se mover

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

            # Atualiza a imagem da Cobel de acordo com a direção
            if dx == 1: self.image = self.sprites['direita']
            elif dx == -1: self.image = self.sprites['esquerda']
            elif dy == -1: self.image = self.sprites['cima']
            elif dy == 1: self.image = self.sprites['baixo']

    def causar_dano(self):
        # CAUSA DANO AO JOGADOR QUANDO HÁ COLISÃO
        self.game.vidas -= 2
        if self.game.vidas < 0:
            self.game.vidas = 0
        print(f"Cobel atacou! Vidas restantes: {self.game.vidas}")