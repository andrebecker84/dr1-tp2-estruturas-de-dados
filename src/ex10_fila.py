"""Exercício 10: fila de capacidade fixa com ponteiros de início e fim (array circular)."""
import random

from algoritmos.erros import Overflow, Underflow
from algoritmos.fila import Queue
from apresentacao.terminal import celulas, cor, milhar, ok, tabela, titulo
from dados import SEMENTE

CAPACIDADE = 4
# Enche, esvazia em parte e volta a inserir: o fim dá a volta para a posição 0.
OPERACOES = (
    ("enqueue", 10), ("enqueue", 20), ("enqueue", 30), ("dequeue", None), ("dequeue", None),
    ("enqueue", 40), ("enqueue", 50), ("enqueue", 60), ("enqueue", 70), ("peek", None),
    ("dequeue", None), ("dequeue", None), ("dequeue", None), ("dequeue", None), ("dequeue", None),
)
OPERACOES_ALEATORIAS = 100_000
CAPACIDADE_ALEATORIA = 8


def aplicar(fila, operacao, valor):
    """Executa a operação e devolve o texto do resultado. Os erros são capturados e mostrados."""
    try:
        if operacao == "enqueue":
            fila.enqueue(valor)
            return "ok"
        return f"devolveu {getattr(fila, operacao)()}"
    except (Overflow, Underflow) as erro:
        return cor("1;31", f"{type(erro).__name__}: {erro}")


def rotulo(operacao, valor):
    return f"{operacao}({valor})" if valor is not None else f"{operacao}()"


def estado(fila):
    return [celulas(fila.array()), fila.inicio, fila.fim, f"{fila.size()}/{fila.capacidade}"]


def mostrar_sequencia():
    titulo(f"Exercício 10: Queue com capacidade {CAPACIDADE}, estado interno após cada operação")
    fila = Queue(CAPACIDADE)
    linhas = [[0, "Queue(4)", "fila criada", *estado(fila)]]
    for passo, (operacao, valor) in enumerate(OPERACOES, start=1):
        resultado = aplicar(fila, operacao, valor)
        linhas.append([passo, rotulo(operacao, valor), resultado, *estado(fila)])
    tabela(["passo", "operação", "resultado", "array interno", "início", "fim", "tamanho"], linhas, "><<<>>>")
    print("início = próximo a sair; fim = posição onde entra o próximo; os dois avançam com (i + 1) % capacidade")


def validar_fifo():
    """Operações aleatórias: entram 1, 2, 3, ... e cada dequeue precisa devolver o próximo da sequência."""
    titulo(f"Validação FIFO com {milhar(OPERACOES_ALEATORIAS)} operações aleatórias (capacidade {CAPACIDADE_ALEATORIA})")
    gerador = random.Random(SEMENTE)
    fila = Queue(CAPACIDADE_ALEATORIA)
    proximo_a_entrar, proximo_a_sair = 1, 1
    contagem = {"enqueue": 0, "dequeue": 0, "Overflow": 0, "Underflow": 0}
    fifo = True
    for _ in range(OPERACOES_ALEATORIAS):
        try:
            if gerador.random() < 0.5:
                fila.enqueue(proximo_a_entrar)
                proximo_a_entrar += 1
                contagem["enqueue"] += 1
            else:
                fifo = fifo and fila.dequeue() == proximo_a_sair
                proximo_a_sair += 1
                contagem["dequeue"] += 1
        except (Overflow, Underflow) as erro:
            contagem[type(erro).__name__] += 1
    tabela(["enqueue", "dequeue", "Overflow tratados", "Underflow tratados", "na fila ao fim"],
           [[*map(milhar, contagem.values()), fila.size()]], ">>>>>")
    ok(fifo, "todo dequeue devolveu o elemento mais antigo da fila (ordem 1, 2, 3, ...)")
    ok(fila.size() == proximo_a_entrar - proximo_a_sair, "tamanho = inseridos - removidos")


def main():
    mostrar_sequencia()
    print()
    validar_fifo()


if __name__ == "__main__":
    main()
