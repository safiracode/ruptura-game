# classes/cobel.py
import pygame
import constants
import mapa
import os
import collections
import random

class Cobel(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        
        self.carregar_imagens()
        self.image = self.imagens['baixo']
        self.rect = self.image.get_rect()

        self.velocidade = constants.VELOCIDADE_SEGURANCA
        self.rect.topleft = (x * constants.TAMANHO_BLOCO, y * constants.TAMANHO_BLOCO)
        self.x = float(self.rect.x); self.y = float(self.rect.y)
        
        self.dx, self.dy = 0, 0
        self.definir_direcao_aleatoria()
        
        self.modo = 'dispersar'
        self.tempo_mudanca_modo = pygame.time.get_ticks() + random.randint(constants.TEMPO_MIN_MODO, constants.TEMPO_MAX_MODO)

    def carregar_imagens(self):
        self.imagens = {
            'cima': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_CIMA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'baixo': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_BAIXO)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'esquerda': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_ESQUERDA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'direita': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_DIREITA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        }

    def eh_piso(self, x, y):
        """Verifica se uma coordenada da GRADE é um piso."""
        if 0 <= y < mapa.ALTURA_GRADE and 0 <= x < mapa.LARGURA_GRADE:
            return self.game.mapa_do_jogo[y][x] == mapa.PISO
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
        agora = pygame.time.get_ticks()

        # Gerencia a mudança de modos
        if agora > self.tempo_mudanca_modo:
            self.modo = 'dispersar' if self.modo == 'perseguir' else 'perseguir'
            self.tempo_mudanca_modo = agora + random.randint(constants.TEMPO_MIN_MODO, constants.TEMPO_MAX_MODO)

        # A decisão só acontece quando a Cobel está alinhada com a grade
        esta_alinhado_x = self.rect.centerx % constants.TAMANHO_BLOCO == constants.TAMANHO_BLOCO // 2
        esta_alinhado_y = self.rect.centery % constants.TAMANHO_BLOCO == constants.TAMANHO_BLOCO // 2

        if esta_alinhado_x and esta_alinhado_y:
            grid_x = self.rect.centerx // constants.TAMANHO_BLOCO
            grid_y = self.rect.centery // constants.TAMANHO_BLOCO
            
            # Verifica os caminhos possíveis (não pode voltar, a menos que seja um beco sem saída)
            caminhos_possiveis = []
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if self.eh_piso(grid_x + dx, grid_y + dy):
                    if not (dx == -self.dx and dy == -self.dy):
                        caminhos_possiveis.append((dx, dy))

            if not caminhos_possiveis:
                caminhos_possiveis.append((-self.dx, -self.dy))

            # Se está numa interseção (mais de um caminho possível), toma uma decisão
            if len(caminhos_possiveis) > 1:
                
                # --- LÓGICA DE ALVO CORRIGIDA ---
                distancia_jogador = abs(self.rect.centerx - self.game.jogador.rect.centerx) + abs(self.rect.centery - self.game.jogador.rect.centery)
                alvo_x, alvo_y = None, None

                # Prioridade 1: Jogador está perto? Persegue, não importa o modo.
                if distancia_jogador <= constants.DISTANCIA_SEGURA * constants.TAMANHO_BLOCO:
                    alvo_x, alvo_y = self.game.jogador.rect.center
                
                # Prioridade 2: Qual o modo atual?
                elif self.modo == 'perseguir':
                    alvo_x, alvo_y = self.game.jogador.rect.center
                
                elif self.modo == 'dispersar':
                    # No modo dispersar, o alvo é um canto aleatório
                    canto_x, canto_y = random.choice([(1,1), (mapa.LARGURA_GRADE-2, 1), (1, mapa.ALTURA_GRADE-2), (mapa.LARGURA_GRADE-2, mapa.ALTURA_GRADE-2)])
                    alvo_x = canto_x * constants.TAMANHO_BLOCO
                    alvo_y = canto_y * constants.TAMANHO_BLOCO
                # --- FIM DA LÓGICA DE ALVO ---

                # Encontra o melhor caminho para o alvo definido
                melhor_caminho = (self.dx, self.dy) # Mantém a direção atual por padrão
                menor_distancia = float('inf')

                for dx, dy in caminhos_possiveis:
                    dist = abs((grid_x + dx) * constants.TAMANHO_BLOCO - alvo_x) + abs((grid_y + dy) * constants.TAMANHO_BLOCO - alvo_y)
                    if dist < menor_distancia:
                        menor_distancia = dist
                        melhor_caminho = (dx, dy)
                
                self.dx, self.dy = melhor_caminho

            # Se só tem um caminho, segue reto
            elif len(caminhos_possiveis) == 1:
                self.dx, self.dy = caminhos_possiveis[0]

        # Lógica de movimento e colisão
        self.rect.x += self.dx * self.velocidade
        self.rect.y += self.dy * self.velocidade

        # Atualiza a animação
        if self.dx > 0: self.image = self.imagens['direita']
        elif self.dx < 0: self.image = self.imagens['esquerda']
        elif self.dy > 0: self.image = self.imagens['baixo']
        elif self.dy < 0: self.image = self.imagens['cima']