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



def desenhar_estrela(tela, x, y, raio):
    
    pontos = []
    for i in range(10):
        angulo = i * math.pi / 5 - math.pi / 2
        tamanho = raio if i % 2 == 0 else raio * 0.48
        pontos.append((round(x + math.cos(angulo) * tamanho),
                       round(y + math.sin(angulo) * tamanho)))
    pygame.draw.polygon(tela, (255, 218, 81), pontos)
    pygame.draw.polygon(tela, (180, 104, 52), pontos, 1)

class Jogo:

    def __init__(self, sons):
        self.sons = sons
        self.monica = Personagem()
        self.pontos = 0
        self.recorde = carregar_recorde()
        self.indice = 0
        self.carregar_fase()

    def carregar_fase(self):
        """Monta a fase e repõe os itens da nova área."""
        self.fase = FASES[self.indice]
        self.fundo = carregar_fundo(self.fase["fundo"])
        self.chao = [pygame.Rect(a, CHAO, b - a, ALTURA - CHAO) for a, b in self.fase["trechos"]]
        self.plataformas = self.chao + [pygame.Rect(x, y, largura, 18)
                                        for x, y, largura in self.fase["plataformas"]]
        self.caixas = [pygame.Rect(x, CHAO - 18, largura, 18)
                       for x, largura in self.fase["caixas"]]
        self.estrelas = [pygame.Rect(x - 10, y - 10, 20, 20) for x, y in self.fase["estrelas"]]
        self.final = self.fase["largura"] - 130
        self.recomecar_trecho()


    def recomecar_trecho(self):
        self.monica.reposicionar()
        self.cebolinha = 0
        self.quadro = 0
        self.camera = 0
        self.efeitos = []
        self.cascao = {x: 0 for x in self.fase["cascao"]}
        self.bolas = []
        self.poderes = [(pygame.Rect(x - 12, y - 12, 24, 24), tipo)
                        for x, y, tipo in self.fase["poderes"]]
    def tocar(self, nome):
        som = self.sons.get(nome)
        if som:
            som.play()
    def pontuar(self, pontos):
        self.pontos += pontos
        if self.pontos > self.recorde:
            self.recorde = self.pontos
            try:
                ARQUIVO_RECORDE.write_text(str(self.recorde), encoding="utf-8")
            except OSError:
                pass


    def distancia(self):
        return max(0, round(self.monica.corpo.centerx - self.cebolinha))

    def altura_cebolinha(self):
        for i in range(len(self.chao) - 1):
            inicio = self.chao[i].right - 18
            fim = self.chao[i + 1].left + 18
            if inicio < self.cebolinha < fim:
                progresso = (self.cebolinha - inicio) / (fim - inicio)
                return round(54 * math.sin(progresso * math.pi))
        return 0
    
    def atualizar_perseguicao(self):
        x = self.monica.corpo.centerx
        if self.quadro > 50:
            self.cebolinha = max(self.cebolinha + self.fase["velocidade_cebolinha"], x - 245)
        self.camera = max(0, min(x - 295, self.fase["largura"] - LARGURA))



    def atualizar_cascao(self):
        for x, lancamento in self.cascao.items():
            distancia = x - self.monica.corpo.centerx
            if lancamento == 0 and 0 < distancia < 210:
                self.cascao[x] = self.quadro + 28
            elif lancamento == self.quadro:
                self.bolas.append(pygame.Rect(x - 19, CHAO - 16, 16, 16))
                self.cascao[x] = -1

        for bola in self.bolas[:]:
            bola.x -= 4
            if not any(piso.left <= bola.centerx < piso.right for piso in self.chao):
                self.bolas.remove(bola)