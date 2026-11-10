"""Conferências usadas nos scripts e nos testes. Ficam fora do núcleo para não se misturarem à contagem."""


def esta_ordenada(seq):
    return all(seq[i] <= seq[i + 1] for i in range(len(seq) - 1))


def mesma_colecao(a, b):
    """Mesmos elementos com as mesmas quantidades, em qualquer ordem."""
    contagem = {}
    for valor in a:
        contagem[valor] = contagem.get(valor, 0) + 1
    for valor in b:
        contagem[valor] = contagem.get(valor, 0) - 1
    return all(quantidade == 0 for quantidade in contagem.values())


def ordenacao_correta(entrada, saida):
    """A saída está em ordem e é uma permutação da entrada."""
    return esta_ordenada(saida) and mesma_colecao(entrada, saida)


def inversoes(seq):
    """Pares (i, j) com i < j e seq[i] > seq[j]. O(N²), só para conferir o Insertion Sort."""
    return sum(1 for i in range(len(seq)) for j in range(i + 1, len(seq)) if seq[i] > seq[j])


def e_o_inverso(texto, invertido):
    """Confere posição a posição, sem slicing: o caractere i do invertido é o caractere N - 1 - i do texto."""
    n = len(texto)
    return len(invertido) == n and all(invertido[i] == texto[n - 1 - i] for i in range(n))
