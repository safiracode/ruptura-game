# main.py
import pygame
import constants
import mapa
import os
from classes import balao, mark, parede, cobel, chave, cafe
import random
import game_over, tela_start

class Game:
    def __init__(self):
        # INICIALIZA O JOGO E SUAS VARIAVEIS PRINCIPAIS
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((constants.LARGURA, constants.ALTURA))
        pygame.display.set_caption(constants.TITULO_JOGO)
        caminho_icone = os.path.join('imagens', 'ruptura_logo.png')
        ICONE = pygame.image.load(caminho_icone)
        pygame.display.set_icon(ICONE)
        self.relogio = pygame.time.Clock()
        self.esta_rodando = True
        self.fonte = pygame.font.match_font(constants.FONTE)
        self.carregar_arquivos()

    def novo_jogo(self):
        # CONFIGURA E INICIA UMA NOVA PARTIDA
        self.vidas = constants.VIDAS_INICIAIS
        self.partes_coletadas = [False] * constants.NUMERO_PARTES_CHAVE
        self.proxima_parte_a_spawnar = 0
        self.mapa_do_jogo = mapa.gerar_mapa_aleatorio(mapa.LARGURA_GRADE, mapa.ALTURA_GRADE)
        
        # Grupos de Sprites
        self.todas_sprites = pygame.sprite.Group()
        self.grupo_vidas_extras = pygame.sprite.Group()
        self.grupo_paredes = pygame.sprite.Group()
        self.grupo_cobels = pygame.sprite.Group()
        self.grupo_chave_partes = pygame.sprite.Group()
        self.grupo_cafe = pygame.sprite.Group()

        # Posiciona jogador, paredes e encontra locais livres
        posicao_inicial_jogador = None
        self.posicoes_livres = []
        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                if celula == mapa.PAREDE:
                    self.grupo_paredes.add(parede.Parede(x, y))
                if celula == mapa.PISO:
                    self.posicoes_livres.append((x, y))
                    if posicao_inicial_jogador is None:
                        posicao_inicial_jogador = (x, y)
        
        self.jogador = mark.Mark(self, posicao_inicial_jogador[0], posicao_inicial_jogador[1])
        self.todas_sprites.add(self.jogador)

        # Spawna 1 cobel em posição aleatória
        if self.posicoes_livres:
            pos_x, pos_y = random.choice(self.posicoes_livres)
            novo_cobel = cobel.Cobel(self, pos_x, pos_y)
            self.todas_sprites.add(novo_cobel); self.grupo_cobels.add(novo_cobel)

        self.agendar_proximo_spawn_balao()
        self.timer_spawn_chave = pygame.time.get_ticks() + constants.TIMER_INICIAL_CHAVE
        self.agendar_proximo_spawn_cafe() # Agenda o primeiro café
        
        self.rodar()
    
    def rodar(self):
        # CONTROLA O LOOP PRINCIPAL DO JOGO
        self.jogando = True
        while self.jogando:
            self.relogio.tick(constants.FPS)
            self.eventos(); self.atualizar_sprites(); self.desenhar_sprites()
            if self.vidas <= 0: self.jogando = False

    def eventos(self):
        # PROCESSA TODOS OS EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.jogando: self.jogando = False
                self.esta_rodando = False
            
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]: self.jogador.adicionar_movimento(dx=-1, dy=0)
                if event.key in [pygame.K_RIGHT, pygame.K_d]: self.jogador.adicionar_movimento(dx=1, dy=0)
                if event.key in [pygame.K_UP, pygame.K_w]: self.jogador.adicionar_movimento(dx=0, dy=-1)
                if event.key in [pygame.K_DOWN, pygame.K_s]: self.jogador.adicionar_movimento(dx=0, dy=1)

    def atualizar_sprites(self):
            # ATUALIZA O ESTADO DE TODAS AS SPRITES
            self.checar_spawn_balao()
            self.checar_spawn_chave()
            self.checar_spawn_cafe()
            self.checar_efeito_cafe()
            self.todas_sprites.update()

            if self.jogador:
                # Colisão com o balão de vida
                if pygame.sprite.spritecollide(self.jogador, self.grupo_vidas_extras, True):
                    self.vidas += 1
                    if self.vidas > constants.VIDAS_INICIAIS: self.vidas = constants.VIDAS_INICIAIS
                
                # Colisão com as PARTES da chave
                partes_colididas = pygame.sprite.spritecollide(self.jogador, self.grupo_chave_partes, True)
                for parte in partes_colididas:
                    self.partes_coletadas[parte.parte_index] = True
                    self.proxima_parte_a_spawnar += 1
                    if self.proxima_parte_a_spawnar < constants.NUMERO_PARTES_CHAVE: self.agendar_proxima_chave()
                
                # Colisão com o Café
                if pygame.sprite.spritecollide(self.jogador, self.grupo_cafe, True):
                    self.ativar_efeito_cafe()

                # --- LÓGICA DE COLISÃO COM 50% DE SOBREPOSIÇÃO ---
                # Primeiro, pega a lista de todos os seguranças que estão tocando no jogador
                colisoes_potenciais = pygame.sprite.spritecollide(self.jogador, self.grupo_cobels, False)
                for inimigo in colisoes_potenciais:
                    # Calcula a área do retângulo do jogador
                    area_jogador = self.jogador.rect.width * self.jogador.rect.height
                    
                    # Encontra o retângulo exato da sobreposição
                    rect_intersecao = self.jogador.rect.clip(inimigo.rect)
                    
                    # Calcula a área da sobreposição
                    area_intersecao = rect_intersecao.width * rect_intersecao.height
                    
                    # Verifica se a área de sobreposição é de pelo menos 50%
                    if area_intersecao >= (area_jogador * 0.3):
                        # Se for, aplica a lógica de dano
                        if not self.jogador.invencivel:
                            self.vidas = 0 # Game Over, como a Cobel é a chefona
                            break # Sai do loop, pois o jogo já acabou

    def desenhar_sprites(self):
        # DESENHA TODOS OS ELEMENTOS NA TELA
        self.tela.fill(constants.PRETO)

        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                pos_x = x * constants.TAMANHO_BLOCO; pos_y = y * constants.TAMANHO_BLOCO
                if celula == mapa.PAREDE: self.tela.blit(self.imagem_parede, (pos_x, pos_y))
                elif celula == mapa.PISO: pygame.draw.rect(self.tela, constants.VERDE, (pos_x, pos_y, constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        
        self.todas_sprites.draw(self.tela)

        # Desenha a HUD
        pos_y_interface = constants.ALTURA - (mapa.ALTURA_INTERFACE_INFERIOR // 2)
        for i in range(self.vidas):
             self.tela.blit(self.imagem_balao_vida, (20 + i * 35, pos_y_interface - 15))
        
        # Lógica para desenhar o café na HUD com a opacidade correta
        if self.jogador.invencivel:
            self.tela.blit(self.imagem_xicara_cafe, (constants.LARGURA - 50, pos_y_interface - 15))
        else:
            self.tela.blit(self.imagem_xicara_cafe_opaca, (constants.LARGURA - 50, pos_y_interface - 15))
        
        largura_total_chave = self.imagem_chave_original.get_width()
        pos_x_chave_hud = (constants.LARGURA - largura_total_chave) // 2
        for i in range(constants.NUMERO_PARTES_CHAVE):
            if self.partes_coletadas[i]:
                imagem_da_parte = self.imagens_partes_chave[i]
                largura_parte = imagem_da_parte.get_width()
                self.tela.blit(imagem_da_parte, (pos_x_chave_hud + i * largura_parte, pos_y_interface - 20))

        pygame.display.flip()

    def carregar_arquivos(self):
        # CARREGA E CORTA OS ARQUIVOS NECESSARIOS
        diretorio_imagens = os.path.join(os.getcwd(), 'imagens')
        
        self.imagem_parede = pygame.image.load(os.path.join(diretorio_imagens, constants.PAREDE)).convert()
        self.imagem_balao_vida = pygame.image.load(os.path.join(diretorio_imagens, constants.BALAO)).convert_alpha()
        self.imagem_xicara_cafe = pygame.image.load(os.path.join(diretorio_imagens, constants.CAFE)).convert_alpha()
        self.imagem_game_over = pygame.image.load(os.path.join(diretorio_imagens, constants.GAME_OVER_IMG)).convert()
        
        # Prepara as duas versões do ícone do café para a HUD
        self.imagem_xicara_cafe_opaca = self.imagem_xicara_cafe.copy()
        self.imagem_xicara_cafe_opaca.set_alpha(100) # Opacidade baixa (0-255)

        self.imagem_chave_original = pygame.image.load(os.path.join(diretorio_imagens, constants.CHAVE)).convert_alpha()
        largura_chave, altura_chave = self.imagem_chave_original.get_size()
        largura_parte = largura_chave // constants.NUMERO_PARTES_CHAVE
        
        self.imagens_partes_chave = []
        for i in range(constants.NUMERO_PARTES_CHAVE):
            x_corte = i * largura_parte
            area_corte = pygame.Rect(x_corte, 0, largura_parte, altura_chave)
            imagem_cortada = self.imagem_chave_original.subsurface(area_corte)
            self.imagens_partes_chave.append(imagem_cortada)
    
    # --- Métodos de Lógica Específica ---

    # Métodos para controlar o café
    def agendar_proximo_spawn_cafe(self):
        intervalo = random.randint(constants.TIMER_MIN_CAFE, constants.TIMER_MAX_CAFE)
        self.timer_spawn_cafe = pygame.time.get_ticks() + intervalo
    def spawnar_cafe(self):
        if self.posicoes_livres:
            pos_x, pos_y = random.choice(self.posicoes_livres)
            novo_cafe = cafe.Cafe(pos_x, pos_y)
            self.todas_sprites.add(novo_cafe); self.grupo_cafe.add(novo_cafe)
    def checar_spawn_cafe(self):
        if len(self.grupo_cafe) > 0 or self.jogador.invencivel: return
        if pygame.time.get_ticks() >= self.timer_spawn_cafe:
            self.spawnar_cafe()
    def ativar_efeito_cafe(self):
        self.jogador.invencivel = True
        self.jogador.timer_efeito_cafe = pygame.time.get_ticks() + constants.DURACAO_EFEITO_CAFE
        self.agendar_proximo_spawn_cafe() # Agenda o próximo para depois que o efeito acabar
    def checar_efeito_cafe(self):
        if self.jogador.invencivel and pygame.time.get_ticks() > self.jogador.timer_efeito_cafe:
            self.jogador.invencivel = False

    def agendar_proxima_chave(self):
        intervalo = random.randint(constants.TIMER_MIN_CHAVE, constants.TIMER_MAX_CHAVE)
        self.timer_spawn_chave = pygame.time.get_ticks() + intervalo

    def spawnar_proxima_chave(self):
        if self.posicoes_livres:
            pos_x, pos_y = random.choice(self.posicoes_livres)
            
            parte_index = self.proxima_parte_a_spawnar
            imagem_da_parte = self.imagens_partes_chave[parte_index]
            
            nova_parte = chave.ChaveParte(pos_x, pos_y, parte_index, imagem_da_parte)
            self.todas_sprites.add(nova_parte)
            self.grupo_chave_partes.add(nova_parte)

    def checar_spawn_chave(self):
        if self.proxima_parte_a_spawnar >= constants.NUMERO_PARTES_CHAVE: return
        if len(self.grupo_chave_partes) > 0: return
        
        if pygame.time.get_ticks() >= self.timer_spawn_chave:
            self.spawnar_proxima_chave()

    def agendar_proximo_spawn_balao(self):
        intervalo = random.randint(5000, 20000); self.timer_spawn_balao = pygame.time.get_ticks() + intervalo
    def spawnar_balao(self):
        if self.posicoes_livres:
            pos_x, pos_y = random.choice(self.posicoes_livres)
            novo_balao = balao.Balao(pos_x, pos_y)
            self.todas_sprites.add(novo_balao); self.grupo_vidas_extras.add(novo_balao)
    def checar_spawn_balao(self):
        if self.vidas >= constants.VIDAS_INICIAIS or len(self.grupo_vidas_extras) > 0: return
        if pygame.time.get_ticks() >= self.timer_spawn_balao:
            self.spawnar_balao(); self.agendar_proximo_spawn_balao()
    def perder_vida(self):
        if self.vidas > 0: self.vidas -= 1
        self.agendar_proximo_spawn_balao()
    def mostrar_texto(self, texto, tamanho, cor, x, y):
        fonte = pygame.font.Font(self.fonte, tamanho)
        texto_render = fonte.render(texto, True, cor)
        texto_rect = texto_render.get_rect(); texto_rect.midtop = (x, y)
        self.tela.blit(texto_render, texto_rect)
        
    def tela_start(self):
        tela_start.mostrar_tela_start(
        tela=self.tela,
        fonte_path=self.fonte,
        largura=constants.LARGURA,
        altura=constants.ALTURA
    )
    def esperar_por_jogador(self):
        esperando = True
        while esperando:
            self.relogio.tick(constants.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False; self.esta_rodando = False
    def tela_game_over(self):
        return game_over.tela_game_over(self.tela, self.fonte, self.imagem_game_over)

# --- Inicialização e Loop Principal ---
g = Game()
g.tela_start()
while g.esta_rodando:
    g.novo_jogo()
    if g.vidas <= 0 and not g.tela_game_over():
        break
pygame.quit()