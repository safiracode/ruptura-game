import pygame
import sys
import os
import constants

# Funções Auxiliares para Texto e Imagens

def desenhar_texto(surface, text, size, x, y, fonte_path, cor=constants.BRANCO):

    try:
        fonte = pygame.font.Font(fonte_path, size)
    except:
        fonte = pygame.font.SysFont(None, size)
    
    text_surface = fonte.render(text, True, cor)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect # Retorna para obter a altura e usar como referência

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
        # Cria uma superfície vazia se a imagem não for encontrada
        return pygame.Surface((int(50*escala), int(50*escala)), pygame.SRCALPHA)


# Função Principal do Tutorial

def mostrar_tela_tutorial(tela, fonte_path, largura, altura):
  
    # Configurações 
    COR_FUNDO = (10, 20, 50)
    COR_BOTAO = (50, 50, 200)
    COR_BOTAO_HOVER = (80, 80, 255)
    COR_TEXTO_BOTAO = (255, 255, 255)

    # Carregar Imagens do Tutorial
    img_mark = carregar_imagem_tutorial('mark.png', 1.5)
    img_chave = carregar_imagem_tutorial(constants.CHAVE, 1.2)
    img_porta = carregar_imagem_tutorial('porta.png', 1.5)
    img_setas = carregar_imagem_tutorial('setas.png', 1.0) # Você precisará de uma imagem 'setas.png'
    img_wasd = carregar_imagem_tutorial('wasd.png', 1.0) # Você precisará de uma imagem 'wasd.png'
    img_balao = carregar_imagem_tutorial(constants.BALAO, 1.5)
    img_cafe = carregar_imagem_tutorial(constants.CAFE, 1.5)
    img_seguranca = carregar_imagem_tutorial('milchick.png', 1.5) # Usando um segurança como exemplo
    img_cobel = carregar_imagem_tutorial('cobel.png', 1.5)

    # --- Conteúdo das Páginas ---
    paginas = [
        {
            "titulo": "OBJETIVO",
            "textos": [
                "Você é Mark, um funcionário da Lumon.",
                "Sua missão é escapar do andar seccionado.",
                "Para isso, colete as 4 partes da chave",
                "e abra a porta de saída."
            ],
            "imagens": [
                (img_mark, largura * 0.25, altura * 0.5),
                (img_chave, largura * 0.5, altura * 0.5),
                (img_porta, largura * 0.75, altura * 0.5)
            ]
        },
        {
            "titulo": "ITENS E CONTROLES",
            "textos": [
                "Use as SETAS ou W,A,S,D para mover.",
                "Colete BALÕES para recuperar vidas.",
                "Pegue o CAFÉ para invencibilidade temporária."
            ],
            "imagens": [
                (img_setas, largura * 0.25, altura * 0.4),
                (img_wasd, largura * 0.25, altura * 0.6),
                (img_balao, largura * 0.5, altura * 0.5),
                (img_cafe, largura * 0.75, altura * 0.5)
            ]
        },
        {
            "titulo": "OS PERIGOS",
            "textos": [
                "Os SEGURANÇAS patrulham o local.",
                "Evite-os para não perder vidas.",
                "Harmony COBEL é a chefe. Um toque é fatal!",
                "Fique longe dela a todo custo."
            ],
            "imagens": [
                (img_seguranca, largura * 0.33, altura * 0.55),
                (img_cobel, largura * 0.66, altura * 0.55)
            ]
        },
        {
            "titulo": "DICA FINAL",
            "textos": [
                "A cada parte da chave coletada, um novo",
                "segurança aparecerá no mapa.",
                "O desafio aumenta, então planeje seus",
                "movimentos e use o café com sabedoria.",
                "Boa sorte!"
            ],
            "imagens": []
        }
    ]
    
    pagina_atual = 0
    num_paginas = len(paginas)

    # Botões de Navegação 
    fonte_botao = pygame.font.Font(fonte_path, 24)
    largura_botao = 140
    altura_botao = 50
    
    # Botão Voltar ao Menu
    ret_voltar = pygame.Rect(largura / 2 - largura_botao / 2, altura - 70, largura_botao, altura_botao)
    texto_voltar = fonte_botao.render("VOLTAR", True, COR_TEXTO_BOTAO)

    # Botões Próximo e Anterior
    ret_proximo = pygame.Rect(largura - largura_botao - 30, altura - 70, largura_botao, altura_botao)
    texto_proximo = fonte_botao.render("PRÓXIMO >", True, COR_TEXTO_BOTAO)
    
    ret_anterior = pygame.Rect(30, altura - 70, largura_botao, altura_botao)
    texto_anterior = fonte_botao.render("< ANTERIOR", True, COR_TEXTO_BOTAO)

    # Loop do Tutorial 
    relogio = pygame.time.Clock()
    mostrando_tutorial = True
    while mostrando_tutorial:
        tela.fill(COR_FUNDO)
        mouse_pos = pygame.mouse.get_pos()

        # Desenhar Conteúdo da Página Atual 
        pagina = paginas[pagina_atual]
        
        # Título
        desenhar_texto(tela, pagina["titulo"], 48, largura / 2, 50, fonte_path)

        # Textos
        pos_y_texto = 150
        for linha in pagina["textos"]:
            rect = desenhar_texto(tela, linha, 28, largura / 2, pos_y_texto, fonte_path)
            pos_y_texto += rect.height + 10 

        # Imagens
        for img, x, y in pagina["imagens"]:
            rect_img = img.get_rect(center=(x, y))
            tela.blit(img, rect_img)
            
        # Desenhar Botões
        # Botão Voltar
        cor_voltar = COR_BOTAO_HOVER if ret_voltar.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela, cor_voltar, ret_voltar, border_radius=10)
        texto_rect = texto_voltar.get_rect(center=ret_voltar.center)
        tela.blit(texto_voltar, texto_rect)

        # Botão Próximo
        if pagina_atual < num_paginas - 1:
            cor_proximo = COR_BOTAO_HOVER if ret_proximo.collidepoint(mouse_pos) else COR_BOTAO
            pygame.draw.rect(tela, cor_proximo, ret_proximo, border_radius=10)
            texto_rect = texto_proximo.get_rect(center=ret_proximo.center)
            tela.blit(texto_proximo, texto_rect)

        # Botão Anterior
        if pagina_atual > 0:
            cor_anterior = COR_BOTAO_HOVER if ret_anterior.collidepoint(mouse_pos) else COR_BOTAO
            pygame.draw.rect(tela, cor_anterior, ret_anterior, border_radius=10)
            texto_rect = texto_anterior.get_rect(center=ret_anterior.center)
            tela.blit(texto_anterior, texto_rect)

        pygame.display.flip()
        relogio.tick(constants.FPS)

        # Processar Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    # Clicou em Voltar
                    if ret_voltar.collidepoint(mouse_pos):
                        mostrando_tutorial = False # Fecha o tutorial e volta ao menu
                    
                    # Clicou em Próximo
                    if pagina_atual < num_paginas - 1 and ret_proximo.collidepoint(mouse_pos):
                        pagina_atual += 1

                    # Clicou em Anterior
                    if pagina_atual > 0 and ret_anterior.collidepoint(mouse_pos):
                        pagina_atual -= 1
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mostrando_tutorial = False
                if evento.key == pygame.K_RIGHT and pagina_atual < num_paginas - 1:
                     pagina_atual += 1
                if evento.key == pygame.K_LEFT and pagina_atual > 0:
                     pagina_atual -= 1
