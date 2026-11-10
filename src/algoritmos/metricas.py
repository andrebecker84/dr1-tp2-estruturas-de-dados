"""Contadores das operações que dominam o custo: medimos passos, não tempo."""
from dataclasses import dataclass


@dataclass
class Metricas:
    comparacoes: int = 0
    trocas: int = 0
    deslocamentos: int = 0
    acessos: int = 0


def medir(algoritmo, *args, **kwargs):
    """Executa o algoritmo com contadores zerados e devolve (resultado, metricas)."""
    metricas = Metricas()
    return algoritmo(*args, metricas=metricas, **kwargs), metricas
