import pygame
import constants

def tela_game_over(tela, fonte, imagem_game_over):
    esperando = True
    largura_botao = 200
    altura_botao = 50
    x_botao = (constants.LARGURA - largura_botao) // 2 + 50
    y_botao = constants.ALTURA // 2 + 220

    while esperando:
        tela.blit(imagem_game_over, (0, 0))

        # Botão "Recomeçar"
        pygame.draw.rect(tela, constants.BRANCO, (x_botao, y_botao, largura_botao, altura_botao))
        fonte_botao = pygame.font.Font(fonte, 36)
        texto = fonte_botao.render("Recomeçar", True, constants.VERDE)
        texto_rect = texto.get_rect(center=(x_botao + largura_botao // 2, y_botao + altura_botao // 2))
        tela.blit(texto, texto_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
                return False  # Sai do jogo
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if x_botao <= mouse_x <= x_botao + largura_botao and y_botao <= mouse_y <= y_botao + altura_botao:
                    esperando = False
                    return True  # Recomeça o jogo