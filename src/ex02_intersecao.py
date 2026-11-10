"""Exercício 2: interseção de arrays em O(N + M) com hash table, sem funções prontas de interseção."""
import time

from algoritmos.intersecao import intersecao, intersecao_aninhada
from algoritmos.metricas import medir
from apresentacao.terminal import milhar, ok, tabela, titulo
from dados import SEMENTE, embaralhada

EXEMPLOS = (
    ([1, 2, 3, 4, 5], [4, 5, 6, 7], [4, 5]),
    ([1, 2, 2, 3], [2, 2, 4, 3], [2, 3]),               # repetidos: cada valor sai uma vez
    (["ana", "bia", "caio"], ["caio", "dani", "ana"], ["caio", "ana"]),
    ([1, 2, 3], [4, 5, 6], []),
    ([], [1, 2], []),
)
TAMANHOS_ANINHADO = (500, 1_000, 2_000)
TAMANHOS_GRANDES = (10_000, 100_000, 1_000_000)


def pares_e_multiplos_de_3(n):
    """a = n pares e b = n múltiplos de 3, embaralhados. Os comuns são os múltiplos de 6 menores que 2n."""
    a = embaralhada(range(0, 2 * n, 2), SEMENTE)
    b = embaralhada(range(0, 3 * n, 3), SEMENTE + 1)
    return a, b, (2 * n + 5) // 6


def sem_repetidos(valores):
    vistos = {}
    for valor in valores:
        if valor in vistos:
            return False
        vistos[valor] = True
    return True


def mostrar_exemplos():
    titulo("Exercício 2: interseção de arrays com hash table")
    linhas = [[str(a), str(b), str(intersecao(a, b))] for a, b, _ in EXEMPLOS]
    tabela(["a", "b", "comuns (ordem de b)"], linhas, "<<<")
    ok(all(intersecao(a, b) == esperado for a, b, esperado in EXEMPLOS), f"{len(EXEMPLOS)} exemplos com o resultado esperado")


def mostrar_comparacao():
    titulo("Laços aninhados x hash table (N = M)")
    linhas, iguais = [], True
    for n in TAMANHOS_ANINHADO:
        a, b, _ = pares_e_multiplos_de_3(n)
        aninhado, m_aninhado = medir(intersecao_aninhada, a, b)
        hash_, m_hash = medir(intersecao, a, b)
        iguais = iguais and aninhado == hash_
        linhas.append([milhar(n), milhar(len(hash_)), milhar(m_aninhado.comparacoes), milhar(m_hash.acessos)])
    tabela(["N = M", "comuns", "comparações (aninhado)", "acessos (hash)"], linhas)
    ok(iguais, "as duas versões devolvem a mesma lista")


def mostrar_validacao_grande():
    titulo("Validação com arrays grandes (a: pares, b: múltiplos de 3)")
    linhas, conferido = [], True
    for n in TAMANHOS_GRANDES:
        a, b, esperados = pares_e_multiplos_de_3(n)
        inicio = time.perf_counter()
        comuns, metricas = medir(intersecao, a, b)
        segundos = time.perf_counter() - inicio
        certo = len(comuns) == esperados and all(v % 6 == 0 for v in comuns) and sem_repetidos(comuns)
        conferido = conferido and certo and metricas.acessos <= 2 * n + n
        por_elemento = f"{metricas.acessos / (2 * n):.2f}".replace(".", ",")
        tempo = f"{segundos:.3f} s".replace(".", ",")
        linhas.append([milhar(n), milhar(len(comuns)), milhar(metricas.acessos), por_elemento, milhar(n * n), tempo])
    tabela(["N = M", "comuns", "acessos (hash)", "acessos / (N+M)", "N x M (aninhado)", "tempo"], linhas)
    ok(conferido, "comuns = múltiplos de 6, sem repetidos e na quantidade esperada; acessos ≤ N + 2M")


def main():
    mostrar_exemplos()
    print()
    mostrar_comparacao()
    print()
    mostrar_validacao_grande()


if __name__ == "__main__":
    main()
