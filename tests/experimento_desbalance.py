import gc
import json
import math
import random
import sys
import time
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algoritmos.arbol import ArbolBinario
from algoritmos.arbol_avl import ArbolAVL
from modelos.videojuego import Videojuego

TAMANOS = [100, 1000, 10000]
ESCENARIOS = ["ordenado", "inverso", "aleatorio"]
REPETICIONES_CONSTRUCCION = 5
PRESUPUESTO = 1_000_000
TITULO_INEXISTENTE = "zzzzzzzz_mayor_que_todos"
TITULO_INEXISTENTE_MIN = "00000000_menor_que_todos"
PROBAS = [TITULO_INEXISTENTE, TITULO_INEXISTENTE_MIN]
RUTA_DATOS = Path(__file__).resolve().parent.parent / "datos" / "juegos.json"
ESTRUCTURAS = [("BST", ArbolBinario), ("AVL", ArbolAVL)]


def catalogo_sintetico(tamano, escenario):
    titulos = []
    for i in range(tamano):
        titulos.append(f"Juego_{i:06d}")
    if escenario == "inverso":
        titulos.reverse()
    elif escenario == "aleatorio":
        random.Random(42).shuffle(titulos)

    juegos = []
    for titulo in titulos:
        juegos.append(Videojuego(titulo, "Genero", "Estudio", 5.0))
    return juegos


def medir_construccion(clase, juegos):
    muestras = []
    for _ in range(REPETICIONES_CONSTRUCCION):
        gc.disable()
        inicio = time.perf_counter()
        arbol = clase()
        arbol.construir(juegos)
        muestras.append(time.perf_counter() - inicio)
        gc.enable()
    return median(muestras)


def medir_busqueda(arbol, costo_estimado, titulo):
    consultas = max(1, int(PRESUPUESTO // max(1, costo_estimado)))
    gc.disable()
    inicio = time.perf_counter()
    for _ in range(consultas):
        arbol.buscar_con_comparaciones(titulo)
    total = time.perf_counter() - inicio
    gc.enable()
    return total / consultas


def muestra_titulos(juegos, cantidad=200):
    paso = max(1, len(juegos) // cantidad)
    titulos = []
    for juego in juegos[::paso][:cantidad]:
        titulos.append(juego.get_titulo())
    return titulos


def evaluar(clase, juegos, muestra):
    arbol = clase()
    arbol.construir(juegos)

    peor = 0
    for titulo in PROBAS:
        _, comparaciones = arbol.buscar_con_comparaciones(titulo)
        if comparaciones > peor:
            peor = comparaciones

    total = 0
    for titulo in muestra:
        _, comparaciones = arbol.buscar_con_comparaciones(titulo)
        total += comparaciones

    tiempo_busqueda = 0
    for titulo in PROBAS:
        tiempo = medir_busqueda(arbol, arbol.altura(), titulo)
        if tiempo > tiempo_busqueda:
            tiempo_busqueda = tiempo

    return {
        "altura": arbol.altura(),
        "altura_minima": int(math.floor(math.log2(len(juegos)))),
        "comparaciones_peor": peor,
        "comparaciones_promedio": total / len(muestra),
        "tiempo_construccion": medir_construccion(clase, juegos),
        "tiempo_busqueda": tiempo_busqueda,
    }


def ejecutar_escenario(tamano, escenario):
    juegos = catalogo_sintetico(tamano, escenario)
    muestra = muestra_titulos(juegos)
    filas = []
    for nombre, clase in ESTRUCTURAS:
        resultado = evaluar(clase, juegos, muestra)
        resultado.update({"escenario": escenario, "tamano": tamano, "estructura": nombre})
        filas.append(resultado)
    return filas


def ejecutar_reales():
    with open(RUTA_DATOS, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    juegos = []
    for item in datos:
        juegos.append(Videojuego(item["titulo"], item["genero"], item["estudio"], item["rating"]))

    desplazado = list(juegos)
    random.Random(7).shuffle(desplazado)

    def clave_titulo(juego):
        return juego.get_titulo().lower()

    ordenado = sorted(juegos, key=clave_titulo)

    conjuntos = [
        ("reales_ordenado", ordenado),
        ("reales_desordenado", desplazado),
    ]

    filas = []
    for nombre_orden, conjunto in conjuntos:
        muestra = muestra_titulos(conjunto)
        for nombre, clase in ESTRUCTURAS:
            resultado = evaluar(clase, conjunto, muestra)
            resultado.update({"escenario": nombre_orden, "tamano": len(conjunto), "estructura": nombre})
            filas.append(resultado)
    return filas


def mostrar(filas):
    encabezado = f"{'escenario':>20} {'n':>7} {'estructura':>11} {'altura':>7} {'alt.min':>8} {'cmp.peor':>9} {'cmp.prom':>9} {'t.constr':>10} {'t.busq':>10}"
    print("\n" + encabezado)
    print("-" * len(encabezado))
    for fila in filas:
        print(
            f"{fila['escenario']:>20} {fila['tamano']:>7} {fila['estructura']:>11} "
            f"{fila['altura']:>7} {fila['altura_minima']:>8} "
            f"{fila['comparaciones_peor']:>9} {fila['comparaciones_promedio']:>9.1f} "
            f"{fila['tiempo_construccion']:>10.6f} {fila['tiempo_busqueda']:>10.6f}"
        )
    print()


def main():
    tamanos = []
    for argumento in sys.argv[1:]:
        tamanos.append(int(argumento))
    if not tamanos:
        tamanos = TAMANOS

    filas = []
    for escenario in ESCENARIOS:
        for tamano in tamanos:
            filas.extend(ejecutar_escenario(tamano, escenario))
    filas.extend(ejecutar_reales())
    mostrar(filas)


if __name__ == "__main__":
    main()
