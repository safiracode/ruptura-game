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
    # Para a música principal e toca o som de derrota da Cobel
    pygame.mixer.music.stop()

    caminho_som_cobel = os.path.join('audios', 'som_perdeu_cobel.mp3')
    if os.path.exists(caminho_som_cobel):
        som_derrota = pygame.mixer.Sound(caminho_som_cobel)
        som_derrota.set_volume(1.0)
        som_derrota.play()

    # Define a imagem de fundo
    if imagem_fundo:
        tela.blit(imagem_fundo, (0, 0))
    else:
        tela.fill(constants.PRETO)

    largura_tela = tela.get_width()
    altura_tela = tela.get_height()

    # Mensagens customizadas para a Cobel
    titulo = ""
    subtitulo = ""
    instrucao = ""

    # Cores
    COR_VERMELHO_LUMON = (200, 0, 0)
    COR_BRANCO = (255, 255, 255)
    COR_AMARELO = (255, 255, 0)

    # Desenha as mensagens na tela
    mostrar_texto(tela, fonte_path, titulo, 60, COR_VERMELHO_LUMON,
                  largura_tela / 2, altura_tela / 2 - 60)
    mostrar_texto(tela, fonte_path, subtitulo, 28, COR_BRANCO,
                  largura_tela / 2, altura_tela / 2 + 10)
    mostrar_texto(tela, fonte_path, instrucao, 22, COR_AMARELO,
                  largura_tela / 2, altura_tela - 100)

    pygame.display.flip()

    # Loop que aguarda o jogador pressionar uma tecla para continuar
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYUP:
                esperando = False

    pygame.mixer.music.play(-1)
    return True