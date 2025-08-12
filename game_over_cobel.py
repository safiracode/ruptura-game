import pygame
import os
import constants

def mostrar_texto(tela, fonte_path, texto, tamanho, cor, x, y):
    try:
        fonte = pygame.font.Font(fonte_path, tamanho)
    except FileNotFoundError:
        fonte = pygame.font.Font(None, tamanho)

    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect(center=(x, y))
    tela.blit(texto_surface, texto_rect)


def tela_game_over_cobel(tela, fonte_path, imagem_fundo):
    pygame.mixer.music.stop()
    caminho_som_cobel = os.path.join('audios', 'som_perdeu_cobel.mp3')
    if os.path.exists(caminho_som_cobel):
        som_derrota = pygame.mixer.Sound(caminho_som_cobel)
        som_derrota.set_volume(1.0)
        som_derrota.play()

    largura_tela = tela.get_width()
    altura_tela = tela.get_height()

    # Definição do Botão
    COR_BRANCO = (255, 255, 255)
    COR_BOTAO_NORMAL = (115, 160, 35)      
    COR_BOTAO_HOVER = (140, 195, 40)      

    # Posição e dimensões do botão
    botao_largura = 220
    botao_altura = 50
    
    # Botão centralizado na tela 
    botao_x = (constants.LARGURA - constants.LARGURA_BOTAO) // 2 + 60
    botao_y = constants.ALTURA // 2 + 220

    botao_rect = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)

    # Lógica de Interação no Loop 
    esperando = True
    while esperando:
        mouse_pos = pygame.mouse.get_pos()
        
        cor_botao_atual = COR_BOTAO_NORMAL
        if botao_rect.collidepoint(mouse_pos):
            cor_botao_atual = COR_BOTAO_HOVER

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT" 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(mouse_pos):
                    return "RESTART"

        # Desenho dos Elementos na Tela
        if imagem_fundo:
            tela.blit(imagem_fundo, (0, 0))
        else:
            tela.fill(constants.PRETO)


        # Lógica para desenhar o botão
        pygame.draw.rect(tela, cor_botao_atual, botao_rect, border_radius=10)
        mostrar_texto(tela, fonte_path, "RECOMEÇAR", 36, COR_BRANCO,
                      botao_rect.centerx, botao_rect.centery)

        pygame.display.flip()
    
    return "QUIT"