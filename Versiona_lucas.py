# ===== Inicialização =====
# ----- Importa e inicia pacotes

from typing import Any
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
largura_ninja = 100
altura_ninja = 90

vida_jogador = 3

ALTURA_BOMBA = 70
LARGURA_BOMBA = 50

ALTURA_PULO = 15
GRAvida_jogadorDE = 1

fonte = pygame.font.SysFont(None, 48)
fundo = pygame.image.load('fundoo.jpg') # carrega imagem de fundo
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA)) # redimensiona imagem de fundo

ninja_img = pygame.image.load('ninja.png').convert_alpha() # carrega imagem do ninja
ninja_img_small = pygame.transform.scale(ninja_img, (largura_ninja, altura_ninja)) # diminui o tamanho da imagem do ninja

bomba_img = pygame.image.load('bomba.png').convert_alpha() # carrega imagem da bomba
bomba_img_small = pygame.transform.scale(bomba_img, (LARGURA_BOMBA, ALTURA_BOMBA)) # diminui o tamanho da imagem da bomba

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

class enviar (pygame.sprite.Sprite):
    def __init__(self,img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA / 2
        self.rect.bottom = ALTURA - 10 
        self.speedx = 0

        # Variáveis de controle de salto
        self.pulando = False
        self.velocidade_y = 0

    def update(self):
        #Atualiza a posição 
        self.rect.x += self.speedx

        # Aplicar gravida_jogadorde
        self.velocidade_y += GRAvida_jogadorDE
        self.rect.y += self.velocidade_y

        # Impedir que o personagem saia da tela no eixo vertical
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA
            self.pulando = False

        #Mantem dentro da tela
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA
        if self.rect.left < 0:
            self.rect.left = 0

    def pular(self):
        if not self.pulando:
            self.velocidade_y = -ALTURA_PULO
            self.pulando = True

def renderizar_vida(vida): #função para renderizar a vida
    return fonte.render("vida: " + chr(9829) * vida, True, (0, 0, 0))
texto_vida = renderizar_vida(vida_jogador) #texto da vida
texto_vida_rect = texto_vida.get_rect() #retangulo do texto da vida

game = True  # Variável para o loop principal
# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 60 

# grupos de bombas
todas_sprites = pygame.sprite.Group()
todas_bombas = pygame.sprite.Group()

# criando personagem
jogador = enviar(ninja_img_small)
todas_sprites.add(jogador)

for i in range(5):
    bomba = Bomba(bomba_img_small)
    todas_sprites.add(bomba)
    todas_bombas.add(bomba)

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
            
        # Verifica se apertou alguma tecla.
        if evento.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if evento.key == pygame.K_LEFT:
                jogador.speedx -= 5
            if evento.key == pygame.K_RIGHT:
                jogador.speedx += 5
        
        # Verifica se soltou alguma tecla.
        if evento.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if evento.key == pygame.K_LEFT:
                jogador.speedx += 5
            if evento.key == pygame.K_RIGHT:
                jogador.speedx -= 5

            if evento.key == pygame.K_SPACE:
                jogador.pular()  # Chama a função de pular do jogador

    # ----- Atualiza estado do jogo
    # Atualizando a posição da bomba
    todas_sprites.update()

    # Verifica se houve colisão entre a bomba e o jogador
    hits = pygame.sprite.spritecollide(jogador, todas_bombas, True)
    if len(hits) > 0:
        vida_jogador -= 1
        if vida_jogador == 0:
            game = False

    # Atualiza o texto da vida do jogador
    texto_vida = renderizar_vida(vida_jogador)

    # ----- Gera saídas
    janela.fill((255, 255, 255))  # Preenche com a cor branca
    janela.blit(fundo, (0, 0)) # coloca a imagem de fundo na tela
    janela.blit(texto_vida, texto_vida_rect) #coloca o texto da vida na tela


    # Desenhando a bomba
    todas_sprites.draw(janela)
    pygame.display.update() # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados 