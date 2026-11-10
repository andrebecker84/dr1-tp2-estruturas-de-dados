"""Exercício 6: Selection Sort com contagem de comparações e trocas."""
from algoritmos.metricas import medir
from algoritmos.ordenacao import selection_sort
from apresentacao.terminal import compacta, milhar, ok, tabela, titulo
from dados import ARRAY_DAS_AULAS, TAMANHOS_DAS_ORDENACOES, Cenario, lista_no_cenario
from verificacao import ordenacao_correta


def comparacoes_teoricas(n):
    return n * (n - 1) // 2


def mostrar_passo_a_passo():
    titulo(f"Exercício 6: Selection Sort no array da Aula 4 {compacta(ARRAY_DAS_AULAS)}")
    linhas = []

    def registrar(lista, metricas):
        linhas.append([len(linhas) + 1, compacta(lista), metricas.comparacoes, metricas.trocas])

    selection_sort(ARRAY_DAS_AULAS, ao_fim_da_travessia=registrar)
    tabela(["travessia", "lista ao fim", "comparações (acum.)", "trocas (acum.)"], linhas, "><>>")
    print("2ª e 4ª travessias: o menor já estava no lugar, então não houve troca")


def mostrar_cenarios():
    titulo("Listas em diferentes estados iniciais")
    linhas, conferido = [], True
    for n in TAMANHOS_DAS_ORDENACOES:
        for cenario in Cenario:
            entrada = lista_no_cenario(n, cenario)
            saida, metricas = medir(selection_sort, entrada)
            conferido = conferido and ordenacao_correta(entrada, saida) and metricas.comparacoes == comparacoes_teoricas(n)
            conferido = conferido and metricas.trocas <= n - 1
            linhas.append([milhar(n), cenario, milhar(metricas.comparacoes), milhar(metricas.trocas), milhar(comparacoes_teoricas(n))])
    tabela(["N", "estado inicial", "comparações", "trocas", "N(N-1)/2"], linhas, "><>>>")
    ok(conferido, "saídas ordenadas; comparações = N(N-1)/2 em todo estado; trocas ≤ N - 1")
    print("N x10  ->  comparações x~100: O(N²) no melhor, no médio e no pior caso")


def main():
    mostrar_passo_a_passo()
    print()
    mostrar_cenarios()


if __name__ == "__main__":
    main()
