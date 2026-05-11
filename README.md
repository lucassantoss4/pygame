# 🥷 Jogo Ninja - Pygame

Um jogo de arcade frenético desenvolvido em Python utilizando a biblioteca Pygame (ou Pygame-ce). Controle o ninja, colete estrelas para ganhar pontos e desvie das bombas para sobreviver!

## 🚀 Melhorias e Destaques (Refatoração)

Este projeto passou por uma reestruturação completa para seguir padrões profissionais de desenvolvimento de jogos:

- **Arquitetura Modular**: O código foi dividido em `src/main.py`, `src/config.py` e `src/sprites.py`.
- **Game Feel Aprimorado**:
    - **Inércia**: Movimentação com aceleração e atrito para maior fluidez.
    - **Dificuldade Progressiva**: O jogo acelera conforme você ganha pontos.
    - **Screen Shake**: Efeito de tremor na tela ao sofrer dano.
    - **Partículas**: Efeitos visuais dinâmicos ao coletar itens ou colidir com bombas.
- **Colisões Precisas**: Implementação de `Masks` para detecção de colisão baseada em pixels, não apenas em retângulos.

## 🛠️ Pré-requisitos

- Python 3.10 ou superior.
- [Pygame-ce](https://pygam-ce.org/) (recomendado para melhor compatibilidade em versões novas do Python).

## 📥 Instalação e Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/lucassantoss4/pygame.git
   cd pygame
   ```

2. **Crie e ative um ambiente virtual**:
   ```powershell
   # Windows
   python -m venv .venv
   & ".\.venv\Scripts\Activate.ps1"
   ```

3. **Instale as dependências**:
   ```bash
   pip install pygame-ce
   ```

## 🎮 Como Jogar

Execute o jogo a partir da raiz do projeto:
```bash
python -m src.main
```

### Controles:
- **A / Seta Esquerda**: Mover para a esquerda.
- **D / Seta Direita**: Mover para a direita.
- **Espaço / W / Seta Cima**: Pular.
- **Espaço (no Menu)**: Iniciar o jogo.

## 📁 Estrutura do Projeto

```
pygame/
├── src/
│   ├── main.py       # Loop principal e gerenciamento de estados
│   ├── sprites.py    # Classes do Jogador, Inimigos e Partículas
│   └── config.py     # Constantes de física e visual
├── util/
│   ├── img/          # Assets de imagem
│   └── som/          # Assets de áudio
├── requirements.txt  # Lista de dependências
└── README.md         # Documentação
```

## 📜 Licença
Este projeto é para fins educacionais. Sinta-se à vontade para clonar e melhorar!
