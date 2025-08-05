import pygame
import constants
import mapa
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

    # MÉTODO CORRIGIDO E SIMPLIFICADO
    def novo_jogo(self):
        # 1. Gera o mapa aleatório e o armazena
        self.mapa_do_jogo = mapa.gerar_mapa_aleatorio(mapa.LARGURA_GRADE, mapa.ALTURA_GRADE)
        
        # 2. Prepara o grupo de sprites
        self.todas_sprites = pygame.sprite.Group()

        # 3. Futuramente, você adicionará o jogador e outros elementos aqui
        # self.jogador = sprites.Jogador()
        # self.todas_sprites.add(self.jogador)
        
        # 4. Agora que tudo está pronto, inicia o loop do jogo
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
        self.tela.fill(constants.PRETO) # Limpando a tela

        # --- LÓGICA PARA DESENHAR O MAPA ---
        for y, linha in enumerate(self.mapa_do_jogo):
            for x, celula in enumerate(linha):
                pos_x = x * constants.TAMANHO_BLOCO
                pos_y = y * constants.TAMANHO_BLOCO
                
                if celula == mapa.PAREDE:
                    self.tela.blit(self.imagem_parede, (pos_x, pos_y))
                elif celula == mapa.PISO:
                    # Desenha um retângulo preenchido com a nova cor
                    pygame.draw.rect(self.tela, constants.VERDE, (pos_x, pos_y, constants.TAMANHO_BLOCO, constants.TAMANHO_BLOCO))           
        
        # --- DESENHA A INTERFACE (VIDAS E CAFÉ) ---
        # Posição y centralizada na área inferior
        pos_y_interface = constants.ALTURA - (mapa.ALTURA_INTERFACE_INFERIOR // 2)

        # Desenha os balões de vida (exemplo com 5 vidas)
        for i in range(5):
             self.tela.blit(self.imagem_balao_vida, (20 + i * 35, pos_y_interface - 15))

        # Desenha o café (exemplo)
        # Futuramente, você pode usar uma variável como `if cafe_ativo:`
        self.tela.blit(self.imagem_xicara_cafe, (constants.LARGURA - 50, pos_y_interface - 15))


        self.todas_sprites.draw(self.tela) # Desenhando as sprites (jogador, inimigos) por cima do mapa
        pygame.display.flip() # Atualiza a tela a cada frame

    # Carregar arquivos
    def carregar_arquivos(self):
        diretorio_imagens = os.path.join(os.getcwd(), 'imagens')
        self.diretorio_audios = os.path.join(os.getcwd(), 'audios')
        self.spritesheet = os.path.join(diretorio_imagens, constants.SPRITESHEET)
        self.ruptura_start_logo = os.path.join(diretorio_imagens, constants.RUPTURA_START_LOGO)
        self.ruptura_start_logo = pygame.image.load(self.ruptura_start_logo).convert()

        # imagens mapa
        self.imagem_parede = os.path.join(diretorio_imagens, constants.PAREDE)
        self.imagem_balao_vida = os.path.join(diretorio_imagens, constants.BALAO)
        self.imagem_xicara_cafe = os.path.join(diretorio_imagens, constants.CAFE)

        self.imagem_parede = pygame.image.load(self.imagem_parede).convert()
        self.imagem_balao_vida = pygame.image.load(self.imagem_balao_vida).convert_alpha()
        self.imagem_xicara_cafe = pygame.image.load(self.imagem_xicara_cafe).convert_alpha()

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

pygame.quit() # Adicionado para fechar o Pygame corretamente ao final