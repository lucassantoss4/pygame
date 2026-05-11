import pygame
import random
from config import *

class Particula(pygame.sprite.Sprite):
    def __init__(self, x, y, cor):
        super().__init__()
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.image, cor, (3, 3), 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = [random.uniform(-5, 5), random.uniform(-10, 2)]
        self.lifetime = PARTICLE_LIFETIME

    def update(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        self.vel[1] += 0.5 
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Estrela(pygame.sprite.Sprite):
    def __init__(self, img, bonus_velocidade=0):
        super().__init__()
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.bonus_velocidade = bonus_velocidade
        self.spawn_aleatorio()

    def spawn_aleatorio(self):
        self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA)
        self.rect.y = random.randint(-200, -ALTURA_BOMBA)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(3, 8) + self.bonus_velocidade

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > ALTURA or self.rect.left > LARGURA or self.rect.right < 0:
            self.spawn_aleatorio()

class Bomba(pygame.sprite.Sprite):
    def __init__(self, img, bonus_velocidade=0):
        super().__init__()
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.bonus_velocidade = bonus_velocidade
        self.spawn_aleatorio()

    def spawn_aleatorio(self):
        self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA)
        self.rect.y = random.randint(-200, -ALTURA_BOMBA)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(4, 10) + self.bonus_velocidade

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > ALTURA or self.rect.left > LARGURA or self.rect.right < 0:
            self.spawn_aleatorio()

class Jogador(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA / 2
        self.rect.bottom = ALTURA - 10
        self.pos = pygame.Vector2(self.rect.centerx, self.rect.bottom)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.pulando = False

    def update(self):
        self.acc = pygame.Vector2(0, GRAVIDADE)
        keys = pygame.key.get_pressed()
        
        # Detecção de movimento (A/D ou Setas)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -ACELERACAO * 1.5 # Leve aumento para compensar lag do browser
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = ACELERACAO * 1.5
        
        # Aplica atrito e física
        self.acc.x += self.vel.x * ATRITO
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > LARGURA: self.pos.x = LARGURA
        if self.pos.x < 0: self.pos.x = 0
        if self.pos.y > ALTURA:
            self.pos.y = ALTURA
            self.vel.y = 0
            self.pulando = False
        self.rect.centerx = self.pos.x
        self.rect.bottom = self.pos.y

    def pular(self):
        if not self.pulando:
            self.vel.y = -ALTURA_PULO
            self.pulando = True
