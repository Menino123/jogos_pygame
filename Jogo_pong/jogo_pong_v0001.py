import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pong Game")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Raquetes e bola
raquete_esquerda = pygame.Rect(50, altura // 2 - 50, 10, 100)
raquete_direita = pygame.Rect(largura - 60, altura // 2 - 50, 10, 100)
bola = pygame.Rect(largura // 2 - 10, altura // 2 - 10, 20, 20)
bola_velocidade_x = 5
bola_velocidade_y = 5

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento das raquetes
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        raquete_esquerda.y -= 5
    if teclas[pygame.K_s]:
        raquete_esquerda.y += 5
    if teclas[pygame.K_UP]:
        raquete_direita.y -= 5
    if teclas[pygame.K_DOWN]:
        raquete_direita.y += 5

    # Atualização da bola
    bola.x += bola_velocidade_x
    bola.y += bola_velocidade_y

    # Colisões com as paredes
    if bola.top <= 0 or bola.bottom >= altura:
        bola_velocidade_y *= -1
    if bola.colliderect(raquete_esquerda) or bola.colliderect(raquete_direita):
        bola_velocidade_x *= -1

    # Desenho na tela
    tela.fill(preto)
    pygame.draw.rect(tela, branco, raquete_esquerda)
    pygame.draw.rect(tela, branco, raquete_direita)
    pygame.draw.ellipse(tela, branco, bola)
    pygame.display.flip()

    # Controle de velocidade
    pygame.time.Clock().tick(60)

