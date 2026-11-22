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