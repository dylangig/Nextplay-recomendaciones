"""Tests unitarios del grafo y de la consulta de juegos relacionados (TP7).

Ejecutar desde la raíz del proyecto:

    python -m unittest tests.test_grafo -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algoritmos.grafo import Grafo
from modelos.catalogo import Catalogo
from modelos.videojuego import Videojuego
from servicios.recomendador import Recomendador


class TestGrafoEstructura(unittest.TestCase):
    def test_vacio(self):
        grafo = Grafo()
        self.assertEqual(grafo.cantidad_vertices(), 0)
        self.assertEqual(grafo.cantidad_aristas(), 0)
        self.assertFalse(grafo.tiene_vertice("a"))
        self.assertEqual(grafo.vecinos("a"), [])
        self.assertIsNone(grafo.peso_entre("a", "b"))

    def test_agregar_vertice_idempotente(self):
        grafo = Grafo()
        grafo.agregar_vertice("a")
        grafo.agregar_vertice("a")
        self.assertEqual(grafo.cantidad_vertices(), 1)

    def test_arista_no_dirigida(self):
        grafo = Grafo()
        grafo.agregar_arista("a", "b", 0.9)
        self.assertTrue(grafo.estan_conectados("a", "b"))
        self.assertTrue(grafo.estan_conectados("b", "a"))
        self.assertEqual(grafo.peso_entre("a", "b"), 0.9)
        self.assertEqual(grafo.peso_entre("b", "a"), 0.9)
        self.assertEqual(grafo.cantidad_aristas(), 1)

    def test_lazo_prohibido(self):
        grafo = Grafo()
        with self.assertRaises(ValueError):
            grafo.agregar_arista("a", "a")

    def test_actualizar_peso(self):
        grafo = Grafo()
        grafo.agregar_arista("a", "b", 0.5)
        grafo.agregar_arista("a", "b", 0.8)
        self.assertEqual(grafo.cantidad_aristas(), 1)
        self.assertEqual(grafo.peso_entre("a", "b"), 0.8)

    def test_grado_y_vecinos(self):
        grafo = Grafo()
        grafo.agregar_arista("a", "b", 1.0)
        grafo.agregar_arista("a", "c", 0.5)
        grafo.agregar_vertice("aislado")
        self.assertEqual(grafo.grado("a"), 2)
        self.assertEqual(grafo.grado("aislado"), 0)
        vecinos = dict(grafo.vecinos("a"))
        self.assertEqual(set(vecinos), {"b", "c"})
        self.assertEqual(vecinos["c"], 0.5)


class TestGrafoDominio(unittest.TestCase):
    """construir_grafo(): vértice = juego, arista = mismo género o estudio."""

    @classmethod
    def setUpClass(cls):
        cls.catalogo = Catalogo()
        for titulo, genero, estudio, rating in [
            ("J1", "RPG", "Estudio A", 9.0),
            ("J2", "RPG", "Estudio B", 8.0),     # mismo género que J1
            ("J3", "FPS", "Estudio A", 7.0),     # mismo estudio que J1
            ("J4", "Puzzle", "Estudio C", 6.0),  # no comparte nada
        ]:
            cls.catalogo.agregar_juego(Videojuego(titulo, genero, estudio, rating))
        cls.recomendador = Recomendador(cls.catalogo)
        cls.grafo = cls.recomendador.construir_grafo()

    def test_vertices_son_los_juegos(self):
        self.assertEqual(self.grafo.cantidad_vertices(), 4)

    def test_conexiones_por_genero_y_estudio(self):
        j1, j2, j3, j4 = self.catalogo.listar_todos()
        # J1 ↔ J2 (mismo género RPG), J1 ↔ J3 (mismo estudio A).
        self.assertTrue(self.grafo.estan_conectados(j1, j2))
        self.assertTrue(self.grafo.estan_conectados(j1, j3))
        # J4 no comparte género ni estudio con nadie.
        self.assertFalse(self.grafo.estan_conectados(j1, j4))
        self.assertFalse(self.grafo.estan_conectados(j2, j4))
        self.assertEqual(self.grafo.cantidad_aristas(), 2)

    def test_peso_es_similitud_de_rating(self):
        j1, j2, _, _ = self.catalogo.listar_todos()
        # |9.0 - 8.0| = 1.0 → peso = 1/(1+1) = 0.5
        self.assertAlmostEqual(self.grafo.peso_entre(j1, j2), 0.5)

    def test_relacionados_ordenados_por_afinidad(self):
        j1 = self.catalogo.listar_todos()[0]
        relacionados = self.recomendador.juegos_relacionados(j1)
        titulos = [j.get_titulo() for j, _ in relacionados]
        # J3 (Δrating 2.0 → peso 0.33) va después que J2 (Δ 1.0 → 0.5).
        self.assertEqual(titulos, ["J2", "J3"])
        pesos = [peso for _, peso in relacionados]
        self.assertEqual(pesos, sorted(pesos, reverse=True))

    def test_relacionados_sin_conexiones(self):
        _, _, _, j4 = self.catalogo.listar_todos()
        self.assertEqual(self.recomendador.juegos_relacionados(j4), [])

    def test_construir_grafo_no_modifica_catalogo(self):
        antes = len(self.catalogo.listar_todos())
        self.recomendador.construir_grafo()
        self.assertEqual(len(self.catalogo.listar_todos()), antes)


if __name__ == "__main__":
    unittest.main()
