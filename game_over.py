import pygame
import constants

def tela_game_over(tela, fonte, imagem_game_over):
    esperando = True
    x_botao = (constants.LARGURA - constants.LARGURA_BOTAO) // 2 + 60
    y_botao = constants.ALTURA // 2 + 220

    #som de game over
    pygame.mixer.music.stop() #para qualquer som anterior
    pygame.mixer.music.load('audios/musica game over.mp3')
    pygame.mixer.music.play() #inicia a musica game over

    # Configurações do botão | feito "manualmente" assim como da tela start
    COR_BOTAO = (115, 160, 35)
    COR_BOTAO_HOVER = (140, 195, 40)
    COR_TEXTO = constants.BRANCO
    fonte_botao = pygame.font.Font(fonte, 36)

    # Retângulo do botão
    ret_botao = pygame.Rect(x_botao, y_botao, 210, constants.ALTURA_BOTAO)

    while esperando:
        tela.blit(imagem_game_over, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        # Cor muda se o mouse estiver em cima
        cor_atual = COR_BOTAO_HOVER if ret_botao.collidepoint(mouse_pos) else COR_BOTAO

        # Desenha o botão
        pygame.draw.rect(tela, cor_atual, ret_botao, border_radius=10)

        # Texto centralizado no botão
        texto = fonte_botao.render("Recomeçar", True, COR_TEXTO)
        texto_rect = texto.get_rect(center=ret_botao.center)
        tela.blit(texto, texto_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
                return False  # Sai do jogo
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and ret_botao.collidepoint(event.pos):
                    #parar música game over e iniciar principal
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("audios/música principal.mp3")
                    pygame.mixer.music.play(-1) #loop infinito
                    esperando = False
                    return True  # Recomeça o jogo