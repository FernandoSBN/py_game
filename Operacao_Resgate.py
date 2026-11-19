import pygame

LARGURA, ALTURA = 960, 540
FPS = 60
CHAO = 452
TAMANHO_FASE = 23500
AEROPORTO_X = TAMANHO_FASE - 280
INICIO_JOGADOR_X = 90
ANDAR, CORRER = 160, 245
PIXELS_POR_METRO = 50
FRENTE_PERSEGUIDOR = 24
GRAVIDADE, FORCA_PULO = 1500, 620
DURACAO_PODER, DURACAO_MITO = 8.0, 2.0
INVULNERABILIDADE = 1.6
ATRASO_PERSEGUIDOR = 2.0
PROPORCAO_PERSEGUIDOR = 0.96
VELOCIDADE_PERSEGUIDOR = CORRER * PROPORCAO_PERSEGUIDOR
POSICAO_PERSEGUIDOR = -220
ALERTA_PODER = 3.0
VELOCIDADE_PATRULHA = 74
VELOCIDADE_SENTINELA = 112
ALCANCE_SENTINELA = 220
AVISO_SENTINELA = 0.55
INTERVALO_SALTO = 1.8
PULO_INIMIGO = 305
VIDAS = 3
BRANCO = (239, 239, 219)
AMARELO = (255, 207, 87)
VERMELHO = (224, 71, 84)
ESCURO = (14, 20, 34)


def texto(tela, mensagem, x, y, tamanho=24, cor=BRANCO, centro=False):
    chave = tamanho
    if chave not in texto.fontes:
        texto.fontes[chave] = pygame.font.Font(None, tamanho)
    imagem = texto.fontes[chave].render(mensagem, True, cor)
    retangulo = imagem.get_rect()
    if centro:
        retangulo.center = (int(x), int(y))
    else:
        retangulo.topleft = (int(x), int(y))
    tela.blit(imagem, retangulo)