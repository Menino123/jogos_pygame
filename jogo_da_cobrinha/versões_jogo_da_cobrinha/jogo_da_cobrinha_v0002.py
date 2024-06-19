# Aqui eu acrescentei o nível ao jogo
# (fazendo com que quando a pontuação ficasse 5, o nível subiria 1 e a velocidade subisse x), a terceira versão

import pygame
import random
 
AUTHOR = "Snake Game by Rodrigo Alves"
 
# Inicializando o Pygame
pygame.init()
 
# Definindo as cores Red, Green, Blue
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
 
# Configurações da tela
WIDTH, HEIGHT = 800, 700
BLOCK_SIZE = 20
FPS = 10
 
# Configurações da cobrinha
snake_speed = 15
snake_block = 10
 
snake_level = 5
snake_level_jump = 5
 
# Inicializando a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(AUTHOR)
 
# Função para desenhar a cobrinha na tela
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])
 
# Função para exibir a pontuação na tela
def display_score(score):
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("Pontuação: " + str(score), True, RED)
    screen.blit(score_text, [10, 10])
    score_text = font.render("Nível: " + str(snake_level), True, RED)
    screen.blit(score_text, [700, 10])

 
# Função principal do jogo
def gameLoop():
    game_over = False
    game_close = False
 
    # Posição inicial da cobra
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
 
    # Movimento inicial
    x1_change = 0
    y1_change = 0
 
    # Tamanho inicial da cobra
    snake_list = []
    length_of_snake = 1
 
    # Gerando a posição inicial da comida
    foodx = round(random.randrange(10, WIDTH - snake_block) / 10.0) * 10
    foody = round(random.randrange(10, HEIGHT - snake_block) / 10.0) * 10
 
    score = 0
 
    while not game_over:
 
        while game_close == True:
            screen.fill(WHITE)
            font_style = pygame.font.SysFont(None, 50)
            message = font_style.render("Você perdeu!", True, RED)
            screen.blit(message, [WIDTH / 3, HEIGHT / 3])
            font_style = pygame.font.SysFont(None, 25)
            message = font_style.render("Pressione Q para sair ou C para jogar novamente", True, BLACK)
            screen.blit(message, [WIDTH / 4.5, HEIGHT / 2])
            display_score(score)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
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
        # Verificando as bordas
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(WHITE)
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
        display_score(score)
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10
            foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10
            length_of_snake += 1
            score += 1
            if score % snake_level_jump == 0:
                snake_level = snake_level + 1

 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
# Inicializando o relógio
clock = pygame.time.Clock()
 
# Inicializando o jogo
gameLoop()
