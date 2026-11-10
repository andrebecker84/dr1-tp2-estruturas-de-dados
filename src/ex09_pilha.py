"""Exercício 9: pilha de capacidade fixa sobre array, com overflow e underflow tratados."""
from algoritmos.erros import Overflow, Underflow
from algoritmos.pilha import Stack
from apresentacao.terminal import celulas, cor, ok, tabela, titulo

CAPACIDADE = 4
# Sequência que enche a pilha, passa do limite, esvazia e tenta tirar de uma pilha vazia.
OPERACOES = (
    ("push", 10), ("push", 20), ("push", 30), ("peek", None), ("push", 40), ("push", 50),
    ("pop", None), ("pop", None), ("push", 60), ("pop", None), ("pop", None), ("pop", None),
    ("pop", None), ("peek", None),
)


def aplicar(pilha, operacao, valor):
    """Executa a operação e devolve o texto do resultado. Os erros são capturados e mostrados."""
    try:
        if operacao == "push":
            pilha.push(valor)
            return "ok"
        return f"devolveu {getattr(pilha, operacao)()}"
    except (Overflow, Underflow) as erro:
        return cor("1;31", f"{type(erro).__name__}: {erro}")


def rotulo(operacao, valor):
    return f"{operacao}({valor})" if valor is not None else f"{operacao}()"


def estado(pilha):
    return [celulas(pilha.array()), pilha.topo, f"{pilha.size()}/{pilha.capacidade}"]


def mostrar_sequencia():
    titulo(f"Exercício 9: Stack com capacidade {CAPACIDADE}, estado interno após cada operação")
    pilha = Stack(CAPACIDADE)
    linhas = [[0, "Stack(4)", "pilha criada", *estado(pilha)]]
    for passo, (operacao, valor) in enumerate(OPERACOES, start=1):
        resultado = aplicar(pilha, operacao, valor)
        linhas.append([passo, rotulo(operacao, valor), resultado, *estado(pilha)])
    tabela(["passo", "operação", "resultado", "array interno", "topo", "tamanho"], linhas, "><<<>>")
    print("topo = índice do último elemento; -1 indica pilha vazia")


def mostrar_verificacoes():
    titulo("Verificações")
    pilha = Stack(2)
    pilha.push("a")
    pilha.push("b")
    antes = pilha.array(), pilha.topo
    try:
        pilha.push("c")
        overflow = False
    except Overflow:
        overflow = (pilha.array(), pilha.topo) == antes
    ok(overflow, "push em pilha cheia levanta Overflow e não altera array nem topo")
    ok([pilha.pop(), pilha.pop()] == ["b", "a"], "pop devolve na ordem inversa da inserção (LIFO)")
    try:
        pilha.pop()
        underflow = False
    except Underflow:
        underflow = pilha.topo == -1 and pilha.is_empty()
    ok(underflow, "pop em pilha vazia levanta Underflow e a pilha continua vazia")


def main():
    mostrar_sequencia()
    print()
    mostrar_verificacoes()


if __name__ == "__main__":
    main()
