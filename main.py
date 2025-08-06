# main.py
import pygame
import constants
import mapa
import os
from classes import balao, mark, parede, cobel
import random
import game_over

class Game:
    def __init__(self):
        """Inicializa o jogo e suas variáveis principais."""
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
        """Configura e inicia uma nova partida."""
        self.vidas = constants.VIDAS_INICIAIS
        self.mapa_do_jogo = mapa.gerar_mapa_aleatorio(mapa.LARGURA_GRADE, mapa.ALTURA_GRADE)
        
        self.todas_sprites = pygame.sprite.Group()
        self.grupo_vidas_extras = pygame.sprite.Group()
        self.grupo_paredes = pygame.sprite.Group()
        self.grupo_cobels = pygame.sprite.Group()

        posicao_inicial_jogador = None
        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                if celula == mapa.PAREDE:
                    p = parede.Parede(x, y)
                    self.grupo_paredes.add(p)
                if celula == mapa.PISO and posicao_inicial_jogador is None:
                    posicao_inicial_jogador = (x, y)
        
        self.jogador = mark.Mark(self, posicao_inicial_jogador[0], posicao_inicial_jogador[1])
        self.todas_sprites.add(self.jogador)

        # spawnar apenas uma cobel
        posicoes_livres = []
        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                if celula == mapa.PISO:
                    posicoes_livres.append((x, y))
        
        # Spawna 1 cobel em posição aleatória
        if posicoes_livres:
            pos_x, pos_y = random.choice(posicoes_livres)
            novo_cobel = cobel.Cobel(self, pos_x, pos_y)
            self.todas_sprites.add(novo_cobel)
            self.grupo_cobels.add(novo_cobel)

        self.agendar_proximo_spawn_balao()
        self.rodar()
    
    def rodar(self):
        """Controla o loop principal do jogo (game loop)."""
        self.jogando = True
        while self.jogando:
            self.relogio.tick(constants.FPS)
            self.eventos()
            self.atualizar_sprites()
            self.desenhar_sprites()
            # Verifica se o jogador ficou sem vidas
            if self.vidas <= 0:
                self.jogando = False  # Sai do loop do jogo

    def eventos(self):
        """Processa todos os eventos de input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.jogando: self.jogando = False
                self.esta_rodando = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.jogador.adicionar_movimento(dx=-1, dy=0)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.jogador.adicionar_movimento(dx=1, dy=0)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.jogador.adicionar_movimento(dx=0, dy=-1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.jogador.adicionar_movimento(dx=0, dy=1)

    def atualizar_sprites(self):
        """Atualiza o estado de todas as sprites e gerencia a lógica do jogo."""
        self.checar_spawn_balao()
        self.todas_sprites.update()

        if self.jogador:
            colisoes = pygame.sprite.spritecollide(self.jogador, self.grupo_vidas_extras, True)
            if colisoes:
                self.vidas += 1
                if self.vidas > constants.VIDAS_INICIAIS:
                    self.vidas = constants.VIDAS_INICIAIS
        
        # Verifica colisão entre jogador e Cobels
        if self.jogador:
            colisoes_cobel = pygame.sprite.spritecollide(self.jogador, self.grupo_cobels, False)
            if colisoes_cobel:
                for cobel_sprite in colisoes_cobel:
                    cobel_sprite.causar_dano()
                    # Remove o Cobel após o ataque (opcional)
                    # cobel_sprite.kill()

    def desenhar_sprites(self):
        """Desenha todos os elementos na tela."""
        self.tela.fill(constants.PRETO)

        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                pos_x = x * constants.TAMANHO_BLOCO
                pos_y = y * constants.TAMANHO_BLOCO
                if celula == mapa.PAREDE:
                    self.tela.blit(self.imagem_parede, (pos_x, pos_y))
                elif celula == mapa.PISO:
                    pygame.draw.rect(self.tela, constants.VERDE, (pos_x, pos_y, constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        
        self.todas_sprites.draw(self.tela)

        pos_y_interface = constants.ALTURA - (mapa.ALTURA_INTERFACE_INFERIOR // 2)
        for i in range(self.vidas):
             self.tela.blit(self.imagem_balao_vida, (20 + i * 35, pos_y_interface - 15))
        self.tela.blit(self.imagem_xicara_cafe, (constants.LARGURA - 50, pos_y_interface - 15))
        
        pygame.display.flip()

    def carregar_arquivos(self): # Imagens adicionadas apenas aqui, falta inserir nos demais métodos e nas classes 
        """Carrega todas as imagens e arquivos de áudio necessários para o jogo."""
        diretorio_imagens = os.path.join(os.getcwd(), 'imagens')
        self.diretorio_audios = os.path.join(os.getcwd(), 'audios')
        self.spritesheet = os.path.join(diretorio_imagens, constants.SPRITESHEET)
        
        self.ruptura_start_logo = pygame.image.load(os.path.join(diretorio_imagens, constants.RUPTURA_START_LOGO)).convert()
        self.imagem_game_over = pygame.image.load(os.path.join(diretorio_imagens, constants.GAME_OVER_IMG)).convert()

        self.imagem_parede = pygame.image.load(os.path.join(diretorio_imagens, constants.PAREDE)).convert()
        self.imagem_balao_vida = pygame.image.load(os.path.join(diretorio_imagens, constants.BALAO)).convert_alpha()
        self.imagem_xicara_cafe = pygame.image.load(os.path.join(diretorio_imagens, constants.CAFE)).convert_alpha()
        self.imagem_chave_inteira = pygame.image.load(os.path.join(diretorio_imagens, constants.CHAVE_INTEIRA)).convert_alpha()
        self.imagem_chave_parte1 = pygame.image.load(os.path.join(diretorio_imagens, constants.CHAVE_PARTE1)).convert_alpha()
        self.imagem_chave_parte2 = pygame.image.load(os.path.join(diretorio_imagens, constants.CHAVE_PARTE2)).convert_alpha()
        self.imagem_chave_parte3 = pygame.image.load(os.path.join(diretorio_imagens, constants.CHAVE_PARTE3)).convert_alpha()

        self.imagem_mark_baixo = pygame.image.load(os.path.join(diretorio_imagens, constants.MARK_BAIXO)).convert_alpha()
        self.imagem_mark_cima = pygame.image.load(os.path.join(diretorio_imagens, constants.MARK_CIMA)).convert_alpha()
        self.imagem_mark_esquerda = pygame.image.load(os.path.join(diretorio_imagens, constants.MARK_ESQUERDA)).convert_alpha()
        self.imagem_mark_direita = pygame.image.load(os.path.join(diretorio_imagens, constants.MARK_DIREITA)).convert_alpha()
        self.imagem_cobel_baixo = pygame.image.load(os.path.join(diretorio_imagens, constants.COBEL_BAIXO)).convert_alpha()
        self.imagem_cobel_cima = pygame.image.load(os.path.join(diretorio_imagens, constants.COBEL_CIMA)).convert_alpha()
        self.imagem_cobel_esquerda = pygame.image.load(os.path.join(diretorio_imagens, constants.COBEL_ESQUERDA)).convert_alpha()
        self.imagem_cobel_direita = pygame.image.load(os.path.join(diretorio_imagens, constants.COBEL_DIREITA)).convert_alpha()
        self.imagem_milchick_baixo = pygame.image.load(os.path.join(diretorio_imagens, constants.MILCHICK_BAIXO)).convert_alpha()
        self.imagem_milchick_cima = pygame.image.load(os.path.join(diretorio_imagens, constants.MILCHICK_CIMA)).convert_alpha()
        self.imagem_milchick_esquerda = pygame.image.load(os.path.join(diretorio_imagens, constants.MILCHICK_ESQUERDA)).convert_alpha()
        self.imagem_milchick_direita = pygame.image.load(os.path.join(diretorio_imagens, constants.MILCHICK_DIREITA)).convert_alpha()
        self.imagem_drummond_baixo = pygame.image.load(os.path.join(diretorio_imagens, constants.DRUMMOND_BAIXO)).convert_alpha()
        self.imagem_drummond_cima = pygame.image.load(os.path.join(diretorio_imagens, constants.DRUMMOND_CIMA)).convert_alpha()
        self.imagem_drummond_esquerda = pygame.image.load(os.path.join(diretorio_imagens, constants.DRUMMOND_ESQUERDA)).convert_alpha()
        self.imagem_drummond_direita = pygame.image.load(os.path.join(diretorio_imagens, constants.DRUMMOND_DIREITA)).convert_alpha()
        self.imagem_mauer_baixo = pygame.image.load(os.path.join(diretorio_imagens, constants.MAUER_BAIXO)).convert_alpha()
        self.imagem_mauer_cima = pygame.image.load(os.path.join(diretorio_imagens, constants.MAUER_CIMA)).convert_alpha()
        self.imagem_mauer_esquerda = pygame.image.load(os.path.join(diretorio_imagens, constants.MAUER_ESQUERDA)).convert_alpha()
        self.imagem_mauer_direita = pygame.image.load(os.path.join(diretorio_imagens, constants.MAUER_DIREITA)).convert_alpha()
        self.imagem_huang_baixo = pygame.image.load(os.path.join(diretorio_imagens, constants.HUANG_BAIXO)).convert_alpha()
        self.imagem_huang_cima = pygame.image.load(os.path.join(diretorio_imagens, constants.HUANG_CIMA)).convert_alpha()
        self.imagem_huang_esquerda = pygame.image.load(os.path.join(diretorio_imagens, constants.HUANG_ESQUERDA)).convert_alpha()
        self.imagem_huang_direita = pygame.image.load(os.path.join(diretorio_imagens, constants.HUANG_DIREITA)).convert_alpha()

    def agendar_proximo_spawn_balao(self):
        intervalo = random.randint(5000, 20000); self.timer_spawn_balao = pygame.time.get_ticks() + intervalo
    def spawnar_balao(self):
        posicoes_livres = [];
        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                if celula == mapa.PISO: posicoes_livres.append((x, y))
        if posicoes_livres:
            pos_x, pos_y = random.choice(posicoes_livres)
            novo_balao = balao.Balao(pos_x, pos_y)
            self.todas_sprites.add(novo_balao); self.grupo_vidas_extras.add(novo_balao)
    def checar_spawn_balao(self):
        if self.vidas >= constants.VIDAS_INICIAIS or len(self.grupo_vidas_extras) > 0: return
        if pygame.time.get_ticks() >= self.timer_spawn_balao:
            self.spawnar_balao(); self.agendar_proximo_spawn_balao()
    def perder_vida(self):
        if self.vidas > 0: self.vidas -= 1
        print(f"Vida perdida! Vidas restantes: {self.vidas}"); self.agendar_proximo_spawn_balao()

    def mostrar_texto(self, texto, tamanho, cor, x, y):
        """Exibe um texto na tela do jogo"""
        fonte = pygame.font.Font(self.fonte, tamanho)
        texto = fonte.render(texto, True, cor)
        texto_rect = texto.get_rect()
        texto_rect.midtop = (x, y)
        self.tela.blit(texto, texto_rect)

    
    def tela_start(self):
        # """Mostra a tela inicial do jogo."""
        # self.mostrar_texto('Pressione uma tecla para jogar', 32, constants.BRANCO, constants.LARGURA / 2, 320)
        # pygame.display.flip()
        # self.esperar_por_jogador()
        pass
        
    def esperar_por_jogador(self):
        esperando = True
        while esperando:
            self.relogio.tick(constants.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.esta_rodando = False
             
                    

    def tela_game_over(self):
        # Chama a tela de game over do arquivo externo
        return game_over.tela_game_over(self.tela, self.fonte, self.imagem_game_over)

# --- Inicialização e Loop Principal ---
g = Game()
g.tela_start()
while g.esta_rodando:
    g.novo_jogo()
    # Exibe tela de game over se o jogador perdeu todas as vidas
    if not g.tela_game_over():
        break  # Sai do loop se o jogador fechar o jogo
pygame.quit()
