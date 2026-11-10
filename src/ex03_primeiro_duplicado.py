"""Exercício 3: primeiro valor duplicado de um array de strings, em O(N) com hash table."""
from algoritmos.duplicados import primeiro_duplicado, primeiro_duplicado_aninhado
from algoritmos.metricas import medir
from apresentacao.terminal import milhar, ok, tabela, titulo

# (entrada, duplicado esperado): exatamente um par repetido em cada uma
EXEMPLOS = (
    (["maçã", "banana", "uva", "banana", "kiwi"], "banana"),
    (["x", "x", "y", "z", "w"], "x"),                                   # par logo no início
    (["d1", "d2", "d3", "d4", "d5", "d6", "d1"], "d1"),                 # par nas pontas
    (["Ana", "ana", "Bia", "Caio", "Bia"], "Bia"),                      # 'Ana' e 'ana' são diferentes
    (["", "a", " ", "b", ""], ""),                                      # a string vazia também conta
)
TAMANHOS = (100, 1_000, 5_000)


def identificadores(n):
    """n strings distintas e, no fim, a repetição da primeira: o duplicado é lido por último (pior caso)."""
    valores = [f"pedido-{i:07d}" for i in range(n)]
    return [*valores, valores[0]]


def posicao_da_repeticao(valores, duplicado):
    vistos = 0
    for indice, valor in enumerate(valores):
        if valor == duplicado:
            vistos += 1
            if vistos == 2:
                return indice
    return None


def mostrar_exemplos():
    titulo("Exercício 3: primeiro valor duplicado")
    linhas, certos = [], True
    for valores, esperado in EXEMPLOS:
        duplicado, metricas = medir(primeiro_duplicado, valores)
        certos = certos and duplicado == esperado
        linhas.append([str(valores), repr(duplicado), posicao_da_repeticao(valores, duplicado), metricas.acessos])
    tabela(["entrada", "duplicado", "índice da 2ª ocorrência", "acessos à hash"], linhas, "<<>>")
    ok(certos, f"{len(EXEMPLOS)} entradas com o duplicado esperado")


def mostrar_crescimento():
    titulo("Duplicado no fim (pior caso): hash x laços aninhados")
    linhas, conferido = [], True
    for n in TAMANHOS:
        valores = identificadores(n)
        hash_, m_hash = medir(primeiro_duplicado, valores)
        aninhado, m_aninhado = medir(primeiro_duplicado_aninhado, valores)
        conferido = conferido and hash_ == aninhado == valores[0] and m_hash.acessos == 2 * n + 1
        linhas.append([milhar(len(valores)), hash_, milhar(m_hash.acessos), milhar(m_aninhado.comparacoes)])
    tabela(["N", "duplicado", "acessos (hash)", "comparações (aninhado)"], linhas, "><>>")
    ok(conferido, "mesmo resultado; hash faz 2N - 1 acessos: uma passada só, O(N)")


def main():
    mostrar_exemplos()
    print()
    mostrar_crescimento()


if __name__ == "__main__":
    main()
