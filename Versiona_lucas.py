# ===== Inicialização =====
# ----- Importa e inicia pacotes

from typing import Any
import pygame
import random
import time

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

largura_estrela = 30
altura_estrela = 30

vida_jogador = 3
pontos = 0

ALTURA_BOMBA = 70
LARGURA_BOMBA = 50

ALTURA_PULO = 15
GRAvida_jogadorDE = 1

fonte = pygame.font.SysFont(None, 48)
fundo = pygame.image.load('fundo2.jpg') # carrega imagem de fundo
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA)) # redimensiona imagem de fundo

ninja_img = pygame.image.load('ninja.png').convert_alpha() # carrega imagem do ninja
ninja_img_small = pygame.transform.scale(ninja_img, (largura_ninja, altura_ninja)) # diminui o tamanho da imagem do ninja

bomba_img = pygame.image.load('bomba.png').convert_alpha() # carrega imagem da bomba
bomba_img_small = pygame.transform.scale(bomba_img, (LARGURA_BOMBA, ALTURA_BOMBA)) # diminui o tamanho da imagem da bomba

estrela_img = pygame.image.load('estrela.png').convert_alpha() # carrega imagem da estrela
estrela_img_small = pygame.transform.scale(estrela_img, (largura_estrela, altura_estrela)) # diminui o tamanho da imagem da estrela

#Toca a música no jogo
som_fundo = pygame.mixer.Sound('musica.mp3') #som de fundo
som_fundo.set_volume(0.2) #volume som da musica
# som_fundo.play() #toca a musica sem loop
som_fundo.play(loops = -1) #toca a musica com loop

#Músicas do Pulo
som_pulo = pygame.mixer.Sound('som_pulo.mp3') #som do pulo
som_pulo.set_volume(0.4) #volume som do pulo

# Som de explosão
som_explosao = pygame.mixer.Sound('bomba_som.mp3')
som_explosao.set_volume(0.1)

# Som de estrela
som_estrela = pygame.mixer.Sound('som_estrela.mp3')
som_estrela.set_volume(0.1)

# ========== Inicia estruturas de dados ==========
class Estrela(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img # imagem da estrela   
        self.rect = self.image.get_rect() # pega o retângulo da imagem
        self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA) # posição x aleatória
        self.rect.y = random.randint(-ALTURA_BOMBA, -ALTURA_BOMBA) # posição y aleatória
        self.speedx = random.randint(-3, 3) # velocidade x aleatória
        self.speedy = random.randint(1, 11) # velocidade y aleatória

    def update(self):
        # Atualiza a posição da estrela
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Se a estrela passar do final da tela, reinicie sua posição e velocidade
        if self.rect.top > ALTURA or self.rect.left > LARGURA or self.rect.right < 0:
            self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA)
            self.rect.y = random.randint(-100, -ALTURA_BOMBA)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(1, 11)


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

    def pular(self): #função para pular
        if not self.pulando: #se não estiver pulando
            self.velocidade_y = -ALTURA_PULO #velocidade do pulo
            self.pulando = True #está pulando

def tocar_som_explosao(): #função para tocar o som de explosão
    som_explosao.play() #toca o som de explosão

def renderizar_vida(vida): #função para renderizar a vida
    return fonte.render("vida: " + chr(9829) * vida, True, (255, 255, 255))

def renderizar_pontuacao(pontos):
    return fonte.render("Pontuação: " + str(pontos), True, (255, 255, 255))

texto_vida = renderizar_vida(vida_jogador) #texto da vida
texto_vida_rect = texto_vida.get_rect() #retangulo do texto da vida

game = True  # Variável para o loop principal
# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 60 

# grupos de bombas e estrelas
todas_sprites = pygame.sprite.Group()
todas_bombas = pygame.sprite.Group()
todas_estrelas = pygame.sprite.Group()

# criando personagem
jogador = enviar(ninja_img_small)
todas_sprites.add(jogador)


# variável para o som do pulo
pulando = False
pulo_inicial = jogador.rect.bottom # posição inicial do pulo

intervalo_estrela = 1  # Intervalo em segundos
ultimo_spawn_estrela = time.time() # Tempo da última estrela
max_estrelas = random.randint(0,5) # Número máximo de estrelas na tela


intervalo_bomba = 1  # Intervalo em segundos para criar uma nova bomba
ultimo_spawn_bomba = time.time()  # Tempo da última bomba
max_bombas = random.randint(0,10)  # Número máximo de bombas na tela
# ===== Loop principal =====
while game:
    clock.tick(FPS) # Ajusta a velocidade do jogo

    # ------- Trata eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # Verifica se foi fechado
            game = False
            
        # Verifica se apertou alguma tecla.
        if evento.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if evento.key == pygame.K_LEFT:
                jogador.speedx -= 5 #diminui a velocidade do jogador
            if evento.key == pygame.K_RIGHT:
                jogador.speedx += 5 #aumenta a velocidade do jogador
        
        # Verifica se soltou alguma tecla.
        if evento.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if evento.key == pygame.K_LEFT:
                jogador.speedx += 5 #aumenta a velocidade do jogador
            if evento.key == pygame.K_RIGHT:
                jogador.speedx -= 5 #diminui a velocidade do jogador

            if evento.key == pygame.K_SPACE and not pulando:
                pulando = True
                som_pulo.play() #toca a música quando pula
                jogador.speedy = -15
                jogador.pular() #Chama a função de pular do jogador

        if pulando: #se estiver pulando
            jogador.rect.y += jogador.speedy #atualiza a posição do jogador
            jogador.speedy += 1 # aumenta a velocidade do pulo
            if jogador.rect.bottom >= pulo_inicial: #se o jogador estiver no chão
                jogador.rect.bottom = pulo_inicial #atualiza a posição do jogador
                pulando = False #não está mais pulando

    # ----- Atualiza estado do jogo
    # Verifica se é hora de criar uma nova estrela
    agora = time.time()
    if agora - ultimo_spawn_estrela >= intervalo_estrela and len(todas_estrelas) < max_estrelas:
        estrela = Estrela(estrela_img_small) # Cria uma nova estrela
        todas_sprites.add(estrela) # Adiciona a estrela no grupo de sprites
        todas_estrelas.add(estrela) # Adiciona a estrela no grupo de estrelas
        ultimo_spawn_estrela = agora # Atualiza o tempo da última estrela

    if agora - ultimo_spawn_bomba >= intervalo_bomba and len(todas_bombas) < max_bombas: # Verifica se é hora de criar uma nova bomba
        bomba = Bomba(bomba_img_small) # Cria uma nova bomba
        todas_sprites.add(bomba) # Adiciona a bomba no grupo de sprites
        todas_bombas.add(bomba) # Adiciona a bomba no grupo de bombas
        ultimo_spawn_bomba = agora # Atualiza o tempo da última bomba

    # Atualizando a posição da bomba
    todas_sprites.update()

    # Verifica se houve colisão entre a bomba e o jogador
    hits_bomba = pygame.sprite.spritecollide(jogador, todas_bombas, True)

    # Verifica se houve colisão entre o ninja e a estrela
    hits_estrela = pygame.sprite.spritecollide(jogador, todas_estrelas, True)

    if len(hits_estrela) > 0:
        pontos += 10
        som_estrela.play()
        if pontos % 50 == 0:
            vida_jogador += 1 # Aumenta a vida do jogador a cada 50 pontos

    if len(hits_bomba) > 0:
        som_explosao.play()
        vida_jogador -= 1
    if vida_jogador == 0:
        # tocar_som_explosao()
        som_explosao.play()
        pygame.time.wait(1000)
        game = False

    # Atualiza o texto da vida do jogador
    texto_vida = renderizar_vida(vida_jogador)

    # Atualiza o texto da pontuação
    texto_pontuacao = renderizar_pontuacao(pontos)

    # ----- Gera saídas
    janela.fill((255, 255, 255))  # Preenche com a cor branca
    janela.blit(fundo, (0, 0)) # coloca a imagem de fundo na tela
    janela.blit(texto_vida, texto_vida_rect) #coloca o texto da vida na tela
    janela.blit(texto_pontuacao, (620, 0)) # posicione o texto da pontuação na tela


    # Desenhando a bomba
    todas_sprites.draw(janela)
    pygame.display.update() # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados 