"""Primeiro valor duplicado de um array de strings (Exercício 3)."""
from algoritmos.metricas import Metricas


def primeiro_duplicado_aninhado(valores, metricas=None):
    """Compara cada valor com todos os anteriores. O(N²)."""
    metricas = metricas or Metricas()
    for j in range(len(valores)):
        for i in range(j):
            metricas.comparacoes += 1
            if valores[i] == valores[j]:
                return valores[j]
    return None


def primeiro_duplicado(valores, metricas=None):
    """Primeiro valor que reaparece na ordem de leitura, ou None. Uma passada só: O(N)."""
    metricas = metricas or Metricas()
    vistos = {}
    for valor in valores:
        metricas.acessos += 1
        if valor in vistos:
            return valor
        metricas.acessos += 1
        vistos[valor] = True
    return None
