import pygame
import sys
import os
import constants

# FUNÇÕES AUXILIARES


def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "

        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines


def desenhar_texto_alinhado(surface, text, size, x, y, fonte_path, cor=constants.BRANCO, align="center"):
    try:
        fonte = pygame.font.Font(fonte_path, size)
    except:
        fonte = pygame.font.SysFont(None, size)

    text_surface = fonte.render(text, True, cor)
    text_rect = text_surface.get_rect()

    if align == "left":
        text_rect.topleft = (x, y)
    elif align == "right":
        text_rect.topright = (x, y)
    else:  # Padrão é 'center'
        text_rect.midtop = (x, y)

    surface.blit(text_surface, text_rect)
    return text_rect


def carregar_imagem_tutorial(nome_arquivo, escala):
    try:
        caminho = os.path.join('imagens', nome_arquivo)
        imagem = pygame.image.load(caminho).convert_alpha()
        largura, altura = imagem.get_size()
        nova_largura = int(largura * escala)
        nova_altura = int(altura * escala)
        return pygame.transform.scale(imagem, (nova_largura, nova_altura))
    except Exception as e:
        print(f"Erro ao carregar imagem para o tutorial: {nome_arquivo} - {e}")

        return pygame.Surface((int(50*escala), int(50*escala)), pygame.SRCALPHA)

# FUNÇÃO PRINCIPAL DA TELA DE TUTORIAL
def mostrar_tela_tutorial(tela, fonte_path, largura, altura):
    # --- CONFIGURAÇÕES ---
    COR_BOTAO = (31, 125, 83)           # cor normal
    COR_BOTAO_HOVER = (47, 191, 122)    # cor no hover
    COR_TEXTO_BOTAO = (255, 255, 255) 

    # --- CARREGAR IMAGENS ---
    img_mark = carregar_imagem_tutorial('mark_baixo.png', 0.06)
    img_logo_neurotreco = carregar_imagem_tutorial('logo_neurotreco.png', 0.22)
    img_chave = carregar_imagem_tutorial(constants.CHAVE, 1.2)
    img_pedaco_chave = carregar_imagem_tutorial('pedaco_chave.png', 0.15)
    img_porta = carregar_imagem_tutorial('porta.png', 2.1)
    img_setas = carregar_imagem_tutorial('setas.png', 0.1)
    img_wasd = carregar_imagem_tutorial('wasd.png', 0.1)
    img_balao = carregar_imagem_tutorial(constants.BALAO, 1.7)
    img_cafe = carregar_imagem_tutorial(constants.CAFE, 1.5)
    img_segurancas = carregar_imagem_tutorial('img_segurancas.png', 0.18)
    img_cobel = carregar_imagem_tutorial('cobel_baixo.png', 0.07)
    img_segurancas_block = carregar_imagem_tutorial('img_segurancas_block.png', 0.16)
    img_logo_tutorial = carregar_imagem_tutorial('logo_tutorial.png', 0.06)
    img_trevo = carregar_imagem_tutorial('trevo.png', 0.1)

    img_fundo_tutorial = pygame.image.load(os.path.join("imagens", "img_fundo_tutorial_att.png")).convert()
    img_fundo_tutorial = pygame.transform.scale(img_fundo_tutorial, (largura, altura))

    # --- CONTEÚDO DAS PÁGINAS ---
    paginas = [
        {
            "titulo": "OBJETIVO",
            "linhas": [
                {
                    "texto": "Você é Mark, um funcionário da Neurotreco",
                    "imgs": [img_mark],
                    # "inline_img": img_logo_neurotreco
                },
                {"texto": "Sua missão é escapar da empresa", "imgs": [img_logo_neurotreco]},
                {"texto": "Para isso, colete as 3 partes da chave...",
                    "imgs": [img_chave]},
                {"texto": "E use-as para abrir a porta de saída!",
                    "imgs": [img_porta]}
            ]
        },
        {
            "titulo": "ITENS/CONTROLES",
            "linhas": [
                {"texto": "Use as SETAS ou W,A,S,D para se mover pelo escritório", "imgs": [
                    img_setas, img_wasd]},
                {"texto": "Colete BALÕES para recuperar vidas perdidas",
                    "imgs": [img_balao]},
                {"texto": "Pegue o CAFÉ para se tornar invulnerável por um tempo",
                    "imgs": [img_cafe]}
            ]
        },
        {
            "titulo": "OS PERIGOS",
            "linhas": [
                {"texto": "Os SEGURANÇAS patrulham o local",
                    "imgs": [img_segurancas]},
                {"texto": "Evite-os para não perder vidas", "imgs": [img_segurancas_block]},
                {"texto": "COBEL é a chefe. Ser pego por ela é o fim do jogo!",
                    "imgs": [img_cobel]}
            ]
        },
        {
            "titulo": "DICA FINAL",
            "linhas": [
                {"texto": "A cada pedaço de chave coletado, um novo segurança aparece", "imgs": [img_pedaco_chave]},
                {"texto": "O desafio aumenta, então planeje seus movimentos e use o café com sabedoria", "imgs": [img_logo_tutorial]},
                {"texto": "Boa sorte na sua fuga!", "imgs": [img_trevo]}
            ]
        }
    ]

    pagina_atual = 0
    num_paginas = len(paginas)

    # CONFIGURAÇÃO DOS BOTÕES DE NAVEGAÇÃO
    fonte_botao = pygame.font.Font(fonte_path, 24)
    largura_botao = 110
    altura_botao = 50
    ret_voltar = pygame.Rect(
        largura / 2 - largura_botao / 2, altura - 70, largura_botao, altura_botao)
    texto_voltar = fonte_botao.render("INÍCIO", False, COR_TEXTO_BOTAO)
    ret_proximo = pygame.Rect(
        largura - largura_botao - 30, altura - 70, largura_botao, altura_botao)
    texto_proximo = fonte_botao.render("PRÓXIMO", False, COR_TEXTO_BOTAO)
    ret_anterior = pygame.Rect(30, altura - 70, largura_botao, altura_botao)
    texto_anterior = fonte_botao.render("VOLTAR", False, COR_TEXTO_BOTAO)

    tamanho_fonte_tutorial = 24
    fonte_tutorial = pygame.font.Font(fonte_path, tamanho_fonte_tutorial)
    pos_x_texto = 120
    margem_direita_texto = 30
    max_largura_texto = largura - pos_x_texto - margem_direita_texto

    # LOOP PRINCIPAL DO TUTORIAL
    relogio = pygame.time.Clock()
    mostrando_tutorial = True
    while mostrando_tutorial:
        tela.blit(img_fundo_tutorial, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        pagina = paginas[pagina_atual]
        
        # Desenha o Título
        fonte_titulo = pygame.font.Font(fonte_path, 48)  # Fonte base
        fonte_titulo.set_bold(True)  # Ativa negrito
        
        desenhar_texto_alinhado(
            tela, pagina["titulo"], 48, largura / 2, 50, fonte_path, align="center")

        # Posições e espaçamentos para o conteúdo
        pos_y_atual = 150
        pos_x_imgs = 50
        espaco_entre_linhas = 40

        # Loop para desenhar cada linha da página (texto + imagens)
        for linha in pagina["linhas"]:
            altura_imgs_total = 0

            # Desenha as imagens da linha (da coluna da esquerda)
            y_offset = 0
            for img in linha["imgs"]:
                if img in (img_setas, img_wasd, img_chave, img_logo_neurotreco):
                    img_rect = img.get_rect(topleft=(pos_x_imgs - 10, pos_y_atual + y_offset)) # coloca essas imagens mais pra esquerda
                elif img in (img_balao,img_trevo):
                    img_rect = img.get_rect(topleft=(pos_x_imgs + 5, pos_y_atual + y_offset)) # coloca essas imagens mais pra direita
                else:
                    img_rect = img.get_rect(topleft=(pos_x_imgs, pos_y_atual + y_offset))

                tela.blit(img, img_rect)
                y_offset += img.get_height() + 5
            altura_imgs_total = y_offset

            linhas_quebradas = wrap_text(
               linha["texto"], fonte_tutorial, max_largura_texto)

            y_texto_offset = 0
            for i, sub_linha in enumerate(linhas_quebradas):
                texto_renderizado = fonte_tutorial.render(
                    sub_linha, True, constants.BRANCO)

                y_pos_final = pos_y_atual + y_texto_offset

                if altura_imgs_total > 0 and i == 0:
                    altura_bloco_texto = len(
                        linhas_quebradas) * fonte_tutorial.get_linesize()
                    if altura_imgs_total > altura_bloco_texto:
                            
                        y_pos_final = pos_y_atual + \
                            (altura_imgs_total / 2) - \
                            (altura_bloco_texto / 2)
                            
                        y_texto_offset = (y_pos_final - pos_y_atual)

                tela.blit(texto_renderizado, (pos_x_texto, y_pos_final))
                y_texto_offset += fonte_tutorial.get_linesize()
            altura_total_texto = y_texto_offset
            

            # Calcula a altura da linha e atualiza a posição Y para o próximo item
            altura_linha = max(altura_imgs_total, altura_total_texto)
            pos_y_atual += altura_linha + espaco_entre_linhas

        # Desenha os Botões de Navegação
        cor_voltar = COR_BOTAO_HOVER if ret_voltar.collidepoint(
            mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela, cor_voltar, ret_voltar, border_radius=10)
        texto_rect_voltar = texto_voltar.get_rect(center=ret_voltar.center)
        tela.blit(texto_voltar, texto_rect_voltar)

        if pagina_atual < num_paginas - 1:
            cor_proximo = COR_BOTAO_HOVER if ret_proximo.collidepoint(
                mouse_pos) else COR_BOTAO
            pygame.draw.rect(tela, cor_proximo, ret_proximo, border_radius=10)
            texto_rect_proximo = texto_proximo.get_rect(
                center=ret_proximo.center)
            tela.blit(texto_proximo, texto_rect_proximo)

        if pagina_atual > 0:
            cor_anterior = COR_BOTAO_HOVER if ret_anterior.collidepoint(
                mouse_pos) else COR_BOTAO
            pygame.draw.rect(tela, cor_anterior,
                             ret_anterior, border_radius=10)
            texto_rect_anterior = texto_anterior.get_rect(
                center=ret_anterior.center)
            tela.blit(texto_anterior, texto_rect_anterior)

        pygame.display.flip()
        relogio.tick(constants.FPS if 'constants' in sys.modules and hasattr(
            constants, 'FPS') else 60)

        # Processa Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if ret_voltar.collidepoint(mouse_pos):
                    mostrando_tutorial = False
                if pagina_atual < num_paginas - 1 and ret_proximo.collidepoint(mouse_pos):
                    pagina_atual += 1
                if pagina_atual > 0 and ret_anterior.collidepoint(mouse_pos):
                    pagina_atual -= 1
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mostrando_tutorial = False
                if evento.key == pygame.K_RIGHT and pagina_atual < num_paginas - 1:
                    pagina_atual += 1
                if evento.key == pygame.K_LEFT and pagina_atual > 0:
                    pagina_atual -= 1
