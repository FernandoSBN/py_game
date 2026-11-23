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


    def coletar_itens(self):
        monica = self.monica
        for estrela in self.estrelas[:]:
            if monica.corpo.colliderect(estrela):
                self.estrelas.remove(estrela)
                self.efeitos.append((estrela.center, (255, 209, 70), self.quadro))
                self.pontuar(10)
                self.tocar("coleta")

        for item in self.poderes[:]:
            area, tipo = item
            if monica.corpo.colliderect(area):
                self.poderes.remove(item)
                if tipo == "escudo":
                    monica.escudo = True
                else:
                    monica.impulso = 360
                self.efeitos.append((area.center, (96, 218, 247), self.quadro))
                self.tocar("coleta")
    def atualizar(self, eixo, pular):
        self.quadro += 1
        monica = self.monica
        corpo = monica.corpo
        if monica.mover(eixo, pular, self.plataformas):
            self.tocar("salto")
        corpo.right = min(corpo.right, self.fase["largura"])
        self.atualizar_perseguicao()
        self.atualizar_cascao()
        self.coletar_itens()

        caiu = corpo.top > ALTURA
        alcancada = corpo.left <= self.cebolinha + 13
        impacto = alcancada or corpo.collidelist(self.caixas) >= 0 or corpo.collidelist(self.bolas) >= 0
        if caiu or (impacto and not monica.imunidade):
            self.tocar("dano")
            if monica.escudo and not caiu:
                monica.escudo = False
                monica.imunidade = 90
                monica.atordoada = 18
                if alcancada:
                    self.cebolinha = corpo.left - 160
            else:
                monica.vidas -= 1
                if monica.vidas == 0:
                    return "derrota"
                self.recomecar_trecho()
                self.aviso_retorno = "Cebolinha te alcançou!" if alcancada else "Tente a fuga de novo!"
                return "respawn"

        if corpo.centerx >= self.final and monica.no_chao:
            self.pontuar(100)
            self.tocar("coleta")
            if self.indice == len(FASES) - 1:
                return "vitoria"
            self.aviso_transicao = ("Mônica fugiu pelo quintal!" if self.fase.get("interior")
                                    else "Mônica entrou na casa do Cascão!")
            self.indice += 1
            self.carregar_fase()
            return "transicao"

        self.efeitos = [efeito for efeito in self.efeitos if self.quadro - efeito[2] < 22]
        return "partida"

    def desenhar_fundo_provisorio(self, tela):
        parque = self.indice == 2
        if self.fase.get("interior"):
            tela.fill((238, 188, 171))
            for x in range(-self.camera % 210 - 210, LARGURA, 210):
                pygame.draw.rect(tela, (160, 106, 91), (x, 175, 85, 106), border_radius=7)
                pygame.draw.rect(tela, (254, 230, 186), (x + 7, 182, 71, 92), border_radius=4)
            pygame.draw.rect(tela, (184, 126, 102), (0, 421, LARGURA, 23))
            return
        ceu = (146, 222, 236) if parque else (140, 211, 251)
        tela.fill(ceu)
        pygame.draw.circle(tela, (255, 229, 142), (769 - self.camera // 22, 145), 45)
        for i in range(8):
            x = i * 213 - self.camera // 5 - 186
            y = 125 + (i * 27) % 106
            pygame.draw.ellipse(tela, (239, 250, 252), (x, y, 124, 27))
            pygame.draw.ellipse(tela, (239, 250, 252), (x + 28, y - 15, 62, 36))
        for i in range(11):
            x = i * 188 - self.camera // 3 - 155
            pygame.draw.ellipse(tela, (119, 207, 170), (x, 302 - i % 3 * 19, 270, 201))
            if not parque and i % 3 != 0:
                cor = [(247, 172, 127), (254, 214, 131), (224, 177, 223)][i % 3]
                y = 308 - i % 2 * 32
                pygame.draw.rect(tela, cor, (x, y, 120, CHAO - y))
                pygame.draw.polygon(tela, (177, 88, 108), [(x - 12, y), (x + 58, y - 49), (x + 132, y)])
                pygame.draw.rect(tela, (119, 93, 143), (x + 71, CHAO - 65, 29, 65), border_radius=5)
                pygame.draw.rect(tela, (236, 248, 249), (x + 19, y + 29, 34, 31), border_radius=3)
                pygame.draw.line(tela, (105, 155, 170), (x + 36, y + 29), (x + 36, y + 59), 2)
            else:
                pygame.draw.rect(tela, (145, 104, 84), (x + 66, 355, 14, 89), border_radius=5)
                for dx, dy in ((0, 9), (24, -27), (43, 3)):
                    pygame.draw.circle(tela, (67, 167 + i % 3 * 13, 126), (x + 51 + dx, 342 + dy), 34)
                pygame.draw.ellipse(tela, (78, 174, 128), (x + 95, 404, 65, 36))

    def desenhar_cenario(self, tela):
        parque = self.indice == 2
        interior = self.fase.get("interior")
        if self.fundo is None:
            self.desenhar_fundo_provisorio(tela)
        else:
            # Usa a largura extra da imagem ao longo da fase inteira
            percurso = self.fase["largura"] - LARGURA
            sobra = self.fundo.get_width() - LARGURA
            x = -round(self.camera * sobra / percurso)
            y = CHAO - round(self.fundo.get_height() * 0.91)
            tela.blit(self.fundo, (x, y))
        pygame.draw.rect(tela, (84, 148, 151), (0, CHAO, LARGURA, ALTURA - CHAO))

        for piso in self.plataformas:
            area = piso.move(-self.camera, 0)
            base = (160, 106, 91) if parque or interior else (106, 106, 134)
            topo = (102, 208, 110) if parque else (254, 219, 179)
            pygame.draw.rect(tela, base, area, border_radius=4)
            pygame.draw.rect(tela, topo, (area.x, area.y, area.w, 6), border_radius=3)
            if piso.height > 18:
                y = area.top + (33 if parque else 49)
                if not parque and not interior:
                    pygame.draw.rect(tela, (196, 180, 182), (area.x, area.top + 6, area.w, 14))
                for x in range(area.x + 12, area.right - 17, 44):
                    pygame.draw.line(tela, topo, (x, y), (x + 16, y), 2)