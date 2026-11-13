"""Grafo no dirigido y pesado de NextPlay — TP7.

Representa las relaciones entre videojuegos del catálogo:
- Vértice: un juego (o cualquier objeto hasheable; la estructura es genérica).
- Arista no dirigida: dos juegos están conectados si comparten género
  o comparten estudio (decisión de dominio tomada en `servicios/recomendador.py`).
- Peso: afinidad/rating-similitud entre ambos (siempre > 0).

Representación: **lista de adyacencia** — el grafo del sistema es disperso
(100 vértices, cada uno con pocos vecinos), así que O(V + E) memoria y
recorridos, frente a O(V²) de la matriz de adyacencia.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Tuple, TypeVar

V = TypeVar("V")


class Grafo:
    """Grafo no dirigido pesado con lista de adyacencia.

    Estructura genérica: los vértices pueden ser strings (en tests) u
    objetos del dominio como `Videojuego`. Se apoya en que Python
    permite usar cualquier objeto hasheable como clave de diccionario.
    """

    def __init__(self) -> None:
        # {vértice: [(vecino, peso), ...]}
        self._adyacencia: Dict[V, List[Tuple[V, float]]] = {}

    # ------------------------------------------------------------------
    # Construcción
    # ------------------------------------------------------------------
    def agregar_vertice(self, vertice: V) -> None:
        """Agrega un vértice aislado. Idempotente (no duplica). O(1)."""
        self._adyacencia.setdefault(vertice, [])

    def agregar_arista(self, origen: V, destino: V, peso: float = 1.0) -> None:
        """Conecta `origen` y `destino` con `peso` (no dirigida). O(1).

        La arista se registra en ambas direcciones con el mismo peso.
        Si la arista ya existía, se actualiza su peso.

        Raises:
            ValueError: si se intenta crear un lazo (origen == destino).
        """
        if origen == destino:
            raise ValueError("Un grafo de relaciones no admite lazos (A ↔ A)")
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        self._vincular(origen, destino, peso)
        self._vincular(destino, origen, peso)

    def _vincular(self, origen: V, destino: V, peso: float) -> None:
        """Agrega o actualiza `destino` en la lista de vecinos de `origen`."""
        vecinos = self._adyacencia[origen]
        for i, (vecino, _) in enumerate(vecinos):
            if vecino == destino:
                vecinos[i] = (destino, peso)
                return
        vecinos.append((destino, peso))

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    def tiene_vertice(self, vertice: V) -> bool:
        """True si el vértice pertenece al grafo. O(1)."""
        return vertice in self._adyacencia

    def vertices(self) -> List[V]:
        """Lista de todos los vértices. O(V)."""
        return list(self._adyacencia.keys())

    def vecinos(self, vertice: V) -> List[Tuple[V, float]]:
        """Vecinos de `vertice` con su peso. O(1) de acceso + O(grado).

        Devuelve [] si el vértice no existe (la UI informa aparte).
        """
        return list(self._adyacencia.get(vertice, []))

    def grado(self, vertice: V) -> int:
        """Cantidad de conexiones de un vértice. O(1)."""
        return len(self._adyacencia.get(vertice, []))

    def peso_entre(self, a: V, b: V) -> Optional[float]:
        """Peso de la arista a↔b, o None si no están conectados. O(grado)."""
        for vecino, peso in self._adyacencia.get(a, []):
            if vecino == b:
                return peso
        return None

    def estan_conectados(self, a: V, b: V) -> bool:
        """True si existe arista entre a y b. O(grado)."""
        return self.peso_entre(a, b) is not None

    def cantidad_vertices(self) -> int:
        """Total de vértices. O(1)."""
        return len(self._adyacencia)

    def cantidad_aristas(self) -> int:
        """Total de aristas (cada una aparece dos veces en la lista). O(V)."""
        return sum(len(vecinos) for vecinos in self._adyacencia.values()) // 2

    # ------------------------------------------------------------------
    # Recorridos (TP8)
    # ------------------------------------------------------------------
    def bfs(self, origen: V) -> List[Tuple[V, int]]:
        """Recorrido por niveles (BFS) con cola. Complejidad: O(V + E).

        Visita primero los vecinos de `origen`, luego los vecinos de los
        vecinos, etc. Devuelve **(vértice, distancia en aristas)** en orden
        de descubrimiento: la lista está ordenada por distancia creciente,
        por eso el elemento [1:] empieza por los más cercanos.

        Returns:
            Lista [(vértice, distancia), ...]; [(origen, 0)] si está aislado;
            [] si el vértice no existe.
        """
        if not self.tiene_vertice(origen):
            return []
        visitados = {origen}
        cola = deque([(origen, 0)])
        recorrido: List[Tuple[V, int]] = []
        while cola:
            vertice, distancia = cola.popleft()
            recorrido.append((vertice, distancia))
            for vecino, _ in self._adyacencia[vertice]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append((vecino, distancia + 1))
        return recorrido

    def dfs(self, origen: V) -> List[V]:
        """Recorrido en profundidad (DFS) con pila explícita. O(V + E).

        Desciende por una rama antes que pasar a la hermana (útil para
        "explorar en profundidad" toda la red conectada). Usa pila y
        conjunto de visitados para no repetir vértices.

        Returns:
            Lista de vértices alcanzables en orden de visita (incluye
            `origen`); [] si el vértice no existe.
        """
        if not self.tiene_vertice(origen):
            return []
        visitados = set()
        pila = [origen]
        recorrido: List[V] = []
        while pila:
            vertice = pila.pop()
            if vertice in visitados:
                continue
            visitados.add(vertice)
            recorrido.append(vertice)
            # Se apilan en orden inverso para visitarlos en el orden de la lista.
            for vecino, _ in reversed(self._adyacencia[vertice]):
                if vecino not in visitados:
                    pila.append(vecino)
        return recorrido
