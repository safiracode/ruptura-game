import pygame
import sprites
import constants
import os


class Game:
    def __init__(self):
        # Criando a tela do jogo
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((constants.LARGURA, constants.ALTURA))
        pygame.display.set_caption(constants.TITULO_JOGO)
        ICONE = pygame.image.load('imagens/icone.png')
        pygame.display.set_icon(ICONE)
        self.relogio = pygame.time.Clock() # relógio fps
        self.esta_rodando = True # jogo começa assim que ele for executador
        self.fonte = pygame.font.match_font(constants.FONTE)
        self.carregar_arquivos()

    #--------- Métodos ----------

    # Instancia as classes das sprites do jogo e chama o loop do jogo
    def novo_jogo(self):
        self.todas_sprites = pygame.sprite.Group()
        self.rodar()
    
    # Método para rodar o jogo
    def rodar(self):
        self.jogando = True
        while self.jogando:
            self.relogio.tick(constants.FPS) # permite adicionar a taxa de frames do jogo
            self.eventos()
            self.atualizar_sprites()
            self.desenhar_sprites()

    # define os eventos do jogo
    def eventos(self):
        for event in pygame.event.get():
            # se o evento for fechar o jogo
            if event.type == pygame.QUIT:
                if self.jogando:
                    self.jogando = False
                self.esta_rodando = False

    # atualiza a sprites, por exemplo quando dois objetos se chocam
    def atualizar_sprites(self):
        self.todas_sprites.update()

    # Desenha as sprites
    def desenhar_sprites(self):
        self.tela.fill(constants.PRETO) # limpando a tela
        self.todas_sprites.draw(self.tela) # desenhando as sprites
        pygame.display.flip() # atualiza a tela a cada frame

    # Carregar arquivos
    def carregar_arquivos(self):
        diretorio_imagens = os.path.join(os.getcwd(), 'imagens')
        self.diretorio_audios = os.path.join(os.getcwd(), 'audios')
        self.spritesheet = os.path.join(diretorio_imagens, constants.SPRITESHEET)
        self.ruptura_start_logo = os.path.join(diretorio_imagens, constants.RUPTURA_START_LOGO)
        self.ruptura_start_logo = pygame.image.load(self.ruptura_start_logo).convert()



    
    # mostra a tela de start
    def tela_start(self):
        pass # palavra reservada no python que significa não faça nada. Usada para partes que ainda serão implementadas

    # mostra tela game over
    def tela_game_over(self):
        pass

g = Game()
g.tela_start()

while g.esta_rodando:
    g.novo_jogo()
    g.tela_game_over()