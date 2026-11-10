"""Exercício 8: atendimento estritamente na ordem de chegada, simulado com uma fila e com uma pilha."""
from algoritmos.fila import Queue
from algoritmos.pilha import Stack
from apresentacao.terminal import celulas, ok, tabela, titulo

CAPACIDADE = 5
# Chegadas e atendimentos intercalados, como num balcão de suporte: ("chega", nome) ou ("atende", None).
EVENTOS = (
    ("chega", "A"), ("chega", "B"), ("atende", None), ("chega", "C"), ("chega", "D"),
    ("atende", None), ("chega", "E"), ("atende", None), ("atende", None), ("atende", None),
)


def simular():
    """Aplica os mesmos eventos às duas estruturas. Devolve as linhas da tabela e o instante de cada evento."""
    fila, pilha = Queue(CAPACIDADE), Stack(CAPACIDADE)
    linhas, chegada, saida_fila, saida_pilha = [], {}, {}, {}
    for instante, (tipo, nome) in enumerate(EVENTOS, start=1):
        if tipo == "chega":
            fila.enqueue(nome)
            pilha.push(nome)
            chegada[nome] = instante
            linhas.append([instante, f"chega {nome}", celulas(fila.array()), "", celulas(pilha.array()), ""])
            continue
        pela_fila, pela_pilha = fila.dequeue(), pilha.pop()
        saida_fila[pela_fila], saida_pilha[pela_pilha] = instante, instante
        linhas.append([instante, "atende", celulas(fila.array()), pela_fila, celulas(pilha.array()), pela_pilha])
    return linhas, chegada, saida_fila, saida_pilha


def mostrar_simulacao(linhas):
    titulo("Exercício 8: atendimento na ordem de chegada, fila (FIFO) x pilha (LIFO)")
    tabela(["t", "evento", "fila: array", "fila atende", "pilha: array", "pilha atende"], linhas, "><<^<^")


def mostrar_esperas(chegada, saida_fila, saida_pilha):
    titulo("Espera de cada solicitação (instante do atendimento - instante da chegada)")
    linhas = [[nome, chegada[nome], saida_fila[nome] - chegada[nome], saida_pilha[nome] - chegada[nome]] for nome in chegada]
    tabela(["solicitação", "chegou em t", "espera na fila", "espera na pilha"], linhas, "<>>>")
    ordem_fila = sorted(saida_fila, key=saida_fila.get)
    ordem_pilha = sorted(saida_pilha, key=saida_pilha.get)
    print(f"ordem de atendimento  fila: {' '.join(ordem_fila)}   pilha: {' '.join(ordem_pilha)}")
    ok(ordem_fila == list(chegada), "a fila atende exatamente na ordem de chegada")
    ok(ordem_pilha != list(chegada), "a pilha quebra a regra: o último a chegar passa na frente e A espera até o fim")


def main():
    linhas, chegada, saida_fila, saida_pilha = simular()
    mostrar_simulacao(linhas)
    print()
    mostrar_esperas(chegada, saida_fila, saida_pilha)


if __name__ == "__main__":
    main()
