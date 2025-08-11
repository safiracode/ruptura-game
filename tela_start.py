import pygame
import sys
import os
import constants

def mostrar_tela_start(tela, fonte_path, largura, altura):
    pygame.font.init()

    # Configurações básicas
    COR_FUNDO = (10, 20, 50)
    COR_BOTAO = (50, 50, 200)
    COR_BOTAO_HOVER = (80, 80, 255)
    COR_TEXTO_BOTAO = (255, 255, 255)
    TAMANHO_FONTE = 36
    
    CAMINHO_IMAGEM = os.path.join("imagens", "ruptura_start_recortado.png")

    # Fonte
    try:
        fonte = pygame.font.Font(fonte_path, TAMANHO_FONTE)
    except:
        fonte = pygame.font.SysFont(None, TAMANHO_FONTE)

    # Imagem
    imagem = None
    if CAMINHO_IMAGEM:
        try:
            imagem = pygame.image.load(CAMINHO_IMAGEM)
        except pygame.error as e:
            print(f"Erro ao carregar imagem: {CAMINHO_IMAGEM} - {e}")
            

    # Configuração dos Botões
    largura_botao = 200 
    altura_botao = 55   
    espaco_entre_botoes = 20

    # Posição X: Alinhada à direita com uma margem
    margem_direita = 20 
    pos_x_botoes = largura - largura_botao - margem_direita

    
    # Altura onde o primeiro botão vai começar.
    # AUMENTE para descer os botões, DIMINUA para subir.
    posicao_y_base = 320

    # Define um espaço entre a "base" e o primeiro botão
    espaco_abaixo_texto = 20

    # Posição Y do botão de cima (START)
    pos_y_start = posicao_y_base + espaco_abaixo_texto

    # Posição Y do botão de baixo (TUTORIAL)
    pos_y_tutorial = pos_y_start + altura_botao + espaco_entre_botoes


    # Botão START
    texto_start = "START"
    render_start = fonte.render(texto_start, True, COR_TEXTO_BOTAO)
    ret_botao_start = pygame.Rect(
        pos_x_botoes,
        pos_y_start,
        largura_botao,
        altura_botao
    )

    # Botão TUTORIAL
    texto_tutorial = "TUTORIAL"
    render_tutorial = fonte.render(texto_tutorial, True, COR_TEXTO_BOTAO)
    ret_botao_tutorial = pygame.Rect(
        pos_x_botoes,
        pos_y_tutorial,
        largura_botao,
        altura_botao
    )

    relogio = pygame.time.Clock()
    esperando = True
    acao = None

    while esperando:
        tela.fill(COR_FUNDO)
        if imagem:
             # Centraliza a imagem no topo
            pos_x_imagem = (largura - imagem.get_width()) // 2
            tela.blit(imagem, (pos_x_imagem, 0))

        mouse_pos = pygame.mouse.get_pos()

        # Cores padrão para os botões
        cor_start_atual = COR_BOTAO
        cor_tutorial_atual = COR_BOTAO
        
        if ret_botao_start.collidepoint(mouse_pos):
            cor_start_atual = COR_BOTAO_HOVER
        elif ret_botao_tutorial.collidepoint(mouse_pos):
            cor_tutorial_atual = COR_BOTAO_HOVER

        # Desenha o botão START
        pygame.draw.rect(tela, cor_start_atual, ret_botao_start, border_radius=25) # Aumentei o raio
        texto_rect_start = render_start.get_rect(center=ret_botao_start.center)
        tela.blit(render_start, texto_rect_start)

        # Desenha o botão TUTORIAL
        pygame.draw.rect(tela, cor_tutorial_atual, ret_botao_tutorial, border_radius=25) # Aumentei o raio
        texto_rect_tutorial = render_tutorial.get_rect(center=ret_botao_tutorial.center)
        tela.blit(render_tutorial, texto_rect_tutorial)

        pygame.display.flip()
        relogio.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if ret_botao_start.collidepoint(evento.pos):
                        acao = "START"
                        esperando = False
                    elif ret_botao_tutorial.collidepoint(evento.pos):
                        acao = "TUTORIAL"
                        esperando = False
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    acao = "START"
                    esperando = False

    return acao
