def busqueda_lineal(catalogo, titulo):
    titulo = titulo.lower()
    for juego in catalogo:
        if juego.get_titulo().lower() == titulo:
            return juego
    return None


def busqueda_binaria(catalogo_ordenado, titulos_ordenados, titulo):
    titulo = titulo.lower()
    lo = 0
    hi = len(titulos_ordenados) - 1
    while lo <= hi:
        medio = (lo + hi) // 2
        titulo_medio = titulos_ordenados[medio]
        if titulo_medio == titulo:
            return catalogo_ordenado[medio]
        elif titulo_medio < titulo:
            lo = medio + 1
        else:
            hi = medio - 1
    return None


def preparar_indice_binario(catalogo):
    catalogo_ordenado = sorted(catalogo, key=lambda juego: juego.get_titulo().lower())
    titulos_ordenados = [juego.get_titulo().lower() for juego in catalogo_ordenado]
    return catalogo_ordenado, titulos_ordenados