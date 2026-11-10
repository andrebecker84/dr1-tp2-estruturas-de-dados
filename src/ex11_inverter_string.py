"""Exercício 11: inversão de string com a pilha do Exercício 9, sem slicing nem reversed()."""
from algoritmos.texto import inverter
from apresentacao.terminal import celulas, ok, tabela, titulo
from verificacao import e_o_inverso

EXEMPLO = "Infnet"
TEXTOS = ("algoritmo", "Infnet", "arara", "Olá, mundo!", "ação e reação", "2026-11-09", "a", "")


def mostrar_passo_a_passo():
    titulo(f'Exercício 11: inverter "{EXEMPLO}" com uma pilha')
    linhas, saida = [], []

    def registrar(operacao, caractere, pilha):
        if operacao == "pop":
            saida.append(caractere)
        rotulo = f"push('{caractere}')" if operacao == "push" else f"pop() -> '{caractere}'"
        linhas.append([len(linhas) + 1, rotulo, celulas(pilha.array()), pilha.topo, "".join(saida)])

    resultado = inverter(EXEMPLO, ao_operar=registrar)
    tabela(["passo", "operação", "pilha (array)", "topo", "saída até aqui"], linhas, "><<><")
    print(f'"{EXEMPLO}" -> "{resultado}": {len(EXEMPLO)} push + {len(EXEMPLO)} pop = {2 * len(EXEMPLO)} operações O(1)')


def mostrar_testes():
    titulo("Testes com diferentes strings")
    linhas, certos = [], True
    for texto in TEXTOS:
        invertido = inverter(texto)
        certo = e_o_inverso(texto, invertido) and inverter(invertido) == texto
        certos = certos and certo
        linhas.append([repr(texto), repr(invertido), len(texto), "[OK]" if certo else "[FALHA]"])
    tabela(["entrada", "invertida", "N", "conferida"], linhas, "<<>^")
    ok(certos, "caractere i da saída = caractere N - 1 - i da entrada, e inverter duas vezes devolve o original")


def main():
    mostrar_passo_a_passo()
    print()
    mostrar_testes()


if __name__ == "__main__":
    main()
