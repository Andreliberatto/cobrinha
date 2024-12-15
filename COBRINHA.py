import pygame
import random

# Inicializa o pygame
pygame.init()

# Definir cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (213, 50, 80)
VERDE = (0, 255, 0)
AZUL = (50, 153, 213)
CINZA = (169, 169, 169)
AMARELO = (255, 255, 0)
LARANJA = (255, 165, 0)

# Definir o tamanho da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Cobrinha")

# Configurações do relógio
relogio = pygame.time.Clock()

# Definir variáveis do jogo
tamanho_bloco = 20
velocidade_inicial = 15
nivel = 1
vidas = 3
pontuacao_maxima = 0

# Função para carregar fontes
def carregar_fonte(tamanho):
    return pygame.font.SysFont("comicsansms", tamanho)

# Função para desenhar a cobrinha
def nossa_cobrinha(lista_cobra, cor):
    for i, bloco in enumerate(lista_cobra):
        if i == 0:
            pygame.draw.rect(tela, cor, [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])  # Cabeça
        else:
            pygame.draw.rect(tela, VERDE, [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])  # Corpo

# Função para mostrar a pontuação e informações na tela
def pontuacao(score, nivel, vidas, high_score):
    fonte = carregar_fonte(25)
    valor = fonte.render(f"Pontuação: {score} | Nível: {nivel} | Vidas: {vidas} | High Score: {high_score}", True, BRANCO)
    tela.blit(valor, [10, 10])

# Função para desenhar obstáculos móveis
def desenhar_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, CINZA, [obstaculo[0], obstaculo[1], tamanho_bloco, tamanho_bloco])

# Função para criar obstáculos aleatórios
def gerar_obstaculos(n, largura, altura):
    return [[random.randrange(0, largura - tamanho_bloco, tamanho_bloco),
             random.randrange(0, altura - tamanho_bloco, tamanho_bloco)] for _ in range(n)]

# Função para criar alimentos especiais
def gerar_alimento_especial():
    tipo = random.choice(['normal', 'extra_pontos', 'velocidade', 'escudo'])
    x = round(random.randrange(0, LARGURA - tamanho_bloco) / 20.0) * 20.0
    y = round(random.randrange(0, ALTURA - tamanho_bloco) / 20.0) * 20.0
    return {'tipo': tipo, 'x': x, 'y': y}

# Função para a tela inicial
def tela_inicial():
    tela.fill(AZUL)
    fonte = carregar_fonte(50)
    texto = fonte.render("Jogo da Cobrinha", True, VERDE)
    tela.blit(texto, [LARGURA / 4, ALTURA / 3])

    fonte_menor = carregar_fonte(25)
    texto_instrucoes = fonte_menor.render("Pressione ENTER para jogar ou ESC para sair", True, BRANCO)
    tela.blit(texto_instrucoes, [LARGURA / 4, ALTURA / 2 + 50])

    pygame.display.update()

    # Espera pela entrada do usuário
    espera = True
    while espera:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if evento.key == pygame.K_RETURN:  # Alterado para ENTER
                    espera = False
                    jogo()

# Função para a tela de "Game Over"
def tela_game_over(pontos, high_score):
    tela.fill(AZUL)
    fonte = carregar_fonte(50)
    mensagem = fonte.render("Você perdeu!", True, VERMELHO)
    tela.blit(mensagem, [LARGURA / 3, ALTURA / 3])

    fonte_menor = carregar_fonte(25)
    mensagem_pontuacao = fonte_menor.render(f"Pontuação final: {pontos}", True, BRANCO)
    tela.blit(mensagem_pontuacao, [LARGURA / 3, ALTURA / 2])

    if pontos > high_score:
        high_score = pontos
        mensagem_high_score = fonte_menor.render(f"Novo High Score: {high_score}", True, AMARELO)
        tela.blit(mensagem_high_score, [LARGURA / 3, ALTURA / 1.7])

    fonte_instrucoes = carregar_fonte(25)
    mensagem_instrucoes = fonte_instrucoes.render("Pressione ENTER para jogar novamente ou ESC para sair", True, BRANCO)
    tela.blit(mensagem_instrucoes, [LARGURA / 6, ALTURA / 1.5])

    pygame.display.update()

    espera = True
    while espera:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Alterado para ESC
                    pygame.quit()
                    quit()
                if evento.key == pygame.K_RETURN:  # Alterado para ENTER
                    espera = False
                    jogo()

# Função principal do jogo
def jogo():
    global nivel, vidas, pontuacao_maxima
    game_over = False
    game_close = False
    pausa = False

    x1 = LARGURA / 2
    y1 = ALTURA / 2

    x1_mudar = 0
    y1_mudar = 0

    lista_cobra = []
    comprimento_cobra = 1

    # Posição inicial do alimento
    alimento = gerar_alimento_especial()

    # Pontuação inicial
    score = 0
    velocidade = velocidade_inicial
    obstaculos = gerar_obstaculos(3, LARGURA, ALTURA)  # Começar com 3 obstáculos
    cor_cobrinha = VERDE

    while not game_over:

        while game_close:
            tela_game_over(score, pontuacao_maxima)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if evento.key == pygame.K_RETURN:
                        jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and x1_mudar == 0:
                    x1_mudar = -tamanho_bloco
                    y1_mudar = 0
                elif evento.key == pygame.K_RIGHT and x1_mudar == 0:
                    x1_mudar = tamanho_bloco
                    y1_mudar = 0
                elif evento.key == pygame.K_UP and y1_mudar == 0:
                    y1_mudar = -tamanho_bloco
                    x1_mudar = 0
                elif evento.key == pygame.K_DOWN and y1_mudar == 0:
                    y1_mudar = tamanho_bloco
                    x1_mudar = 0

        if x1 >= LARGURA or x1 < 0 or y1 >= ALTURA or y1 < 0:
            vidas -= 1
            if vidas <= 0:
                game_close = True
            else:
                x1 = LARGURA / 2
                y1 = ALTURA / 2
                x1_mudar = 0
                y1_mudar = 0
                lista_cobra = []
                comprimento_cobra = 1

        x1 += x1_mudar
        y1 += y1_mudar
        tela.fill(AZUL)

        pygame.draw.rect(tela, VERMELHO, [alimento['x'], alimento['y'], tamanho_bloco, tamanho_bloco])

        lista_cabeça = []
        lista_cabeça.append(x1)
        lista_cabeça.append(y1)
        lista_cobra.append(lista_cabeça)

        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]

        for x in lista_cobra[:-1]:
            if x == lista_cabeça:
                vidas -= 1
                if vidas <= 0:
                    game_close = True
                else:
                    x1 = LARGURA / 2
                    y1 = ALTURA / 2
                    x1_mudar = 0
                    y1_mudar = 0
                    lista_cobra = []
                    comprimento_cobra = 1

        nossa_cobrinha(lista_cobra, cor_cobrinha)
        desenhar_obstaculos(obstaculos)

        pontuacao(score, nivel, vidas, pontuacao_maxima)

        # Verifica se a cobrinha comeu o alimento
        if x1 == alimento['x'] and y1 == alimento['y']:
            alimento = gerar_alimento_especial()  # Gerar novo alimento
            if alimento['tipo'] == 'normal':
                comprimento_cobra += 1
                score += 1
            elif alimento['tipo'] == 'extra_pontos':
                score += 5  # Ganhar mais pontos
            elif alimento['tipo'] == 'velocidade':
                velocidade += 5  # Aumenta a velocidade
            elif alimento['tipo'] == 'escudo':
                pass  # Apenas exemplo, sem poder especial por enquanto

        # Desenha a tela
        pygame.display.update()

        # Controla a velocidade do jogo
        relogio.tick(velocidade)

    pygame.quit()
    quit()

# Chama a tela inicial ao iniciar o jogo
tela_inicial()
