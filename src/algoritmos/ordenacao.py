"""Selection Sort (Aula 4) e Insertion Sort (Aula 5).

As duas funções ordenam uma cópia e devolvem a lista nova. O callback ao_fim_da_travessia recebe a
lista ao fim de cada travessia, para mostrar o passo a passo sem print dentro do algoritmo.
"""
from algoritmos.metricas import Metricas


def selection_sort(seq, metricas=None, ao_fim_da_travessia=None):
    """Cada travessia acha o menor do trecho não ordenado e o troca com a 1ª posição dele. O(N²)."""
    metricas = metricas or Metricas()
    lista = list(seq)
    for inicio in range(len(lista) - 1):
        menor = inicio
        for i in range(inicio + 1, len(lista)):
            metricas.comparacoes += 1
            if lista[i] < lista[menor]:
                menor = i
        if menor != inicio:                 # com o menor já no lugar, não há troca
            lista[inicio], lista[menor] = lista[menor], lista[inicio]
            metricas.trocas += 1
        if ao_fim_da_travessia:
            ao_fim_da_travessia(lista, metricas)
    return lista


def insertion_sort(seq, metricas=None, ao_fim_da_travessia=None):
    """Guarda o valor em temp, desloca os maiores à esquerda uma casa e insere temp no espaço vazio.

    Melhor caso (lista ordenada) O(N); pior caso (lista invertida) O(N²).
    """
    metricas = metricas or Metricas()
    lista = list(seq)
    for indice in range(1, len(lista)):
        temp = lista[indice]
        posicao = indice - 1
        while posicao >= 0:
            metricas.comparacoes += 1
            if lista[posicao] <= temp:      # achou um valor menor ou igual: fim dos deslocamentos
                break
            lista[posicao + 1] = lista[posicao]
            metricas.deslocamentos += 1
            posicao -= 1
        lista[posicao + 1] = temp
        if ao_fim_da_travessia:
            ao_fim_da_travessia(lista, metricas)
    return lista
