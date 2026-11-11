"""Servicio de recomendaciones de NextPlay.

Conecta el catálogo (modelos/) con las estructuras de datos para
resolver consultas de negocio, como el ranking Top-N.
"""

from __future__ import annotations

from typing import List

from algoritmos.grafo import Grafo
from estructuras.heap import MaxHeap
from modelos.videojuego import Videojuego


class Recomendador:
    """Servicio principal de recomendaciones sobre un catálogo.

    Usa una MaxHeap con prioridad por rating para obtener los N juegos
    mejor evaluados sin ordenar el catálogo completo, y construye el
    grafo de relaciones entre juegos para las consultas del TP7/TP8.
    """

    def __init__(self, catalogo) -> None:
        self._catalogo = catalogo

    def obtener_top_n(self, n: int) -> List[Videojuego]:
        """Devuelve los `n` juegos de mayor rating, en orden descendente.

        Estrategia:
        1. `heapify` construye la MaxHeap en O(K) (K = tamaño del catálogo).
        2. Se extraen n elementos con `pop`, cada uno en O(log K).

        Total: O(K + n log K), frente a O(K log K) de ordenar el catálogo
        completo con `sort()` cuando n << K. No se modifica el catálogo.

        Args:
            n: cantidad de juegos a devolver.

        Returns:
            Lista de a lo sumo n juegos, del mejor al peor rating.
            Devuelve [] si n <= 0 o el catálogo está vacío.
        """
        if n <= 0 or not self._catalogo.listar_todos():
            return []
        heap = MaxHeap.heapify(
            self._catalogo.listar_todos(),
            key=lambda juego: juego.get_rating(),
        )
        cantidad = min(n, heap.size())
        return [heap.pop() for _ in range(cantidad)]

    def construir_grafo(self) -> Grafo:
        """Grafo de relaciones del catálogo actual (se construye en cada consulta).

        Modelo (justificado en docs/03 y docs/04):
        - **Vértice** = un juego del catálogo.
        - **Arista no dirigida** entre dos juegos si comparten **género**
          o comparten **estudio** (relación real del dominio).
        - **Peso** = afinidad por rating: `1 / (1 + |Δrating|)` → (0, 1],
          a mayor cercanía de ratings, mayor peso (siempre > 0, apto para
          un futuro camino mínimo).

        Complejidad: O(V²) por comparar todos los pares (V ≤ ~100 en el
        sistema real; con datos masivos convendría indexar por género/estudio).
        Se reconstruye en cada consulta porque el catálogo es pequeño y
        dinámico: es más barato recalcular que mantener sincronizado.
        """
        grafo = Grafo()
        juegos = self._catalogo.listar_todos()
        for juego in juegos:
            grafo.agregar_vertice(juego)
        for i in range(len(juegos)):
            for j in range(i + 1, len(juegos)):
                a, b = juegos[i], juegos[j]
                mismo_genero = a.get_genero().casefold() == b.get_genero().casefold()
                mismo_estudio = a.get_estudio().casefold() == b.get_estudio().casefold()
                if mismo_genero or mismo_estudio:
                    peso = 1.0 / (1.0 + abs(a.get_rating() - b.get_rating()))
                    grafo.agregar_arista(a, b, peso)
        return grafo

    def juegos_relacionados(self, juego: Videojuego) -> List[tuple]:
        """Vecinos del grafo ordenados de mayor a menor afinidad.

        Returns:
            Lista de (juego_vecino, peso) o [] si el juego no tiene relaciones.
        """
        grafo = self.construir_grafo()
        vecinos = grafo.vecinos(juego)
        return sorted(vecinos, key=lambda par: par[1], reverse=True)

    def juego_mas_cercano(self, juego: Videojuego):
        """El juego conectado más cercano a `juego` vía BFS (menos aristas).

        Implementa la consulta del TP8: "¿cuál es el juego relacionado más
        cercano a X?". BFS garantiza que el primer nivel alcanzado es el
        de distancia mínima; si hay empate en la distancia, gana el de
        mayor rating (criterio de calidad del sistema).

        Returns:
            (juego, distancia) o None si no tiene conexiones.
        """
        grafo = self.construir_grafo()
        recorrido = grafo.bfs(juego)
        if len(recorrido) <= 1:  # solo el origen: sin vecinos
            return None
        distancia_minima = recorrido[1][1]
        candidatos = [
            vertice for vertice, distancia in recorrido
            if distancia == distancia_minima
        ]
        mas_cercano = max(candidatos, key=lambda j: j.get_rating())
        return mas_cercano, distancia_minima

    def explorar_red(self, juego: Videojuego) -> List[Videojuego]:
        """Toda la red conectada con `juego` en profundidad (DFS). O(V + E).

        TP8: "explorar todos los juegos relacionados con X en profundidad".
        Devuelve los vértices de la componente conexa en orden de visita DFS.
        """
        grafo = self.construir_grafo()
        return grafo.dfs(juego)
