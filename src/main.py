import pygame
import random
import time
import os
import asyncio

from config import *
from sprites import Jogador, Estrela, Bomba, Particula

# Inicialização do Pygame
pygame.init()
try:
    pygame.mixer.init()
except:
    pass

# Cria a Janela
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo Ninja')

# Fontes
fonte = pygame.font.SysFont(None, 48)

# Função para resolver caminhos de arquivos relativos
def get_path(path):
    # Agora a pasta util estará DENTRO da pasta src
    return os.path.join(os.path.dirname(__file__), path)

# ----- Carregamento de Assets -----
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

clock = pygame.time.Clock()

def renderizar_vida(vida):
    return fonte.render(f"Vida: {chr(9829) * vida}", True, BRANCO)

def renderizar_pontuacao(pontos):
    return fonte.render(f"Pontuação: {pontos}", True, BRANCO)

async def menu_principal():
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
        await asyncio.sleep(0)

async def jogo():
    try:
        som_fundo.play(loops=-1)
    except:
        pass
    
    todas_sprites = pygame.sprite.Group()
    todas_bombas = pygame.sprite.Group()
    todas_estrelas = pygame.sprite.Group()
    jogador = Jogador(ninja_img_small)
    todas_sprites.add(jogador)

    vida_jogador = 3
    pontos = 0
    dificuldade = 0
    intervalo_estrela = 1
    ultimo_spawn_estrela = time.time()
    max_estrelas = random.randint(2, 5)
    intervalo_bomba = 1
    ultimo_spawn_bomba = time.time()
    max_bombas = random.randint(4, 10)
    shake_timer = 0

    rodando = True
    while rodando:
        clock.tick(FPS)
        agora = time.time()
        render_offset = [0, 0]
        if shake_timer > 0:
            shake_timer -= 1
            render_offset = [random.randint(-SCREEN_SHAKE_INTENSITY, SCREEN_SHAKE_INTENSITY), 
                             random.randint(-SCREEN_SHAKE_INTENSITY, SCREEN_SHAKE_INTENSITY)]

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    if not jogador.pulando:
                        try: som_pulo.play()
                        except: pass
                        jogador.pular()

        # Lógica de Spawn de Itens (com dificuldade)
        if agora - ultimo_spawn_estrela >= intervalo_estrela and len(todas_estrelas) < max_estrelas:
            estrela = Estrela(estrela_img_small, bonus_velocidade=dificuldade)
            todas_sprites.add(estrela)
            todas_estrelas.add(estrela)
            ultimo_spawn_estrela = agora
            max_estrelas = random.randint(2, 5)

        if agora - ultimo_spawn_bomba >= intervalo_bomba and len(todas_bombas) < max_bombas:
            bomba = Bomba(bomba_img_small, bonus_velocidade=dificuldade)
            todas_sprites.add(bomba)
            todas_bombas.add(bomba)
            ultimo_spawn_bomba = agora
            max_bombas = random.randint(4, 10)

        todas_sprites.update()
        hits_bomba = pygame.sprite.spritecollide(jogador, todas_bombas, True, pygame.sprite.collide_mask)
        hits_estrela = pygame.sprite.spritecollide(jogador, todas_estrelas, True, pygame.sprite.collide_mask)

        if hits_estrela:
            try: som_estrela.play()
            except: pass
            for h in hits_estrela:
                pontos += 10
                for _ in range(10):
                    todas_sprites.add(Particula(h.rect.centerx, h.rect.centery, (255, 215, 0)))
            dificuldade = pontos // 100
            if pontos % 100 == 0:
                vida_jogador = min(vida_jogador + 1, 5)

        if hits_bomba:
            try: som_explosao.play()
            except: pass
            shake_timer = 15
            vida_jogador -= len(hits_bomba)
            for h in hits_bomba:
                for _ in range(15):
                    todas_sprites.add(Particula(h.rect.centerx, h.rect.centery, (255, 69, 0)))

        if vida_jogador <= 0:
            try: som_fundo.stop()
            except: pass
            pygame.time.wait(1000)
            return

        janela.blit(fundo, (render_offset[0], render_offset[1]))
        texto_vida = renderizar_vida(vida_jogador)
        texto_pontuacao = renderizar_pontuacao(pontos)
        janela.blit(texto_vida, (30 + render_offset[0], 10 + render_offset[1]))
        janela.blit(texto_pontuacao, (LARGURA - 300 + render_offset[0], 10 + render_offset[1]))
        for sprite in todas_sprites:
            janela.blit(sprite.image, (sprite.rect.x + render_offset[0], sprite.rect.y + render_offset[1]))
        pygame.display.update()
        await asyncio.sleep(0)

async def main():
    while True:
        await menu_principal()
        await jogo()

if __name__ == '__main__':
    asyncio.run(main())
