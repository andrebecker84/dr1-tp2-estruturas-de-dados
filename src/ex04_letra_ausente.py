"""Exercício 4: letra ausente do alfabeto, marcando presença num array de 26 posições."""
from algoritmos.metricas import medir
from algoritmos.texto import LETRAS, letras_ausentes
from apresentacao.terminal import milhar, ok, tabela, titulo

# (texto, letras ausentes esperadas)
EXEMPLOS = (
    ("The quick brown fox jumps over the lay dog", ["z"]),
    ("Jane quer LP, fax, CD, giz, TV e bom whiky.", ["s"]),
    ("À noite, vovô Kowalsky vê o ímã cair no pé do pinguim queixoso e vovó põe açúcar no chá de tâmaras do jabuti zeloso.", ["f"]),
    ("ABCDEFGHIJKLMNOPQRSTUVWXY", ["z"]),
    ("Sphinx of black quartz, judge my vo... 2026!", ["w"]),
    ("Zebras caolhas de Java querem mandar fax para moça gigante de New York.", []),
    ("Um pequeno jabuti xereta viu dez cegonhas felizes.", ["k", "w", "y"]),
)
LARGURA = 60
TAMANHOS = (1_000, 10_000, 100_000, 1_000_000)
FRASE = "Sphinx of black quartz, judge my vo! "


def resumo(texto):
    return texto if len(texto) <= LARGURA else texto[:LARGURA - 3] + "..."


def mostrar_exemplos():
    titulo("Exercício 4: letra ausente do alfabeto")
    linhas, certos = [], True
    for texto, esperado in EXEMPLOS:
        ausentes, metricas = medir(letras_ausentes, texto)
        certos = certos and ausentes == esperado
        linhas.append([resumo(texto), ", ".join(ausentes) or "(nenhuma)", len(texto), metricas.acessos])
    tabela(["texto", "ausente", "caracteres", "acessos"], linhas, "<<>>")
    ok(certos, f"{len(EXEMPLOS)} textos: acentos, maiúsculas, dígitos e pontuação tratados")


def mostrar_crescimento():
    titulo(f"Crescimento: a frase repetida até N caracteres (falta o w)")
    linhas, conferido = [], True
    for n in TAMANHOS:
        texto = (FRASE * (n // len(FRASE) + 1))[:n]
        ausentes, metricas = medir(letras_ausentes, texto)
        letras = sum(1 for c in texto if c.isalpha())
        conferido = conferido and ausentes == ["w"] and metricas.acessos == letras + LETRAS
        linhas.append([milhar(n), milhar(letras), milhar(metricas.acessos), ", ".join(ausentes)])
    tabela(["N (caracteres)", "letras", "acessos (letras + 26)", "ausente"], linhas)
    ok(conferido, "1 acesso por letra + 26 na verificação final: O(N) de tempo e O(1) de espaço")


def main():
    mostrar_exemplos()
    print()
    mostrar_crescimento()


if __name__ == "__main__":
    main()
