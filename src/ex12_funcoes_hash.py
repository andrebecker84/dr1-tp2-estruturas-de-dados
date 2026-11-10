"""Exercício 12: distribuição de h1(k) = k mod M, h2(k) = 7k mod M e h3(k) = k² mod M com M = 10."""
import random

from algoritmos.hashing import M, colisoes, distribuicao, h1, h2, h3, imagem
from apresentacao.terminal import ok, tabela, titulo
from dados import SEMENTE

FUNCOES = {"h1 = k mod 10": h1, "h2 = 7k mod 10": h2, "h3 = k² mod 10": h3}
QUANTIDADE = 50
CONJUNTOS = {
    "sequenciais 0..49": list(range(QUANTIDADE)),
    "aleatórias 0..9999": random.Random(SEMENTE).sample(range(10_000), QUANTIDADE),
    "pares": list(range(0, 2 * QUANTIDADE, 2)),
    "múltiplos de 5": list(range(0, 5 * QUANTIDADE, 5)),
    "múltiplos de 10": list(range(0, 10 * QUANTIDADE, 10)),
}
PRIMO = 11


def mostrar_imagem():
    titulo(f"Exercício 12: funções hash com M = {M}. Balde de cada resto k mod 10")
    linhas = [[nome, *[funcao(k) for k in range(M)], len(imagem(funcao))] for nome, funcao in FUNCOES.items()]
    tabela(["função", *[f"k≡{k}" for k in range(M)], "baldes atingíveis"], linhas, "<" + ">" * (M + 1))
    ok(imagem(h2) == list(range(M)), "h2 só renomeia os baldes de h1 (7 e 10 são primos entre si): mesma distribuição")
    ok(imagem(h3) == [0, 1, 4, 5, 6, 9], "h3 nunca atinge os baldes 2, 3, 7 e 8")


def mostrar_distribuicoes():
    titulo(f"Distribuição de {QUANTIDADE} chaves (ideal: 5 por balde; com 10 baldes, ao menos {QUANTIDADE - M} colisões)")
    linhas = []
    for conjunto, chaves in CONJUNTOS.items():
        for nome, funcao in FUNCOES.items():
            baldes = distribuicao(chaves, funcao)
            ocupados = sum(1 for q in baldes if q)
            linhas.append([conjunto, nome.split(" =")[0], " ".join(f"{q:2}" for q in baldes), ocupados, max(baldes), colisoes(baldes)])
        linhas.append(["", "", "", "", "", ""])
    tabela(["chaves", "função", "baldes 0 a 9", "ocupados", "maior balde", "colisões"], linhas[:-1], "<<<>>>")


def mostrar_tabela_prima():
    titulo(f"Mesmo conjunto com M = {PRIMO} (primo)")
    linhas = []
    for conjunto in ("múltiplos de 5", "múltiplos de 10"):
        baldes = distribuicao(CONJUNTOS[conjunto], h1, PRIMO)
        linhas.append([conjunto, " ".join(f"{q:2}" for q in baldes), sum(1 for q in baldes if q), max(baldes)])
    tabela(["chaves", "baldes 0 a 10 de k mod 11", "ocupados", "maior balde"], linhas, "<<>>")
    print("com M primo, um fator comum entre as chaves (5, 10) não concentra mais tudo em poucos baldes")


def main():
    mostrar_imagem()
    print()
    mostrar_distribuicoes()
    print()
    mostrar_tabela_prima()


if __name__ == "__main__":
    main()
