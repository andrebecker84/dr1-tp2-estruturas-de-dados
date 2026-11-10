"""Letra ausente (Exercício 4), primeiro caractere não repetido (Exercício 5) e inversão com pilha (Exercício 11)."""
import unicodedata

from algoritmos.metricas import Metricas
from algoritmos.pilha import Stack

LETRAS = 26


def sem_acento(texto):
    """Minúsculas e sem acentos ('Ação' -> 'acao'): a letra base continua contando como letra."""
    decomposto = unicodedata.normalize("NFD", texto.casefold())
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def letras_ausentes(texto, metricas=None):
    """Letras de a a z que não aparecem no texto, em ordem alfabética. O(N) e espaço O(1)."""
    metricas = metricas or Metricas()
    presente = [False] * LETRAS              # uma posição por letra: a -> 0, ..., z -> 25
    for caractere in texto:
        for letra in sem_acento(caractere):  # 'Ç' -> 'c'; um caractere só, sem copiar o texto inteiro
            if "a" <= letra <= "z":         # espaços, dígitos e pontuação ficam de fora
                metricas.acessos += 1
                presente[ord(letra) - ord("a")] = True

    ausentes = []
    for posicao in range(LETRAS):
        metricas.acessos += 1
        if not presente[posicao]:
            ausentes.append(chr(ord("a") + posicao))
    return ausentes


def primeiro_nao_repetido(texto, metricas=None):
    """Primeiro caractere que aparece uma vez só, na ordem do texto, ou None. O(N)."""
    metricas = metricas or Metricas()
    frequencia = {}
    for caractere in texto:                 # 1ª passada: contagem
        metricas.acessos += 2
        frequencia[caractere] = frequencia.get(caractere, 0) + 1

    for caractere in texto:                 # 2ª passada: verificação na ordem original
        metricas.acessos += 1
        if frequencia[caractere] == 1:
            return caractere
    return None


def inverter(texto, ao_operar=None):
    """Empilha cada caractere e desempilha todos: o último a entrar é o primeiro a sair. O(N)."""
    pilha = Stack(max(len(texto), 1))
    for caractere in texto:
        pilha.push(caractere)
        if ao_operar:
            ao_operar("push", caractere, pilha)

    invertido = []
    while not pilha.is_empty():
        caractere = pilha.pop()
        invertido.append(caractere)
        if ao_operar:
            ao_operar("pop", caractere, pilha)
    return "".join(invertido)
