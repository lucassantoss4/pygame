# ===== Inicialização =====
# ----- Importa e inicia pacotes

from typing import Any #importa o tipo Any
import pygame #importa o pygame
import random #importa o random
import time #importa o time


from pygame.sprite import AbstractGroup #importa o grupo de sprites

pygame.init() # Inicia o pygame

# ----- Gera tela principal
LARGURA = 900
ALTURA = 600

janela = pygame.display.set_mode((LARGURA, ALTURA)) # cria a janela
pygame.display.set_caption('Jogo ninja') #muda o nome da janela

# ----- Inicia assets
largura_ninja = 100
altura_ninja = 90

largura_estrela = 30
altura_estrela = 30

vida_jogador = 3  
pontos = 0

ALTURA_BOMBA = 70 #altura da bomba
LARGURA_BOMBA = 50 #largura da bomba

# Variáveis de velocidade do jogador
VELOCIDADE_JOGADOR = 9.5

# Variáveis para o pulo do jogador
ALTURA_PULO = 15 #altura do pulo do ninja
GRAVIDADE = 1.25 #gravidade do pulo do ninja
GRAvida_jogadorDE = 1 #gravidade do ninja


fonte = pygame.font.SysFont(None, 48)
fundo = pygame.image.load('util/img/fundo2.jpg') # carrega imagem de fundo
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA)) # redimensiona imagem de fundo

ninja_img = pygame.image.load('util/img/ninja.png').convert_alpha() # carrega imagem do ninja
ninja_img_small = pygame.transform.scale(ninja_img, (largura_ninja, altura_ninja)) # diminui o tamanho da imagem do ninja

bomba_img = pygame.image.load('util/img/bomba.png').convert_alpha() # carrega imagem da bomba
bomba_img_small = pygame.transform.scale(bomba_img, (LARGURA_BOMBA, ALTURA_BOMBA)) # diminui o tamanho da imagem da bomba

estrela_img = pygame.image.load('util/img/estrela.png').convert_alpha() # carrega imagem da estrela
estrela_img_small = pygame.transform.scale(estrela_img, (largura_estrela, altura_estrela)) # diminui o tamanho da imagem da estrela

#Toca a música no jogo
som_fundo = pygame.mixer.Sound('util/som/musica.mp3') #som de fundo
som_fundo.set_volume(0.2) #volume som da musica
# som_fundo.play() #toca a musica sem loop
som_fundo.play(loops = -1) #toca a musica com loop

#Músicas do Pulo
som_pulo = pygame.mixer.Sound('util/som/som_pulo.mp3') #som do pulo
som_pulo.set_volume(0.4) #volume som do pulo

som_explosao = pygame.mixer.Sound('util/som/bomba_som.mp3') #som da explosão
som_explosao.set_volume(0.1) #volume som da explosão

som_estrela = pygame.mixer.Sound('util/som/som_estrela.mp3') #som da estrela
som_estrela.set_volume(0.1) #volume som da estrela 


## Carregue a imagem do menu
menu_img = pygame.image.load('util/img/tela_de_inicio.png').convert_alpha()
menu_img = pygame.transform.scale(menu_img, (900, 600))

## Função para exibir o menu e aguardar a tecla espaço ser pressionada
def menu_principal():
    global vida_jogador, pontos # Variáveis globais para o jogo 
    while True:
        for evento in pygame.event.get(): # Verifica se o usuário quer sair
            if evento.type == pygame.QUIT: # Se o usuário clicar no X da janela
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN: # Se o usuário apertar alguma tecla
                if evento.key == pygame.K_SPACE: # Se a tecla for espaço
                    return  # Retorna da função e inicia o jogo

        janela.blit(menu_img, (0, 0)) # Desenha a imagem do menu na tela
        pygame.display.update() # Atualiza a tela
        clock.tick(FPS) # Controla a velocidade do jogo

#=====reiniciar o jogo=======
def inicializar_jogo():
    global jogador, todas_sprites, todas_bombas, todas_estrelas # Variáveis globais para o jogo 
    global pulando, vida_jogador, pontos # Variáveis globais para o jogo

    jogador = enviar(ninja_img_small) # Cria o jogador com a imagem do ninja
    todas_sprites = pygame.sprite.Group() # Cria um grupo de sprites para desenhar na tela
    todas_bombas = pygame.sprite.Group() 
    todas_estrelas = pygame.sprite.Group()

    todas_sprites.add(jogador) # Adiciona o jogador no grupo de sprites

    pulando = False
    vida_jogador = 3
    pontos = 0


# ========== Inicia estruturas de dados ==========
class Estrela(pygame.sprite.Sprite): #classe estrela para criar as estrelas
    def __init__(self, img): # Construtor da classe mãe (Sprite).
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
        self.rect.x += self.speedx # velocidade x
        self.rect.y += self.speedy  # velocidade y

        if self.rect.top > ALTURA or self.rect.left > LARGURA or self.rect.right < 0: #se a estrela passar do final da tela
            self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA) #posição x aleatoria
            self.rect.y = random.randint(-100, -ALTURA_BOMBA) #posição y aleatoria
            self.speedx = random.randint(-3, 3) #velocidade x aleatoria
            self.speedy = random.randint(1, 11) #velocidade y aleatoria


class Bomba(pygame.sprite.Sprite): #classe bomba para criar as bombas
    def __init__(self, img): #construtor da classe mãe (Sprite)
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self) #inicia a classe mãe    

        self.image = img #imagem da bomba   
        self.rect = self.image.get_rect() #pega o retangulo da imagem
        self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA) #posição x aleatoria
        self.rect.y = random.randint(-ALTURA_BOMBA, -ALTURA_BOMBA) #posição y aleatoria
        self.speedx = random.randint(-3, 3) #velocidade x aleatoria
        self.speedy = random.randint(1, 11) #velocidade y aleatoria

    def update(self):
        #atualiza a posição da bomba
        self.rect.x += self.speedx #velocidade x
        self.rect.y += self.speedy #velocidade y

        if self.rect.top > ALTURA or self.rect.left > LARGURA or self.rect.right < 0: #se a bomba passar do final da tela
            self.rect.x = random.randint(0, LARGURA - LARGURA_BOMBA) #posição x aleatoria
            self.rect.y = random.randint(-100, -ALTURA_BOMBA) #posição y aleatoria
            self.speedx = random.randint(-3, 3) #velocidade x aleatoria
            self.speedy = random.randint(1, 11) #velocidade y aleatoria


class enviar (pygame.sprite.Sprite):
    def __init__(self,img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self) #inicia a classe mãe

        self.image = img  # imagem da bomba
        self.rect = self.image.get_rect() # pega o retangulo da imagem
        self.rect.centerx = LARGURA / 2 #posição x no centro
        self.rect.bottom = ALTURA - 10 # posição y no final da tela
        self.speedx = 0 #velocidade x

        # Variáveis de controle de salto
        self.pulando = False #não está pulando
        self.velocidade_y = 0 #velocidade do pulo

    def update(self):
        #Atualiza a posição 
        self.rect.x += self.speedx #atualiza a posição

        # Aplicar gravida_jogadorde
        self.velocidade_y += GRAvida_jogadorDE #gravidade
        self.rect.y += self.velocidade_y #atualiza a posição

        # Impedir que o personagem saia da tela no eixo vertical
        if self.rect.bottom > ALTURA: #se a posição for maior que a altura
            self.rect.bottom = ALTURA #mantem dentro da tela
            self.pulando = False #não está pulando

        #Mantem dentro da tela
        if self.rect.right > LARGURA: #se a posição for maior que a largura
            self.rect.right = LARGURA #mantem dentro da tela
        if self.rect.left < 0: #se a posição for menor que 0
            self.rect.left = 0 #mantem dentro da tela

    def pular(self): #função para pular
        if not self.pulando: #se não estiver pulando
            self.velocidade_y = -ALTURA_PULO #velocidade do pulo
            self.pulando = True #está pulando

def renderizar_vida(vida): #função para renderizar a vida
    return fonte.render("Vida: " + chr(9829) * vida, True, (255, 255, 255)) 

def renderizar_pontuacao(pontos):
    return fonte.render("Pontuação: " + str(pontos), True, (255, 255, 255)) #função para renderizar a pontuação

texto_vida = renderizar_vida(vida_jogador) #texto da vida
texto_vida_rect = texto_vida.get_rect() #retangulo do texto da vida

game = True  # Variável para o loop principal
# Variável para o ajuste de velocidade
clock = pygame.time.Clock() #variável para o clock
FPS = 60 

# grupos de bombas e estrelas
todas_sprites = pygame.sprite.Group() #grupo de todas as sprites
todas_bombas = pygame.sprite.Group() #grupo de todas as bombas
todas_estrelas = pygame.sprite.Group() #grupo de todas as estrelas

# criando personagem
jogador = enviar(ninja_img_small) #cria o personagem
todas_sprites.add(jogador) #adiciona o personagem ao grupo de sprites


# variável para o som do pulo
pulando = False
pulo_inicial = jogador.rect.bottom # posição inicial do pulo

intervalo_estrela = 1  # Intervalo em segundos
ultimo_spawn_estrela = time.time() # Tempo da última estrela
max_estrelas = random.randint(0,5) # Número máximo de estrelas na tela


intervalo_bomba = 1  # Intervalo em segundos para criar uma nova bomba
ultimo_spawn_bomba = time.time()  # Tempo da última bomba
max_bombas = random.randint(4,16)  # Número máximo de bombas na tela

# Chama a função para exibir o menu antes do loop principal do jogo
menu_principal()

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
            if evento.key == pygame.K_a:
                jogador.speedx -= VELOCIDADE_JOGADOR #diminui a velocidade do jogador
            if evento.key == pygame.K_d:
                jogador.speedx += VELOCIDADE_JOGADOR #aumenta a velocidade do jogador
        
        # Verifica se soltou alguma tecla.
        if evento.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if evento.key == pygame.K_a:
                jogador.speedx += VELOCIDADE_JOGADOR #aumenta a velocidade do jogador
            if evento.key == pygame.K_d:
                jogador.speedx -= VELOCIDADE_JOGADOR #diminui a velocidade do jogador

        # Verifica se apertou a tecla espaço.
        if evento.type == pygame.KEYDOWN:
            if (evento.key == pygame.K_SPACE and not pulando) or (evento.key == pygame.K_w and not pulando):
                pulando = True
                som_pulo.play()  # toca o som quando pula
                jogador.speedy = -ALTURA_PULO
                jogador.pular()  # Chama a função de pular do jogador

    if pulando: #se estiver pulando
        jogador.rect.y += jogador.speedy #atualiza a posição do jogador
        jogador.speedy += GRAVIDADE # aumenta a velocidade do pulo
        if jogador.rect.bottom >= pulo_inicial:  #se o jogador estiver no chão
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
        som_explosao.play()
        pygame.time.wait(1000)
        inicializar_jogo()  # Reinicia o jogo
        menu_principal()

    # Atualiza o texto da vida do jogador
    texto_vida = renderizar_vida(vida_jogador)

    # Atualiza o texto da pontuação
    texto_pontuacao = renderizar_pontuacao(pontos)

    # ----- Gera saídas
    janela.fill((255, 255, 255))  # Preenche com a cor branca
    janela.blit(fundo, (0, 0)) # coloca a imagem de fundo na tela
    janela.blit(texto_vida, (30, 10)) #coloca o texto da vida na tela
    janela.blit(texto_pontuacao, (630, 10)) # posicione o texto da pontuação na tela


    # Desenhando a bomba
    todas_sprites.draw(janela)
    pygame.display.update() # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados 