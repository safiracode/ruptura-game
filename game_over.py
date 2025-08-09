import pygame
import constants

def tela_game_over(tela, fonte, imagem_game_over):
    esperando = True
    x_botao = (constants.LARGURA - constants.LARGURA_BOTAO) // 2 + 80
    y_botao = constants.ALTURA // 2 + 220

    #som de game over
    pygame.mixer.music.stop() #para qualquer som anterior

    som_cobel = pygame.mixer.Sound('audios/som_cobel.mp3')
    som_cobel.set_volume(1.0)  #ajusta o volume do som
    som_cobel.play() #inicia o som do cobel

    pygame.mixer.music.load('audios/musica game over.mp3')
    pygame.mixer.music.play() #inicia a musica game over

    img_botao = pygame.image.load(constants.IMG_BOTAO).convert_alpha()
    img_botao = pygame.transform.scale(img_botao, (constants.LARGURA_BOTAO, constants.ALTURA_BOTAO))

    while esperando:
        tela.blit(imagem_game_over, (0, 0))

        # Desenha a imagem do botão como fundo do botão
        tela.blit(img_botao, (x_botao, y_botao))

        # Texto do botão
        fonte_botao = pygame.font.Font(fonte, 36)
        texto = fonte_botao.render("Recomeçar", True, constants.BRANCO)
        texto_rect = texto.get_rect(center=(x_botao + constants.LARGURA_BOTAO // 2, y_botao + constants.ALTURA_BOTAO // 2))
        tela.blit(texto, texto_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
                return False  # Sai do jogo
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if x_botao <= mouse_x <= x_botao + constants.LARGURA_BOTAO and y_botao <= mouse_y <= y_botao + constants.ALTURA_BOTAO:
                    #parar música game over e iniciar principal
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("audios/música principal.mp3")
                    pygame.mixer.music.play(-1) #loop infinito
                    esperando = False
                    return True  # Recomeça o jogo