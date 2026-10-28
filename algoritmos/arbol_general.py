"""Árbol general (n-ario) de NextPlay.

Representa la jerarquía natural del dominio: categorías de videojuegos
(Videojuegos → géneros → subgéneros). A diferencia del BST y el AVL, cada
nodo puede tener cantidad arbitraria de hijos, porque una categoría puede
contener muchas subcategorías.
"""

from __future__ import annotations

from collections import deque
from typing import Callable, Iterator, Optional, Union

# Jerarquía de géneros basada en los 25 géneros reales de datos/juegos.json.
# Un género hoja se representa con valor None; un nodo interno con un dict
# anidado. Los nodos intermedios también pueden ser géneros reales
# (Estrategia, Simulación), por eso un nodo puede tener dict vacío y a la
# vez ser un género del catálogo.
JERARQUIA_GENEROS: dict = {
    "Acción": {
        "Acción-aventura": None,
        "Hack and slash": None,
        "Sigilo": None,
        "Lucha": None,
        "Run and gun": None,
    },
    "Shooter": {
        "FPS": None,
        "Battle royale": None,
    },
    "Rol": {
        "RPG": None,
        "Action RPG": None,
        "JRPG": None,
        "RPG táctico": None,
    },
    "Aventura": {
        "Metroidvania": None,
        "Survival horror": None,
        "Immersive sim": None,
    },
    "Estrategia": {
        "Estrategia por turnos": None,
        "Estrategia táctica": None,
    },
    "Plataformas": None,
    "Puzzle": None,
    "Roguelike": None,
    "Simulación": {
        "Sandbox": None,
    },
    "Deportes": None,
}


class NodoGeneral:
    """Nodo de un árbol n-ario.

    Guarda su dato, una referencia al padre (para reconstruir la ruta
    hasta la raíz) y la lista ordenada de hijos.
    """

    def __init__(self, dato: Union[str, object]) -> None:
        self._dato = dato
        self._padre: Optional[NodoGeneral] = None
        self._hijos: list[NodoGeneral] = []

    @property
    def dato(self) -> Union[str, object]:
        """Dato almacenado en el nodo (una categoría, en NextPlay)."""
        return self._dato

    @property
    def padre(self) -> Optional["NodoGeneral"]:
        """Nodo padre, o None si es la raíz."""
        return self._padre

    @property
    def hijos(self) -> list["NodoGeneral"]:
        """Lista de hijos, en el orden en que fueron agregados."""
        return self._hijos

    def __repr__(self) -> str:
        return f"NodoGeneral({self._dato!r})"


class ArbolGeneral:
    """Árbol n-ario sobre nodos enlazados.

    La raíz puede ser None (árbol vacío). Todas las operaciones de
    búsqueda son case-insensitive cuando los datos son strings.
    """

    def __init__(self, raiz: Optional[Union[str, object]] = None) -> None:
        self._raiz: Optional[NodoGeneral] = (
            NodoGeneral(raiz) if raiz is not None else None
        )

    @property
    def raiz(self) -> Optional[NodoGeneral]:
        """Nodo raíz del árbol (None si está vacío)."""
        return self._raiz

    # ------------------------------------------------------------------
    # Construcción
    # ------------------------------------------------------------------
    @classmethod
    def construir_desde_diccionario(
        cls,
        raiz_dato: Union[str, object],
        jerarquia: Optional[dict],
    ) -> "ArbolGeneral":
        """Construye el árbol a partir de un dict anidado.

        Cada clave es el dato de un nodo y su valor es:
        - None o dict vacío: nodo hoja.
        - dict: subcategorías (recursivo).
        """
        arbol = cls(raiz_dato)
        if jerarquia:
            arbol._poblar(arbol._raiz, jerarquia)
        return arbol

    def _poblar(self, nodo: NodoGeneral, jerarquia: dict) -> None:
        for nombre, subjerarquia in jerarquia.items():
            hijo = self.agregar_hijo(nodo, nombre)
            if subjerarquia:
                self._poblar(hijo, subjerarquia)

    def agregar_hijo(self, padre: NodoGeneral, dato: Union[str, object]) -> NodoGeneral:
        """Agrega un hijo con `dato` debajo de `padre` y lo devuelve.

        Raises:
            TypeError: si `padre` no es un NodoGeneral.
            ValueError: si `padre` no pertenece a este árbol.
        """
        if not isinstance(padre, NodoGeneral):
            raise TypeError("padre debe ser un NodoGeneral")
        if not self._pertenece(padre):
            raise ValueError(
                f"El nodo {padre.dato!r} no pertenece a este árbol"
            )
        hijo = NodoGeneral(dato)
        hijo._padre = padre
        padre._hijos.append(hijo)
        return hijo

    def _pertenece(self, objetivo: NodoGeneral) -> bool:
        """Indica si `objetivo` es un nodo de este árbol (por identidad)."""
        return any(nodo is objetivo for nodo in self._iter_preorden())

    # ------------------------------------------------------------------
    # Búsqueda
    # ------------------------------------------------------------------
    def buscar(self, dato: Union[str, object]) -> Optional[NodoGeneral]:
        """Busca el primer nodo cuyo dato coincida (case-insensitive).

        Devuelve None si no existe o el árbol está vacío.
        Complejidad: O(n) — no hay orden que aprovechar en un árbol general.
        """
        for nodo in self._iter_preorden():
            if self._coincide(nodo._dato, dato):
                return nodo
        return None

    def buscar_ruta(self, dato: Union[str, object]) -> Optional[list]:
        """Devuelve la ruta desde la raíz hasta la categoría buscada.

        Ej.: buscar_ruta("Metroidvania") -> ["Videojuegos", "Aventura", "Metroidvania"]
        """
        nodo = self.buscar(dato)
        if nodo is None:
            return None
        ruta = []
        while nodo is not None:
            ruta.append(nodo._dato)
            nodo = nodo._padre
        ruta.reverse()
        return ruta

    @staticmethod
    def _coincide(a: object, b: object) -> bool:
        if isinstance(a, str) and isinstance(b, str):
            return a.casefold() == b.casefold()
        return a == b

    def nombres_en_subarbol(self, dato: Union[str, object]) -> list:
        """Lista los nombres de la categoría `dato` y todos sus descendientes.

        Útil para relacionar una categoría con los géneros reales del
        catálogo (los nombres del árbol son los valores del campo `genero`).

        Raises:
            ValueError: si la categoría no existe en el árbol.
        """
        nodo = self.buscar(dato)
        if nodo is None:
            raise ValueError(f"La categoría {dato!r} no existe en el árbol")
        nombres = []
        for actual in self._iter_preorden_desde(nodo):
            nombres.append(actual._dato)
        return nombres

    # ------------------------------------------------------------------
    # Recorridos
    # ------------------------------------------------------------------
    @staticmethod
    def _iter_preorden_desde(nodo: NodoGeneral) -> Iterator[NodoGeneral]:
        pila = [nodo]
        while pila:
            actual = pila.pop()
            yield actual
            pila.extend(reversed(actual._hijos))

    def _iter_preorden(self) -> Iterator[NodoGeneral]:
        if self._raiz is None:
            return
        yield from self._iter_preorden_desde(self._raiz)

    def recorrido_preorden(self) -> list:
        """Recorrido en profundidad: nodo, hijo 1, subárbol 1, hijo 2...

        Complejidad: O(n). Muestra primero la categoría y luego sus ramas.
        """
        return [nodo._dato for nodo in self._iter_preorden()]

    def recorrido_por_niveles(self) -> list:
        """Recorrido por niveles (BFS) con cola.

        Complejidad: O(n). Muestra primero la raíz y nivel a nivel.
        """
        if self._raiz is None:
            return []
        resultado = []
        cola = deque([self._raiz])
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo._dato)
            cola.extend(nodo._hijos)
        return resultado

    def recorrido_postorden(self) -> list:
        """Recorrido postorden: los hijos antes que el padre.

        Complejidad: O(n). Útil para procesar subcategorías antes que
        su categoría (por ejemplo, agregar conteos de abajo hacia arriba).
        """
        resultado: list = []

        def _visitar(nodo: NodoGeneral) -> None:
            for hijo in nodo._hijos:
                _visitar(hijo)
            resultado.append(nodo._dato)

        if self._raiz is not None:
            _visitar(self._raiz)
        return resultado

    # ------------------------------------------------------------------
    # Métricas y visualización
    # ------------------------------------------------------------------
    def altura(self) -> int:
        """Altura del árbol en niveles (la raíz sola tiene altura 1).

        Complejidad: O(n) en el peor caso (cadena).
        """
        if self._raiz is None:
            return 0
        maxima = 0
        pila = [(self._raiz, 1)]
        while pila:
            nodo, nivel = pila.pop()
            if nivel > maxima:
                maxima = nivel
            for hijo in nodo._hijos:
                pila.append((hijo, nivel + 1))
        return maxima

    def cantidad_nodos(self) -> int:
        """Cantidad total de categorías del árbol. Complejidad: O(n)."""
        return sum(1 for _ in self._iter_preorden())

    def dibujar(self, sufijo: Optional[Callable[[str], str]] = None) -> str:
        """Devuelve el árbol como texto ASCII (├── / └──).

        `sufijo` es opcional: una función que recibe el nombre del nodo y
        devuelve texto a concatenar (ej. " (14 juegos)").
        """
        if self._raiz is None:
            return ""
        sufijo = sufijo or (lambda _nombre: "")
        lineas: list[str] = []

        def _visitar(
            nodo: NodoGeneral, prefijo: str, es_ultimo: bool, es_raiz: bool
        ) -> None:
            etiqueta = str(nodo._dato) + sufijo(str(nodo._dato))
            if es_raiz:
                lineas.append(etiqueta)
            else:
                conector = "└── " if es_ultimo else "├── "
                lineas.append(prefijo + conector + etiqueta)
            if es_raiz:
                prefijo_hijos = ""
            else:
                prefijo_hijos = prefijo + ("    " if es_ultimo else "│   ")
            for i, hijo in enumerate(nodo._hijos):
                _visitar(
                    hijo,
                    prefijo_hijos,
                    i == len(nodo._hijos) - 1,
                    False,
                )

        _visitar(self._raiz, "", True, True)
        return "\n".join(lineas)


def arbol_por_defecto() -> ArbolGeneral:
    """Árbol de categorías por defecto de NextPlay (jerarquía de géneros)."""
    return ArbolGeneral.construir_desde_diccionario("Videojuegos", JERARQUIA_GENEROS)
