import pygame
import random
import time
import os

from src.config import *
from src.sprites import Jogador, Estrela, Bomba

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Cria a Janela
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo Ninja')

# Fontes
fonte = pygame.font.SysFont(None, 48)

# Função para resolver caminhos de arquivos relativos
def get_path(path):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), path)

# ----- Carregamento de Assets -----
# Imagens
try:
    fundo = pygame.image.load(get_path('util/img/fundo2.jpg')).convert()
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

    ninja_img = pygame.image.load(get_path('util/img/ninja.png')).convert_alpha()
    ninja_img_small = pygame.transform.scale(ninja_img, (LARGURA_NINJA, ALTURA_NINJA))

    bomba_img = pygame.image.load(get_path('util/img/bomba.png')).convert_alpha()
    bomba_img_small = pygame.transform.scale(bomba_img, (LARGURA_BOMBA, ALTURA_BOMBA))

    estrela_img = pygame.image.load(get_path('util/img/estrela.png')).convert_alpha()
    estrela_img_small = pygame.transform.scale(estrela_img, (LARGURA_ESTRELA, ALTURA_ESTRELA))

    menu_img = pygame.image.load(get_path('util/img/tela_de_inicio.png')).convert_alpha()
    menu_img = pygame.transform.scale(menu_img, (LARGURA, ALTURA))
except Exception as e:
    print(f"Erro ao carregar imagens: {e}")
    pygame.quit()
    exit()

# Sons
try:
    som_fundo = pygame.mixer.Sound(get_path('util/som/musica.mp3'))
    som_fundo.set_volume(0.2)

    som_pulo = pygame.mixer.Sound(get_path('util/som/som_pulo.mp3'))
    som_pulo.set_volume(0.4)

    som_explosao = pygame.mixer.Sound(get_path('util/som/bomba_som.mp3'))
    som_explosao.set_volume(0.1)

    som_estrela = pygame.mixer.Sound(get_path('util/som/som_estrela.mp3'))
    som_estrela.set_volume(0.1)
except Exception as e:
    print(f"Erro ao carregar sons: {e}")
    # Se der erro no som, o jogo pode continuar sem áudio, mas idealmente seria tratado

clock = pygame.time.Clock()

def renderizar_vida(vida):
    return fonte.render(f"Vida: {chr(9829) * vida}", True, BRANCO)

def renderizar_pontuacao(pontos):
    return fonte.render(f"Pontuação: {pontos}", True, BRANCO)

def menu_principal():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return

        janela.blit(menu_img, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

def jogo():
    som_fundo.play(loops=-1)
    
    # Grupos de Sprites
    todas_sprites = pygame.sprite.Group()
    todas_bombas = pygame.sprite.Group()
    todas_estrelas = pygame.sprite.Group()

    jogador = Jogador(ninja_img_small)
    todas_sprites.add(jogador)

    vida_jogador = 3
    pontos = 0

    intervalo_estrela = 1
    ultimo_spawn_estrela = time.time()
    max_estrelas = random.randint(2, 5)

    intervalo_bomba = 1
    ultimo_spawn_bomba = time.time()
    max_bombas = random.randint(4, 10)

    rodando = True
    while rodando:
        clock.tick(FPS)
        agora = time.time()

        # Tratamento de Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                exit()
                
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    jogador.speedx -= VELOCIDADE_JOGADOR
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    jogador.speedx += VELOCIDADE_JOGADOR
                if evento.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    if not jogador.pulando:
                        som_pulo.play()
                        jogador.pular()
            
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    jogador.speedx += VELOCIDADE_JOGADOR
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    jogador.speedx -= VELOCIDADE_JOGADOR

        # Lógica de Spawn de Itens
        if agora - ultimo_spawn_estrela >= intervalo_estrela and len(todas_estrelas) < max_estrelas:
            estrela = Estrela(estrela_img_small)
            todas_sprites.add(estrela)
            todas_estrelas.add(estrela)
            ultimo_spawn_estrela = agora
            max_estrelas = random.randint(2, 5)

        if agora - ultimo_spawn_bomba >= intervalo_bomba and len(todas_bombas) < max_bombas:
            bomba = Bomba(bomba_img_small)
            todas_sprites.add(bomba)
            todas_bombas.add(bomba)
            ultimo_spawn_bomba = agora
            max_bombas = random.randint(4, 10)

        # Atualização dos Sprites
        todas_sprites.update()

        # Colisões
        hits_bomba = pygame.sprite.spritecollide(jogador, todas_bombas, True)
        hits_estrela = pygame.sprite.spritecollide(jogador, todas_estrelas, True)

        if hits_estrela:
            som_estrela.play()
            pontos += 10 * len(hits_estrela)
            if pontos > 0 and pontos % 100 == 0:
                vida_jogador = min(vida_jogador + 1, 5) # Cap em 5 de vida max

        if hits_bomba:
            som_explosao.play()
            vida_jogador -= len(hits_bomba)

        if vida_jogador <= 0:
            som_fundo.stop()
            som_explosao.play()
            pygame.time.wait(1000)
            return # Retorna para o menu principal

        # Renderização
        janela.blit(fundo, (0, 0))
        
        texto_vida = renderizar_vida(vida_jogador)
        texto_pontuacao = renderizar_pontuacao(pontos)
        
        janela.blit(texto_vida, (30, 10))
        janela.blit(texto_pontuacao, (LARGURA - 300, 10))

        todas_sprites.draw(janela)
        pygame.display.update()

def main():
    while True:
        menu_principal()
        jogo()

if __name__ == '__main__':
    main()
