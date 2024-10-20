import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1360, 665
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Inicializando a fonte
font = pygame.font.SysFont(None, 30)

# Raquetes e bola
raquete_esquerda = pygame.Rect(50, HEIGHT // 3 - 50, 10, 100)
raquete_direita = pygame.Rect(WIDTH - 60, HEIGHT // 3 - 50, 10, 100)

# Pontuação dos jogadores
pontuacao_esquerda = 0
pontuacao_direita = 0

# Contador regressivo
contador = 5
fonte_contador = pygame.font.Font(None, 72)

def save_high_score(pontuacao_esquerda, pontuacao_direita):
    try:
        with open("high_scores.txt", "r") as file:
            high_scores = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        high_scores = []
    
    high_scores.append(pontuacao_esquerda)
    high_scores.append(pontuacao_direita)
    high_scores = sorted(high_scores, reverse=True)[:5]  # Guarda apenas os top 5
    
    with open("high_scores.txt", "w") as file:
        for high_score in high_scores:
            file.write(str(high_score) + "\n")

def show_instructions():
    instructions = True
    while instructions:
        tela.fill(preto)
        font_style = pygame.font.SysFont(None, 50)
        message = font_style.render("Instruções", True, branco)
        tela.blit(message, [WIDTH / 2, HEIGHT / 40])
            
        font_style = pygame.font.SysFont(None, 30)
        instructions_text = [
            "Use as setas do teclado para mover as raquetes:",
            "",
            "       W e S - para mover a raquete esquerda;",
            "",
            "       Seta baixo e cima - para mover a raquete direita;",
            "",
            "As raquetes devem bater na bola para marcar pontos.",
            "",
            "A cada rebatida bem-sucedida, a velocidade da bola aumenta.",
            "",
            "O jogo termina quando um jogador atinge 10 pontos.",
            "",
            "",
"______MODO VELOCIDADE________________________________________________________",
            "   A bola vai amentando de valocidade.",
            "",
            "",
"______MODO MULTIBOLA________________________________________________________",
            "   Vai haver TRÊS bolas no campo.",
            "",
            "",
"______MODO IA________________________________________________________",
            "   As regras são normais só que vais jogar contra uma IA"
            "",
            "",
            "Pressione P durante o jogo para pausar.",
            "",
            "Pressione ESC durante o jogo para voltar ao menu."
        ]
        y_offset = HEIGHT / 16 
        for line in instructions_text:
            instruction_message = font_style.render(line, True, branco)
            tela.blit(instruction_message, [WIDTH / 16, y_offset])
            y_offset += 20
            
        message = font_style.render("Pressione ESC para voltar ao menu", True, branco)
        tela.blit(message, [WIDTH / 4, y_offset + 50])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    instructions = False
            
        pygame.display.update()

def display_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            high_scores = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        high_scores = []

    y_offset = 100
    for idx, high_score in enumerate(high_scores):
        score_text = font.render(f"{idx + 1}. {high_score}", True, branco)
        tela.blit(score_text, [WIDTH / 2 - 50, y_offset])
        y_offset += 30

def modos_jogo_menu():
    modos_jogo_options = ["Clássico", "Desafio de Velocidade", "Multibola", "Contra IA", "Voltar"]
    selected_option = 0
    submenu = True
    while submenu:        
        tela.fill(preto)
        font_style = pygame.font.SysFont(None, 50)
        title = font_style.render("Modos de Jogo", True, branco)
        tela.blit(title, [WIDTH / 3, HEIGHT / 5])

        # Exibe as opções do submenu
        for idx, option in enumerate(modos_jogo_options):
            if idx == selected_option:
                font_style = pygame.font.SysFont(None, 40, bold=True)
            else:
                font_style = pygame.font.SysFont(None, 40)
            message = font_style.render(option, True, branco)
            tela.blit(message, [WIDTH / 3, HEIGHT / 3 + idx * 50])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(modos_jogo_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(modos_jogo_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Clássico
                        return "classico"
                    elif selected_option == 1:  # Desafio de Velocidade
                        return "desafio_velocidade"
                    elif selected_option == 2:  # Multibola
                        return "multibola"
                    elif selected_option == 3:  # Contra IA
                        return "contra_ia"
                    elif selected_option == 4:  # Voltar
                        return None

def game_menu():
    menu_options = ["Modos de Jogo", "Instruções", "Pontuações Altas", "Sair"]
    selected_option = 0
    menu = True
    while menu:        
        tela.fill(preto)
        font_style = pygame.font.SysFont(None, 50)
        title = font_style.render("Pong Game", True, branco)
        tela.blit(title, [WIDTH / 3, HEIGHT / 5])

        # Exibe as opções do menu
        for idx, option in enumerate(menu_options):
            if idx == selected_option:
                font_style = pygame.font.SysFont(None, 40, bold=True)
            else:
                font_style = pygame.font.SysFont(None, 40)
            message = font_style.render(option, True, branco)
            tela.blit(message, [WIDTH / 3, HEIGHT / 3 + idx * 50])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Modos de Jogo
                        mode = modos_jogo_menu()
                        if mode:
                            return mode
                    elif selected_option == 1:  # Mostrar instruções
                        show_instructions()
                    elif selected_option == 2:  # Mostrar pontuações altas
                        tela.fill(preto)
                        display_high_scores()
                        pygame.display.update()
                        pygame.time.delay(2000)
                    elif selected_option == 3:  # Sair do jogo
                        pygame.quit()
                        quit()

def pause_game():
    paused = True
    while paused:
        tela.fill(preto)
        font_style = pygame.font.SysFont(None, 50)
        message = font_style.render("Jogo Pausado", True, branco)
        tela.blit(message, [WIDTH / 2.5, HEIGHT / 3])
        
        font_style = pygame.font.SysFont(None, 30)
        message = font_style.render("Pressione C para continuar ou Q para sair", True, branco)
        tela.blit(message, [WIDTH / 3, HEIGHT / 2])
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    return game_menu ()

def game_loop(mode):
    global pontuacao_esquerda
    global pontuacao_direita
    global contador

    bola = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
    bola_velocidade_x = random.choice([-5, 5])  # Escolhe aleatoriamente a direção da bola
    bola_velocidade_y = random.choice([-5, 5])  # Escolhe aleatoriamente a direção da bola

    if mode == "desafio_velocidade":
        tempo_incremento = pygame.USEREVENT + 1
        velocidade_incremento = 0.1
        pygame.time.set_timer(tempo_incremento, 5000)  # Incrementa a velocidade a cada 5 segundos

    if mode == "multibola":
        bolas = [bola]
        bolas_velocidades = [(bola_velocidade_x, bola_velocidade_y)]
        tempo_multibola = pygame.USEREVENT + 2
        pygame.time.set_timer(tempo_multibola, 1000)  # Adiciona uma nova bola a cada 1 segundos

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            if mode == "desafio_velocidade" and event.type == tempo_incremento:
                bola_velocidade_x *= (1 + velocidade_incremento)
                bola_velocidade_y *= (1 + velocidade_incremento)
            
            if mode == "multibola" and event.type == tempo_multibola:
                nova_bola = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
                nova_velocidade_x = random.choice([-5, 5])
                nova_velocidade_y = random.choice([-5, 5])
                bolas.append(nova_bola)
                bolas_velocidades.append((nova_velocidade_x, nova_velocidade_y))

        teclas = pygame.key.get_pressed()

        # Movimento das raquetes
        if teclas[pygame.K_w] and raquete_esquerda.top > 0:
            raquete_esquerda.y -= 5
        if teclas[pygame.K_s] and raquete_esquerda.bottom < HEIGHT:
            raquete_esquerda.y += 5

        if mode == "contra_ia":
            # Movimento da raquete da IA
            if raquete_direita.centery < bola.centery and raquete_direita.bottom < HEIGHT:
                raquete_direita.y += 5
            if raquete_direita.centery > bola.centery and raquete_direita.top > 0:
                raquete_direita.y -= 5
        else:
            if teclas[pygame.K_UP] and raquete_direita.top > 0:
                raquete_direita.y -= 5
            if teclas[pygame.K_DOWN] and raquete_direita.bottom < HEIGHT:
                raquete_direita.y += 5

        if teclas[pygame.K_p]:
            pause_game()

        # Contagem regressiva antes de iniciar o jogo
        if contador > 0:
            tela.fill(preto)
            mensagem_contador = fonte_contador.render(str(contador), True, branco)
            tela.blit(mensagem_contador, (WIDTH // 2 - 20, HEIGHT // 2 - 20))
            pygame.display.flip()
            pygame.time.delay(1000)
            contador -= 1
            continue  # Continua no loop para aguardar o término da contagem regressiva

        # Atualização das bolas
        if mode == "classico" or mode == "desafio_velocidade" or mode == "contra_ia":
            bola.x += bola_velocidade_x
            bola.y += bola_velocidade_y

            # Colisões com as paredes
            if bola.top <= 0 or bola.bottom >= HEIGHT:
                bola_velocidade_y *= -1
            if bola.colliderect(raquete_esquerda) or bola.colliderect(raquete_direita):
                bola_velocidade_x *= -1

            # Verificação da pontuação
            if bola.left <= 0:
                pontuacao_direita += 1
                bola.x = WIDTH // 2 - 10
            elif bola.right >= WIDTH:
                pontuacao_esquerda += 1
                bola.x = WIDTH // 2 - 10

        elif mode == "multibola":
            for i in range(len(bolas)):
                bolas[i].x += bolas_velocidades[i][0]
                bolas[i].y += bolas_velocidades[i][1]

                # Colisões com as paredes
                if bolas[i].top <= 0 or bolas[i].bottom >= HEIGHT:
                    bolas_velocidades[i] = (bolas_velocidades[i][0], bolas_velocidades[i][1] * -1)
                if bolas[i].colliderect(raquete_esquerda) or bolas[i].colliderect(raquete_direita):
                    bolas_velocidades[i] = (bolas_velocidades[i][0] * -1, bolas_velocidades[i][1])

                # Verificação da pontuação
                if bolas[i].left <= 0:
                    pontuacao_direita += 1
                    bolas[i].x = WIDTH // 2 - 10
                elif bolas[i].right >= WIDTH:
                    pontuacao_esquerda += 1
                    bolas[i].x = WIDTH // 2 - 10

        # Desenho na tela
        tela.fill(preto)
        pygame.draw.rect(tela, branco, raquete_esquerda)
        pygame.draw.rect(tela, branco, raquete_direita)
        if mode == "classico" or mode == "desafio_velocidade" or mode == "contra_ia":
            pygame.draw.ellipse(tela, branco, bola)
        elif mode == "multibola":
            for bola in bolas:
                pygame.draw.ellipse(tela, branco, bola)

        # Exibição da pontuação
        fonte_pontuacao = pygame.font.Font(None, 36)
        texto_pontuacao = fonte_pontuacao.render(f"{pontuacao_esquerda} - {pontuacao_direita}", True, branco)
        tela.blit(texto_pontuacao, (WIDTH // 2 - 40, 10))

        # Verificação de vitória
        if pontuacao_esquerda == 10 or pontuacao_direita == 10:
            vencedor = "Esquerda" if pontuacao_esquerda == 10 else "Direita"
            save_high_score(pontuacao_esquerda, pontuacao_direita)
            while True:
                tela.fill(preto)
                mensagem_vitoria = fonte_pontuacao.render(f"Jogador {vencedor} Ganhou!", True, branco)
                mensagem_voltar_menu = fonte_pontuacao.render("Pressione ESC para voltar ao menu", True, branco)
                tela.blit(mensagem_vitoria, (WIDTH // 2 - 200, HEIGHT // 2 - 20))
                tela.blit(mensagem_voltar_menu, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
                pygame.display.flip()

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            return game_menu()

        pygame.display.flip()

        # Controle de velocidade
        pygame.time.Clock().tick(60)

    pygame.quit()

# Iniciar o jogo
while True:
    game_mode = game_menu()
    if game_mode:
        # Reset das variáveis antes de iniciar o jogo
        pontuacao_esquerda = 0
        pontuacao_direita = 0
        contador = 5
        game_loop(game_mode)
