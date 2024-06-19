# Aqui eu fiz teclas de beneficio e fiz o menu

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
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

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
    menu_options = ["Iniciar", "Instruções", "Pontuações Altas", "Sair"]
    selected_option = 0
    menu = True

    while menu:
        screen.fill(WHITE)
        font_style = pygame.font.SysFont(None, 50)
        title = font_style.render("Snake Game", True, BLACK)
        screen.blit(title, [WIDTH / 3, HEIGHT / 5])

        # Exibe as opções do menu
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
                    if selected_option == 0:  # Iniciar o jogo
                        menu = False
                    elif selected_option == 1:  # Mostrar instruções
                        show_instructions()
                    elif selected_option == 2:  # Mostrar pontuações altas
                        display_high_scores()
                    elif selected_option == 3:  # Sair do jogo
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

def gameLoop():
    global WHITE, GREEN, RED, BLACK
    global WIDTH, HEIGHT, BLOCK_SIZE, FPS
    global SNAKE_SPEED, SNAKE_SPEED_JUMP, SNAKE_BLOCK, SNAKE_LEVEL, SNAKE_LEVEL_JUMP
    global snake_level
    global snake_speed
    global snake_block
    global length_of_snake

    extra_food_count = 500

    while True:
        game_menu()  # Chama o menu inicial

        # Configurações iniciais do jogo
        RESET_SNAKE = (SNAKE_SPEED, SNAKE_BLOCK, SNAKE_LEVEL, SNAKE_LEVEL_JUMP, 1)
        snake_speed, snake_block, snake_level, snake_level_jump, length_of_snake = RESET_SNAKE
        snake_list = []

        RESET_GAME = (False, False, 0, (WIDTH // snake_block // 2) * snake_block, (HEIGHT // snake_block // 2) * snake_block, 0, 0)
        game_over, game_close, score, x1, y1, x1_change, y1_change = RESET_GAME

        food_list = []
        foodx = round(random.randrange(20, WIDTH - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(20, HEIGHT - snake_block) / snake_block) * snake_block
        food_list.append((foodx, foody))

        t_init = datetime.datetime.now()
        last_food_spawn_time = datetime.datetime.now()

        while not game_over:

            while game_close:
                screen.fill(WHITE)
                font_style = pygame.font.SysFont(None, 50)
                message = font_style.render("Você perdeu!", True, RED)
                screen.blit(message, [WIDTH / 2.5, HEIGHT / 3])
                
                font_style = pygame.font.SysFont(None, 30)
                message = font_style.render(f"Pontuação: {score}, Nível: {snake_level} ", True, BLACK)
                screen.blit(message, [WIDTH / 2.5, HEIGHT / 2.3])
                
                font_style = pygame.font.SysFont(None, 25)
                message = font_style.render("Pressione Q para voltar para o menu", True, BLACK)
                screen.blit(message, [WIDTH / 2.7, HEIGHT / 2])
                
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        elif event.key == pygame.K_c:
                            game_close = False
                            game_over = False  # Isso fará o loop principal do jogo reiniciar

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
                    elif event.key == pygame.K_RSHIFT:
                        snake_level += 20
                        score += 100
                    elif event.key == pygame.K_RCTRL:
                        snake_level = 1
                        score = 0
                    elif event.key == pygame.K_SPACE:
                        snake_speed += 5
                    elif event.key == pygame.K_LALT:
                        snake_speed -= 5
                    elif event.key == pygame.K_RALT:
                        snake_speed -= 20
                    elif event.key == pygame.K_z:
                        length_of_snake += 1
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_f:
                        current_time = datetime.datetime.now()
                        if (current_time - last_food_spawn_time).total_seconds() >= 30:
                            for _ in range(5):
                                foodx = round(random.randrange(snake_block, WIDTH - snake_block) / snake_block) * snake_block
                                foody = round(random.randrange(snake_block, HEIGHT - snake_block) / snake_block) * snake_block
                                food_list.append((foodx, foody))
                            last_food_spawn_time = current_time
                    elif event.key == pygame.K_LCTRL:
                        for _ in range(extra_food_count):
                            foodx = round(random.randrange(snake_block, WIDTH - snake_block) / snake_block) * snake_block
                            foody = round(random.randrange(snake_block, HEIGHT - snake_block) / snake_block) * snake_block
                            food_list.append((foodx, foody))

            if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
                game_close = True

            x1 += x1_change
            y1 += y1_change

            screen.fill(WHITE)
            for foodx, foody in food_list:
                pygame.draw.rect(screen, RED, [foodx, foody, snake_block, snake_block])
            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            draw_snake(snake_block, snake_list)
            display_score(score, snake_level)
            display_duration(t_init)
            pygame.display.update()

            for foodx, foody in food_list:
                if x1 == foodx and y1 == foody:
                    food_list.remove((foodx, foody))
                    length_of_snake += 1
                    score += 1
                    foodx = round(random.randrange(20, WIDTH - snake_block) / snake_block) * snake_block
                    foody = round(random.randrange(20, HEIGHT - snake_block) / snake_block) * snake_block
                    food_list.append((foodx, foody))
                    if score % snake_level_jump == 0:
                        snake_level += 1
                        snake_speed = int(SNAKE_SPEED * snake_level * SNAKE_SPEED_JUMP)

            clock.tick(snake_speed)

        save_high_score(score)

    pygame.quit()
    quit()

# Inicializando o relógio
clock = pygame.time.Clock()

# Inicializando o jogo
gameLoop()
