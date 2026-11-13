"""Cola de prioridad (heap binaria) de NextPlay — TP6.

Implementación manual según las reglas de la cátedra: NO se usa la
librería estándar `heapq`. La heap vive sobre una lista/arreglo interno
donde el elemento en la posición i tiene hijos en 2i+1 y 2i+2, y el
padre en (i-1)//2 (índices desde 0).

Se usa para el ranking Top-N de juegos: mantener rápido el elemento de
mayor prioridad (rating) sin ordenar el catálogo completo cada vez.
"""

from __future__ import annotations

from typing import Callable, List, Optional, TypeVar

T = TypeVar("T")


class MaxHeap:
    """Heap binaria de máximo sobre un arreglo, con prioridad configurable.

    La prioridad de un elemento se calcula con la función `key`
    (por defecto, el propio elemento). El máximo siempre está en la raíz
    (posición 0), lo que permite extraerlo en O(1) y reordenar en O(log n).

    Ejemplo de uso con el dominio:

        heap = MaxHeap(key=lambda j: j.get_rating())
        heap.push(juego)
        mejor = heap.pop()   # juego con mayor rating
    """

    def __init__(self, key: Optional[Callable[[T], object]] = None) -> None:
        self._datos: List[T] = []
        self._key: Callable[[T], object] = key if key is not None else (lambda x: x)

    # ------------------------------------------------------------------
    # Consultas básicas
    # ------------------------------------------------------------------
    def size(self) -> int:
        """Cantidad de elementos de la heap. O(1)."""
        return len(self._datos)

    def is_empty(self) -> bool:
        """True si la heap no tiene elementos. O(1)."""
        return len(self._datos) == 0

    def peek(self) -> T:
        """Devuelve el elemento de mayor prioridad sin extraerlo. O(1).

        Raises:
            IndexError: si la heap está vacía.
        """
        if not self._datos:
            raise IndexError("peek sobre una heap vacía")
        return self._datos[0]

    def clear(self) -> None:
        """Vacía la heap. O(1)."""
        self._datos.clear()

    # ------------------------------------------------------------------
    # Inserción y extracción
    # ------------------------------------------------------------------
    def push(self, item: T) -> None:
        """Inserta un elemento y lo hace flotar hasta su lugar. O(log n).

        El elemento se agrega al final del arreglo (para mantener la
        forma de árbol completa) y `_sift_up` lo intercambia con su
        padre mientras su prioridad sea mayor.
        """
        self._datos.append(item)
        self._sift_up(len(self._datos) - 1)

    def pop(self) -> T:
        """Extrae y devuelve el elemento de mayor prioridad. O(log n).

        Se intercambia la raíz con el último elemento, se quita el último
        y la nueva raíz se hunde con `_sift_down` hasta restaurar la
        propiedad de heap.

        Raises:
            IndexError: si la heap está vacía.
        """
        if not self._datos:
            raise IndexError("pop sobre una heap vacía")
        self._intercambiar(0, len(self._datos) - 1)
        maximo = self._datos.pop()
        if self._datos:
            self._sift_down(0)
        return maximo

    # ------------------------------------------------------------------
    # Construcción lineal
    # ------------------------------------------------------------------
    @classmethod
    def heapify(cls, items, key: Optional[Callable[[T], object]] = None) -> "MaxHeap":
        """Construye una heap a partir de una colección en O(n) (Floyd).

        En vez de hacer n pushes (O(n log n)), se copian los elementos y
        se hunden desde el último padre hasta la raíz. El costo total es
        n/2 + n/4 + ... ≈ n operaciones amortizadas.
        """
        heap = cls(key=key)
        heap._datos = list(items)
        # Último nodo que tiene al menos un hijo: (n // 2) - 1.
        for i in range(len(heap._datos) // 2 - 1, -1, -1):
            heap._sift_down(i)
        return heap

    # ------------------------------------------------------------------
    # Operaciones internas (flotado / hundido)
    # ------------------------------------------------------------------
    def _sift_up(self, idx: int) -> None:
        """Flota el elemento en `idx` hacia la raíz mientras sea mayor que su padre."""
        while idx > 0:
            padre = (idx - 1) // 2
            if self._prioridad(idx) > self._prioridad(padre):
                self._intercambiar(idx, padre)
                idx = padre
            else:
                break

    def _sift_down(self, idx: int) -> None:
        """Hunde el elemento en `idx` hacia las hojas mientras sea menor que algún hijo."""
        n = len(self._datos)
        while True:
            izquierdo = 2 * idx + 1
            derecho = 2 * idx + 2
            mayor = idx
            if izquierdo < n and self._prioridad(izquierdo) > self._prioridad(mayor):
                mayor = izquierdo
            if derecho < n and self._prioridad(derecho) > self._prioridad(mayor):
                mayor = derecho
            if mayor == idx:
                break
            self._intercambiar(idx, mayor)
            idx = mayor

    def _prioridad(self, idx: int) -> object:
        """Prioridad (clave) del elemento en la posición `idx` del arreglo."""
        return self._key(self._datos[idx])

    def _intercambiar(self, i: int, j: int) -> None:
        """Intercambia los elementos en las posiciones i y j."""
        self._datos[i], self._datos[j] = self._datos[j], self._datos[i]
