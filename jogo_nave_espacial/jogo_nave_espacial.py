import pygame
import random
import os

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
base_path = os.path.dirname(__file__)
background_image = pygame.image.load(os.path.join(base_path, "imagens/background_space.png"))

class Player:
    def __init__(self):
        self.image = pygame.image.load(os.path.join(base_path, "imagens/spaceship.png"))
        self.size = 60
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 2 * self.size
        self.speed = 15

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image, (self.size, self.size)), (self.x, self.y))

class Meteor:
    def __init__(self):
        self.image = pygame.image.load(os.path.join(base_path, "imagens/meteor.png"))
        self.size = 25
        self.speed = 5
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = -self.size

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image, (self.size, self.size)), (self.x, self.y))

class Star:
    def __init__(self):
        self.image = pygame.image.load(os.path.join(base_path, "imagens/star.png"))
        self.size = 30
        self.speed = 10
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = -self.size

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image, (self.size, self.size)), (self.x, self.y))

class Laser:
    def __init__(self, x, y):
        self.width = 10
        self.height = 30
        self.speed = 10
        self.color = RED
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

def check_collision(obj1, obj2, size1, size2):
    return (obj1.x < obj2.x + size2 and
            obj1.x + size1 > obj2.x and
            obj1.y < obj2.y + size2 and
            obj1.y + size1 > obj2.y)

def reset_game():
    global player, meteors, stars, lasers, score, level
    player = Player()
    meteors = []
    stars = []
    lasers = []
    score = 0
    level = 1

def game_loop():
    global player, meteors, stars, lasers, score, level
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
                        lasers.append(Laser(player.x + player.size // 2 - Laser.width // 2, player.y))

            # Movimento do jogador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x > 0:
                player.x -= player.speed
            if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player.size:
                player.x += player.speed

            # Adicionar meteoros e estrelas
            if random.randint(1, 20) == 1:
                meteors.append(Meteor())
            if random.randint(1, 50) == 1:
                stars.append(Star())

            # Mover meteoros, estrelas e lasers
            for meteor in meteors:
                meteor.y += meteor.speed * level
            meteors = [meteor for meteor in meteors if meteor.y < SCREEN_HEIGHT]

            for star in stars:
                star.y += star.speed * level
            stars = [star for star in stars if star.y < SCREEN_HEIGHT]

            for laser in lasers:
                laser.y -= laser.speed
            lasers = [laser for laser in lasers if laser.y > 0]

            # Verificar colisões de lasers com meteoros e estrelas
            for laser in lasers:
                for meteor in meteors:
                    if check_collision(laser, meteor, laser.width, meteor.size):
                        meteors.remove(meteor)
                        lasers.remove(laser)
                        score += 1
                        break
                for star in stars:
                    if check_collision(laser, star, laser.width, star.size):
                        stars.remove(star)
                        lasers.remove(laser)
                        score += 1
                        break

            # Verificar se o jogador subiu de nível
            if score // 50 + 1 > level:
                level = score // 50 + 1

            # Verificar colisões da nave com meteoros e estrelas
            for meteor in meteors:
                if check_collision(meteor, player, meteor.size, player.size):
                    game_over = True
                    break
            for star in stars:
                if check_collision(star, player, star.size, player.size):
                    game_over = True
                    break

            # Desenhar tudo na tela
            screen.blit(pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            player.draw(screen)
            for meteor in meteors:
                meteor.draw(screen)
            for star in stars:
                star.draw(screen)
            for laser in lasers:
                laser.draw(screen)

            # Desenhar pontuação e nível
            font = pygame.font.SysFont(None, 30)
            text = font.render(f"Score: {score}", True, RED)
            screen.blit(text, [10, 10])
            text = font.render(f"Level: {level}", True, RED)
            screen.blit(text, [10, 40])

            pygame.display.flip()
            clock.tick(30)

    pygame.quit()

# Iniciar o jogo
reset_game()
game_loop()