# classes/mark.py
import pygame
import constants
import mapa
import os

class Mark(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # Carrega a imagem do Mark
        self.image = pygame.image.load(constants.MARK_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        self.rect = self.image.get_rect()

        # Posição e Velocidade
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)
        self.velocidade = constants.VELOCIDADE_JOGADOR
        
        # Sistema de Fila de Comandos
        self.dx, self.dy = 1, 0  # Direção ATUAL (começa andando para a direita)
        self.proximos_movimentos = [] # A fila de comandos do jogador

    def adicionar_movimento(self, dx=0, dy=0):
        """Adiciona um novo movimento à fila com um carimbo de tempo."""
        timestamp = pygame.time.get_ticks()
        self.proximos_movimentos.append({'dx': dx, 'dy': dy, 'tempo': timestamp})

    def pode_mover(self, dx, dy):
        """Verifica se o próximo bloco na direção desejada é um piso."""
        # Calcula a posição do centro do PRÓXIMO bloco na grade
        proximo_x_grid = (self.rect.centerx // constants.TAMANHO_BLOCO) + dx
        proximo_y_grid = (self.rect.centery // constants.TAMANHO_BLOCO) + dy
        
        # Verifica se a célula na grade é um piso
        if 0 <= proximo_y_grid < mapa.ALTURA_GRADE and 0 <= proximo_x_grid < mapa.LARGURA_GRADE:
            # CORRIGIDO: Usa mapa.PISO em vez de constants.PISO
            if self.game.mapa_do_jogo[proximo_y_grid][proximo_x_grid] == mapa.PISO:
                return True
        return False

    def update(self):
        """Atualiza a posição e a lógica de movimento a cada frame."""
        agora = pygame.time.get_ticks()

        # 1. Limpa comandos antigos da fila (com mais de 3 segundos)
        self.proximos_movimentos = [
            mov for mov in self.proximos_movimentos if agora - mov['tempo'] < constants.COMANDO_TIMEOUT
        ]

        # O jogador só pode mudar de direção quando estiver perfeitamente alinhado com a grade
        esta_alinhado_x = self.rect.x % constants.TAMANHO_BLOCO == 0
        esta_alinhado_y = self.rect.y % constants.TAMANHO_BLOCO == 0

        if esta_alinhado_x and esta_alinhado_y:
            # 2. Tenta executar o primeiro comando válido da fila
            comando_executado = False
            for i, comando in enumerate(self.proximos_movimentos):
                if self.pode_mover(comando['dx'], comando['dy']):
                    self.dx = comando['dx']
                    self.dy = comando['dy']
                    self.proximos_movimentos = self.proximos_movimentos[i+1:]
                    comando_executado = True
                    break
            
            # 3. Se nenhum comando da fila foi executado, verifica se pode continuar reto
            if not comando_executado:
                if not self.pode_mover(self.dx, self.dy):
                    # Se a direção atual está bloqueada, para
                    self.dx, self.dy = 0, 0

        # Define a velocidade com base na direção final
        vx = self.dx * self.velocidade
        vy = self.dy * self.velocidade

        # Move o jogador
        self.rect.x += vx
        self.rect.y += vy