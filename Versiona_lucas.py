import pygame
import random

# Inicialização do Pygame
pygame.init()

# Definindo a largura e a altura da janela do jogo
largura, altura = 1600, 900

# Carregando as imagens do fundo e do pescador
imagem_fundo = pygame.transform.scale(pygame.image.load("fundoo.jpg"), (largura, altura))
pescador = pygame.transform.scale(pygame.image.load("Fisherman.png"), (largura // 20, altura // 11))
pescador_virado = pygame.transform.flip(pescador, True, False)

# Criando a janela do jogo
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo")

# Definindo as velocidades e direções do pescador
velocidade_caminhada = 10
velocidade_pulo = 20
direcao = "direita"
pulou = False
gravidade = 1

# Lista para armazenar os peixes
lista_peixes = []

