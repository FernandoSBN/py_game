e coloca esse texto:

# Turma da Mônica: A Grande Perseguição

Jogo de plataforma e fuga em 2D desenvolvido em Python com **Pygame**, no qual a Mônica precisa escapar do Cebolinha, desviar de obstáculos e atravessar fases até colocar o Sansão a salvo.

---

## Autores

* **Carlos Eduardo da Silva Brito Duarte**
* **Vitor Ribeiro Helbusto**
* **Fernando da Silva Braga Neto**

---

## Ideia do Jogo e Evolução do Projeto

### Conceito inicial (*Lina*)
Antes da construção deste jogo, a ideia inicial era criar um projeto chamado **Lina**, no qual a protagonista fugia de uma sombra perseguidora ao longo de fases. Naquela concepção inicial, o jogo não contava com poderes especiais nem trilha sonora de fundo, pois esses elementos ainda não haviam sido pensados.

### Mudança de direção e implementação atual
Com o avanço do projeto, a equipe decidiu mudar a proposta para uma perseguição protagonizada pela **Turma da Mônica** (*A Grande Perseguição*), mantendo a estrutura de progressão por fases e a mecânica de fuga contínua, mas expandindo a jogabilidade e a imersão com:
* **Fases variadas:** *Correria no Bairro do Limoeiro*, *Casa do Cascão* e *Confusão no Parque*.
* **Poderes temporários:** **Proteção** (escudo que absorve um impacto, exceto queda em buraco, e afasta temporariamente o Cebolinha caso ele alcance a Mônica) e **Velocidade** (impulso de movimento por 6 segundos).
* **Áudio e trilha sonora:** Efeitos sonoros de salto, coleta e dano (`salto.wav`, `coleta.wav`, `dano.wav`), além de música de fundo contínua (`trilha.wav`) com opção de pausar/retomar.
* **Sistema de pontuação e recorde:** Estrelas valem 10 pontos, concluir cada fase vale 100 pontos, e o maior recorde é salvo localmente em `recorde_perseguicao.txt`.

---

## Como os Arquivos da Pasta `assets/` Foram Obtidos e Integrados

O jogo utiliza 4 imagens e 4 arquivos de áudio localizados na pasta `assets/`:
* **Imagens:** `A Grande Perseguição no Bairro.png`, `bg01.png`, `bg02.png` e `bg03 (2).png`.
* **Áudios:** `salto.wav`, `coleta.wav`, `dano.wav` e `trilha.wav`.

Na organização do projeto, esses recursos podem ter sido reunidos a partir de bibliotecas gratuitas e bancos de ativos independentes para prototipagem e desenvolvimento (como *OpenGameArt*, *itch.io* e *Freesound*), além de artes adaptadas ou criadas para compor a capa e os cenários das fases, sendo padronizados e salvos diretamente em `assets/`.

No código, o carregamento é feito de forma centralizada a partir do diretório do projeto (`PASTA / "assets"`):
* **Cenários e capa:** `carregar_fundo()` em `jogo.py` e `carregar_capa()` em `main.py` carregam as imagens com `pygame.image.load()`, redimensionam mantendo proporção com `pygame.transform.smoothscale()` e incluem fallback visual caso algum arquivo de imagem não esteja disponível.
* **Efeitos e música:** `carregar_sons()` em `main.py` carrega os efeitos `.wav` via `pygame.mixer.Sound()` quando o áudio está inicializado, enquanto `pygame.mixer.music` carrega e reproduz `trilha.wav` em loop contínuo.

---

## Estrutura do Repositório

```text
├── main.py                  # Loop principal, menus, HUD, tela cheia, áudio e controles
├── jogo.py                  # Definição das fases, física da fuga, itens, colisões e recorde
├── personagem.py            # Classe Personagem (Mônica) e desenho da turma e do Sansão
├── requirement.txt          # Dependência do projeto (pygame==2.6.1)
├── recorde_perseguicao.txt  # Armazena o maior recorde de pontuação
├── .gitignore               # Arquivos e pastas ignorados pelo Git
└── assets/                  # Imagens de fundo/capa e arquivos de áudio (.wav)
```

---

## Requisitos para Jogar

* **Python 3.x** instalado no sistema.
* **Pygame 2.6.1** (conforme especificado em `requirement.txt`).
* Dispositivo de saída de áudio (opcional, pois o jogo trata a ausência do mixer sem interromper a execução).

Instalação das dependências:

```bash
pip install -r requirement.txt
```

---

## Como Executar o Jogo

O arquivo principal que deve ser executado é o **`main.py`**.

No terminal, dentro da pasta raiz do projeto, execute:

```bash
python main.py
```

*(Em sistemas Linux/macOS onde o comando padrão seja `python3`, utilize `python3 main.py`.)*

---

## Como Jogar

### Controles
* **Mover para a esquerda / direita:** `A` / `D` ou setas `←` / `→`
* **Pular:** `Espaço`
* **Pausar / retomar partida:** `Esc` (a partida também pausa automaticamente se a janela perder o foco)
* **Pausar / retomar música:** `M`
* **Navegar nos menus:** setas do teclado + `Enter`, ou clique com o botão esquerdo do mouse (há também um botão de fechar no canto superior direito).

### Regras e Objetivo
* Fuja do **Cebolinha** enquanto avança por cada fase até alcançar a saída (ou a bandeira de chegada) com o **Sansão**.
* Evite cair nos buracos entre trechos do chão, encostar no Cebolinha, colidir com caixas ou ser atingido pelas bolas rasteiras lançadas após o aviso do **Cascão**.
* A Mônica começa com **3 vidas**. Se todas acabarem, ocorre o fim da perseguição; se alcançar o fim da última fase, o Sansão está a salvo e a partida é vencida.
* Colete **estrelas** (`+10` pontos cada) e finalize fases (`+100` pontos cada) para bater o recorde.

## Apoio de Ferramentas no Desenvolvimento
Durante a criação do projeto, a equipe utilizou:
* **GitHub Copilot:** auxílio geral na construção e organização dos códigos em Python/Pygame, como estrutura de estados e menus em `main.py` e organização das mecânicas e fases em `jogo.py`.
* **ChatGPT (cálculos e desenhos):** apoio pontual em trechos com cálculos — como física de pulo/gravidade/colisão (`personagem.py`), avanço da perseguição, câmera, arco sobre buracos e escala de cenários (`jogo.py`), além de cálculos de HUD, tempo de impulso e ajuste da capa (`main.py`) — e em desenhos via código com Pygame, como os personagens (`desenhar_turma`, `desenhar_sansao`), estrelas, poderes, efeitos, cenários provisórios e cenas finais.