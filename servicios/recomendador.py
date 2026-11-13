"""Servicio de recomendaciones de NextPlay.

Conecta el catálogo (modelos/) con las estructuras de datos para
resolver consultas de negocio, como el ranking Top-N.
"""

from __future__ import annotations

from typing import List

from estructuras.heap import MaxHeap
from modelos.videojuego import Videojuego


class Recomendador:
    """Servicio principal de recomendaciones sobre un catálogo.

    Usa una MaxHeap con prioridad por rating para obtener los N juegos
    mejor evaluados sin ordenar el catálogo completo.
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
