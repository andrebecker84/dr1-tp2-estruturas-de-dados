"""Testes da pilha, da fila e da inversão de string (Exercícios 9, 10 e 11).

    cd src && python3 -m unittest discover -s tests -t . -v
"""
import random
import unittest

from algoritmos.erros import Overflow, Underflow
from algoritmos.fila import Queue
from algoritmos.pilha import Stack
from algoritmos.texto import inverter


class TestStack(unittest.TestCase):

    def test_lifo(self):
        pilha = Stack(3)
        for valor in (1, 2, 3):
            pilha.push(valor)
        self.assertEqual([pilha.pop(), pilha.pop(), pilha.pop()], [3, 2, 1])

    def test_overflow_nao_altera_o_estado(self):
        pilha = Stack(2)
        pilha.push("a")
        pilha.push("b")
        with self.assertRaises(Overflow):
            pilha.push("c")
        self.assertEqual((pilha.array(), pilha.topo, pilha.size()), (["a", "b"], 1, 2))

    def test_underflow_em_pop_e_peek(self):
        pilha = Stack(1)
        with self.assertRaises(Underflow):
            pilha.pop()
        with self.assertRaises(Underflow):
            pilha.peek()
        self.assertTrue(pilha.is_empty())

    def test_pop_libera_a_posicao(self):
        pilha = Stack(2)
        pilha.push(10)
        pilha.pop()
        self.assertEqual(pilha.array(), [None, None])

    def test_capacidade_invalida(self):
        for capacidade in (0, -1, 2.5):
            with self.assertRaises(ValueError):
                Stack(capacidade)


class TestQueue(unittest.TestCase):

    def test_fifo_com_volta_no_array(self):
        fila = Queue(3)
        for valor in (1, 2, 3):
            fila.enqueue(valor)
        self.assertEqual(fila.dequeue(), 1)
        fila.enqueue(4)                         # entra na posição 0: o fim deu a volta
        self.assertEqual((fila.inicio, fila.fim, fila.array()), (1, 1, [4, 2, 3]))
        self.assertEqual([fila.dequeue() for _ in range(3)], [2, 3, 4])

    def test_overflow_e_underflow(self):
        fila = Queue(1)
        fila.enqueue("a")
        with self.assertRaises(Overflow):
            fila.enqueue("b")
        self.assertEqual(fila.dequeue(), "a")
        with self.assertRaises(Underflow):
            fila.dequeue()
        with self.assertRaises(Underflow):
            fila.peek()

    def test_fifo_em_operacoes_aleatorias(self):
        gerador = random.Random(11)
        fila, entrou, saiu = Queue(5), 0, 0
        for _ in range(5_000):
            if gerador.random() < 0.5 and not fila.is_full():
                entrou += 1
                fila.enqueue(entrou)
            elif not fila.is_empty():
                saiu += 1
                self.assertEqual(fila.dequeue(), saiu)
        self.assertEqual(fila.size(), entrou - saiu)


class TestInverter(unittest.TestCase):

    def test_inverte(self):
        casos = {"Infnet": "tenfnI", "arara": "arara", "": "", "a": "a", "ação": "oãça"}
        for texto, esperado in casos.items():
            self.assertEqual(inverter(texto), esperado)

    def test_usa_push_e_pop(self):
        operacoes = []
        inverter("abc", ao_operar=lambda operacao, caractere, pilha: operacoes.append((operacao, caractere)))
        self.assertEqual(operacoes, [("push", "a"), ("push", "b"), ("push", "c"), ("pop", "c"), ("pop", "b"), ("pop", "a")])


if __name__ == "__main__":
    unittest.main()
