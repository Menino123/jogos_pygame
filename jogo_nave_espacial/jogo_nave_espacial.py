import pygame
import random
import os

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1364
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Nave Espacial")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 255, 0)

# Carregar imagens com caminhos relativos
base_path = os.path.dirname(__file__)
background_image = pygame.image.load(os.path.join(base_path, "imagens/background_space.png"))
player_image = pygame.image.load(os.path.join(base_path, "imagens/spaceship.png"))
meteor_image = pygame.image.load(os.path.join(base_path, "imagens/meteor.png"))
star_image = pygame.image.load(os.path.join(base_path, "imagens/star.png"))

# Configurações do jogador
player_size = 60
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 2 * player_size
player_speed = 15

# Configurações dos meteoros e estrelas
meteor_size = 25
star_size = 30
meteor_speed = 5
star_speed = 10
meteor_list = []
star_list = []

# Configurações dos lasers
laser_width = 10
laser_height = 30
laser_speed = 10
laser_color = RED
laser_list = []

# Relógio
clock = pygame.time.Clock()

# Pontuação
score = 0

# Nível
level = 1

# Função para desenhar o jogador
def draw_player(x, y):
    screen.blit(pygame.transform.scale(player_image, (player_size, player_size)), (x, y))

# Função para desenhar meteoros
def draw_meteors(meteors):
    for meteor in meteors:
        screen.blit(pygame.transform.scale(meteor_image, (meteor_size, meteor_size)), (meteor[0], meteor[1]))

# Função para desenhar estrelas
def draw_stars(stars):
    for star in stars:
        screen.blit(pygame.transform.scale(star_image, (star_size, star_size)), (star[0], star[1]))

# Função para desenhar lasers
def draw_lasers(lasers):
    for laser in lasers:
        pygame.draw.rect(screen, laser_color, pygame.Rect(laser[0], laser[1], laser_width, laser_height))

# Função para verificar colisão
def check_collision(obj1, obj2, size1, size2):
    return (obj1[0] < obj2[0] + size2 and
            obj1[0] + size1 > obj2[0] and
            obj1[1] < obj2[1] + size2 and
            obj1[1] + size1 > obj2[1])

# Função para reiniciar o jogo
def reset_game():
    global player_x, player_y, meteor_list, star_list, laser_list, score, level
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - 2 * player_size
    meteor_list = []
    star_list = []
    laser_list = []
    score = 0
    level = 1

# Função principal do jogo
def game_loop():
    global player_x, player_y, meteor_list, star_list, laser_list, score, level
    running = True
    game_over = False

    while running:
        if game_over:
            font = pygame.font.SysFont(None, 50)
            text = font.render(f"Há, perdeu o jogo!", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 50))
            text = font.render(f"Score: {score}, Level: {level} ", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            text = font.render("Pressione Q para sair ou C para recomeçar", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 + 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_c:
                        game_over = False
                        reset_game()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        laser_list.append([player_x + player_size // 2 - laser_width // 2, player_y])

            # Movimento do jogador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
                player_x += player_speed

            # Adicionar meteoros
            if random.randint(1, 20) == 1:
                meteor_list.append([random.randint(0, SCREEN_WIDTH - meteor_size), -meteor_size])

            # Adicionar estrelas
            if random.randint(1, 50) == 1:
                star_list.append([random.randint(0, SCREEN_WIDTH - star_size), -star_size])

            # Mover meteoros
            for meteor in meteor_list:
                meteor[1] += meteor_speed * level
            meteor_list = [meteor for meteor in meteor_list if meteor[1] < SCREEN_HEIGHT]

            # Mover estrelas
            for star in star_list:
                star[1] += star_speed * level
            star_list = [star for star in star_list if star[1] < SCREEN_HEIGHT]

            # Mover lasers
            for laser in laser_list:
                laser[1] -= laser_speed
            laser_list = [laser for laser in laser_list if laser[1] > 0]

            # Verificar colisões de lasers com meteoros e estrelas
            for laser in laser_list:
                for meteor in meteor_list:
                    if check_collision(laser, meteor, laser_width, meteor_size):
                        meteor_list.remove(meteor)
                        laser_list.remove(laser)
                        score += 1
                        break
                for star in star_list:
                    if check_collision(laser, star, laser_width, star_size):
                        star_list.remove(star)
                        laser_list.remove(laser)
                        score += 1
                        break

            # Verificar se o jogador subiu de nível
            if score // 50 + 1 > level:
                level = score // 50 + 1

            # Verificar colisões da nave com meteoros e estrelas
            for meteor in meteor_list:
                if check_collision(meteor, [player_x, player_y], meteor_size, player_size):
                    game_over = True
                    break
            for star in star_list:
                if check_collision(star, [player_x, player_y], star_size, player_size):
                    game_over = True
                    break

            # Desenhar tudo na tela
            screen.blit(pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            draw_player(player_x, player_y)
            draw_meteors(meteor_list)
            draw_stars(star_list)
            draw_lasers(laser_list)

            # Desenhar pontuação
            font = pygame.font.SysFont(None, 30)
            text = font.render(f"Score: {score}", True, RED)
            screen.blit(text, [10, 10])

            # Desenhar nível
            text = font.render(f"Level: {level}", True, RED)
            screen.blit(text, [10, 40])

            pygame.display.flip()
            clock.tick(30)

    pygame.quit()

# Iniciar o jogo
game_loop()