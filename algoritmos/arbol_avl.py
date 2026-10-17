class NodoAVL:
    def __init__(self, juego):
        self._juego = juego
        self._clave = juego.get_titulo().lower()
        self._izquierdo = None
        self._derecho = None
        self._altura = 0


class ArbolAVL:
    def __init__(self):
        self._raiz = None

    def construir(self, catalogo):
        for juego in catalogo:
            self.insertar(juego)

    def insertar(self, juego):
        self._raiz = self._insertar_nodo(self._raiz, juego)

    def _insertar_nodo(self, nodo, juego):
        if nodo is None:
            return NodoAVL(juego)
        clave = juego.get_titulo().lower()
        if clave < nodo._clave:
            nodo._izquierdo = self._insertar_nodo(nodo._izquierdo, juego)
        elif clave > nodo._clave:
            nodo._derecho = self._insertar_nodo(nodo._derecho, juego)
        else:
            return nodo
        return self._rebalancear(nodo)

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

    def buscar_con_comparaciones(self, titulo):
        clave = titulo.lower()
        comparaciones = 0
        actual = self._raiz
        while actual is not None:
            comparaciones += 1
            if clave == actual._clave:
                return actual._juego, comparaciones
            elif clave < actual._clave:
                actual = actual._izquierdo
            else:
                actual = actual._derecho
        return None, comparaciones

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
        return self._rebalancear(nodo)

    def _minimo(self, nodo):
        while nodo._izquierdo is not None:
            nodo = nodo._izquierdo
        return nodo

    def _altura_nodo(self, nodo):
        if nodo is None:
            return -1
        return nodo._altura

    def _factor_balance(self, nodo):
        return self._altura_nodo(nodo._derecho) - self._altura_nodo(nodo._izquierdo)

    def _actualizar_altura(self, nodo):
        nodo._altura = 1 + max(self._altura_nodo(nodo._izquierdo), self._altura_nodo(nodo._derecho))

    def _rebalancear(self, nodo):
        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)
        if balance > 1:
            if self._factor_balance(nodo._derecho) < 0:
                nodo._derecho = self._rotar_derecha(nodo._derecho)
            return self._rotar_izquierda(nodo)
        if balance < -1:
            if self._factor_balance(nodo._izquierdo) > 0:
                nodo._izquierdo = self._rotar_izquierda(nodo._izquierdo)
            return self._rotar_derecha(nodo)
        return nodo

    def _rotar_izquierda(self, nodo):
        pivote = nodo._derecho
        nodo._derecho = pivote._izquierdo
        pivote._izquierdo = nodo
        self._actualizar_altura(nodo)
        self._actualizar_altura(pivote)
        return pivote

    def _rotar_derecha(self, nodo):
        pivote = nodo._izquierdo
        nodo._izquierdo = pivote._derecho
        pivote._derecho = nodo
        self._actualizar_altura(nodo)
        self._actualizar_altura(pivote)
        return pivote

    def altura(self):
        return self._altura_nodo(self._raiz)

    def vaciar(self):
        self._raiz = None

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
