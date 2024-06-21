# Aqui foi tudo alterado:

# Menu de Seleção de Modo de Jogo:

# Adicionei um novo menu onde o jogador pode escolher entre diferentes modos de jogo: 
# Clássico 
# Cronometrado 
# Infinito 
# Multiplayer.

# Modos de Jogo (defenições):

# Modo Clássico: 
# O jogo continua como antes.

# Modo Cronometrado: 
# O jogador tem 1 minuto para alcançar a maior pontuação possível.

# Modo Infinito: 
# A cobra pode atravessar as bordas da tela e aparecer do lado oposto.

# Modo Multiplayer: 
# Dois jogadores podem jogar simultaneamente no mesmo teclado.

# Funções de Auxílio:

# Criação de funções como: 
# timed_mode
# display_timer (para estar constamtemente a atualizar o tempo)
# para auxiliar na implementação do modo cronometrado.

# Adição de lógica para multiplayer dentro da função game_loop.
# Melhoria de Código:

# Alteração de partes do código para melhorar a legibilidade e a organização.
# Uso de variáveis globais para configurações comuns do jogo.

# Esta versão tem menos botões secretos
#_________________________________________________________________________________________________________________________________
import pygame
import random
import datetime
from time import sleep

# Para aparecer o nome
AUTHOR = "Snake Game by Rodrigo Alves"

# Inicializando o Pygame
pygame.init()

# Definindo as cores Red, Green, Blue
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)

# Configurações da tela
WIDTH, HEIGHT = 1360, 656
BLOCK_SIZE = 20
FPS = 10

SNAKE_BLOCK = 10
SNAKE_LEVEL = 1
SNAKE_LEVEL_JUMP = 5

SNAKE_SPEED_JUMP = 1
SNAKE_SPEED = 0.5 + int(SNAKE_BLOCK * SNAKE_SPEED_JUMP)

# Inicializando a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(AUTHOR)

# Inicializando a fonte
font = pygame.font.SysFont(None, 30)

# Função para desenhar a cobrinha na tela
def draw_snake(snake_block, snake_list, color=GREEN):
    for x in snake_list:
        pygame.draw.rect(screen, color, [x[0], x[1], snake_block, snake_block])

# Função para exibir a pontuação na tela
def display_score(score, level):
    score_text = font.render("Pontuação: " + str(score), True, BLACK)
    screen.blit(score_text, [10, 10])
    score_text = font.render("Nível: " + str(level), True, BLACK)
    screen.blit(score_text, [1200, 10])

def display_duration(init):
    font = pygame.font.SysFont(None, 20)
    t_now = datetime.datetime.now()
    t_delta = t_now - init
    duration_text = font.render(f"Duration: {t_delta}", True, GRAY)
    screen.blit(duration_text, [10, 40])

# Função para salvar pontuações altas
def save_high_score(score):
    try:
        with open("high_scores.txt", "r") as file:
            high_scores = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        high_scores = []
    high_scores.append(score)
    high_scores = sorted(high_scores, reverse=True)[:5]  # Guarda apenas os top 5
    with open("high_scores.txt", "w") as file:
        for high_score in high_scores:
            file.write(str(high_score) + "\n")

def display_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            high_scores = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        high_scores = []
    y_offset = 100
    for idx, high_score in enumerate(high_scores):
        score_text = font.render(f"{idx + 1}. {high_score}", True, BLACK)
        screen.blit(score_text, [WIDTH / 2 - 50, y_offset])
        y_offset += 30

def game_menu():
    menu_options = ["Modo Clássico", "Modo Cronometrado", "Modo Infinito", "Modo Multiplayer", "Instruções", "Pontuações Altas", "Sair"]
    selected_option = 0
    menu = True
    while menu:
        screen.fill(WHITE)
        font_style = pygame.font.SysFont(None, 50)
        title = font_style.render("Snake Game", True, BLACK)
        screen.blit(title, [WIDTH / 3, HEIGHT / 5])
        for idx, option in enumerate(menu_options):
            if idx == selected_option:
                font_style = pygame.font.SysFont(None, 40, bold=True)
            else:
                font_style = pygame.font.SysFont(None, 40)
            message = font_style.render(option, True, BLACK)
            screen.blit(message, [WIDTH / 3, HEIGHT / 3 + idx * 50])
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
                    if selected_option == 0:  # Modo Clássico
                        game_loop("classic")
                    elif selected_option == 1:  # Modo Cronometrado
                        game_loop("timed")
                    elif selected_option == 2:  # Modo Infinito
                        game_loop("infinite")
                    elif selected_option == 3:  # Modo Multiplayer
                        game_loop("multiplayer")
                    elif selected_option == 4:  # Mostrar instruções
                        show_instructions()
                    elif selected_option == 5:  # Mostrar pontuações altas
                        display_high_scores()
                    elif selected_option == 6:  # Sair do jogo
                        pygame.quit()
                        quit()

def show_instructions():
    instructions = True
    while instructions:
        screen.fill(WHITE)
        font_style = pygame.font.SysFont(None, 50)
        message = font_style.render("Instruções", True, BLACK)
        screen.blit(message, [WIDTH / 3, HEIGHT / 4])
        font_style = pygame.font.SysFont(None, 30)
        instructions_text = [
            "Use as setas do teclado para mover a cobra.",
            "Coma a comida vermelha para crescer.",
            "Evite colidir com as bordas ou com a própria cobra.",
            "Pressione P para pausar o jogo."
        ]
        y_offset = HEIGHT / 2.5
        for line in instructions_text:
            instruction_message = font_style.render(line, True, BLACK)
            screen.blit(instruction_message, [WIDTH / 4, y_offset])
            y_offset += 30
        message = font_style.render("Pressione ESC para voltar ao menu", True, BLACK)
        screen.blit(message, [WIDTH / 4, y_offset + 50])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    instructions = False

def pause_game():
    paused = True
    while paused:
        screen.fill(WHITE)
        font_style = pygame.font.SysFont(None, 50)
        message = font_style.render("Jogo Pausado", True, BLACK)
        screen.blit(message, [WIDTH / 2.5, HEIGHT / 3])
        font_style = pygame.font.SysFont(None, 30)
        message = font_style.render("Pressione C para continuar ou Q para sair", True, BLACK)
        screen.blit(message, [WIDTH / 3, HEIGHT / 2])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def timed_mode():
    game_start_time = datetime.datetime.now()
    game_end_time = game_start_time + datetime.timedelta(minutes=1)
    return game_end_time

def display_timer(end_time):
    time_left = end_time - datetime.datetime.now()
    if time_left.total_seconds() < 0:
        return False
    timer_text = font.render(f"Tempo restante: {time_left.seconds}s", True, BLACK)
    screen.blit(timer_text, [WIDTH / 2 - 100, 10])
    return True

def game_loop(mode="classic"):
    global WHITE, GREEN, RED, BLACK
    global WIDTH, HEIGHT, BLOCK_SIZE, FPS
    global SNAKE_SPEED, SNAKE_SPEED_JUMP, SNAKE_BLOCK, SNAKE_LEVEL, SNAKE_LEVEL_JUMP
    global snake_level
    global snake_speed
    global snake_block
    global length_of_snake

    extra_food_count = 500

    # Configurações iniciais do jogo
    RESET_SNAKE = (SNAKE_SPEED, SNAKE_BLOCK, SNAKE_LEVEL, SNAKE_LEVEL_JUMP, 1)
    snake_speed, snake_block, snake_level, snake_level_jump, length_of_snake = RESET_SNAKE
    game_over = False
    game_close = False

    # Posições iniciais da cobra
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    init = datetime.datetime.now()

    snake_List = []
    Length_of_snake = 1

    # Geração da comida
    food_list = []
    foodx = round(random.randrange(snake_block, WIDTH - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(snake_block, HEIGHT - snake_block) / snake_block) * snake_block
    food_list.append((foodx, foody))

    if mode == "timed":
        game_end_time = timed_mode()

    if mode == "multiplayer":
        x2 = WIDTH / 4
        y2 = HEIGHT / 4
        x2_change = 0
        y2_change = 0
        snake_list_2 = []
        length_of_snake_2 = 1
        color_2 = BLUE

    # Loop principal do jogo
    while not game_over:
        while game_close:
            screen.fill(WHITE)
            font_style = pygame.font.SysFont(None, 50)
            message = font_style.render("Game Over", True, RED)
            screen.blit(message, [WIDTH / 3, HEIGHT / 3])
            score_text = font.render("Pontuação: " + str(length_of_snake - 1), True, BLACK)
            screen.blit(score_text, [WIDTH / 3, HEIGHT / 3 + 50])
            message = font.render("Pressione C para jogar novamente ou Q para sair", True, BLACK)
            screen.blit(message, [WIDTH / 5, HEIGHT / 3 + 100])
            save_high_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_menu()
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_game()
                # Botões especiais
                elif event.key == pygame.K_RCTRL or event.key == pygame.K_f:
                    x1 = random.randrange(0, WIDTH, snake_block)
                    y1 = random.randrange(0, HEIGHT, snake_block)
                elif event.key == pygame.K_RSHIFT or event.key == pygame.K_t:
                    for _ in range(5):
                        foodx = round(random.randrange(snake_block, WIDTH - snake_block) / snake_block) * snake_block
                        foody = round(random.randrange(snake_block, HEIGHT - snake_block) / snake_block) * snake_block
                        food_list.append((foodx, foody))

                if mode == "multiplayer":
                    if event.key == pygame.K_a:
                        x2_change = -snake_block
                        y2_change = 0
                    elif event.key == pygame.K_d:
                        x2_change = snake_block
                        y2_change = 0
                    elif event.key == pygame.K_w:
                        y2_change = -snake_block
                        x2_change = 0
                    elif event.key == pygame.K_s:
                        y2_change = snake_block
                        x2_change = 0
                    # Botões especiais
                    elif event.key == pygame.K_RCTRL or event.key == pygame.K_f:
                        x1 = random.randrange(0, WIDTH, snake_block)
                        y1 = random.randrange(0, HEIGHT, snake_block)
                    elif event.key == pygame.K_RSHIFT or event.key == pygame.K_t:
                        for _ in range(5):
                            foodx = round(random.randrange(snake_block, WIDTH - snake_block) / snake_block) * snake_block
                            foody = round(random.randrange(snake_block, HEIGHT - snake_block) / snake_block) * snake_block
                            food_list.append((foodx, foody))

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            if mode == "infinite":
                if x1 >= WIDTH:
                    x1 = 0
                elif x1 < 0:
                    x1 = WIDTH - snake_block
                elif y1 >= HEIGHT:
                    y1 = 0
                elif y1 < 0:
                    y1 = HEIGHT - snake_block
                # Botões especiais
                elif event.key == pygame.K_RCTRL or event.key == pygame.K_f:
                    x1 = random.randrange(0, WIDTH, snake_block)
                    y1 = random.randrange(0, HEIGHT, snake_block)
                elif event.key == pygame.K_RSHIFT or event.key == pygame.K_t:
                    for _ in range(5):
                        foodx = round(random.randrange(snake_block, WIDTH - snake_block) / snake_block) * snake_block
                        foody = round(random.randrange(snake_block, HEIGHT - snake_block) / snake_block) * snake_block
                        food_list.append((foodx, foody))
            else:
                game_close = True
        x1 += x1_change
        y1 += y1_change

        if mode == "multiplayer":
            if x2 >= WIDTH or x2 < 0 or y2 >= HEIGHT or y2 < 0:
                game_close = True
            x2 += x2_change
            y2 += y2_change

        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, [foodx, foody, snake_block, snake_block])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        if mode != "infinite":
            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_close = True

        if mode == "multiplayer":
            snake_head_2 = []
            snake_head_2.append(x2)
            snake_head_2.append(y2)
            snake_list_2.append(snake_head_2)
            if len(snake_list_2) > length_of_snake_2:
                del snake_list_2[0]

            for segment in snake_list_2[:-1]:
                if segment == snake_head_2:
                    game_close = True

            draw_snake(snake_block, snake_list_2, color=color_2)

        draw_snake(snake_block, snake_list)

        # Verificar se a cobra comeu a comida
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(snake_block, WIDTH - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(snake_block, HEIGHT - snake_block) / snake_block) * snake_block
            length_of_snake += 1
            if length_of_snake % extra_food_count == 0:
                snake_speed += SNAKE_SPEED_JUMP
                snake_level += SNAKE_LEVEL_JUMP

        if mode == "multiplayer" and abs(x2 - foodx) < snake_block and abs(y2 - foody) < snake_block:
            foodx = round(random.randrange(snake_block, WIDTH - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(snake_block, HEIGHT - snake_block) / snake_block) * snake_block
            length_of_snake_2 += 1

        display_score(length_of_snake - 1, snake_level)
        display_duration(init)
        if mode == "timed":
            if not display_timer(game_end_time):
                game_close = True

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

    pygame.quit()
    quit()

if __name__ == "__main__":
    game_menu()
