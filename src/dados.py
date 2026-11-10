"""Entradas dos experimentos. A semente é fixa: toda execução gera os mesmos dados."""
import random
from enum import StrEnum

SEMENTE = 42
ARRAY_DAS_AULAS = (4, 2, 7, 1, 3)           # exemplo das Aulas 4 e 5 (Selection e Insertion Sort)
TAMANHOS_DAS_ORDENACOES = (10, 100, 1_000)  # os Exercícios 6 e 7 usam os mesmos dados
FRACAO_FORA_DO_LUGAR = 20                   # quase ordenada: 1 troca de vizinhos a cada 20 elementos


class Cenario(StrEnum):
    ORDENADA = "ordenada"
    QUASE_ORDENADA = "quase ordenada"
    ALEATORIA = "aleatória"
    INVERTIDA = "invertida"


def lista_no_cenario(n, cenario, semente=SEMENTE):
    """Os inteiros de 1 a n na ordem do cenário."""
    gerador = random.Random(semente)
    lista = list(range(1, n + 1))
    if cenario is Cenario.INVERTIDA:
        lista.reverse()
    elif cenario is Cenario.ALEATORIA:
        gerador.shuffle(lista)
    elif cenario is Cenario.QUASE_ORDENADA:
        for _ in range(max(1, n // FRACAO_FORA_DO_LUGAR)):
            i = gerador.randrange(n - 1)
            lista[i], lista[i + 1] = lista[i + 1], lista[i]
    return lista


def inteiros_com_repetidos(n, semente=SEMENTE):
    """n inteiros entre 0 e n: cerca de um terço dos valores se repete."""
    gerador = random.Random(semente)
    return [gerador.randint(0, n) for _ in range(n)]


def embaralhada(seq, semente=SEMENTE):
    lista = list(seq)
    random.Random(semente).shuffle(lista)
    return lista
