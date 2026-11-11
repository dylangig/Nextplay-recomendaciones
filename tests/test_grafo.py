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


class TestRecorridos(unittest.TestCase):
    """BFS y DFS sobre un grafo pequeño de referencia:

        a — b — d
        │
        c        e   (e aislado)
    """

    @classmethod
    def setUpClass(cls):
        cls.grafo = Grafo()
        for arista in [("a", "b"), ("a", "c"), ("b", "d")]:
            cls.grafo.agregar_arista(*arista)
        cls.grafo.agregar_vertice("e")

    def test_bfs_ordena_por_distancia(self):
        recorrido = dict(self.grafo.bfs("a"))
        self.assertEqual(recorrido["a"], 0)
        # vecinos directos de a: distancia 1.
        self.assertEqual(recorrido["b"], 1)
        self.assertEqual(recorrido["c"], 1)
        # d está a 2 aristas.
        self.assertEqual(recorrido["d"], 2)
        # La lista sale ordenada por distancia creciente.
        distancias = [dist for _, dist in self.grafo.bfs("a")]
        self.assertEqual(distancias, sorted(distancias))

    def test_bfs_no_llega_a_componentes_desconectados(self):
        recorrido = self.grafo.bfs("a")
        vertices = {v for v, _ in recorrido}
        self.assertEqual(vertices, {"a", "b", "c", "d"})
        self.assertNotIn("e", vertices)

    def test_bfs_aislado_e_inexistente(self):
        self.assertEqual(self.grafo.bfs("e"), [("e", 0)])
        self.assertEqual(self.grafo.bfs("z"), [])

    def test_dfs_visita_cada_vertice_una_vez(self):
        recorrido = self.grafo.dfs("a")
        self.assertEqual(len(recorrido), len(set(recorrido)))
        self.assertEqual(set(recorrido), {"a", "b", "c", "d"})
        self.assertEqual(recorrido[0], "a")

    def test_dfs_inexistente(self):
        self.assertEqual(self.grafo.dfs("z"), [])

    def test_juego_mas_cercano_bfs(self):
        # J1 (RPG, 9.0) está a 1 arista de J2 y a 2 de J4? No: J4 no conecta.
        catalogo = Catalogo()
        for titulo, genero, estudio, rating in [
            ("J1", "RPG", "A", 9.0),
            ("J2", "RPG", "B", 8.0),
            ("J3", "Puzzle", "A", 7.0),   # conecta con J1 por estudio
            ("J4", "Puzzle", "C", 6.0),   # conecta con J3 por género
        ]:
            catalogo.agregar_juego(Videojuego(titulo, genero, estudio, rating))
        recomendador = Recomendador(catalogo)
        j1 = catalogo.listar_todos()[0]
        # J2 y J3 están a 1 arista; con empate gana el de mayor rating (J2).
        resultado = recomendador.juego_mas_cercano(j1)
        self.assertIsNotNone(resultado)
        cercano, distancia = resultado
        self.assertEqual(cercano.get_titulo(), "J2")
        self.assertEqual(distancia, 1)

    def test_juego_mas_cercano_sin_conexiones(self):
        catalogo = Catalogo()
        catalogo.agregar_juego(Videojuego("Solo", "Puzzle", "Único", 9.0))
        recomendador = Recomendador(catalogo)
        self.assertIsNone(
            recomendador.juego_mas_cercano(catalogo.listar_todos()[0])
        )

    def test_explorar_red_dfs_llega_a_toda_la_componente(self):
        catalogo = Catalogo()
        for titulo, genero, estudio, rating in [
            ("J1", "RPG", "A", 9.0),
            ("J2", "RPG", "B", 8.0),
            ("J3", "Puzzle", "A", 7.0),
            ("J4", "Puzzle", "C", 6.0),
        ]:
            catalogo.agregar_juego(Videojuego(titulo, genero, estudio, rating))
        recomendador = Recomendador(catalogo)
        j1 = catalogo.listar_todos()[0]
        recorrido = recomendador.explorar_red(j1)
        # Componente completa: J1—J2 (género), J1—J3 (estudio), J3—J4 (género).
        self.assertEqual(len(recorrido), 4)
        self.assertEqual(recorrido[0].get_titulo(), "J1")


if __name__ == "__main__":
    unittest.main()
