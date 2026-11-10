"""Funções hash do Exercício 12 e a distribuição das chaves numa tabela de M posições.

Não é uma hash table: só calcula em que posição (balde) cada chave cairia.
"""
M = 10


def h1(k, m=M):
    return k % m


def h2(k, m=M):
    return (k * 7) % m


def h3(k, m=M):
    return (k * k) % m


def distribuicao(chaves, funcao, m=M):
    """Quantas chaves caem em cada um dos m baldes."""
    baldes = [0] * m
    for chave in chaves:
        baldes[funcao(chave, m)] += 1
    return baldes


def colisoes(baldes):
    """Chaves que caem num balde já ocupado: todas menos a primeira de cada balde."""
    return sum(quantidade - 1 for quantidade in baldes if quantidade > 1)


def imagem(funcao, m=M):
    """Baldes que a função consegue atingir. Só k mod m decide o resultado, então basta testar k de 0 a m - 1."""
    return sorted({funcao(k, m) for k in range(m)})
