import pygame
import constants
import mapa
import os
from classes import balao, mark, parede, cobel, chave, cafe, porta, segurancas
import random
import game_over
import tela_start
import tela_tutorial
import venceu

pygame.mixer.init()


class Game:
    def __init__(self):
        # INICIALIZA O JOGO E SUAS VARIAVEIS PRINCIPAIS
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('audios/música principal.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.tela = pygame.display.set_mode(
            (constants.LARGURA, constants.ALTURA))
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
        self.venceu_jogo = False
        self.mapa_do_jogo = mapa.gerar_mapa_aleatorio(
            mapa.LARGURA_GRADE, mapa.ALTURA_GRADE)

        # Grupos de Sprites
        self.todas_sprites = pygame.sprite.Group()
        self.grupo_vidas_extras = pygame.sprite.Group()
        self.grupo_paredes = pygame.sprite.Group()
        self.grupo_chave_partes = pygame.sprite.Group()
        self.grupo_cafe = pygame.sprite.Group()
        self.grupo_porta = pygame.sprite.Group()
        self.grupo_chefes = pygame.sprite.Group()
        self.grupo_segurancas = pygame.sprite.Group()

        self.ultimo_dano_tempo = 0
        self.modo_inimigo = 'dispersar'
        self.timer_mudanca_modo = pygame.time.get_ticks() + constants.TEMPO_DISPERSAO

        # Posiciona jogador, paredes e encontra locais livres
        posicao_inicial_jogador = None
        self.posicoes_livres = []
        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                # O local da porta começa como uma parede de colisão normal
                if celula == mapa.PAREDE or celula == mapa.PORTA:
                    self.grupo_paredes.add(parede.Parede(x, y))
                if celula == mapa.PISO:
                    self.posicoes_livres.append((x, y))

        largura_mapa = len(self.mapa_do_jogo[0])
        altura_mapa = len(self.mapa_do_jogo)
        posicao_inicial_jogador = (largura_mapa - 2, altura_mapa - 2)
        if posicao_inicial_jogador not in self.posicoes_livres:
            posicao_inicial_jogador = self.posicoes_livres[-1] if self.posicoes_livres else (
                1, 1)

        self.jogador = mark.Mark(
            self, posicao_inicial_jogador[0], posicao_inicial_jogador[1])
        self.todas_sprites.add(self.jogador)

        self.spawnar_inimigo(cobel.Cobel, self.grupo_chefes,
                             posicao_inicial_jogador)
        self.spawnar_inimigo(
            segurancas.Huang, self.grupo_segurancas, posicao_inicial_jogador)

        self.agendar_proximo_spawn_balao()
        self.timer_spawn_chave = pygame.time.get_ticks() + constants.TIMER_INICIAL_CHAVE
        self.agendar_proximo_spawn_cafe()

        self.rodar()

    def spawnar_inimigo(self, classe_inimigo, grupo, pos_jogador_grid):
        posicoes_spawn_seguras = [p for p in self.posicoes_livres if abs(
            p[0] - pos_jogador_grid[0]) + abs(p[1] - pos_jogador_grid[1]) >= constants.DISTANCIA_SEGURA]
        if not posicoes_spawn_seguras:
            posicoes_spawn_seguras = self.posicoes_livres

        if posicoes_spawn_seguras:
            pos_x, pos_y = random.choice(posicoes_spawn_seguras)
            novo_inimigo = classe_inimigo(self, pos_x, pos_y)
            self.todas_sprites.add(novo_inimigo)
            grupo.add(novo_inimigo)

    def rodar(self):
        # CONTROLA O LOOP PRINCIPAL DO JOGO
        self.jogando = True
        while self.jogando:
            self.relogio.tick(constants.FPS)
            self.eventos()
            self.atualizar_sprites()
            self.desenhar_sprites()
            if self.vidas <= 0:
                self.jogando = False

    def eventos(self):
        # PROCESSA TODOS OS EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.jogando:
                    self.jogando = False
                self.esta_rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.jogador.adicionar_movimento(dx=-1, dy=0)
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    self.jogador.adicionar_movimento(dx=1, dy=0)
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.jogador.adicionar_movimento(dx=0, dy=-1)
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.jogador.adicionar_movimento(dx=0, dy=1)

    def atualizar_sprites(self):
        self.gerenciar_modos_inimigos()
        self.checar_spawn_balao()
        self.checar_spawn_chave()
        self.checar_spawn_cafe()
        self.checar_efeito_cafe()
        self.todas_sprites.update()

        if self.jogador:
            # Colisões com itens
            if pygame.sprite.spritecollide(self.jogador, self.grupo_vidas_extras, True):
                self.vidas += 1
                if self.vidas > constants.VIDAS_INICIAIS:
                    self.vidas = constants.VIDAS_INICIAIS
                self.som_balao_ganha.play()  # se ele tocar em um balão

            partes_colididas = pygame.sprite.spritecollide(
                self.jogador, self.grupo_chave_partes, True)
            for parte in partes_colididas:
                self.partes_coletadas[parte.parte_index] = True
                self.proxima_parte_a_spawnar += 1
                self.som_chave.play()  # som da chave

                pos_jogador_grid = (self.jogador.rect.x // constants.TAMANHO_BLOCO,
                                    self.jogador.rect.y // constants.TAMANHO_BLOCO)
                if self.proxima_parte_a_spawnar == 1:
                    self.spawnar_inimigo(
                        segurancas.Drummond, self.grupo_segurancas, pos_jogador_grid)
                elif self.proxima_parte_a_spawnar == 2:
                    self.spawnar_inimigo(
                        segurancas.Milchick, self.grupo_segurancas, pos_jogador_grid)
                elif self.proxima_parte_a_spawnar == 3:
                    self.spawnar_inimigo(
                        segurancas.Mauer, self.grupo_segurancas, pos_jogador_grid)

                if self.proxima_parte_a_spawnar < constants.NUMERO_PARTES_CHAVE:
                    self.agendar_proxima_chave()
                elif all(self.partes_coletadas):  # Se foi a última parte
                    x_porta, y_porta = constants.X_PORTA, constants.Y_PORTA

                    # Procura pela parede de colisão no local da porta e a remove
                    for parede_sprite in self.grupo_paredes:
                        if parede_sprite.rect.x == x_porta * constants.TAMANHO_BLOCO and parede_sprite.rect.y == y_porta * constants.TAMANHO_BLOCO:
                            parede_sprite.kill()  # DESTRÓI A BARREIRA INVISÍVEL
                            break

                    self.mapa_do_jogo[y_porta][x_porta] = mapa.PISO

                    # Adiciona a sprite VISUAL da porta aberta
                    nova_porta = porta.Porta(x_porta, y_porta)
                    self.todas_sprites.add(nova_porta)
                    self.grupo_porta.add(nova_porta)

            if pygame.sprite.spritecollide(self.jogador, self.grupo_cafe, True):
                self.ativar_efeito_cafe()
                self.som_cafe.play()  # som café

            # Colisão com a Chefona (Cobel)
            if pygame.sprite.spritecollide(self.jogador, self.grupo_chefes, False) and not self.jogador.invencivel:
                som_cobel = pygame.mixer.Sound('audios/som_cobel.mp3')
                som_cobel.set_volume(1.0)  #ajusta o volume do som
                som_cobel.play()  #inicia o som do cobel
                
                self.vidas = 0

            # Colisão com Seguranças Comuns
            colisoes_segurancas = pygame.sprite.spritecollide(
                self.jogador, self.grupo_segurancas, False)
            if colisoes_segurancas:
                agora = pygame.time.get_ticks()
                if not self.jogador.invencivel and agora - self.ultimo_dano_tempo > constants.COOLDOWN_DANO:
                    self.ultimo_dano_tempo = agora

                    #tocar som do segurança
                    som_segurancas = pygame.mixer.Sound('audios/som_segurancas.mp3')
                    som_segurancas.set_volume(1.0)  #ajusta o volume do som
                    som_segurancas.play()

                    #se o jogador já estiver com 1 vida restante e for atingido por um segurança, ele ouvirá o som de "perdeu seguranças" no momento em que perde o último balão
                    if self.vidas==1: 
                        som_perdeu_segurancas = pygame.mixer.Sound('audios/som_perdeu_segurancas.mp3')
                        som_perdeu_segurancas.set_volume(1.0)  #ajusta o volume do som
                        som_perdeu_segurancas.play()

                    self.perder_vida()

            # Colisão com a Porta (para vencer o jogo)
            colisoes_porta = pygame.sprite.spritecollide(
                self.jogador, self.grupo_porta, False)
            if colisoes_porta:
                area_jogador = self.jogador.rect.width * self.jogador.rect.height
                rect_intersecao = self.jogador.rect.clip(
                    colisoes_porta[0].rect)
                area_intersecao = rect_intersecao.width * rect_intersecao.height

                if area_intersecao >= (area_jogador * constants.INTERSECAO):
                    self.venceu_jogo = True
                    self.jogando = False

    def desenhar_sprites(self):
        # DESENHA TODOS OS ELEMENTOS NA TELA
        self.tela.fill(constants.PRETO)
        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                pos_x = x * constants.TAMANHO_BLOCO
                pos_y = y * constants.TAMANHO_BLOCO
                # A porta não é mais desenhada aqui, pois agora é uma sprite
                if celula == mapa.PAREDE:
                    self.tela.blit(self.imagem_parede, (pos_x, pos_y))
                elif celula == mapa.PISO:
                    pygame.draw.rect(self.tela, constants.VERDE, (pos_x, pos_y,
                                     constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))

        # Desenha o jogador, inimigos, e a porta
        self.todas_sprites.draw(self.tela)

        pos_y_interface = constants.ALTURA - \
            (mapa.ALTURA_INTERFACE_INFERIOR // 2)
        for i in range(self.vidas):
            self.tela.blit(self.imagem_balao_vida,
                           (20 + i * 35, pos_y_interface - 15))
        if self.jogador.invencivel:
            self.tela.blit(self.imagem_xicara_cafe,
                           (constants.LARGURA - 50, pos_y_interface - 15))
        else:
            self.tela.blit(self.imagem_xicara_cafe_opaca,
                           (constants.LARGURA - 50, pos_y_interface - 15))
        largura_total_chave = self.imagem_chave_original.get_width()
        pos_x_chave_hud = (constants.LARGURA - largura_total_chave) // 2
        for i in range(constants.NUMERO_PARTES_CHAVE):
            if self.partes_coletadas[i]:
                imagem_da_parte = self.imagens_partes_chave[i]
                largura_parte = imagem_da_parte.get_width()
                altura_balao = self.imagem_balao_vida.get_height()
                altura_chave = imagem_da_parte.get_height()
                offset_y = (altura_balao - altura_chave) // 2
                self.tela.blit(imagem_da_parte, (pos_x_chave_hud +
                               i * largura_parte, pos_y_interface - 15 + offset_y))

        pygame.display.flip()

    def carregar_arquivos(self):
        # CARREGA E CORTA OS ARQUIVOS NECESSARIOS
        diretorio_imagens = os.path.join(os.getcwd(), 'imagens')

        self.imagem_parede = pygame.image.load(os.path.join(
            diretorio_imagens, constants.PAREDE)).convert()
        self.imagem_balao_vida = pygame.image.load(os.path.join(
            diretorio_imagens, constants.BALAO)).convert_alpha()
        self.imagem_xicara_cafe = pygame.image.load(os.path.join(
            diretorio_imagens, constants.CAFE)).convert_alpha()
        self.imagem_game_over = pygame.image.load(os.path.join(
            diretorio_imagens, constants.GAME_OVER_IMG)).convert()
        self.imagem_venceu = pygame.image.load(os.path.join(
            diretorio_imagens, constants.VENCEU_IMG)).convert()

        self.imagem_xicara_cafe_opaca = self.imagem_xicara_cafe.copy()
        self.imagem_xicara_cafe_opaca.set_alpha(100)

        self.imagem_chave_original = pygame.image.load(
            os.path.join(diretorio_imagens, constants.CHAVE)).convert_alpha()
        largura_chave, altura_chave = self.imagem_chave_original.get_size()
        largura_parte = largura_chave // constants.NUMERO_PARTES_CHAVE

        self.imagens_partes_chave = []
        for i in range(constants.NUMERO_PARTES_CHAVE):
            x_corte = i * largura_parte
            area_corte = pygame.Rect(x_corte, 0, largura_parte, altura_chave)
            imagem_cortada = self.imagem_chave_original.subsurface(area_corte)
            self.imagens_partes_chave.append(imagem_cortada)

        # Sons do jogo
        self.som_cafe = pygame.mixer.Sound(
            os.path.join('audios', 'som_café.mp3'))
        self.som_balao_ganha = pygame.mixer.Sound(
            os.path.join('audios', 'som_balão_ganha.mp3'))
        self.som_balao_perde = pygame.mixer.Sound(
            os.path.join('audios', 'som_balão_perde.mp3'))
        self.som_chave = pygame.mixer.Sound(
            os.path.join('audios', 'som_chaves.mp3'))
        self.som_aplauso_venceu = pygame.mixer.Sound(
            os.path.join('audios', 'som_aplauso_venceu.mp3'))

    # --- Métodos de Lógica Específica ---

    def spawnar_inimigo(self, classe_inimigo, grupo, pos_jogador_grid):
        posicoes_spawn_seguras = [p for p in self.posicoes_livres if abs(
            p[0] - pos_jogador_grid[0]) + abs(p[1] - pos_jogador_grid[1]) >= constants.DISTANCIA_SEGURA]
        if not posicoes_spawn_seguras:
            posicoes_spawn_seguras = self.posicoes_livres

        if posicoes_spawn_seguras:
            pos_x, pos_y = random.choice(posicoes_spawn_seguras)
            novo_inimigo = classe_inimigo(self, pos_x, pos_y)
            self.todas_sprites.add(novo_inimigo)
            grupo.add(novo_inimigo)

    def gerenciar_modos_inimigos(self):
        agora = pygame.time.get_ticks()
        if agora > self.timer_mudanca_modo:
            if self.modo_inimigo == 'perseguir':
                self.modo_inimigo = 'dispersar'
                self.timer_mudanca_modo = agora + constants.TEMPO_DISPERSAO
            else:  # se estava em 'dispersar'
                self.modo_inimigo = 'perseguir'
                self.timer_mudanca_modo = agora + constants.TEMPO_PERSEGUICAO

    def agendar_proximo_spawn_cafe(self):
        intervalo = random.randint(
            constants.TIMER_MIN_CAFE, constants.TIMER_MAX_CAFE)
        self.timer_spawn_cafe = pygame.time.get_ticks() + intervalo

    def spawnar_cafe(self):
        if self.posicoes_livres:
            pos_x, pos_y = random.choice(self.posicoes_livres)
            novo_cafe = cafe.Cafe(pos_x, pos_y)
            self.todas_sprites.add(novo_cafe)
            self.grupo_cafe.add(novo_cafe)

    def checar_spawn_cafe(self):
        if len(self.grupo_cafe) > 0 or self.jogador.invencivel:
            return
        if pygame.time.get_ticks() >= self.timer_spawn_cafe:
            self.spawnar_cafe()

    def ativar_efeito_cafe(self):
        self.jogador.invencivel = True
        self.jogador.timer_efeito_cafe = pygame.time.get_ticks() + \
            constants.DURACAO_EFEITO_CAFE
        self.agendar_proximo_spawn_cafe()

    def checar_efeito_cafe(self):
        if self.jogador.invencivel and pygame.time.get_ticks() > self.jogador.timer_efeito_cafe:
            self.jogador.invencivel = False

    def agendar_proxima_chave(self):
        intervalo = random.randint(
            constants.TIMER_MIN_CHAVE, constants.TIMER_MAX_CHAVE)
        self.timer_spawn_chave = pygame.time.get_ticks() + intervalo

    def spawnar_proxima_chave(self):
        if self.posicoes_livres:
            pos_x, pos_y = random.choice(self.posicoes_livres)

            parte_index = self.proxima_parte_a_spawnar
            imagem_da_parte = self.imagens_partes_chave[parte_index]

            nova_parte = chave.ChaveParte(
                pos_x, pos_y, parte_index, imagem_da_parte)
            self.todas_sprites.add(nova_parte)
            self.grupo_chave_partes.add(nova_parte)

    def checar_spawn_chave(self):
        if self.proxima_parte_a_spawnar >= constants.NUMERO_PARTES_CHAVE:
            return
        if len(self.grupo_chave_partes) > 0:
            return

        if pygame.time.get_ticks() >= self.timer_spawn_chave:
            self.spawnar_proxima_chave()

    def agendar_proximo_spawn_balao(self):
        intervalo = random.randint(5000, 20000)
        self.timer_spawn_balao = pygame.time.get_ticks() + intervalo

    def spawnar_balao(self):
        if self.posicoes_livres:
            pos_x, pos_y = random.choice(self.posicoes_livres)
            novo_balao = balao.Balao(pos_x, pos_y)
            self.todas_sprites.add(novo_balao)
            self.grupo_vidas_extras.add(novo_balao)

    def checar_spawn_balao(self):
        if self.vidas >= constants.VIDAS_INICIAIS or len(self.grupo_vidas_extras) > 0:
            return
        if pygame.time.get_ticks() >= self.timer_spawn_balao:
            self.spawnar_balao()
            self.agendar_proximo_spawn_balao()

    def perder_vida(self):
        if self.vidas > 0:
            self.vidas -= 1
        self.agendar_proximo_spawn_balao()

    def mostrar_texto(self, texto, tamanho, cor, x, y):
        fonte = pygame.font.Font(self.fonte, tamanho)
        texto_render = fonte.render(texto, True, cor)
        texto_rect = texto_render.get_rect()
        texto_rect.midtop = (x, y)
        self.tela.blit(texto_render, texto_rect)

    def tela_start(self):
        return tela_start.mostrar_tela_start(
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
                    esperando = False
                    self.esta_rodando = False

    def tela_game_over(self):
        return game_over.tela_game_over(self.tela, self.fonte, self.imagem_game_over)

    def tela_venceu(self):
        return venceu.tela_venceu(self.tela, self.fonte, self.imagem_venceu)


# --- Inicialização e Loop Principal ---
g = Game()
g.tela_start()
while g.esta_rodando:
    
    #MOSTRA O MENU E ESPERA A ESCOLHA DO JOGADOR
    acao_escolhida = g.tela_start() 

    #VERIFICA A ESCOLHA E AGE DE ACORDO
    if acao_escolhida == "START":
        g.novo_jogo()
        
        # Se o jogo terminou, verifica se foi por vitória ou derrota
        if g.venceu_jogo:
            if not g.tela_venceu():
                # Sai do jogo se o jogador fechar a tela de vitória
                g.esta_rodando = False 
        elif g.vidas <= 0:
            if not g.tela_game_over():
                # Sai do jogo se o jogador fechar a tela de game over
                g.esta_rodando = False

    elif acao_escolhida == "TUTORIAL":
        # Se a escolha foi "TUTORIAL", apenas mostramos a tela de tutorial.
        
        tela_tutorial.mostrar_tela_tutorial(
            tela=g.tela,
            fonte_path=g.fonte,
            largura=constants.LARGURA,
            altura=constants.ALTURA
        )

    else: # Se a ação for None (jogador fechou a janela do menu) ou outra coisa.
        g.esta_rodando = False # Encerra o loop principal.

pygame.quit()
