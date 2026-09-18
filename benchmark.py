import csv
import gc
import math
import sys
import time
from statistics import median

from estrategias import busqueda_binaria, busqueda_lineal, preparar_indice_binario
from generar_datos import generar_catalogo

TAMANOS = [100, 1000, 10000, 100000, 1000000]
PRESUPUESTO = 1_000_000
REPETICIONES = 5
TITULO_INEXISTENTE = "zzzzzz_inexistente"


def tiempo_lote(funcion, argumentos, consultas):
    gc.disable()
    inicio = time.perf_counter()
    for _ in range(consultas):
        funcion(*argumentos)
    total = time.perf_counter() - inicio
    gc.enable()
    return total / consultas


def medir(funcion, argumentos, costo_estimado):
    consultas = max(1, int(PRESUPUESTO // max(1, costo_estimado)))
    muestras = [tiempo_lote(funcion, argumentos, consultas) for _ in range(REPETICIONES)]
    return median(muestras)


def ejecutar(tamano):
    catalogo = generar_catalogo(tamano)
    titulos = [juego.get_titulo() for juego in catalogo]
    catalogo_ordenado, titulos_ordenados = preparar_indice_binario(catalogo)
    log_n = max(1, math.log2(tamano))

    t_lineal_mejor = medir(busqueda_lineal, (catalogo, titulos[0]), 1)
    t_lineal_promedio = medir(busqueda_lineal, (catalogo, titulos[tamano // 2]), tamano // 2)
    t_lineal_peor = medir(busqueda_lineal, (catalogo, titulos[-1]), tamano)
    t_lineal_ausente = medir(busqueda_lineal, (catalogo, TITULO_INEXISTENTE), tamano)

    t_binaria = medir(busqueda_binaria, (catalogo_ordenado, titulos_ordenados, titulos_ordenados[tamano // 2]), log_n)

    gc.disable()
    inicio = time.perf_counter()
    preparar_indice_binario(catalogo)
    t_ordenamiento = time.perf_counter() - inicio
    gc.enable()

    return {
        "tamano": tamano,
        "lineal_mejor": t_lineal_mejor,
        "lineal_promedio": t_lineal_promedio,
        "lineal_peor": t_lineal_peor,
        "lineal_ausente": t_lineal_ausente,
        "binaria": t_binaria,
        "ordenamiento": t_ordenamiento,
    }


def mostrar(registros):
    encabezado = ["tamano", "lineal_mejor", "lineal_promedio", "lineal_peor", "lineal_ausente", "binaria", "ordenamiento"]
    print(f"\n{'tamano':>12} {'lineal_mejor':>14} {'lineal_promedio':>15} {'lineal_peor':>13} {'lineal_ausente':>15} {'binaria':>12} {'ordenamiento':>14}")
    for registro in registros:
        fila = " ".join(f"{registro[clave]:>15.6f}" if clave != "tamano" else f"{registro[clave]:>12}" for clave in encabezado)
        print(fila)
    print()


def guardar_csv(registros, ruta):
    claves = ["tamano", "lineal_mejor", "lineal_promedio", "lineal_peor", "lineal_ausente", "binaria", "ordenamiento"]
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=claves)
        escritor.writeheader()
        escritor.writerows(registros)
    print(f"Resultados guardados en {ruta}")


def main():
    tamanos = [int(t) for t in sys.argv[1:]] or TAMANOS
    registros = [ejecutar(tamano) for tamano in tamanos]
    mostrar(registros)
    guardar_csv(registros, "resultados.csv")


if __name__ == "__main__":
    main()