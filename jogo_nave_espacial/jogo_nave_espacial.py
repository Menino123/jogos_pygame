import pygame
import random

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

# Carregar imagens
background_image = pygame.image.load(r"C:\Python_codes\Jogos\jogos_pygame\nave_espacial\imagens\background_space.png")    # têm que pôr vocês o vosso nome da pasta pois varia de computador para computador
player_image = pygame.image.load(r"C:\Python_codes\Jogos\jogos_pygame\nave_espacial\imagens\spaceship.png")               # têm que pôr vocês o vosso nome da pasta pois varia de computador para computador
meteor_image = pygame.image.load(r"C:\Python_codes\Jogos\jogos_pygame\nave_espacial\imagens\meteor.png")                  # têm que pôr vocês o vosso nome da pasta pois varia de computador para computador
star_image = pygame.image.load(r"C:\Python_codes\Jogos\jogos_pygame\nave_espacial\imagens\star.png")                      # têm que pôr vocês o vosso nome da pasta pois varia de computador para computador

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
                        player_x = SCREEN_WIDTH // 2
                        player_y = SCREEN_HEIGHT - 2 * player_size
                        meteor_list = []
                        star_list = []
                        laser_list = []
                        score = 0
                        level = 1
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

            # Verificar colisões de lasers com meteoros
            for laser in laser_list:
                for meteor in meteor_list:
                    if (meteor[0] < laser[0] + laser_width and
                        meteor[0] + meteor_size > laser[0] and
                        meteor[1] < laser[1] + laser_height and
                        meteor[1] + meteor_size > laser[1]):
                        meteor_list.remove(meteor)
                        laser_list.remove(laser)
                        score += 1

            # Verificar colisões de lasers com estrelas
            for laser in laser_list:
                for star in star_list:
                    if (star[0] < laser[0] + laser_width and
                        star[0] + star_size > laser[0] and
                        star[1] < laser[1] + laser_height and
                        star[1] + star_size > laser[1]):
                        star_list.remove(star)
                        laser_list.remove(laser)
                        score += 1

            # Verificar se o jogador subiu de nível
            if score // 50 + 1 > level:
                level = score // 50 + 1

            # Verificar colisões da nave com meteoros e estrelas
            for meteor in meteor_list:
                if (meteor[0] < player_x + player_size and
                    meteor[0] + meteor_size > player_x and
                    meteor[1] < player_y + player_size and
                    meteor[1] + meteor_size > player_y):
                    game_over = True
                    break
            for star in star_list:
                if (star[0] < player_x + player_size and
                    star[0] + star_size > player_x and
                    star[1] < player_y + player_size and
                    star[1] + star_size > player_y):
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
