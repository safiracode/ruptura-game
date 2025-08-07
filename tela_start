import pygame
import sys
import os

def mostrar_tela_start(tela, fonte_path, largura, altura):
    pygame.font.init()
    
    # --- Configurações básicas ---
    COR_FUNDO = (10, 20, 50)
    COR_TEXTO = (255, 255, 255)
    COR_BOTAO = (50, 50, 200)
    COR_BOTAO_HOVER = (80, 80, 255)
    COR_TEXTO_BOTAO = (255, 255, 255)
    TEXTO = "Pressione START para jogar"
    TAMANHO_FONTE = 36
    IMAGEM_NOME = "ruptura_logo.png"
    CAMINHO_IMAGEM = os.path.join("imagens", IMAGEM_NOME)
    
    #Fonte 
    try:
        fonte = pygame.font.Font(fonte_path, TAMANHO_FONTE)
    except:
        fonte = pygame.font.SysFont(None, TAMANHO_FONTE)

    #Imagem
    try:
        imagem = pygame.image.load(CAMINHO_IMAGEM)
        imagem = pygame.transform.scale(imagem, (300, 300))
    except:
        print(f"Erro ao carregar imagem: {CAMINHO_IMAGEM}")
        pygame.quit()
        sys.exit()

    #Texto
    texto_render = fonte.render(TEXTO, True, COR_TEXTO)
    texto_rect = texto_render.get_rect(center=(largura // 2, altura - 150))

    #Botão START
    texto_botao = "START"
    botao_render = fonte.render(texto_botao, True, COR_TEXTO_BOTAO)
    largura_botao = 200
    altura_botao = 60
    ret_botao = pygame.Rect(
        (largura - largura_botao) // 2,
        altura - 80,
        largura_botao,
        altura_botao
    )

    relogio = pygame.time.Clock()
    esperando = True

    while esperando:
        tela.fill(COR_FUNDO)
        tela.blit(imagem, imagem.get_rect(center=(largura // 2, altura // 2 - 50)))
        tela.blit(texto_render, texto_rect)

        # Verifica se o mouse está sobre o botão
        mouse_pos = pygame.mouse.get_pos()
        if ret_botao.collidepoint(mouse_pos):
            cor_botao_atual = COR_BOTAO_HOVER
        else:
            cor_botao_atual = COR_BOTAO

        pygame.draw.rect(tela, cor_botao_atual, ret_botao, border_radius=12)

        botao_texto_rect = botao_render.get_rect(center=ret_botao.center)
        tela.blit(botao_render, botao_texto_rect)

        pygame.display.flip()
        relogio.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    esperando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if ret_botao.collidepoint(evento.pos):
                    esperando = False

