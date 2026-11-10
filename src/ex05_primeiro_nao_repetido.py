"""Exercício 5: primeiro caractere não repetido, com contagem numa hash table e verificação na ordem original."""
from algoritmos.metricas import medir
from algoritmos.texto import primeiro_nao_repetido
from apresentacao.terminal import milhar, ok, tabela, titulo

# (texto, esperado): None quando todos os caracteres se repetem
EXEMPLOS = (
    ("swiss", "w"),
    ("stress", "t"),
    ("level", "v"),
    ("abacabad", "c"),
    ("aabbcdc", "d"),
    ("Infnet", "I"),                    # 'I' e 'n' são diferentes: maiúscula conta como outro caractere
    ("aabbccddeez", "z"),               # o único está no fim
    ("aabbcc", None),
    ("", None),
)
TAMANHOS = (1_000, 10_000, 100_000, 1_000_000)


def texto_com_unico_no_fim(n):
    """n - 1 caracteres que se repetem ('ab' em ciclo) e um 'z' no fim: a 2ª passada vai até o último."""
    return "ab" * ((n - 1) // 2) + "a" * ((n - 1) % 2) + "z"


def mostrar_exemplos():
    titulo("Exercício 5: primeiro caractere não repetido")
    linhas, certos = [], True
    for texto, esperado in EXEMPLOS:
        caractere, metricas = medir(primeiro_nao_repetido, texto)
        certos = certos and caractere == esperado
        linhas.append([repr(texto), repr(caractere), len(texto), metricas.acessos])
    tabela(["texto", "resultado", "N", "acessos à hash"], linhas, "<<>>")
    ok(certos, f"{len(EXEMPLOS)} exemplos com o resultado esperado")


def mostrar_crescimento():
    titulo("Pior caso: o único caractere não repetido é o último")
    linhas, conferido = [], True
    for n in TAMANHOS:
        caractere, metricas = medir(primeiro_nao_repetido, texto_com_unico_no_fim(n))
        conferido = conferido and caractere == "z" and metricas.acessos == 3 * n
        linhas.append([milhar(n), repr(caractere), milhar(metricas.acessos), f"{metricas.acessos / n:.0f}N"])
    tabela(["N", "resultado", "acessos", "acessos / N"], linhas)
    ok(conferido, "2 acessos por caractere na contagem + 1 na verificação = 3N: O(N)")


def main():
    mostrar_exemplos()
    print()
    mostrar_crescimento()


if __name__ == "__main__":
    main()
