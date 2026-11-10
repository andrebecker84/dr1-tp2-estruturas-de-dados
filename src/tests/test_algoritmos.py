"""Testes das funções com hash table, das ordenações e das funções hash (Exercícios 1 a 7 e 12).

    cd src && python3 -m unittest discover -s tests -t . -v
"""
import random
import unittest

from algoritmos.duplicados import primeiro_duplicado, primeiro_duplicado_aninhado
from algoritmos.hashing import colisoes, distribuicao, h1, h2, h3, imagem
from algoritmos.intersecao import intersecao, intersecao_aninhada
from algoritmos.metricas import medir
from algoritmos.ordenacao import insertion_sort, selection_sort
from algoritmos.texto import letras_ausentes, primeiro_nao_repetido
from algoritmos.unicos import maior_unico_aninhado, maior_unico_hash
from verificacao import inversoes, ordenacao_correta


def listas_aleatorias(quantidade=100, tamanho_maximo=30):
    gerador = random.Random(7)
    return [[gerador.randint(-10, 10) for _ in range(gerador.randint(0, tamanho_maximo))] for _ in range(quantidade)]


class TestHashTables(unittest.TestCase):

    def test_maior_unico_igual_nas_duas_versoes(self):
        for lista in listas_aleatorias():
            with self.subTest(lista=lista):
                self.assertEqual(maior_unico_hash(lista), maior_unico_aninhado(lista))

    def test_maior_unico_contadores(self):
        lista = [5, 7, 3, 9, 4, 9, 8, 3, 1]
        self.assertEqual(medir(maior_unico_aninhado, lista)[1].comparacoes, len(lista) ** 2)
        self.assertLessEqual(medir(maior_unico_hash, lista)[1].acessos, 3 * len(lista))

    def test_intersecao_sem_repetidos_e_na_ordem_de_b(self):
        self.assertEqual(intersecao([1, 2, 2, 3], [3, 2, 2, 9]), [3, 2])
        self.assertEqual(intersecao([], [1]), [])
        self.assertEqual(intersecao([1], []), [])

    def test_intersecao_igual_a_aninhada_com_valores_distintos(self):
        gerador = random.Random(3)
        for _ in range(50):
            a, b = gerador.sample(range(60), 20), gerador.sample(range(60), 25)
            self.assertEqual(intersecao(a, b), intersecao_aninhada(a, b))

    def test_intersecao_linear_nos_acessos(self):
        a, b = list(range(1_000)), list(range(500, 2_000))
        self.assertLessEqual(medir(intersecao, a, b)[1].acessos, len(a) + 2 * len(b))

    def test_primeiro_duplicado(self):
        self.assertEqual(primeiro_duplicado(["a", "b", "c", "b"]), "b")
        self.assertEqual(primeiro_duplicado(["x", "x"]), "x")
        self.assertEqual(primeiro_duplicado(["Ana", "ana"]), None)
        self.assertEqual(primeiro_duplicado([]), None)

    def test_primeiro_duplicado_respeita_a_ordem_de_leitura(self):
        # 'b' reaparece (índice 3) antes de 'a' (índice 4): o primeiro duplicado encontrado é 'b'.
        valores = ["a", "b", "c", "b", "a"]
        self.assertEqual(primeiro_duplicado(valores), "b")
        self.assertEqual(primeiro_duplicado_aninhado(valores), "b")

    def test_letras_ausentes(self):
        self.assertEqual(letras_ausentes("The quick brown fox jumps over the lay dog"), ["z"])
        self.assertEqual(letras_ausentes("Ação"), [c for c in "bdefghijklmnpqrstuvwxyz"])
        self.assertEqual(letras_ausentes("ABC 123 !?" + "defghijklmnopqrstuvwxyz"), [])
        self.assertEqual(len(letras_ausentes("")), 26)

    def test_primeiro_nao_repetido(self):
        casos = {"swiss": "w", "level": "v", "aabbcc": None, "": None, "Infnet": "I", "aabbz": "z"}
        for texto, esperado in casos.items():
            self.assertEqual(primeiro_nao_repetido(texto), esperado)

    def test_primeiro_nao_repetido_faz_no_maximo_3n_acessos(self):
        texto = "ab" * 500 + "z"
        self.assertEqual(medir(primeiro_nao_repetido, texto)[1].acessos, 3 * len(texto))


class TestOrdenacao(unittest.TestCase):

    def test_as_duas_ordenam(self):
        for algoritmo in (selection_sort, insertion_sort):
            for lista in listas_aleatorias():
                with self.subTest(algoritmo=algoritmo.__name__, lista=lista):
                    self.assertTrue(ordenacao_correta(lista, algoritmo(lista)))

    def test_nao_alteram_a_entrada(self):
        lista = [3, 1, 2]
        for algoritmo in (selection_sort, insertion_sort):
            algoritmo(lista)
            self.assertEqual(lista, [3, 1, 2])

    def test_selection_faz_sempre_n_n_menos_1_sobre_2_comparacoes(self):
        for lista in (list(range(50)), list(range(50, 0, -1)), listas_aleatorias(1, 50)[0]):
            n = len(lista)
            metricas = medir(selection_sort, lista)[1]
            self.assertEqual(metricas.comparacoes, n * (n - 1) // 2)
            self.assertLessEqual(metricas.trocas, max(n - 1, 0))

    def test_exemplo_dos_slides(self):
        selecao = medir(selection_sort, [4, 2, 7, 1, 3])[1]
        insercao = medir(insertion_sort, [4, 2, 7, 1, 3])[1]
        self.assertEqual((selecao.comparacoes, selecao.trocas), (10, 2))
        self.assertEqual((insercao.comparacoes, insercao.deslocamentos), (8, 6))

    def test_insertion_melhor_e_pior_caso(self):
        n = 100
        melhor = medir(insertion_sort, list(range(n)))[1]
        pior = medir(insertion_sort, list(range(n, 0, -1)))[1]
        self.assertEqual((melhor.comparacoes, melhor.deslocamentos), (n - 1, 0))
        self.assertEqual((pior.comparacoes, pior.deslocamentos), (n * (n - 1) // 2, n * (n - 1) // 2))

    def test_insertion_desloca_uma_vez_por_inversao(self):
        for lista in listas_aleatorias():
            self.assertEqual(medir(insertion_sort, lista)[1].deslocamentos, inversoes(lista))


class TestFuncoesHash(unittest.TestCase):

    def test_imagens(self):
        self.assertEqual(imagem(h1), list(range(10)))
        self.assertEqual(imagem(h2), list(range(10)))
        self.assertEqual(imagem(h3), [0, 1, 4, 5, 6, 9])

    def test_h2_e_uma_permutacao_de_h1(self):
        chaves = random.Random(1).sample(range(10_000), 200)
        self.assertEqual(sorted(distribuicao(chaves, h1)), sorted(distribuicao(chaves, h2)))

    def test_colisoes(self):
        self.assertEqual(colisoes(distribuicao(range(10), h1)), 0)
        self.assertEqual(colisoes(distribuicao(range(0, 100, 10), h1)), 9)


if __name__ == "__main__":
    unittest.main()
