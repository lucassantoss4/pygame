import pygame
import random
from .config import *

class Estrela(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.spawn_aleatorio()

    def spawn_aleatorio(self):
        self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA)
        self.rect.y = random.randint(-100, -ALTURA_BOMBA)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(1, 11)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > ALTURA or self.rect.left > LARGURA or self.rect.right < 0:
            self.spawn_aleatorio()


class Bomba(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.spawn_aleatorio()

    def spawn_aleatorio(self):
        self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA)
        self.rect.y = random.randint(-100, -ALTURA_BOMBA)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(1, 11)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > ALTURA or self.rect.left > LARGURA or self.rect.right < 0:
            self.spawn_aleatorio()


class Jogador(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA / 2
        self.rect.bottom = ALTURA - 10
        self.speedx = 0
        
        self.pulando = False
        self.velocidade_y = 0

    def update(self):
        # Movimentação Horizontal
        self.rect.x += self.speedx

        # Movimentação Vertical (Gravidade)
        self.velocidade_y += GRAVIDADE
        self.rect.y += self.velocidade_y

        # Colisão com o chão
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA
            self.velocidade_y = 0
            self.pulando = False

        # Impedir que o personagem saia da tela
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA
        if self.rect.left < 0:
            self.rect.left = 0

    def pular(self):
        if not self.pulando:
            self.velocidade_y = -ALTURA_PULO
            self.pulando = True
