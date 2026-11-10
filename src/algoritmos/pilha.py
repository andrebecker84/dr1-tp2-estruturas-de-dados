"""Pilha de capacidade fixa sobre um array (Exercício 9)."""
from algoritmos.erros import Overflow, Underflow

VAZIA = -1


class Stack:
    """O estado fica no objeto: o array de tamanho fixo e o índice do topo (VAZIA quando não há itens)."""

    def __init__(self, capacidade):
        if not isinstance(capacidade, int) or capacidade < 1:
            raise ValueError("capacidade deve ser um inteiro positivo")
        self._dados = [None] * capacidade
        self._topo = VAZIA

    @property
    def capacidade(self):
        return len(self._dados)

    @property
    def topo(self):
        return self._topo

    def size(self):
        return self._topo + 1

    def is_empty(self):
        return self._topo == VAZIA

    def is_full(self):
        return self._topo == self.capacidade - 1

    def push(self, valor):
        """Põe valor no topo. O(1). Com a pilha cheia levanta Overflow e não altera o estado."""
        if self.is_full():
            raise Overflow(f"push({valor!r}) recusado: pilha cheia ({self.capacidade}/{self.capacidade})")
        self._topo += 1
        self._dados[self._topo] = valor

    def pop(self):
        """Tira e devolve o valor do topo. O(1). Com a pilha vazia levanta Underflow."""
        if self.is_empty():
            raise Underflow("pop() recusado: pilha vazia")
        valor = self._dados[self._topo]
        self._dados[self._topo] = None      # a posição volta a ficar livre
        self._topo -= 1
        return valor

    def peek(self):
        """Valor do topo, sem remover. O(1)."""
        if self.is_empty():
            raise Underflow("peek() recusado: pilha vazia")
        return self._dados[self._topo]

    def array(self):
        """Cópia do array interno, para mostrar o estado."""
        return list(self._dados)
