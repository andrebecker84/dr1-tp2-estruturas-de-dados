"""Maior número que aparece uma única vez (Exercício 1)."""
from algoritmos.metricas import Metricas


def maior_unico_aninhado(arr, metricas=None):
    """Para cada elemento, percorre a lista inteira contando quantas vezes ele aparece. O(N²)."""
    metricas = metricas or Metricas()
    maior = None
    for i in range(len(arr)):
        contador = 0
        for j in range(len(arr)):           # gargalo: N voltas para cada um dos N elementos
            metricas.comparacoes += 1
            if arr[j] == arr[i]:
                contador += 1
        if contador == 1 and (maior is None or arr[i] > maior):
            maior = arr[i]
    return maior


def maior_unico_hash(arr, metricas=None):
    """Conta as ocorrências numa hash table e depois escolhe o maior único. O(N)."""
    metricas = metricas or Metricas()
    ocorrencias = {}
    for valor in arr:
        metricas.acessos += 2               # uma leitura (get) e uma escrita
        ocorrencias[valor] = ocorrencias.get(valor, 0) + 1

    maior = None
    for valor, quantidade in ocorrencias.items():
        metricas.acessos += 1               # leitura de um par valor -> quantidade
        if quantidade == 1 and (maior is None or valor > maior):
            maior = valor
    return maior
