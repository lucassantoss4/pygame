# ===== Inicialização =====
# ----- Importa e inicia pacotes

import pygame
import random

from pygame.sprite import AbstractGroup

pygame.init() # Inicia o pygame

# ----- Gera tela principal
LARGURA = 900
ALTURA = 600

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo ninja') #muda o nome da janela

# ----- Inicia assets
largura_ninja = 70
altura_ninja = 80

ALTURA_BOMBA = 40
LARGURA_BOMBA = 40
fonte = pygame.font.SysFont(None, 48)
fundo = pygame.image.load('fundoo.jpg') # carrega imagem de fundo
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA)) # redimensiona imagem de fundo

ninja_img = pygame.image.load('ninja.png').convert_alpha() # carrega imagem do ninja
ninja_img_small = pygame.transform.scale(ninja_img, (largura_ninja, altura_ninja)) # diminui o tamanho da imagem do ninja

bomba_img = pygame.image.load('bomba.png').convert_alpha() # carrega imagem da bomba
bomba_img_small = pygame.transform.scale(bomba_img, (largura_ninja, altura_ninja)) # diminui o tamanho da imagem da bomba

# ========== Inicia estruturas de dados
# ========== Inicia estruturas de dados
class Bomba(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img #imagem da bomba   
        self.rect = self.image.get_rect() #pega o retangulo da imagem
        self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA) #posição x aleatoria
        self.rect.y = random.randint(-ALTURA_BOMBA, -ALTURA_BOMBA) #posição y aleatoria
        self.speedx = random.randint(-3, 3) #velocidade x aleatoria
        self.speedy = random.randint(1, 11) #velocidade y aleatoria

    def update(self):
        #atualiza a posição da bomba
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # se a bomba passar do final da tela, volta para cima e sorteia novas posições e velocidades
        if self.rect.top > ALTURA or self.rect.left > LARGURA or self.rect.right < 0:
            self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA)
            self.rect.y = random.randint(-100, -ALTURA_BOMBA)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(1, 11)


game = True  # Variável para o loop principal
# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 60 

# Criando um grupo de bombas
bombas = pygame.sprite.Group()

# Criando as bombas
bomba1 = Bomba(bomba_img_small)
bomba2 = Bomba(bomba_img_small)

# ===== Loop principal =====
while game:
    clock.tick(FPS) # Ajusta a velocidade do jogo

    # ------- Trata eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            game = False

    # ----- Atualiza estado do jogo
    # Atualizando a posição da bomba
    bomba1.update()
    bomba2.update()

    # ----- Gera saídas
    janela.fill((255, 255, 255))  # Preenche com a cor branca
    janela.blit(fundo, (0, 0)) # coloca a imagem de fundo na tela

    # Desenhando a bomba
    janela.blit(bomba1.image, bomba1.rect)
    janela.blit(bomba2.image, bomba2.rect)
    pygame.display.update() # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados      
