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
        
        self.caminho = []
        self.ultima_busca = 0
        self.intervalo_busca = random.randint(400, 600)
        
        # Lógica de Modos (Perseguir/Dispersar)
        self.modo = 'dispersar'
        # Define o tempo para a primeira mudança de modo
        self.tempo_mudanca_modo = pygame.time.get_ticks() + random.randint(constants.TEMPO_MIN_MODO, constants.TEMPO_MAX_MODO)

    def carregar_imagens(self):
        # ... (seu método carregar_imagens continua igual)
        self.imagens = {
            'cima': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_CIMA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'baixo': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_BAIXO)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'esquerda': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_ESQUERDA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO)),
            'direita': pygame.transform.scale(pygame.image.load(os.path.join('imagens', constants.COBEL_DIREITA)).convert_alpha(), (constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        }

    def encontrar_caminho(self, alvo_x, alvo_y):
        # ... (seu método encontrar_caminho continua igual)
        inicio = (int(self.rect.x // constants.TAMANHO_BLOCO), int(self.rect.y // constants.TAMANHO_BLOCO))
        fim = (int(alvo_x // constants.TAMANHO_BLOCO), int(alvo_y // constants.TAMANHO_BLOCO))
        fila = collections.deque([(inicio, [inicio])]); visitados = {inicio}
        while fila:
            (cx, cy), caminho_atual = fila.popleft()
            if (cx, cy) == fim:
                return caminho_atual[1:]
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < mapa.LARGURA_GRADE and 0 <= ny < mapa.ALTURA_GRADE and \
                   self.game.mapa_do_jogo[ny][nx] == mapa.PISO and (nx, ny) not in visitados:
                    visitados.add((nx, ny)); novo_caminho = list(caminho_atual); novo_caminho.append((nx, ny)); fila.append(((nx, ny), novo_caminho))
        return []

    def checar_colisao_e_parar(self, direcao):
        """Verifica colisões com as paredes e para o movimento se necessário."""
        colisoes = pygame.sprite.spritecollide(self, self.game.grupo_paredes, False)
        if colisoes:
            if direcao == 'x':
                if self.dx > 0: self.rect.right = colisoes[0].rect.left
                if self.dx < 0: self.rect.left = colisoes[0].rect.right
                self.x = self.rect.x
            if direcao == 'y':
                if self.dy > 0: self.rect.bottom = colisoes[0].rect.top
                if self.dy < 0: self.rect.top = colisoes[0].rect.bottom
                self.y = self.rect.y
            self.caminho = []
            
    def update(self):
        agora = pygame.time.get_ticks()

        # 1. Gerencia a mudança de modos (Perseguir/Dispersar)
        if agora > self.tempo_mudanca_modo:
            if self.modo == 'perseguir':
                self.modo = 'dispersar'
            else:
                self.modo = 'perseguir'
            # Agenda a próxima mudança para 20 a 30 segundos no futuro
            self.tempo_mudanca_modo = agora + random.randint(constants.TEMPO_MIN_MODO, constants.TEMPO_MAX_MODO)
            self.caminho = [] # Limpa o caminho antigo ao mudar de modo

        # 2. Decide o alvo e recalcula o caminho periodicamente
        if not self.caminho and agora - self.ultima_busca > self.intervalo_busca:
            self.ultima_busca = agora
            alvo = None
            if self.modo == 'perseguir':
                alvo = self.game.jogador.rect.center
            else: # modo 'dispersar'
                # Escolhe um ponto aleatório do mapa para andar
                pos_x_aleatoria = random.randint(1, mapa.LARGURA_GRADE - 2)
                pos_y_aleatoria = random.randint(1, mapa.ALTURA_GRADE - 2)
                alvo = (pos_x_aleatoria * constants.TAMANHO_BLOCO, pos_y_aleatoria * constants.TAMANHO_BLOCO)
            
            self.caminho = self.encontrar_caminho(alvo[0], alvo[1])

        # 3. Lógica para seguir o caminho
        if self.caminho:
            proximo_ponto_x = self.caminho[0][0] * constants.TAMANHO_BLOCO
            proximo_ponto_y = self.caminho[0][1] * constants.TAMANHO_BLOCO
            
            dist_x = proximo_ponto_x - self.rect.x
            dist_y = proximo_ponto_y - self.rect.y

            if abs(dist_x) < self.velocidade and abs(dist_y) < self.velocidade:
                self.caminho.pop(0)
            else:
                self.dx = 1 if dist_x > 0 else -1 if dist_x < 0 else 0
                self.dy = 1 if dist_y > 0 else -1 if dist_y < 0 else 0
        else:
            self.dx, self.dy = 0, 0

        # 4. Lógica de movimento e colisão
        vx = self.dx * self.velocidade
        vy = self.dy * self.velocidade

        self.x += vx
        self.rect.x = round(self.x)
        self.checar_colisao_e_parar('x')

        self.y += vy
        self.rect.y = round(self.y)
        self.checar_colisao_e_parar('y')
        
        # 5. Atualiza a animação
        if self.dx == 1: self.image = self.imagens['direita']
        elif self.dx == -1: self.image = self.imagens['esquerda']
        elif self.dy == 1: self.image = self.imagens['baixo']
        elif self.dy == -1: self.image = self.imagens['cima']