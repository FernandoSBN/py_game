import math
import pygame

class Personagem:
    
    def __init__(self):
        self.vidas = 3
        self.corpo = pygame.Rect(100, 406, 28, 38)
        self.reposicionar()

    def reposicionar(self):
        self.corpo.topleft = (100, 406)
        self.vel_y = 0          #velocidade vertical
        self.no_chao = True     #esta no chao
        self.direcao = 1        #1 = direita, -1 = esquerda
        self.passos = 0         #contador para animar as pernas
        self.impulso = 0        #quanto falta no poder de velocidade
        self.escudo = False     #protege contraa dano
        self.imunidade = 0      #quanto tempo personagem pisca
        self.atordoada = 0      #tempo sem andar depois de tomar dano

    def mover(self, eixo, pular, plataformas):
        #contadores para os estados temporarios
        self.impulso = max(0, self.impulso - 1)
        self.imunidade = max(0, self.imunidade - 1)
        if self.atordoada:
            self.atordoada -= 1
            eixo = 0            #atordoado nao anda 
        #direcao e animacao dos passos
        if eixo:
            self.direcao = eixo
            self.passos += 1
        else:
            self.passos = 0
        #movimento horizontal
        self.corpo.x += eixo * (8 if self.impulso else 5)
        self.corpo.left = max(0, self.corpo.left)
        for piso in plataformas:
            if self.corpo.colliderect(piso):
                #encosta no lado do obstaculo        
                if eixo > 0:
                    self.corpo.right = piso.left
                elif eixo < 0:
                    self.corpo.left = piso.right
        #movimento vertical
        saltou = pular and self.no_chao
        if saltou:
            self.vel_y = -13
        self.vel_y = min(16, self.vel_y + 0.65)
        self.corpo.y += round(self.vel_y)
        self.no_chao = False
        for piso in plataformas:
            if self.corpo.colliderect(piso):
                if self.vel_y > 0:          #caindo: pousa em cima
                    self.corpo.bottom = piso.top
                    self.no_chao = True
                else:                       #subindo: bate a cabeca
                    self.corpo.top = piso.bottom
                self.vel_y = 0
        return saltou

    def desenhar(self, tela, camera):
        # desenha a monica na tela
        x, y = self.corpo.x - camera, self.corpo.y
        #efeito de piscar
        if self.imunidade and self.imunidade // 5 % 2:
            return
        #circulo de escudo 
        if self.escudo:
            pygame.draw.circle(tela, (118, 238, 244), (x + 14, y + 19), 25, 2)
        #linha de velocidade atras do personagem 
        if self.impulso:
            for i in range(3):
                inicio = x + 14 - self.direcao * (24 + i * 5)
                pygame.draw.line(tela, (252, 190, 94), (inicio, y + 13 + i * 6),
                                 (inicio - 10 * self.direcao, y + 13 + i * 6), 2)
        passo = round(math.sin(self.passos * 0.38) * 4) if self.no_chao else 4
        desenhar_turma(tela, x, y, "monica", self.direcao, passo)
        desenhar_sansao(tela, x + (19 if self.direcao > 0 else -8), y + 15 + abs(passo) // 2)

def desenhar_sansao(tela, x, y):
    # Desenha o coelho azul que passa de um personagem para o outro
    azul = (71, 165, 237)
    pygame.draw.ellipse(tela, azul, (x + 1, y, 5, 12))      #orelha esquerda
    pygame.draw.ellipse(tela, azul, (x + 9, y - 2, 5, 13))  #orelha direita
    pygame.draw.ellipse(tela, azul, (x, y + 7, 16, 14))     #corpo
    pygame.draw.ellipse(tela, (166, 219, 255), (x + 4, y + 14, 9, 6)) #barriga
    for olho in (4, 11):
        pygame.draw.circle(tela, (29, 41, 82), (x + olho, y + 12), 1)

def desenhar_turma(tela, x, y, nome, direcao=1, passo=0):
    # Identifica cada personagem pela roupa e pela silhueta
    contorno = (44, 35, 64)
    pele = (255, 204, 152)
    cores = {"monica": (235, 64, 93), "cebolinha": (67, 177, 100), "cascao": (249, 197, 68)}
    #perna e sapato
    for lado, altura in ((6, passo), (18, -passo)):
        pygame.draw.ellipse(tela, pele, (x + lado, y + 28, 6, 10 - altura))
        pygame.draw.ellipse(tela, contorno, (x + lado - 2, y + 34 - altura, 11, 4))
    #corpo e roupas
    if nome == "monica":
        pygame.draw.polygon(tela, cores[nome], [(x + 7, y + 16), (x + 21, y + 16),
                                                (x + 27, y + 32), (x + 1, y + 32)])
        pygame.draw.ellipse(tela, contorno, (x + 1, y - 4, 26, 24))
    else:
        pygame.draw.rect(tela, cores[nome], (x + 3, y + 16, 23, 14), border_radius=5)
        calca = (99, 61, 156) if nome == "cascao" else (51, 64, 103)
        pygame.draw.rect(tela, calca, (x + 5, y + 27, 19, 6), border_radius=2)
    #rosto
    pygame.draw.ellipse(tela, pele, (x + 4 + direcao, y + 1, 21, 18))
    if nome == "cebolinha":
        for i in range(5):
            pygame.draw.line(tela, contorno, (x + 8 + i * 3, y + 3),
                             (x + 4 + i * 5, y - 5 - i % 2 * 3), 2)
    elif nome == "cascao":
        for i in range(5):
            pygame.draw.circle(tela, contorno, (x + 6 + i * 4, y + i % 2 * 2), 4)
        pygame.draw.circle(tela, (180, 117, 92), (x + 12, y + 13), 2)
    else:
        pygame.draw.arc(tela, contorno, (x + 1, y - 3, 25, 17), 0.2, 3.2, 4)
    pygame.draw.circle(tela, contorno, (x + 14 + 5 * direcao, y + 9), 2)
    pygame.draw.ellipse(tela, contorno, (x + 12 + 4 * direcao, y + 12, 6, 4))
    if nome == "monica":
        pygame.draw.rect(tela, (255, 250, 233), (x + 12 + 4 * direcao, y + 12, 4, 2))



