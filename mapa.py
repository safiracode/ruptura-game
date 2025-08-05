# Arquivo: mapa.py (Versão Final com Variedade e Espaçamento)
import random
import constants

# As constantes de tamanho continuam as mesmas
ALTURA_GRADE = int((constants.ALTURA * 0.85) // constants.TAMANHO_BLOCO)
LARGURA_GRADE = constants.LARGURA // constants.TAMANHO_BLOCO
ALTURA_INTERFACE_INFERIOR = constants.ALTURA - (ALTURA_GRADE * constants.TAMANHO_BLOCO)

PAREDE = 1
PISO = 0

def gerar_mapa_aleatorio(largura, altura):
    """
    Gera um mapa com T, L e linhas, garantindo espaçamento e sem formar quadrados.
    """
    # 1. Começa com uma grade cheia de PISO
    grade = [[PISO for _ in range(largura)] for _ in range(altura)]

    # 2. Constrói a "muralha" ao redor do mapa
    for x in range(largura):
        grade[0][x] = PAREDE
        grade[altura - 1][x] = PAREDE
    for y in range(altura):
        grade[y][0] = PAREDE
        grade[y][largura - 1] = PAREDE
        
    # --- MODELOS DE OBSTÁCULOS FINOS ESTÃO DE VOLTA ---
    obstaculos_modelos = [
        # Linhas
        [[1, 1, 1]], [[1, 1, 1, 1]],
        [[1], [1], [1]], [[1], [1], [1], [1]],
        # Cantos (L) - Todas as 4 rotações
        [[1, 1], [1, 0]], [[1, 1], [0, 1]],
        [[1, 0], [1, 1]], [[0, 1], [1, 1]],
        # Formas de T - Todas as 4 rotações
        [[1, 1, 1], [0, 1, 0]], [[0, 1, 0], [1, 1, 1]],
        [[1, 0], [1, 1], [1, 0]], [[0, 1], [1, 1], [0, 1]]
    ]

    # Aumentado para um mapa bem mais cheio
    tentativas_de_colocacao = 100
    gerar_simetrico = True

    # 3. Tenta colocar os obstáculos variados
    for _ in range(tentativas_de_colocacao):
        obstaculo = random.choice(obstaculos_modelos)
        obs_altura = len(obstaculo)
        obs_largura = len(obstaculo[0])

        pos_x = random.randrange(2, largura - obs_largura - 2)
        pos_y = random.randrange(2, altura - obs_altura - 2)

        # A "Regra de Ouro": Verifica a área de segurança ao redor do obstáculo
        area_ok = True
        for y_verif in range(pos_y - 1, pos_y + obs_altura + 1):
            for x_verif in range(pos_x - 1, pos_x + obs_largura + 1):
                if grade[y_verif][x_verif] == PAREDE:
                    area_ok = False; break
            if not area_ok: break
        
        # Se a área estiver limpa, coloca o obstáculo
        if area_ok:
            for y_obs in range(obs_altura):
                for x_obs in range(obs_largura):
                    if obstaculo[y_obs][x_obs] == 1:
                        grade[pos_y + y_obs][pos_x + x_obs] = PAREDE
                        if gerar_simetrico:
                            x_espelhado = largura - 1 - (pos_x + x_obs)
                            grade[pos_y + y_obs][x_espelhado] = PAREDE

    # 4. "Fiscal Anti-Quadrados" como garantia final
    for y in range(altura - 1):
        for x in range(largura - 1):
            if (grade[y][x] == PAREDE and grade[y+1][x] == PAREDE and
                grade[y][x+1] == PAREDE and grade[y+1][x+1] == PAREDE):
                grade[y + random.randint(0, 1)][x + random.randint(0, 1)] = PISO

    return grade