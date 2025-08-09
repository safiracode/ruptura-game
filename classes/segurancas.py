# classes/segurancas.py
import pygame
import constants
import mapa
import os
import random

class Seguranca(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = None
        self.rect = None
        self.velocidade = constants.VELOCIDADE_SEGURANCA
        self.x = float(x * constants.TAMANHO_BLOCO)
        self.y = float(y * constants.TAMANHO_BLOCO)
        self.dx, self.dy = 0, 0
        self.canto_dispersao = (0, 0)

        # A IA agora começa com uma direção aleatória válida
        # self.rect é criado aqui para a função abaixo funcionar
        self.rect = pygame.Rect(self.x, self.y, constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)
        self.definir_direcao_aleatoria()

    def eh_piso(self, grid_x, grid_y):
        """Verifica se uma coordenada da GRADE é um piso."""
        if 0 <= grid_y < mapa.ALTURA_GRADE and 0 <= grid_x < mapa.LARGURA_GRADE:
            return self.game.mapa_do_jogo[grid_y][grid_x] == mapa.PISO
        return False

    def definir_direcao_aleatoria(self):
        """Escolhe uma nova direção aleatória que não seja uma parede."""
        direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(direcoes)
        for dx, dy in direcoes:
            grid_x = (self.rect.centerx // constants.TAMANHO_BLOCO) + dx
            grid_y = (self.rect.centery // constants.TAMANHO_BLOCO) + dy
            if self.eh_piso(grid_x, grid_y):
                self.dx, self.dy = dx, dy
                return

    def update(self):
        # A decisão de virar só acontece quando o segurança está perfeitamente alinhado no centro de um bloco
        esta_alinhado = (self.rect.centerx % constants.TAMANHO_BLOCO == constants.TAMANHO_BLOCO // 2 and
                        self.rect.centery % constants.TAMANHO_BLOCO == constants.TAMANHO_BLOCO // 2)

        if esta_alinhado:
            grid_x = self.rect.centerx // constants.TAMANHO_BLOCO
            grid_y = self.rect.centery // constants.TAMANHO_BLOCO
            
            # Verifica todos os caminhos possíveis, exceto voltar
            caminhos_possiveis = []
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if self.eh_piso(grid_x + dx, grid_y + dy):
                    if not (dx == -self.dx and dy == -self.dy):
                        caminhos_possiveis.append((dx, dy))

            if not caminhos_possiveis:
                caminhos_possiveis.append((-self.dx, -self.dy)) # Se for um beco sem saída, a única opção é voltar

            # Se está numa interseção (mais de um caminho), toma uma decisão inteligente
            if len(caminhos_possiveis) > 1:
                alvo_x, alvo_y = self.encontrar_alvo()
                
                # Encontra o melhor caminho para o alvo
                melhor_caminho = None
                menor_distancia = float('inf')
                for dx, dy in caminhos_possiveis:
                    dist = abs((grid_x + dx) * constants.TAMANHO_BLOCO - alvo_x) + abs((grid_y + dy) * constants.TAMANHO_BLOCO - alvo_y)
                    if dist < menor_distancia:
                        menor_distancia = dist
                        melhor_caminho = (dx, dy)
                self.dx, self.dy = melhor_caminho
            
            # Se só tem um caminho (corredor), segue reto
            elif len(caminhos_possiveis) == 1:
                self.dx, self.dy = caminhos_possiveis[0]

        # Lógica de movimento contínuo
        self.rect.x += self.dx * self.velocidade
        self.rect.y += self.dy * self.velocidade

        # Atualiza a animação
        if self.dx > 0: self.image = self.sprites['direita']
        elif self.dx < 0: self.image = self.sprites['esquerda']
        elif self.dy > 0: self.image = self.sprites['baixo']
        elif self.dy < 0: self.image = self.sprites['cima']

# --- CLASSES FILHAS (CADA UMA COM SUA PERSONALIDADE E IMAGENS) ---

class Milchick(Seguranca): # Blinky
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.canto_dispersao = ((mapa.LARGURA_GRADE - 2) * constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)
        self.sprites = {
            'cima': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MILCHICK_CIMA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'baixo': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MILCHICK_BAIXO)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'esquerda': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MILCHICK_ESQUERDA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'direita': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MILCHICK_DIREITA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        }
        self.image = self.sprites['baixo']; self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def encontrar_alvo(self):
        if self.game.modo_inimigo == 'perseguir': return self.game.jogador.rect.center
        else: return self.canto_dispersao

class Huang(Seguranca): # Pinky
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.canto_dispersao = (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)
        self.sprites = {
            'cima': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.HUANG_CIMA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'baixo': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.HUANG_BAIXO)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'esquerda': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.HUANG_ESQUERDA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'direita': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.HUANG_DIREITA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        }
        self.image = self.sprites['baixo']; self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def encontrar_alvo(self):
        distancia_jogador = abs(self.rect.centerx - self.game.jogador.rect.centerx) + abs(self.rect.centery - self.game.jogador.rect.centery)
        if distancia_jogador <= constants.DISTANCIA_SEGURA * constants.TAMANHO_BLOCO: return self.game.jogador.rect.center
        if self.game.modo_inimigo == 'perseguir':
            alvo_x = self.game.jogador.rect.centerx + (self.game.jogador.dx * 4 * constants.TAMANHO_BLOCO)
            alvo_y = self.game.jogador.rect.centery + (self.game.jogador.dy * 4 * constants.TAMANHO_BLOCO)
            return (alvo_x, alvo_y)
        else: return self.canto_dispersao

class Drummond(Seguranca): # Inky
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.canto_dispersao = ((mapa.LARGURA_GRADE - 2) * constants.TAMANHO_BLOCO, (mapa.ALTURA_GRADE - 2) * constants.TAMANHO_BLOCO)
        self.sprites = {
            'cima': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.DRUMMOND_CIMA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'baixo': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.DRUMMOND_BAIXO)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'esquerda': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.DRUMMOND_ESQUERDA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'direita': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.DRUMMOND_DIREITA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        }
        self.image = self.sprites['baixo']; self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def encontrar_alvo(self):
        distancia_jogador = abs(self.rect.centerx - self.game.jogador.rect.centerx) + abs(self.rect.centery - self.game.jogador.rect.centery)
        if distancia_jogador <= constants.DISTANCIA_SEGURA * constants.TAMANHO_BLOCO: return self.game.jogador.rect.center
        if self.game.modo_inimigo == 'perseguir':
            ponto_frente_x = self.game.jogador.rect.centerx + (self.game.jogador.dx * 2 * constants.TAMANHO_BLOCO)
            ponto_frente_y = self.game.jogador.rect.centery + (self.game.jogador.dy * 2 * constants.TAMANHO_BLOCO)
            milchick = next((s for s in self.game.grupo_segurancas if isinstance(s, Milchick)), None)
            if milchick:
                vetor_x = ponto_frente_x - milchick.rect.centerx; vetor_y = ponto_frente_y - milchick.rect.centery
                return (ponto_frente_x + vetor_x, ponto_frente_y + vetor_y)
            return self.game.jogador.rect.center
        else: return self.canto_dispersao

class Mauer(Seguranca): # Clyde
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.canto_dispersao = (constants.TAMANHO_BLOCO, (mapa.ALTURA_GRADE - 2) * constants.TAMANHO_BLOCO)
        self.sprites = {
            'cima': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MAUER_CIMA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'baixo': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MAUER_BAIXO)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'esquerda': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MAUER_ESQUERDA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'direita': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.MAUER_DIREITA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        }
        self.image = self.sprites['baixo']; self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def encontrar_alvo(self):
        distancia_jogador = abs(self.rect.centerx - self.game.jogador.rect.centerx) + abs(self.rect.centery - self.game.jogador.rect.centery)
        if distancia_jogador <= constants.DISTANCIA_SEGURA * constants.TAMANHO_BLOCO: return self.game.jogador.rect.center
        if self.game.modo_inimigo == 'perseguir':
            if distancia_jogador > 8 * constants.TAMANHO_BLOCO: return self.game.jogador.rect.center
            else: return self.canto_dispersao
        else: return self.canto_dispersao