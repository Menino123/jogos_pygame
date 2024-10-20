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

# Raquetes e bola
raquete_esquerda = pygame.Rect(50, HEIGHT // 2 - 50, 10, 100)
raquete_direita = pygame.Rect(WIDTH - 60, HEIGHT // 2 - 50, 10, 100)
bola = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
bola_velocidade_x = random.choice([-5, 5])  # Escolhe aleatoriamente a direção da bola
bola_velocidade_y = random.choice([-5, 5])  # Escolhe aleatoriamente a direção da bola

# Pontuação dos jogadores
pontuacao_esquerda = 0
pontuacao_direita = 0

# Contador regressivo
contador = 3
fonte_contador = pygame.font.Font(None, 72)



# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Contador regressivo
    if contador > 0:
        tela.fill(preto)
        texto_contador = fonte_contador.render(str(contador), True, branco)
        tela.blit(texto_contador, (WIDTH // 2 - 20, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(1000)
        contador -= 1
    else:
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

        # Desenho na tela
        tela.fill(preto)
        pygame.draw.rect(tela, branco, raquete_esquerda)
        pygame.draw.rect(tela, branco, raquete_direita)
        pygame.draw.ellipse(tela, branco, bola)

        # Exibição da pontuação
        fonte_pontuacao = pygame.font.Font(None, 36)
        texto_pontuacao = fonte_pontuacao.render(f"{pontuacao_esquerda} - {pontuacao_direita}", True, branco)
        tela.blit(texto_pontuacao, (WIDTH // 2 - 40, 10))

        pygame.display.flip()

        # Controle de velocidade
        pygame.time.Clock().tick(60)
