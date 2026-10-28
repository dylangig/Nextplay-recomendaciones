"""Tests unitarios del árbol general (TP5).

Ejecutar desde la raíz del proyecto:

    python -m unittest tests.test_arbol_general -v
"""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algoritmos.arbol_general import (
    ArbolGeneral,
    JERARQUIA_GENEROS,
    NodoGeneral,
    arbol_por_defecto,
)

RUTA_DATOS = Path(__file__).resolve().parent.parent / "datos" / "juegos.json"


class TestConstruccion(unittest.TestCase):
    def test_arbol_vacio(self):
        arbol = ArbolGeneral()
        self.assertIsNone(arbol.raiz)
        self.assertEqual(arbol.altura(), 0)
        self.assertEqual(arbol.cantidad_nodos(), 0)
        self.assertEqual(arbol.recorrido_preorden(), [])
        self.assertEqual(arbol.recorrido_por_niveles(), [])
        self.assertEqual(arbol.recorrido_postorden(), [])
        self.assertEqual(arbol.dibujar(), "")

    def test_construir_desde_diccionario(self):
        arbol = ArbolGeneral.construir_desde_diccionario(
            "raiz", {"a": None, "b": {"c": None, "d": None}, "e": None}
        )
        self.assertEqual(arbol.cantidad_nodos(), 6)
        self.assertEqual(arbol.altura(), 3)
        self.assertEqual(
            arbol.recorrido_preorden(), ["raiz", "a", "b", "c", "d", "e"]
        )

    def test_construir_con_jerarquia_vacia(self):
        arbol = ArbolGeneral.construir_desde_diccionario("raiz", None)
        self.assertEqual(arbol.cantidad_nodos(), 1)
        self.assertEqual(arbol.altura(), 1)


class TestInsercion(unittest.TestCase):
    def test_agregar_hijo(self):
        arbol = ArbolGeneral("raiz")
        hijo = arbol.agregar_hijo(arbol.raiz, "hijo")
        self.assertIsInstance(hijo, NodoGeneral)
        self.assertIs(hijo.padre, arbol.raiz)
        self.assertIn(hijo, arbol.raiz.hijos)
        self.assertEqual(arbol.cantidad_nodos(), 2)

    def test_agregar_hijo_a_nodo_ajeno(self):
        ajeno = NodoGeneral("ajeno")
        arbol = ArbolGeneral("raiz")
        with self.assertRaises(ValueError):
            arbol.agregar_hijo(ajeno, "x")

    def test_agregar_hijo_tipo_invalido(self):
        arbol = ArbolGeneral("raiz")
        with self.assertRaises(TypeError):
            arbol.agregar_hijo("no_es_nodo", "x")


class TestBusqueda(unittest.TestCase):
    def setUp(self):
        self.arbol = ArbolGeneral.construir_desde_diccionario(
            "Videojuegos",
            {"Aventura": {"Metroidvania": None}, "RPG": None},
        )

    def test_buscar_existente(self):
        nodo = self.arbol.buscar("metroidvania")
        self.assertIsNotNone(nodo)
        self.assertEqual(nodo.dato, "Metroidvania")

    def test_buscar_inexistente(self):
        self.assertIsNone(self.arbol.buscar("Shooters"))
        self.assertIsNone(self.arbol.buscar("Terror"))

    def test_buscar_ruta(self):
        self.assertEqual(
            self.arbol.buscar_ruta("metroidvania"),
            ["Videojuegos", "Aventura", "Metroidvania"],
        )
        self.assertEqual(
            self.arbol.buscar_ruta("RPG"), ["Videojuegos", "RPG"]
        )
        self.assertIsNone(self.arbol.buscar_ruta("no-existe"))

    def test_nombres_en_subarbol(self):
        nombres = self.arbol.nombres_en_subarbol("Aventura")
        self.assertEqual(set(nombres), {"Aventura", "Metroidvania"})
        with self.assertRaises(ValueError):
            self.arbol.nombres_en_subarbol("no-existe")


class TestRecorridos(unittest.TestCase):
    def setUp(self):
        self.arbol = ArbolGeneral.construir_desde_diccionario(
            "1",
            {"2": {"4": None, "5": None}, "3": {"6": None, "7": None}},
        )

    def test_preorden(self):
        self.assertEqual(
            self.arbol.recorrido_preorden(), ["1", "2", "4", "5", "3", "6", "7"]
        )

    def test_por_niveles(self):
        self.assertEqual(
            self.arbol.recorrido_por_niveles(), ["1", "2", "3", "4", "5", "6", "7"]
        )

    def test_postorden(self):
        self.assertEqual(
            self.arbol.recorrido_postorden(), ["4", "5", "2", "6", "7", "3", "1"]
        )


class TestDibujo(unittest.TestCase):
    def test_dibujar_ascii(self):
        arbol = ArbolGeneral.construir_desde_diccionario(
            "raiz", {"a": None, "b": {"c": None}, "d": None}
        )
        esperado = "\n".join(
            [
                "raiz",
                "├── a",
                "├── b",
                "│   └── c",
                "└── d",
            ]
        )
        self.assertEqual(arbol.dibujar(), esperado)

    def test_dibujar_con_sufijo(self):
        arbol = ArbolGeneral.construir_desde_diccionario("raiz", {"a": None})
        self.assertEqual(
            arbol.dibujar(sufijo=lambda n: f" ({n})"),
            "raiz (raiz)\n└── a (a)",
        )


class TestIntegracionCatalogo(unittest.TestCase):
    """La jerarquía debe cubrir exactamente los géneros de datos/juegos.json."""

    @classmethod
    def setUpClass(cls):
        with open(RUTA_DATOS, encoding="utf-8") as archivo:
            cls.datos = json.load(archivo)
        cls.arbol = arbol_por_defecto()

    def test_cubre_todos_los_generos(self):
        generos_datos = {j["genero"].casefold() for j in self.datos}
        generos_arbol = {n.casefold() for n in self.arbol.recorrido_preorden()}
        # Todo género del JSON existe en el árbol (las categorías
        # intermedias Shooter/Rol y la raíz no son géneros del JSON).
        self.assertTrue(generos_datos <= generos_arbol)
        self.assertEqual(generos_datos - generos_arbol, set())

    def test_conteo_total_es_100(self):
        # Todos los juegos caen en alguna categoría raíz.
        conteos = []
        for hijo in self.arbol.raiz.hijos:
            nombres = {n.casefold() for n in self.arbol.nombres_en_subarbol(hijo.dato)}
            conteos.append(
                sum(1 for j in self.datos if j["genero"].casefold() in nombres)
            )
        self.assertEqual(sum(conteos), 100)

    def test_altura_y_nodos(self):
        self.assertEqual(self.arbol.altura(), 3)
        # 1 raíz + 10 categorías + 17 subgéneros.
        self.assertEqual(self.arbol.cantidad_nodos(), 28)


if __name__ == "__main__":
    unittest.main()
