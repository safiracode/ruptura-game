import pygame
import constants
import mapa
import os
from classes import balao
import random
from classes.mark import Mark

class Game:
    def __init__(self):
        """Inicializa o jogo e suas variáveis principais."""
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((constants.LARGURA, constants.ALTURA))
        pygame.display.set_caption(constants.TITULO_JOGO)
        ICONE = pygame.image.load('imagens/icone.png')
        pygame.display.set_icon(ICONE)
        self.relogio = pygame.time.Clock()
        self.esta_rodando = True
        self.fonte = pygame.font.match_font(constants.FONTE)
        self.carregar_arquivos()

    # --- Métodos de Controle do Jogo ---

    def novo_jogo(self):
        """Configura e inicia uma nova partida."""
        self.vidas = constants.VIDAS_INICIAIS
        self.mapa_do_jogo = mapa.gerar_mapa_aleatorio(mapa.LARGURA_GRADE, mapa.ALTURA_GRADE)
        
        self.todas_sprites = pygame.sprite.Group()
        self.grupo_vidas_extras = pygame.sprite.Group()
        
        self.agendar_proximo_spawn_balao()
        # encontra uma posição livre para o Mark (exemplo: primeira célula livre)
        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                if celula == mapa.PISO:
                    pos_x = x * constants.TAMANHO_BLOCO
                    pos_y = y * constants.TAMANHO_BLOCO
                    self.jogador = Mark(pos_x, pos_y, constants.TAMANHO_BLOCO)
                    self.todas_sprites.add(self.jogador)
                    break
            else:
                continue
            break

        self.rodar()
    
    def rodar(self):
        """Controla o loop principal do jogo (game loop)."""
        self.jogando = True
        while self.jogando:
            self.relogio.tick(constants.FPS)
            self.eventos()
            self.atualizar_sprites()
            self.desenhar_sprites()

    def eventos(self):
        """Processa todos os eventos de input (teclado, fechar janela, etc.)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.jogando:
                    self.jogando = False
                self.esta_rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.jogador.mover('esquerda', self.mapa_do_jogo, constants.TAMANHO_BLOCO)
                elif event.key == pygame.K_RIGHT:
                    self.jogador.mover('direita', self.mapa_do_jogo, constants.TAMANHO_BLOCO)
                elif event.key == pygame.K_UP:
                    self.jogador.mover('cima', self.mapa_do_jogo, constants.TAMANHO_BLOCO)
                elif event.key == pygame.K_DOWN:
                    self.jogador.mover('baixo', self.mapa_do_jogo, constants.TAMANHO_BLOCO)


    def atualizar_sprites(self):
        """Atualiza o estado de todas as sprites e gerencia a lógica do jogo."""
        self.checar_spawn_balao()
        teclas = pygame.key.get_pressed()
        self.todas_sprites.update()

        # Lógica de colisão para quando o jogador pegar o balão (a ser implementada)
        # if self.jogador:
        #     colisoes = pygame.sprite.spritecollide(self.jogador, self.grupo_vidas_extras, True)
        #     if colisoes:
        #         self.vidas += 1
        #         # Garante que a vida não passe do máximo
        #         if self.vidas > constants.VIDAS_INICIAIS:
        #             self.vidas = constants.VIDAS_INICIAIS

    def desenhar_sprites(self):
        """Desenha todos os elementos na tela."""
        self.tela.fill(constants.PRETO)

        # Desenha o mapa
        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                pos_x = x * constants.TAMANHO_BLOCO
                pos_y = y * constants.TAMANHO_BLOCO
                
                if celula == mapa.PAREDE:
                    self.tela.blit(self.imagem_parede, (pos_x, pos_y))
                elif celula == mapa.PISO:
                    pygame.draw.rect(self.tela, constants.VERDE, (pos_x, pos_y, constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))
        
        # Desenha a interface (HUD)
        pos_y_interface = constants.ALTURA - (mapa.ALTURA_INTERFACE_INFERIOR // 2)
        for i in range(self.vidas):
             self.tela.blit(self.imagem_balao_vida, (20 + i * 35, pos_y_interface - 15))
        self.tela.blit(self.imagem_xicara_cafe, (constants.LARGURA - 50, pos_y_interface - 15))
        
        self.todas_sprites.draw(self.tela)
        pygame.display.flip()

    # --- Métodos de Lógica Específica ---

    def agendar_proximo_spawn_balao(self):
        """Calcula um tempo aleatório entre 5 e 20s e agenda o próximo spawn de balão."""
        intervalo = random.randint(5000, 20000)
        self.timer_spawn_balao = pygame.time.get_ticks() + intervalo

    def spawnar_balao(self):
        """Encontra um lugar aleatório no mapa e cria um balão."""
        posicoes_livres = []
        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                if celula == mapa.PISO:
                    posicoes_livres.append((x, y))
        
        if posicoes_livres:
            pos_x, pos_y = random.choice(posicoes_livres)
            novo_balao = balao.Balao(pos_x, pos_y)
            self.todas_sprites.add(novo_balao)
            self.grupo_vidas_extras.add(novo_balao)

    def checar_spawn_balao(self):
        """Verifica se as condições para criar um novo balão foram atendidas."""
        if self.vidas >= constants.VIDAS_INICIAIS or len(self.grupo_vidas_extras) > 0:
            return
            
        if pygame.time.get_ticks() >= self.timer_spawn_balao:
            self.spawnar_balao()
            self.agendar_proximo_spawn_balao()
            
    def perder_vida(self):
        """Função a ser chamada quando o jogador for pego."""
        if self.vidas > 0:
            self.vidas -= 1
        print(f"Vida perdida! Vidas restantes: {self.vidas}")
        self.agendar_proximo_spawn_balao()

    def carregar_arquivos(self):
        """Carrega todas as imagens e arquivos de áudio necessários para o jogo."""
        diretorio_imagens = os.path.join(os.getcwd(), 'imagens')
        self.diretorio_audios = os.path.join(os.getcwd(), 'audios')

        self.imagem_parede = os.path.join(diretorio_imagens, constants.PAREDE)
        self.imagem_balao_vida = os.path.join(diretorio_imagens, constants.BALAO)
        self.imagem_xicara_cafe = os.path.join(diretorio_imagens, constants.CAFE)

        self.imagem_parede = pygame.image.load(self.imagem_parede).convert()
        self.imagem_balao_vida = pygame.image.load(self.imagem_balao_vida).convert_alpha()
        self.imagem_xicara_cafe = pygame.image.load(self.imagem_xicara_cafe).convert_alpha()

    def tela_start(self):
        """Mostra a tela inicial do jogo."""
        pass

    def tela_game_over(self):
        """Mostra a tela de fim de jogo."""
        pass

# --- Inicialização e Loop Principal ---
g = Game()
g.tela_start()

while g.esta_rodando:
    g.novo_jogo()
    g.tela_game_over()

pygame.quit()