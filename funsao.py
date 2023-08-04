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