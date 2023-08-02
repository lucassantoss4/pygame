from typing import Any
import pygame
import random
from pygame.sprite import AbstractGroup

pygame.init()
LARGURA = 900
ALTURA = 600
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo ninja')

largura_ninja = 70
altura_ninja = 80

ALTURA_BOMBA = 40
LARGURA_BOMBA = 40
fonte = pygame.font.SysFont(None, 48)
fundo = pygame.image.load('fundo2.jpg')
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
ninja_img = pygame.image.load('ninja.png').convert_alpha()
ninja_img_small = pygame.transform.scale(ninja_img, (largura_ninja, altura_ninja))
bomba_img = pygame.image.load('bb.png').convert_alpha()
bomba_img_small = pygame.transform.scale(bomba_img, (largura_ninja, altura_ninja))

class Bomba(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA)
        self.rect.y = random.randint(-ALTURA_BOMBA, -ALTURA_BOMBA)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(1, 11)
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > ALTURA or self.rect.left > LARGURA or self.rect.right < 0:
            self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA)
            self.rect.y = random.randint(-100, -ALTURA_BOMBA)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(1, 11)

class enviar (pygame.sprite.Sprite):
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA / 2
        self.rect.bottom = ALTURA - 10 
        self.speedx = 0

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA
        if self.rect.left < 0:
            self.rect.left = 0

# Function to display the score
def mostra_pontuacao(janela, tempo_inicial):
    contagem_tempo = int(pygame.time.get_ticks() / 1000) - tempo_inicial
    texto_pontuacao = fonte.render(f'Pontuação: {contagem_tempo}', True, (255, 255, 255))
    texto_pontuacao_retangulo = texto_pontuacao.get_rect(center=(500, 50))
    janela.blit(texto_pontuacao, texto_pontuacao_retangulo)
    return contagem_tempo

# Function for collision between the player and the obstacles
def colisao(player, obstaculos):
    for obstaculo in obstaculos:
        if player.colliderect(obstaculo.rect):
            return False
    return True

game = True
clock = pygame.time.Clock()
FPS = 60 
todas_sprites = pygame.sprite.Group()

jogador = enviar(ninja_img_small)
todas_sprites.add(jogador)

bombas = pygame.sprite.Group()
for i in range(5):
    bomba = Bomba(bomba_img_small)
    todas_sprites.add(bomba)
    bombas.add(bomba)

pulando = False
pulo_inicial = jogador.rect.bottom

tempo_inicial = int(pygame.time.get_ticks() / 1000)
ultima_atualizacao_pontuacao = tempo_inicial

while game:
    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            game = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                jogador.speedx -= 5
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                jogador.speedx += 5
            if evento.key == pygame.K_w and not pulando:
                pulando = True
                jogador.speedy = -15

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                jogador.speedx += 5
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                jogador.speedx -= 5

    todas_sprites.update()

    if pulando:
        jogador.rect.y += jogador.speedy
        jogador.speedy += 1
        if jogador.rect.bottom >= pulo_inicial:
            jogador.rect.bottom = pulo_inicial
            pulando = False

    if not colisao(jogador.rect, bombas):
        game = False

    # Update the score once per second
    tempo_atual = int(pygame.time.get_ticks() / 1000)
    if tempo_atual > ultima_atualizacao_pontuacao:
        pontuacao = mostra_pontuacao(janela, tempo_inicial)
        ultima_atualizacao_pontuacao = tempo_atual

    janela.fill((255, 255, 255))
    janela.blit(fundo, (0, 0))

    todas_sprites.draw(janela)
    pygame.display.update()

pygame.quit()
