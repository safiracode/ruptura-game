import pygame
import sprites
import constants

class Game:
    def __init__(self):
        # Criando a tela do jogo
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption(constants.TITLE_GAME)
        self.clock = pygame.time.Clock() # relógio fps
        self.is_running = True # jogo começa assim que ele for executador

    #--------- Métodos ----------

    # Instancia as classes das sprites do jogo e chama o loop do jogo
    def new_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.run()
    
    # Método para rodar o jogo
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(constants.FPS) # permite adicionar a taxa de frames do jogo
            self.events()
            self.update_sprites()
            self.draw_sprites()

    # define os eventos do jogo
    def events(self):
        for event in pygame.event.get():
            # se o evento for fechar o jogo
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.is_running = False

    # atualiza a sprites, por exemplo quando dois objetos se chocam
    def update_sprites(self):
        self.all_sprites.update()

    # Desenha as sprites
    def draw_sprites(self):
        self.screen.fill(constants.BLACK) # limpando a tela
        self.all_sprites.draw(self.screen) # desenhando as sprites
        pygame.display.flip() # atualiza a tela a cada frame
    
    # mostra a tela de start
    def start_screen(self):
        pass # palavra reservada no python que significa não faça nada. Usada para partes que ainda serão implementadas

    # mostra tela game over
    def game_over_screen(self):
        pass

g = Game()
g.start_screen()

while g.is_running:
    g.new_game()
    g.game_over_screen()