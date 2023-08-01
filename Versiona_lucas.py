# ===== Inicialização =====
# ----- Importa e inicia pacotes

import pygame

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
game = True
bomba_x = 200
# y negativo significa que está acima do topo da janela. A bomba começa fora da janela
bomba_y = - ALTURA_BOMBA
bomba_velocidade_x = 3
bomba_velocidade_y = 4

# ===== Loop principal =====
while game:
    # ------- Trata eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            game = False

    # ----- Atualiza estado do jogo
    bomba_x += bomba_velocidade_x
    bomba_y += bomba_velocidade_y

    # Se a bomba passar do final da tela, volta para cima  
    if bomba_y > ALTURA or bomba_x + LARGURA_BOMBA < 0 or bomba_x > LARGURA:
        bomba_x = 200
        bomba_y = - ALTURA_BOMBA

    # ----- Gera saídas
    janela.fill((255, 255, 255))  # Preenche com a cor branca
    janela.blit(fundo, (0, 0)) # coloca a imagem de fundo na tela
    janela.blit(bomba_img_small, (bomba_x, bomba_y)) # coloca a bomba na tela
    pygame.display.update() # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados      
