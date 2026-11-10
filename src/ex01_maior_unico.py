"""Exercício 1: maior número único com laços aninhados O(N²) e com hash table O(N)."""
from algoritmos.metricas import medir
from algoritmos.unicos import maior_unico_aninhado, maior_unico_hash
from apresentacao.terminal import milhar, ok, tabela, titulo
from dados import inteiros_com_repetidos

EXEMPLOS = (
    [5, 7, 3, 9, 4, 9, 8, 3, 1],        # 9 e 3 repetem: o maior único é 8
    [10, 10, 9],                        # o maior valor repete: a resposta é 9
    [-5, -1, -1, -7],                   # negativos
    [2, 2, 3, 3],                       # nenhum único: None
    [42],
    [],
)
TAMANHOS = (10, 100, 1_000, 5_000)


def mostrar_exemplos():
    titulo("Exercício 1: maior número único, laços aninhados x hash table")
    linhas, iguais = [], True
    for arr in EXEMPLOS:
        aninhado, m_aninhado = medir(maior_unico_aninhado, arr)
        hash_, m_hash = medir(maior_unico_hash, arr)
        iguais = iguais and aninhado == hash_
        linhas.append([str(arr), aninhado, hash_, m_aninhado.comparacoes, m_hash.acessos])
    tabela(["lista", "aninhado", "hash", "comparações", "acessos à hash"], linhas)
    ok(iguais, f"as duas versões dão o mesmo resultado nos {len(EXEMPLOS)} exemplos")


def mostrar_crescimento():
    titulo("Listas de tamanhos distintos (N inteiros entre 0 e N, com repetidos)")
    linhas, conferido = [], True
    for n in TAMANHOS:
        arr = inteiros_com_repetidos(n)
        aninhado, m_aninhado = medir(maior_unico_aninhado, arr)
        hash_, m_hash = medir(maior_unico_hash, arr)
        conferido = conferido and aninhado == hash_ and m_aninhado.comparacoes == n * n and m_hash.acessos <= 3 * n
        reducao = f"{m_aninhado.comparacoes / m_hash.acessos:.0f}x"
        linhas.append([milhar(n), aninhado, milhar(m_aninhado.comparacoes), milhar(m_hash.acessos), reducao])
    tabela(["N", "maior único", "comparações (aninhado)", "acessos (hash)", "redução"], linhas)
    ok(conferido, "mesmo resultado; aninhado faz N² comparações; hash faz no máximo 3N acessos")
    print("N x10  ->  comparações x100 (O(N²))  e  acessos x10 (O(N))")


def main():
    mostrar_exemplos()
    print()
    mostrar_crescimento()


if __name__ == "__main__":
    main()
