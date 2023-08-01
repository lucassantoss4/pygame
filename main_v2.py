import pygame
import random

# Inicialização do Pygame
pygame.init()

# Definindo a largura e a altura da janela do jogo
largura, altura = 1600, 900

# Carregando as imagens do fundo e do capitão
imagem_fundo = pygame.transform.scale(pygame.image.load("fundoo.jpg"), (largura, altura))
capitao = pygame.transform.scale(pygame.image.load("capitao.png"), (largura // 20, altura // 11))
capitao_virado = pygame.transform.flip(capitao, True, False)

# Criando a janela do jogo
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo")

# Definindo as velocidades e direções do personagem
velocidade_caminhada = 10
velocidade_pulo = 20
direcao = "direita"
pulou = False
gravidade = 1

# Lista para armazenar os moedas
lista_das_bombas = []

# Carregando e ajustando a imagem da bomba
bomba = pygame.transform.scale(pygame.image.load("bomba(1)png"), (largura // 10, altura // 10))
bomba = pygame.transform.rotate(bomba, 90)
velocidade_bomba = 35
gravidade_bomba = 1

# Classe para representar a bomba
class bomba(pygame.sprite.Sprite):
    def _init_(self, x, y, largura, altura, bomba_pulou, velocidade_bomba, altura_chao, pulou):
        super()._init_()
        self.largura = largura
        self.altura = altura
        self.peixe_pulou = bomba_pulou
        self.image = capitao
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade_moeda = velocidade_bomba
        self.altura_chao = altura_chao
        self.pulou = pulou

    def atualizar_movimento(self, indice):
        self.indice = indice
        if not self.bomba_pulou:
            self.velocidade_bomba = -self.velocidade_bomba
            self.bomba_pulou = True
        if self.bomba_pulou:
            self.rect.y += self.velocidade_bomba
            if self.velocidade_bomba < 0:
                self.velocidade_bomba += gravidade_bomba
            if self.velocidade_bomba >= 0:
                self.velocidade_bomba += 0.5
        if self.velocidade_bomba == 30:
            self.pulou = True
            if self.rect.y >= self.altura_chao + 100 and self.pulou:
                lista_das_bombas.pop(indice)
                self.bomba_pulou = False
                self.velocidade_bomba = 30

    def colidir(self, capitao, indice):
        self.capitao = capitao
        self.indice = indice
        if self.rect.colliderect(capitao):
            lista_das_bombas.pop(indice)
