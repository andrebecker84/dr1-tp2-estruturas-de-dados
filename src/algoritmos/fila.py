"""Fila de capacidade fixa sobre um array circular (Exercício 10)."""
from algoritmos.erros import Overflow, Underflow


class Queue:
    """Dois ponteiros: inicio (o próximo a sair) e fim (a posição onde entra o próximo).

    Depois da última posição os ponteiros voltam para a 0 (array circular); sem isso, as posições
    liberadas no começo do array nunca seriam reaproveitadas. O tamanho separa a fila cheia da
    vazia, que nos dois casos têm inicio == fim.
    """

    def __init__(self, capacidade):
        if not isinstance(capacidade, int) or capacidade < 1:
            raise ValueError("capacidade deve ser um inteiro positivo")
        self._dados = [None] * capacidade
        self._inicio = 0
        self._fim = 0
        self._tamanho = 0

    @property
    def capacidade(self):
        return len(self._dados)

    @property
    def inicio(self):
        return self._inicio

    @property
    def fim(self):
        return self._fim

    def size(self):
        return self._tamanho

    def is_empty(self):
        return self._tamanho == 0

    def is_full(self):
        return self._tamanho == self.capacidade

    def enqueue(self, valor):
        """Insere no fim. O(1). Com a fila cheia levanta Overflow e não altera o estado."""
        if self.is_full():
            raise Overflow(f"enqueue({valor!r}) recusado: fila cheia ({self.capacidade}/{self.capacidade})")
        self._dados[self._fim] = valor
        self._fim = (self._fim + 1) % self.capacidade
        self._tamanho += 1

    def dequeue(self):
        """Remove e devolve o valor do início, o mais antigo. O(1). Com a fila vazia levanta Underflow."""
        if self.is_empty():
            raise Underflow("dequeue() recusado: fila vazia")
        valor = self._dados[self._inicio]
        self._dados[self._inicio] = None
        self._inicio = (self._inicio + 1) % self.capacidade
        self._tamanho -= 1
        return valor

    def peek(self):
        """Valor do início, sem remover. O(1)."""
        if self.is_empty():
            raise Underflow("peek() recusado: fila vazia")
        return self._dados[self._inicio]

    def array(self):
        """Cópia do array interno, para mostrar o estado."""
        return list(self._dados)
