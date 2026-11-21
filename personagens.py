import math
import pygame

class Personagem:
    
    def __init__(self):
        self.vidas = 3
        self.corpo = pygame.Rect(100, 406, 28, 38)
        self.reposicionar()

    def reposicionar(self):
        self.corpo.topleft = (100, 406)
        self.vel_y = 0
        self.no_chao = True
        self.direcao = 1
        self.passos = 0
        self.impulso = 0
        self.escudo = False
        self.imunidade = 0
        self.atordoada = 0

    def mover(self, eixo, pular, plataformas):
        self.impulso = max(0, self.impulso - 1)
        self.imunidade = max(0, self.imunidade - 1)
        if self.atordoada:
            self.atordoada -= 1
            eixo = 0
        if eixo:
            self.direcao = eixo
            self.passos += 1
        else:
            self.passos = 0
        self.corpo.x += eixo * (8 if self.impulso else 5)
        self.corpo.left = max(0, self.corpo.left)
        for piso in plataformas:
            if self.corpo.colliderect(piso):
                if eixo > 0:
                    self.corpo.right = piso.left
                elif eixo < 0:
                    self.corpo.left = piso.right

        saltou = pular and self.no_chao
        if saltou:
            self.vel_y = -13
        self.vel_y = min(16, self.vel_y + 0.65)
        self.corpo.y += round(self.vel_y)
        self.no_chao = False
        for piso in plataformas:
            if self.corpo.colliderect(piso):
                if self.vel_y > 0:
                    self.corpo.bottom = piso.top
                    self.no_chao = True
                else:
                    self.corpo.top = piso.bottom
                self.vel_y = 0
        return saltou

    def desenhar(self, tela, camera):
        x, y = self.corpo.x - camera, self.corpo.y
        if self.imunidade and self.imunidade // 5 % 2:
            return
        if self.escudo:
            pygame.draw.circle(tela, (118, 238, 244), (x + 14, y + 19), 25, 2)
        if self.impulso:
            for i in range(3):
                inicio = x + 14 - self.direcao * (24 + i * 5)
                pygame.draw.line(tela, (252, 190, 94), (inicio, y + 13 + i * 6),
                                 (inicio - 10 * self.direcao, y + 13 + i * 6), 2)
        passo = round(math.sin(self.passos * 0.38) * 4) if self.no_chao else 4
        desenhar_turma(tela, x, y, "monica", self.direcao, passo)
        desenhar_sansao(tela, x + (19 if self.direcao > 0 else -8), y + 15 + abs(passo) // 2)


