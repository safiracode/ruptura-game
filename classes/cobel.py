import pygame
import constants
import mapa
import os
import random
import math

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
        self.velocidade = constants.VELOCIDADE_SEGURANCA
        
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
        # ENCONTRA A DIREÇÃO PARA SE MOVER ATÉ O JOGADOR USANDO DISTÂNCIA EUCLIDIANA
        jogador_x = self.game.jogador.rect.centerx // constants.TAMANHO_BLOCO
        jogador_y = self.game.jogador.rect.centery // constants.TAMANHO_BLOCO
        cobel_x = self.rect.centerx // constants.TAMANHO_BLOCO
        cobel_y = self.rect.centery // constants.TAMANHO_BLOCO

        # Descobre a direção anterior (para não voltar)
        if hasattr(self, 'ultimo_dx') and hasattr(self, 'ultimo_dy'):
            ultimo_dx, ultimo_dy = self.ultimo_dx, self.ultimo_dy
        else:
            ultimo_dx, ultimo_dy = 0, 0

        # Direções possíveis: cima, esquerda, baixo, direita (ordem de prioridade)
        direcoes = [ (0, -1), (-1, 0), (0, 1), (1, 0) ]

        # Descobre a direção "em frente" (igual à última direção)
        if ultimo_dx != 0 or ultimo_dy != 0:
            frente = (ultimo_dx, ultimo_dy)
            idx_frente = direcoes.index(frente) if frente in direcoes else None
        else:
            idx_frente = None

        opcoes = []
        for i, (dx, dy) in enumerate(direcoes):
            # Não pode voltar para trás (180 graus)
            if (dx, dy) == (-ultimo_dx, -ultimo_dy) and (ultimo_dx != 0 or ultimo_dy != 0):
                continue
            # Só pode ir para tiles livres
            if self.pode_mover(dx, dy):
                nx, ny = cobel_x + dx, cobel_y + dy
                distancia = math.hypot(jogador_x - nx, jogador_y - ny)
                # Prioridade: cima (0), esquerda (1), baixo (2), direita (3)
                prioridade = i
                opcoes.append( ((dx, dy), distancia, prioridade) )
            

        if not opcoes:
            print(opcoes)
            return (0, 0)

        # Escolhe a opção com menor distância, depois maior prioridade
        opcoes.sort(key=lambda x: (x[1], x[2]))
        melhor_dx, melhor_dy = opcoes[0][0]

        # Salva a última direção para a próxima decisão
        self.ultimo_dx, self.ultimo_dy = melhor_dx, melhor_dy

        return melhor_dx, melhor_dy

    def update(self):
        # Verifica se está em movimento
        if hasattr(self, 'destino'):
            dx = self.destino[0] - self.rect.x
            dy = self.destino[1] - self.rect.y

            if dx != 0:
                passo = self.velocidade if dx > 0 else -self.velocidade
                self.rect.x += passo
                if abs(self.rect.x - self.destino[0]) < self.velocidade:
                    self.rect.x = self.destino[0]
            elif dy != 0:
                passo = self.velocidade if dy > 0 else -self.velocidade
                self.rect.y += passo
                if abs(self.rect.y - self.destino[1]) < self.velocidade:
                    self.rect.y = self.destino[1]

            # Chegou ao destino
            if self.rect.topleft == self.destino:
                del self.destino

        else:
            # Só escolhe nova direção se estiver exatamente no centro de um bloco
            if self.rect.x % constants.TAMANHO_BLOCO == 0 and self.rect.y % constants.TAMANHO_BLOCO == 0:
                dx, dy = self.encontrar_direcao_para_jogador()

                if dx != 0 or dy != 0:
                    self.destino = (
                        self.rect.x + dx * constants.TAMANHO_BLOCO,
                        self.rect.y + dy * constants.TAMANHO_BLOCO
                    )

                    # Atualiza sprite
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