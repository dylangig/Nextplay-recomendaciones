class Nodo:
    def __init__(self, juego):
        self._juego = juego
        self._clave = juego.get_titulo().lower()
        self._izquierdo = None
        self._derecho = None


class ArbolBinario:
    def __init__(self):
        self._raiz = None

    def construir(self, catalogo):
        for juego in catalogo:
            self.insertar(juego)

    def insertar(self, juego):
        clave = juego.get_titulo().lower()
        if self._raiz is None:
            self._raiz = Nodo(juego)
            return
        actual = self._raiz
        while True:
            if clave < actual._clave:
                if actual._izquierdo is None:
                    actual._izquierdo = Nodo(juego)
                    return
                actual = actual._izquierdo
            elif clave > actual._clave:
                if actual._derecho is None:
                    actual._derecho = Nodo(juego)
                    return
                actual = actual._derecho
            else:
                return

    def buscar(self, titulo):
        clave = titulo.lower()
        actual = self._raiz
        while actual is not None:
            if clave == actual._clave:
                return actual._juego
            elif clave < actual._clave:
                actual = actual._izquierdo
            else:
                actual = actual._derecho
        return None

    def eliminar(self, titulo):
        clave = titulo.lower()
        self._raiz = self._eliminar_nodo(self._raiz, clave)

    def _eliminar_nodo(self, nodo, clave):
        if nodo is None:
            return None
        if clave < nodo._clave:
            nodo._izquierdo = self._eliminar_nodo(nodo._izquierdo, clave)
        elif clave > nodo._clave:
            nodo._derecho = self._eliminar_nodo(nodo._derecho, clave)
        else:
            if nodo._izquierdo is None:
                return nodo._derecho
            if nodo._derecho is None:
                return nodo._izquierdo
            sucesor = self._minimo(nodo._derecho)
            nodo._juego = sucesor._juego
            nodo._clave = sucesor._clave
            nodo._derecho = self._eliminar_nodo(nodo._derecho, sucesor._clave)
        return nodo

    def _minimo(self, nodo):
        while nodo._izquierdo is not None:
            nodo = nodo._izquierdo
        return nodo

    def vaciar(self):
        self._postorder_liberar(self._raiz)
        self._raiz = None

    def _postorder_liberar(self, nodo):
        if nodo is None:
            return
        self._postorder_liberar(nodo._izquierdo)
        self._postorder_liberar(nodo._derecho)
        nodo._izquierdo = None
        nodo._derecho = None
        nodo._juego = None

    def recorrido_inorder(self):
        juegos = []
        self._inorder(self._raiz, juegos)
        return juegos

    def _inorder(self, nodo, juegos):
        if nodo is None:
            return
        self._inorder(nodo._izquierdo, juegos)
        juegos.append(nodo._juego)
        self._inorder(nodo._derecho, juegos)

    def recorrido_preorder(self):
        juegos = []
        self._preorder(self._raiz, juegos)
        return juegos

    def _preorder(self, nodo, juegos):
        if nodo is None:
            return
        juegos.append(nodo._juego)
        self._preorder(nodo._izquierdo, juegos)
        self._preorder(nodo._derecho, juegos)

    def recorrido_postorder(self):
        juegos = []
        self._postorder(self._raiz, juegos)
        return juegos

    def _postorder(self, nodo, juegos):
        if nodo is None:
            return
        self._postorder(nodo._izquierdo, juegos)
        self._postorder(nodo._derecho, juegos)
        juegos.append(nodo._juego)