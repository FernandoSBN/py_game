import pygame

from jogo import ALTURA, LARGURA, PASTA, Jogo, desenhar_estrela
from personagem import desenhar_sansao, desenhar_turma

FUNDO = (54, 40, 89)
BORDA = (135, 102, 147)
CLARO = (251, 241, 222)
SUAVE = (204, 199, 226)
OURO = (255, 202, 113)
TURQUESA = (138, 235, 215)
AREA_CAPA = pygame.Rect(344, 85, 584, 368)
BOTAO_FECHAR = pygame.Rect(905, 18, 37, 37)

MENUS = {
    "menu": [("Jogar", "nova"), ("Como jogar", "instrucoes"), ("Sair", "sair")],
    "instrucoes": [("Voltar", "menu")],
    "pausa": [("Continuar", "partida"), ("Reiniciar", "nova"), ("Menu inicial", "menu")],
    "derrota": [("Tentar novamente", "nova"), ("Menu inicial", "menu")],
    "vitoria": [("Jogar novamente", "nova"), ("Menu inicial", "menu")],
}
TITULOS = {
    "instrucoes": "Como jogar",
    "pausa": "Partida pausada",
    "derrota": "Fim da perseguição",
    "vitoria": "Sansão a salvo!",
}


def escrever(tela, fonte, texto, cor, posicao):
    tela.blit(fonte.render(texto, True, cor), posicao)


def botoes(estado, com_capa=False):
    opcoes = MENUS.get(estado, [])
    if estado == "menu" and com_capa:
        return [pygame.Rect(38, 305, 270, 58),
                pygame.Rect(38, 376, 270, 47),
                pygame.Rect(38, 434, 270, 43)]
    return [pygame.Rect(63, 462 - len(opcoes) * 51 + i * 51, 367, 44)
            for i in range(len(opcoes))]

def carregar_capa():
    arquivo = PASTA / "assets" / "A Grande Perseguição no Bairro.png"
    try:
        imagem = pygame.image.load(str(arquivo))
    except (OSError, pygame.error):
        return None
    largura, altura = imagem.get_size()
    escala = min((AREA_CAPA.w - 12) / largura, (AREA_CAPA.h - 12) / altura)
    return pygame.transform.smoothscale(imagem, (round(largura * escala), round(altura * escala)))


def desenhar_hud(tela, jogo, fonte):
    pygame.draw.rect(tela, FUNDO, (15, 14, 875, 55), border_radius=12)
    pygame.draw.rect(tela, BORDA, (15, 14, 875, 55), 1, border_radius=12)
    escrever(tela, fonte, f"{jogo.indice + 1:02d}  {jogo.fase['nome']}", CLARO, (33, 31))
    escrever(tela, fonte, f"Pontos  {jogo.pontos}", OURO, (366, 31))
    escrever(tela, fonte, f"Vidas  {jogo.monica.vidas}", CLARO, (510, 31))
    poderes = []
    if jogo.monica.escudo:
        poderes.append("Proteção")
    if jogo.monica.impulso:
        segundos = (jogo.monica.impulso + 59) // 60
        poderes.append(f"Velocidade {segundos}s")
    if poderes:
        escrever(tela, fonte, "  +  ".join(poderes), TURQUESA, (643, 31))
    distancia = jogo.distancia()
    pygame.draw.rect(tela, FUNDO, (18, 486, 250, 42), border_radius=8)
    escrever(tela, fonte, f"Cebolinha atrás: {distancia} px", CLARO, (29, 489))
    pygame.draw.line(tela, BORDA, (30, 519), (254, 519), 2)
    cor = OURO if distancia < 75 else TURQUESA
    pygame.draw.circle(tela, cor, (30 + round(224 * min(distancia, 270) / 270), 519), 4)


def desenhar_menu(tela, estado, jogo, fontes, selecionado, capa=None):
    titulo, corpo, pequeno = fontes
    if estado == "menu" and capa is not None:
        tela.fill((24, 22, 48))
        pygame.draw.ellipse(tela, (36, 28, 71), (288, -195, 1040, 850))
        pygame.draw.ellipse(tela, (44, 33, 82), (363, -95, 835, 675))
        moldura = capa.get_rect(center=AREA_CAPA.center).inflate(12, 12)
        pygame.draw.rect(tela, (18, 16, 38), moldura.move(0, 10), border_radius=10)
        pygame.draw.rect(tela, (255, 214, 132), moldura, 2, border_radius=9)
        tela.blit(capa, capa.get_rect(center=moldura.center))
        escrever(tela, pequeno, "Turma da Mônica", OURO, (41, 95))
        escrever(tela, titulo, "A Grande", CLARO, (38, 127))
        escrever(tela, titulo, "Perseguição", CLARO, (38, 169))
        escrever(tela, corpo, "Fuja do Cebolinha", SUAVE, (41, 238))
        escrever(tela, corpo, "e leve o Sansão a salvo.", SUAVE, (41, 263))
        escrever(tela, pequeno, f"Recorde  {jogo.recorde}", SUAVE, (41, 495))
        desenhar_botoes(tela, estado, corpo, selecionado, com_capa=True)
        return

    pygame.draw.rect(tela, FUNDO, (36, 52, 421, 434), border_radius=24)
    pygame.draw.rect(tela, BORDA, (36, 52, 421, 434), 1, border_radius=24)
    pygame.draw.line(tela, OURO, (64, 81), (109, 81), 3)

    if estado == "menu":
        escrever(tela, corpo, "Turma da Mônica", OURO, (65, 100))
        escrever(tela, titulo, "A Grande", CLARO, (63, 128))
        escrever(tela, titulo, "Perseguição", CLARO, (63, 171))
        escrever(tela, pequeno, f"Recorde  {jogo.recorde}", SUAVE, (65, 234))
    else:
        escrever(tela, titulo, TITULOS[estado], CLARO, (63, 105))
        if estado == "instrucoes":
            linhas = [
                "Fuja do Cebolinha com o Sansão até a saída.",
                "A / D ou ← / → para correr",
                "Espaço para pular  ·  Esc para pausar",
                "Cuidado com caixas, buracos e bolas do Cascão.",
                "Cada estrela vale 10 pontos. Cada fase vale 100.",
                "Proteção: um impacto. Velocidade: seis segundos.",
                "M para pausar ou retomar a música.",
            ]
            for i, linha in enumerate(linhas):
                escrever(tela, pequeno, linha, SUAVE, (65, 174 + i * 28))
        elif estado == "pausa":
            escrever(tela, corpo, jogo.fase["nome"], SUAVE, (65, 185))
        else:
            escrever(tela, corpo, f"Pontuação final  {jogo.pontos}", OURO, (65, 188))
            escrever(tela, corpo, f"Recorde  {jogo.recorde}", SUAVE, (65, 223))

    desenhar_botoes(tela, estado, corpo, selecionado)

def desenhar_botoes(tela, estado, fonte, selecionado, com_capa=False):
    for i, area in enumerate(botoes(estado, com_capa)):
        ativo = selecionado == i or area.collidepoint(pygame.mouse.get_pos())
        principal = com_capa and i == 0
        fundo = OURO if ativo else (80, 62, 120) if com_capa else (51, 52, 86)
        if principal:
            fundo = (255, 229, 135) if ativo else OURO
        pygame.draw.rect(tela, fundo, area, border_radius=9)
        if com_capa:
            pygame.draw.rect(tela, CLARO if ativo else BORDA, area, 2, border_radius=9)
        texto = fonte.render(MENUS[estado][i][0], True, FUNDO if ativo or principal else CLARO)
        tela.blit(texto, texto.get_rect(center=area.center))