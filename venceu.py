import pygame
import constants

def tela_venceu(tela, fonte, imagem_venceu):
    esperando = True
    x_botao = (constants.LARGURA - constants.LARGURA_BOTAO) // 2 + 100
    y_botao = constants.ALTURA // 2 + 220

    #som you win
    pygame.mixer.music.stop() #para qualquer som anterior
    som_aplauso_venceu = pygame.mixer.Sound('audios/som_aplauso_venceu.mp3')    
    som_aplauso_venceu.play() #inicia o som de aplausos
    pygame.mixer.music.load('audios/música venceu.mp3')
    pygame.mixer.music.play() #inicia a musica venceu

    # Configurações do botão | feito "manualmente" assim como da tela start
    COR_BOTAO = (24, 112, 84)
    COR_BOTAO_HOVER = (44, 132, 104)
    fonte_botao = pygame.font.Font(fonte, 36)

    while esperando:
        tela.blit(imagem_venceu, (0, 0))

        # Pega posição do mouse para hover
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Define cor do botão (normal ou hover)
        if x_botao <= mouse_x <= x_botao + constants.LARGURA_BOTAO_GAMEOVERWIN and y_botao <= mouse_y <= y_botao + constants.ALTURA_BOTAO:
            cor_botao = COR_BOTAO_HOVER
        else:
            cor_botao = COR_BOTAO 

        # Desenha retângulo do botão
        pygame.draw.rect(tela, cor_botao, (x_botao, y_botao, constants.LARGURA_BOTAO_GAMEOVERWIN, constants.ALTURA_BOTAO), border_radius=10)

        # Texto do botão
        fonte_botao = pygame.font.Font(fonte, 36)
        texto = fonte_botao.render("Recomeçar", True, constants.BRANCO)
        texto_rect = texto.get_rect(center=(x_botao + constants.LARGURA_BOTAO_GAMEOVERWIN // 2, y_botao + constants.ALTURA_BOTAO // 2))
        tela.blit(texto, texto_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
                return False  #sai do jogo
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if x_botao <= mouse_x <= x_botao + constants.LARGURA_BOTAO and y_botao <= mouse_y <= y_botao + constants.ALTURA_BOTAO:
                    #parar musica venceu e iniciar principal
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("audios/música principal.mp3")
                    pygame.mixer.music.play(-1) #loop infinito
                    esperando = False
                    return True  #recomeça o jogo