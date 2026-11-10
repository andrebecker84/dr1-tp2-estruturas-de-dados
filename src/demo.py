"""Menu de demonstração: escolhe um exercício, mostra o comando, roda com progresso em
braile, exibe a saída real e volta ao menu.

    cd src && python3 demo.py        (no Windows: cd src; python demo.py)

Os exercícios rodam com o mesmo Python que abriu o menu.
"""
import os
import platform
import re
import subprocess
import sys
import time

from apresentacao.terminal import cor

NO_WINDOWS = os.name == "nt"
PYTHON = "python" if NO_WINDOWS else "python3"      # como o comando é digitado em cada sistema
LISTAR = "dir /b" if NO_WINDOWS else "ls"
TESTES = f"{PYTHON} -m unittest discover -s tests -t ."


def rodar(arquivo):
    return f"{PYTHON} {arquivo}"


# (opção, título, Big O, comandos)
DEMONSTRACOES = [
    ("0", "Organização do código", "", [LISTAR, f"{LISTAR} algoritmos"]),
    ("1", "Maior número único com hash table", "O(N²) → O(N)", [rodar("ex01_maior_unico.py")]),
    ("2", "Interseção de arrays", "O(N × M) → O(N + M)", [rodar("ex02_intersecao.py")]),
    ("3", "Primeiro valor duplicado", "O(N)", [rodar("ex03_primeiro_duplicado.py")]),
    ("4", "Letra ausente do alfabeto", "O(N)", [rodar("ex04_letra_ausente.py")]),
    ("5", "Primeiro caractere não repetido", "O(N)", [rodar("ex05_primeiro_nao_repetido.py")]),
    ("6", "Selection Sort", "O(N²)", [rodar("ex06_selection_sort.py")]),
    ("7", "Insertion Sort", "O(N) a O(N²)", [rodar("ex07_insertion_sort.py")]),
    ("8", "Pilha ou fila no atendimento", "FIFO", [rodar("ex08_pilha_ou_fila.py")]),
    ("9", "Pilha com overflow e underflow", "O(1)", [rodar("ex09_pilha.py")]),
    ("10", "Fila com ponteiros", "O(1)", [rodar("ex10_fila.py")]),
    ("11", "Inversão de string com pilha", "O(N)", [rodar("ex11_inverter_string.py")]),
    ("12", "Funções hash e distribuição", "M = 10", [rodar("ex12_funcoes_hash.py")]),
    ("t", "Testes automatizados", "", [TESTES]),
]

SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
LARGURA_DA_BARRA = 24
TEMPO_MINIMO = 0.8          # segundos: mesmo um exercício rápido deixa o progresso visível
AMBIENTE = {**os.environ, "FORCE_COLOR": "1", "PYTHONDONTWRITEBYTECODE": "1"}
ANSI = re.compile(r"\033\[[0-9;]*m")


def limpar_tela():
    print("\033[2J\033[H", end="")


def cabecalho():
    sistema = "Windows" if NO_WINDOWS else "Linux"
    linhas = ["DR1-TP2 · Hash Tables, Pilhas e Filas", "André Luis Becker · Prof. Ian Monteiro Nunes · Infnet",
              f"Python {platform.python_version()} · {sistema}"]
    largura = max(len(linha) for linha in linhas) + 4
    print(cor("36", "╭" + "─" * largura + "╮"))
    for linha in linhas:
        print(cor("36", "│") + "  " + cor("1", linha.ljust(largura - 2)) + cor("36", "│"))
    print(cor("36", "╰" + "─" * largura + "╯"))


def mostrar_menu():
    limpar_tela()
    cabecalho()
    print()
    for opcao, titulo, big_o, _ in DEMONSTRACOES:
        print(f"  {cor('1;33', opcao.rjust(2))}  {titulo:<38} {cor('35', big_o)}")
    print(f"\n  {cor('1;33', ' s')}  Sair\n")


def barra(quadro):
    """Faixa de braile que corre da esquerda para a direita enquanto o comando executa."""
    posicao = quadro % (LARGURA_DA_BARRA + 4)
    return "".join("⣿" if posicao - 4 <= i < posicao else "⣀" for i in range(LARGURA_DA_BARRA))


def para_executar(comando):
    """O comando que roda de fato: o mesmo Python que abriu o menu e, no Linux, o ls com cores e colunas
    (com a saída capturada ele perderia as duas). O comando mostrado na tela continua o digitável."""
    if comando.startswith(PYTHON + " "):
        return f'"{sys.executable}"' + comando[len(PYTHON):]
    if comando.startswith("ls"):
        return comando.replace("ls", "ls -C --color=always", 1)
    return comando


def executar(comando):
    """Mostra o comando, roda com progresso em braile e imprime a saída. Devolve (saída, segundos)."""
    print(cor("1;32", "$ ") + cor("1", comando))
    inicio = time.monotonic()
    processo = subprocess.Popen(para_executar(comando), shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, env=AMBIENTE)
    quadro = 0
    while processo.poll() is None or time.monotonic() - inicio < TEMPO_MINIMO:
        decorrido = time.monotonic() - inicio
        simbolo = cor("1;36", SPINNER[quadro % len(SPINNER)])
        print(f"\r{simbolo} executando  {cor('36', barra(quadro))}  {decorrido:4.1f} s", end="", flush=True)
        quadro += 1
        time.sleep(0.08)
    print("\r\033[K", end="")
    saida = processo.stdout.read()
    print(saida, end="" if saida.endswith("\n") else "\n")
    return saida, time.monotonic() - inicio


def resumo(saidas, segundos):
    texto = ANSI.sub("", "".join(saidas))
    aprovadas, falhas = texto.count("[OK]"), texto.count("[FALHA]")
    verificacoes = f" · {aprovadas} verificação(ões) [OK]" if aprovadas else ""
    testes = re.search(r"Ran (\d+) tests? in .*\n\nOK", texto)
    verificacoes += f" · {testes.group(1)} testes passando" if testes else ""
    if falhas:
        print(cor("1;31", f"\n✖ {falhas} verificação(ões) com [FALHA]"))
    else:
        print(cor("1;32", f"\n✔ concluído em {segundos:.1f} s{verificacoes}"))


def demonstrar(opcao, titulo, big_o, comandos):
    limpar_tela()
    nome = titulo if opcao in ("0", "t") else f"Exercício {opcao} · {titulo}"
    print(cor("1;36", nome) + (f"  {cor('35', big_o)}" if big_o else ""))
    print(cor("2", "─" * 60) + "\n")
    saidas, total = [], 0.0
    for comando in comandos:
        saida, segundos = executar(comando)
        saidas.append(saida)
        total += segundos
    resumo(saidas, total)


def main():
    if NO_WINDOWS:
        os.system("")       # liga as sequências de cor (ANSI) no console do Windows
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    por_opcao = {demonstracao[0]: demonstracao for demonstracao in DEMONSTRACOES}
    while True:
        mostrar_menu()
        escolha = input(cor("1", "Escolha uma opção: ")).strip().lower()
        if escolha == "s":
            break
        if escolha not in por_opcao:
            continue
        demonstrar(*por_opcao[escolha])
        if input(cor("2", "\n⣿ Enter para voltar ao menu · s para sair: ")).strip().lower() == "s":
            break
    limpar_tela()
    print(cor("1;36", "Obrigado!"))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
