"""Interseção de dois arrays (Exercício 2)."""
from algoritmos.metricas import Metricas


def intersecao_aninhada(a, b, metricas=None):
    """Para cada valor de b, procura em a com um laço interno que para no primeiro igual. O(N x M)."""
    metricas = metricas or Metricas()
    comuns = []
    for valor in b:
        for outro in a:
            metricas.comparacoes += 1
            if valor == outro:
                comuns.append(valor)
                break
    return comuns


def intersecao(a, b, metricas=None):
    """Valores presentes nos dois arrays, uma vez cada, na ordem em que aparecem em b. O(N + M)."""
    metricas = metricas or Metricas()
    tabela = {}
    for valor in a:
        metricas.acessos += 1
        tabela[valor] = True                # True: está em a e ainda não entrou no resultado

    comuns = []
    for valor in b:
        metricas.acessos += 1
        if tabela.get(valor):
            comuns.append(valor)
            metricas.acessos += 1
            tabela[valor] = False           # um repetido em b não entra de novo
    return comuns
