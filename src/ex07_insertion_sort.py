"""Exercício 7: Insertion Sort com contagem de comparações e deslocamentos."""
from algoritmos.metricas import medir
from algoritmos.ordenacao import insertion_sort, selection_sort
from apresentacao.terminal import compacta, milhar, ok, tabela, titulo
from dados import ARRAY_DAS_AULAS, TAMANHOS_DAS_ORDENACOES, Cenario, lista_no_cenario
from verificacao import inversoes, ordenacao_correta

N_COMPARACAO = 1_000


def mostrar_passo_a_passo():
    titulo(f"Exercício 7: Insertion Sort no array da Aula 5 {compacta(ARRAY_DAS_AULAS)}")
    linhas = []

    def registrar(lista, metricas):
        linhas.append([len(linhas) + 1, compacta(lista), metricas.comparacoes, metricas.deslocamentos])

    _, metricas = medir(insertion_sort, ARRAY_DAS_AULAS, ao_fim_da_travessia=registrar)
    tabela(["travessia", "lista ao fim", "comparações (acum.)", "deslocamentos (acum.)"], linhas, "><>>")
    travessias = len(ARRAY_DAS_AULAS) - 1
    passos = metricas.comparacoes + metricas.deslocamentos + 2 * travessias
    print(f"{metricas.comparacoes} comparações + {metricas.deslocamentos} deslocamentos + {travessias} remoções "
          f"+ {travessias} inserções de temp = {passos} passos, como no slide")


def mostrar_cenarios():
    titulo("Quase ordenadas, invertidas e os outros estados")
    linhas, conferido = [], True
    for n in TAMANHOS_DAS_ORDENACOES:
        for cenario in Cenario:
            entrada = lista_no_cenario(n, cenario)
            saida, metricas = medir(insertion_sort, entrada)
            inv = inversoes(entrada)
            conferido = conferido and ordenacao_correta(entrada, saida) and metricas.deslocamentos == inv
            linhas.append([milhar(n), cenario, milhar(metricas.comparacoes), milhar(metricas.deslocamentos), milhar(inv)])
    tabela(["N", "estado inicial", "comparações", "deslocamentos", "inversões"], linhas, "><>>>")
    ok(conferido, "saídas ordenadas; deslocamentos = inversões da entrada em todos os casos")


def mostrar_comparacao():
    titulo(f"Insertion x Selection (N = {milhar(N_COMPARACAO)}): comparações + deslocamentos ou trocas")
    linhas = []
    for cenario in Cenario:
        entrada = lista_no_cenario(N_COMPARACAO, cenario)
        insercao = medir(insertion_sort, entrada)[1]
        selecao = medir(selection_sort, entrada)[1]
        passos_insercao = insercao.comparacoes + insercao.deslocamentos
        passos_selecao = selecao.comparacoes + selecao.trocas
        melhor = "Insertion" if passos_insercao < passos_selecao else "Selection"
        linhas.append([cenario, milhar(passos_insercao), milhar(passos_selecao), melhor])
    tabela(["estado inicial", "Insertion Sort", "Selection Sort", "menos passos"], linhas)


def main():
    mostrar_passo_a_passo()
    print()
    mostrar_cenarios()
    print()
    mostrar_comparacao()


if __name__ == "__main__":
    main()
