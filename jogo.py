import math
from pathlib import Path

import pygame

from personagem import Personagem, desenhar_turma

LARGURA, ALTURA = 960, 540
CHAO = 444
PASTA = Path(__file__).resolve().parent
ARQUIVO_RECORDE = PASTA / "recorde_perseguicao.txt"

FASES = [
    {
        "nome": "Correria no Bairro do Limoeiro", "largura": 2380, "velocidade_cebolinha": 2.4,
        "fundo": "bg02.png",
        "trechos": [(0, 550), (636, 1120), (1224, 1750), (1846, 2380)],
        "plataformas": [(250, 380, 132), (690, 364, 145), (1320, 370, 150), (1920, 360, 105)],
        "caixas": [(910, 48), (1510, 64), (2080, 48)], "cascao": [1020],
        "estrelas": [(200, 415), (285, 352), (345, 352), (595, 378), (759, 335),
                     (1000, 415), (1170, 366), (1390, 342), (1650, 415), (1800, 370), (2200, 415)],
        "poderes": [(320, 347, "impulso")],
    },
    {
        "nome": "Casa do Cascão", "largura": 1650, "velocidade_cebolinha": 2.8,
        "fundo": "bg01.png", "interior": True,
        "trechos": [(0, 1650)],
        "plataformas": [(205, 372, 105), (680, 365, 105), (1150, 360, 100)],
        "caixas": [(420, 48), (840, 48), (1300, 60)], "cascao": [1040],
        "estrelas": [(165, 415), (255, 344), (530, 415), (745, 335),
                     (955, 414), (1200, 332), (1330, 370), (1420, 415)],
        "poderes": [(600, 415, "escudo")],
    },
    {
        "nome": "Confusão no Parque", "largura": 2790, "velocidade_cebolinha": 3.3,
        "fundo": "bg03 (2).png",
        "trechos": [(0, 460), (568, 970), (1092, 1530), (1660, 2090), (2220, 2790)],
        "plataformas": [(140, 370, 110), (615, 352, 109), (1135, 369, 100),
                        (1350, 326, 112), (1720, 366, 105), (2310, 352, 130)],
        "caixas": [(320, 48), (770, 72), (1280, 70), (1875, 72), (2490, 80)],
        "cascao": [900, 2010],
        "estrelas": [(207, 342), (513, 370), (675, 322), (808, 370), (1030, 376),
                     (1200, 342), (1404, 298), (1595, 365), (1810, 338), (2155, 365),
                     (2390, 322), (2530, 366), (2660, 410)],
        "poderes": [(700, 325, "escudo"), (2035, 415, "impulso")],
    },
]


def carregar_recorde():
    try:
        return max(0, int(ARQUIVO_RECORDE.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        return 0


        def carregar_fundo(nome):
   
    try:
        imagem = pygame.image.load(str(PASTA / "assets" / nome))
    except (OSError, pygame.error):
        return None

    largura, altura = imagem.get_size()
    escala = max((LARGURA + 192) / largura, CHAO / (altura * 0.91))
    return pygame.transform.smoothscale(imagem, (round(largura * escala), round(altura * escala)))