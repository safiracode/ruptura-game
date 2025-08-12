

import pygame
import os

# Supondo que suas constantes de cores e dimensões estejam em 'constants.py'
import constants

def mostrar_texto(tela, fonte_path, texto, tamanho, cor, x, y):
    """
    Função auxiliar para renderizar e centralizar texto na tela.
    """
    try:
        fonte = pygame.font.Font(fonte_path, tamanho)
    except FileNotFoundError:
        # Caso a fonte não seja encontrada, usa a fonte padrão do Pygame
        fonte = pygame.font.Font(None, tamanho)
        
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect(center=(x, y))
    tela.blit(texto_surface, texto_rect)

def tela_game_over_cobel(tela, fonte_path, imagem_fundo):
    """
    Exibe a tela de Game Over específica para a derrota pela Cobel.
    """
    # Para a música principal e toca o som de derrota da Cobel
    pygame.mixer.music.stop()
    
    # É uma boa prática verificar se o arquivo de áudio existe
    caminho_som_cobel = os.path.join('audios', 'som_perdeu_cobel.mp3')
    if os.path.exists(caminho_som_cobel):
        som_derrota = pygame.mixer.Sound(caminho_som_cobel)
        som_derrota.set_volume(1.0)
        som_derrota.play()

    # Define a imagem de fundo. Se não for encontrada, preenche com preto.
    if imagem_fundo:
        tela.blit(imagem_fundo, (0, 0))
    else:
        tela.fill(constants.PRETO)

    largura_tela = tela.get_width()
    altura_tela = tela.get_height()

    # Mensagens customizadas para a Cobel
    titulo = "VOCÊ FOI DESLIGADO"
    subtitulo = "A Gerência não tolera a ineficiência."
    instrucao = "Pressione qualquer tecla para retornar ao menu"

    # Cores (é melhor defini-las em seu arquivo constants.py)
    COR_VERMELHO_LUMON = (200, 0, 0)
    COR_BRANCO = (255, 255, 255)
    COR_AMARELO = (255, 255, 0)

    # Desenha as mensagens na tela
    mostrar_texto(tela, fonte_path, titulo, 60, COR_VERMELHO_LUMON, largura_tela / 2, altura_tela / 2 - 60)
    mostrar_texto(tela, fonte_path, subtitulo, 28, COR_BRANCO, largura_tela / 2, altura_tela / 2 + 10)
    mostrar_texto(tela, fonte_path, instrucao, 22, COR_AMARELO, largura_tela / 2, altura_tela - 100)
    
    pygame.display.flip()

    # Loop que aguarda o jogador pressionar uma tecla para continuar
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Sinaliza para fechar o jogo completamente
            if event.type == pygame.KEYUP:
                esperando = False

    # Reinicia a música principal antes de voltar ao menu
    pygame.mixer.music.play(-1)
    return True # Sinaliza para voltar ao menu