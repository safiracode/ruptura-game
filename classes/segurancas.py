# classes/segurancas.py
import pygame
import constants
import mapa
import os
import collections
import random

# --- CLASSE MÃE (BASE PARA TODOS OS SEGURANÇAS) ---
class Seguranca(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = None
        self.rect = None
        
        self.velocidade = constants.VELOCIDADE_SEGURANCA
        self.x = float(x * constants.TAMANHO_BLOCO); self.y = float(y * constants.TAMANHO_BLOCO)
        self.dx, self.dy = 0, 0
        self.caminho = []
        self.ultima_busca = 0
        self.intervalo_busca = random.randint(450, 550)

    def encontrar_caminho(self, alvo_x, alvo_y):
        inicio = (self.rect.centerx // constants.TAMANHO_BLOCO, self.rect.centery // constants.TAMANHO_BLOCO)
        fim = (alvo_x // constants.TAMANHO_BLOCO, alvo_y // constants.TAMANHO_BLOCO)
        fila = collections.deque([[inicio]]); visitados = {inicio}
        while fila:
            caminho_atual = fila.popleft()
            x, y = caminho_atual[-1]
            if (x, y) == fim: return caminho_atual[1:]
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                prox_x, prox_y = x + dx, y + dy
                if (0 <= prox_x < mapa.LARGURA_GRADE and 0 <= prox_y < mapa.ALTURA_GRADE and
                    self.game.mapa_do_jogo[prox_y][prox_x] == mapa.PISO and
                    (prox_x, prox_y) not in visitados):
                    novo_caminho = list(caminho_atual); novo_caminho.append((prox_x, prox_y))
                    visitados.add((prox_x, prox_y)); fila.append(novo_caminho)
        return []
    
    def checar_colisao_e_parar(self, direcao):
        """Verifica colisões com as paredes e para o movimento."""
        colisoes = pygame.sprite.spritecollide(self, self.game.grupo_paredes, False)
        if colisoes:
            if direcao == 'x':
                if self.dx > 0: self.rect.right = colisoes[0].rect.left
                if self.dx < 0: self.rect.left = colisoes[0].rect.right
                self.x = self.rect.x; self.dx = 0
            if direcao == 'y':
                if self.dy > 0: self.rect.bottom = colisoes[0].rect.top
                if self.dy < 0: self.rect.top = colisoes[0].rect.bottom
                self.y = self.rect.y; self.dy = 0
            self.caminho = []

    def update(self):
        """Move o segurança e atualiza sua imagem direcional."""
        agora = pygame.time.get_ticks()
        if agora - self.ultima_busca > self.intervalo_busca:
            self.ultima_busca = agora
            alvo_x, alvo_y = self.encontrar_alvo()
            self.caminho = self.encontrar_caminho(alvo_x, alvo_y)

        if self.caminho:
            proximo_passo = self.caminho[0]
            proximo_x_pixel = proximo_passo[0] * constants.TAMANHO_BLOCO
            proximo_y_pixel = proximo_passo[1] * constants.TAMANHO_BLOCO
            if abs(proximo_x_pixel - self.rect.x) < self.velocidade and abs(proximo_y_pixel - self.rect.y) < self.velocidade:
                 self.caminho.pop(0)
            else:
                if proximo_x_pixel > self.rect.x: self.dx, self.dy = 1, 0
                elif proximo_x_pixel < self.rect.x: self.dx, self.dy = -1, 0
                elif proximo_y_pixel > self.rect.y: self.dx, self.dy = 0, 1
                elif proximo_y_pixel < self.rect.y: self.dx, self.dy = 0, -1
        else: self.dx, self.dy = 0, 0
        
        if self.dx == 1: self.image = self.sprites['direita']
        elif self.dx == -1: self.image = self.sprites['esquerda']
        elif self.dy == -1: self.image = self.sprites['cima']
        elif self.dy == 1: self.image = self.sprites['baixo']

        vx = self.dx * self.velocidade; vy = self.dy * self.velocidade
        self.x += vx; self.rect.x = round(self.x); self.checar_colisao_e_parar('x')
        self.y += vy; self.rect.y = round(self.y); self.checar_colisao_e_parar('y')

# --- CLASSES FILHAS (CADA UMA COM SUA PERSONALIDADE E IMAGENS) ---

class Milchick(Seguranca): # Blinky
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.canto_dispersao = ((mapa.LARGURA_GRADE - 2) * constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO) # Canto superior direito
        self.sprites = {
            'cima': pygame.image.load(os.path.join('imagens', constants.MILCHICK_CIMA)).convert_alpha(),
            'baixo': pygame.image.load(os.path.join('imagens', constants.MILCHICK_BAIXO)).convert_alpha(),
            'esquerda': pygame.image.load(os.path.join('imagens', constants.MILCHICK_ESQUERDA)).convert_alpha(),
            'direita': pygame.image.load(os.path.join('imagens', constants.MILCHICK_DIREITA)).convert_alpha()
        }
        self.image = self.sprites['baixo']
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def encontrar_alvo(self):
        return self.game.jogador.rect.center

class Huang(Seguranca): # Pinky
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.canto_dispersao = (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO) # Canto superior esquerdo
        self.sprites = {
            'cima': pygame.image.load(os.path.join('imagens', constants.HUANG_CIMA)).convert_alpha(),
            'baixo': pygame.image.load(os.path.join('imagens', constants.HUANG_BAIXO)).convert_alpha(),
            'esquerda': pygame.image.load(os.path.join('imagens', constants.HUANG_ESQUERDA)).convert_alpha(),
            'direita': pygame.image.load(os.path.join('imagens', constants.HUANG_DIREITA)).convert_alpha()
        }
        self.image = self.sprites['baixo']
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def encontrar_alvo(self):
        alvo_x = self.game.jogador.rect.centerx + (self.game.jogador.dx * 4 * constants.TAMANHO_BLOCO)
        alvo_y = self.game.jogador.rect.centery + (self.game.jogador.dy * 4 * constants.TAMANHO_BLOCO)
        return (alvo_x, alvo_y)

class Drummond(Seguranca): # Inky
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.canto_dispersao = ((mapa.LARGURA_GRADE - 2) * constants.TAMANHO_BLOCO, (mapa.ALTURA_GRADE - 2) * constants.TAMANHO_BLOCO) # Canto inferior direito
        self.sprites = {
            'cima': pygame.image.load(os.path.join('imagens', constants.DRUMMOND_CIMA)).convert_alpha(),
            'baixo': pygame.image.load(os.path.join('imagens', constants.DRUMMOND_BAIXO)).convert_alpha(),
            'esquerda': pygame.image.load(os.path.join('imagens', constants.DRUMMOND_ESQUERDA)).convert_alpha(),
            'direita': pygame.image.load(os.path.join('imagens', constants.DRUMMOND_DIREITA)).convert_alpha()
        }
        self.image = self.sprites['baixo']
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def encontrar_alvo(self):
        ponto_frente_x = self.game.jogador.rect.centerx + (self.game.jogador.dx * 2 * constants.TAMANHO_BLOCO)
        ponto_frente_y = self.game.jogador.rect.centery + (self.game.jogador.dy * 2 * constants.TAMANHO_BLOCO)
        
        milchick = next((s for s in self.game.grupo_segurancas if isinstance(s, Milchick)), None)
        if milchick:
            vetor_x = ponto_frente_x - milchick.rect.centerx
            vetor_y = ponto_frente_y - milchick.rect.centery
            return (ponto_frente_x + vetor_x, ponto_frente_y + vetor_y)
        return self.game.jogador.rect.center

class Mauer(Seguranca): # Clyde
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.canto_dispersao = (constants.TAMANHO_BLOCO, (mapa.ALTURA_GRADE - 2) * constants.TAMANHO_BLOCO) # Canto inferior esquerdo
        self.sprites = {
            'cima': pygame.image.load(os.path.join('imagens', constants.MAUER_CIMA)).convert_alpha(),
            'baixo': pygame.image.load(os.path.join('imagens', constants.MAUER_BAIXO)).convert_alpha(),
            'esquerda': pygame.image.load(os.path.join('imagens', constants.MAUER_ESQUERDA)).convert_alpha(),
            'direita': pygame.image.load(os.path.join('imagens', constants.MAUER_DIREITA)).convert_alpha()
        }
        self.image = self.sprites['baixo']
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def encontrar_alvo(self):
        distancia_total = abs(self.rect.centerx - self.game.jogador.rect.centerx) + abs(self.rect.centery - self.game.jogador.rect.centery)
        if distancia_total > 8 * constants.TAMANHO_BLOCO:
            return self.game.jogador.rect.center
        else:
            return self.canto_dispersao