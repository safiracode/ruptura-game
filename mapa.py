import random
import constants

# As constantes de tamanho continuam as mesmas
ALTURA_GRADE = int((constants.ALTURA * 0.85) // constants.TAMANHO_BLOCO)
LARGURA_GRADE = constants.LARGURA // constants.TAMANHO_BLOCO
ALTURA_INTERFACE_INFERIOR = constants.ALTURA - (ALTURA_GRADE * constants.TAMANHO_BLOCO)

PAREDE = 1
PISO = 0
PORTA = 2

def gerar_mapa_aleatorio(largura, altura):
    # GERA UM LABIRINTO
    # 1. Começa com uma grade cheia de PAREDES
    grade = [[PAREDE for _ in range(largura)] for _ in range(altura)]

    # 2. Cava os corredores
    pilha = []
    x_inicio = random.choice(range(1, largura, 2))
    y_inicio = random.choice(range(1, altura, 2))
    grade[y_inicio][x_inicio] = PISO
    pilha.append((x_inicio, y_inicio))

    while pilha:
        x, y = pilha[-1]
        vizinhos = []
        if y > 1 and grade[y - 2][x] == PAREDE: vizinhos.append((x, y - 2, x, y - 1))
        if y < altura - 2 and grade[y + 2][x] == PAREDE: vizinhos.append((x, y + 2, x, y + 1))
        if x > 1 and grade[y][x - 2] == PAREDE: vizinhos.append((x - 2, y, x - 1, y))
        if x < largura - 2 and grade[y][x + 2] == PAREDE: vizinhos.append((x + 2, y, x + 1, y))
        
        if vizinhos:
            x_novo, y_novo, x_meio, y_meio = random.choice(vizinhos)
            grade[y_meio][x_meio] = PISO
            grade[y_novo][x_novo] = PISO
            pilha.append((x_novo, y_novo))
        else:
            pilha.pop()

    # 3. Remove os becos sem saída
    becos_sem_saida = []
    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            if grade[y][x] == PISO:
                vizinhos_parede = 0
                if grade[y-1][x] == PAREDE: vizinhos_parede += 1
                if grade[y+1][x] == PAREDE: vizinhos_parede += 1
                if grade[y][x-1] == PAREDE: vizinhos_parede += 1
                if grade[y][x+1] == PAREDE: vizinhos_parede += 1
                if vizinhos_parede >= 3: becos_sem_saida.append((x, y))

    for x, y in becos_sem_saida:
        paredes_adjacentes = []
        if y > 1 and grade[y-1][x] == PAREDE: paredes_adjacentes.append((x, y-1))
        if y < altura - 2 and grade[y+1][x] == PAREDE: paredes_adjacentes.append((x, y+1))
        if x > 1 and grade[y][x-1] == PAREDE: paredes_adjacentes.append((x-1, y))
        if x < largura - 2 and grade[y][x+1] == PAREDE: paredes_adjacentes.append((x+1, y))
        if paredes_adjacentes:
            px, py = random.choice(paredes_adjacentes)
            grade[py][px] = PISO
            
    # 4. Cria loops e atalhos extras
    loops_extras_a_criar = 50 
    for _ in range(loops_extras_a_criar):
        x = random.randrange(1, largura - 1)
        y = random.randrange(1, altura - 1)
        if grade[y][x] == PAREDE:
            if (grade[y-1][x] == PISO and grade[y+1][x] == PISO):
                grade[y][x] = PISO
            elif (grade[y][x-1] == PISO and grade[y][x+1] == PISO):
                grade[y][x] = PISO

    # Limpa as paredes que correm paralelas à muralha externa.
    chance_de_limpar_borda = 0.80 # 80% de chance de remover uma parede paralela

    # Limpa borda de cima (linha y=1)
    for x in range(1, largura - 1):
        if grade[1][x] == PAREDE and (grade[1][x-1] == PAREDE or grade[1][x+1] == PAREDE):
            if random.random() < chance_de_limpar_borda: grade[1][x] = PISO
    # Limpa borda de baixo (linha y = altura-2)
    for x in range(1, largura - 1):
        if grade[altura-2][x] == PAREDE and (grade[altura-2][x-1] == PAREDE or grade[altura-2][x+1] == PAREDE):
            if random.random() < chance_de_limpar_borda: grade[altura-2][x] = PISO
    # Limpa borda da esquerda (coluna x=1)
    for y in range(1, altura - 1):
        if grade[y][1] == PAREDE and (grade[y-1][1] == PAREDE or grade[y+1][1] == PAREDE):
            if random.random() < chance_de_limpar_borda: grade[y][1] = PISO
    # Limpa borda da direita (coluna x = largura-2)
    for y in range(1, altura - 1):
        if grade[y][largura-2] == PAREDE and (grade[y-1][largura-2] == PAREDE or grade[y+1][largura-2] == PAREDE):
            if random.random() < chance_de_limpar_borda: grade[y][largura-2] = PISO
    # Este passo garante que a moldura do mapa esteja sempre intacta.
    for x in range(largura):
        grade[0][x] = PAREDE
        grade[altura - 1][x] = PAREDE
    for y in range(altura):
        grade[y][0] = PAREDE
        grade[y][largura - 1] = PAREDE

    return grade