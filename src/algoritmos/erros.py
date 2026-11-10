"""Erros de uso indevido das estruturas de capacidade fixa (Exercícios 9 e 10)."""


class Overflow(Exception):
    """Inserção numa estrutura cheia."""


class Underflow(Exception):
    """Remoção (ou consulta) numa estrutura vazia."""
