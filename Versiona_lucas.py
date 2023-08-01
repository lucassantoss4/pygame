import pygame
import random

# Inicialização do Pygame
pygame.init()

# Definindo a largura e a altura da janela do jogo
largura = 1600
altura = 900

# Carregando as imagens do fundo e do pescador
imagem_fundo = pygame.transform.scale(pygame.image.load("fundoo.jpg"), (largura, altura))
pescador = pygame.transform.scale(pygame.image.load("Fisherman.jpg"), (largura // 20, altura // 11))
pescador_virado = pygame.transform.flip(pescador, True, False)