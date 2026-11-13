"""Tests unitarios de la MaxHeap y del servicio Top-N (TP6).

Ejecutar desde la raíz del proyecto:

    python -m unittest tests.test_heap -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from estructuras.heap import MaxHeap
from modelos.catalogo import Catalogo
from modelos.videojuego import Videojuego
from servicios.recomendador import Recomendador


def _es_heap(datos, key):
    """Propiedad de heap: ningún hijo puede superar a su padre."""
    for i in range(len(datos)):
        for hijo in (2 * i + 1, 2 * i + 2):
            if hijo < len(datos) and key(datos[hijo]) > key(datos[i]):
                return False
    return True


class TestMaxHeap(unittest.TestCase):
    def test_vacia(self):
        heap = MaxHeap()
        self.assertTrue(heap.is_empty())
        self.assertEqual(heap.size(), 0)
        with self.assertRaises(IndexError):
            heap.pop()
        with self.assertRaises(IndexError):
            heap.peek()

    def test_push_pop_orden_descendente(self):
        heap = MaxHeap()
        for x in [3, 1, 4, 1, 5, 9, 2, 6]:
            heap.push(x)
        self.assertEqual(heap.size(), 8)
        self.assertEqual(heap.peek(), 9)
        salidos = [heap.pop() for _ in range(8)]
        self.assertEqual(salidos, [9, 6, 5, 4, 3, 2, 1, 1])
        self.assertTrue(heap.is_empty())

    def test_pop_en_orden_no_altera_los_demas(self):
        heap = MaxHeap()
        for x in [10, 40, 20, 50, 30]:
            heap.push(x)
        self.assertEqual(heap.pop(), 50)
        self.assertEqual(heap.pop(), 40)
        self.assertEqual(heap.peek(), 30)
        self.assertEqual(heap.size(), 3)

    def test_heapify_es_heap(self):
        datos = [7, 2, 9, 4, 1, 8, 3]
        heap = MaxHeap.heapify(datos)
        self.assertEqual(heap.size(), len(datos))
        self.assertTrue(_es_heap(heap._datos, lambda x: x))
        # heapify no debe mutar la lista original.
        self.assertEqual(datos, [7, 2, 9, 4, 1, 8, 3])

    def test_heapify_extrae_en_orden(self):
        heap = MaxHeap.heapify([7, 2, 9, 4, 1, 8, 3])
        self.assertEqual([heap.pop() for _ in range(7)], [9, 8, 7, 4, 3, 2, 1])

    def test_heapify_vacio(self):
        heap = MaxHeap.heapify([])
        self.assertTrue(heap.is_empty())

    def test_key_configurable(self):
        # Prioridad por campo: gana siempre el mayor 'rating'.
        datos = [("a", 5.0), ("b", 9.5), ("c", 7.0)]
        heap = MaxHeap.heapify(datos, key=lambda t: t[1])
        self.assertEqual(heap.pop(), ("b", 9.5))
        self.assertEqual(heap.pop(), ("c", 7.0))
        self.assertEqual(heap.pop(), ("a", 5.0))

    def test_clear(self):
        heap = MaxHeap.heapify([1, 2, 3])
        heap.clear()
        self.assertTrue(heap.is_empty())


class TestRecomendador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogo = Catalogo()
        for titulo, rating in [
            ("Alpha", 7.5),
            ("Beta", 9.8),
            ("Gamma", 8.2),
            ("Delta", 9.1),
            ("Epsilon", 6.4),
        ]:
            cls.catalogo.agregar_juego(Videojuego(titulo, "RPG", "Estudio X", rating))
        cls.recomendador = Recomendador(cls.catalogo)

    def test_top_n_ordenado(self):
        top = self.recomendador.obtener_top_n(3)
        self.assertEqual(
            [j.get_titulo() for j in top], ["Beta", "Delta", "Gamma"]
        )

    def test_top_n_mayor_que_catalogo(self):
        top = self.recomendador.obtener_top_n(50)
        self.assertEqual(len(top), 5)

    def test_top_n_invalido(self):
        self.assertEqual(self.recomendador.obtener_top_n(0), [])
        self.assertEqual(self.recomendador.obtener_top_n(-5), [])

    def test_top_n_coincide_con_sort(self):
        # Mismo resultado que ordenar todo el dataset (referencia).
        referencial = sorted(
            self.catalogo.listar_todos(),
            key=lambda j: j.get_rating(),
            reverse=True,
        )[:4]
        top = self.recomendador.obtener_top_n(4)
        self.assertEqual(
            [j.get_titulo() for j in top], [j.get_titulo() for j in referencial]
        )

    def test_top_n_no_modifica_catalogo(self):
        antes = [j.get_titulo() for j in self.catalogo.listar_todos()]
        self.recomendador.obtener_top_n(2)
        despues = [j.get_titulo() for j in self.catalogo.listar_todos()]
        self.assertEqual(antes, despues)


if __name__ == "__main__":
    unittest.main()
