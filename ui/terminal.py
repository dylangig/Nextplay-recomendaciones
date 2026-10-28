import json
from pathlib import Path

from algoritmos.arbol_avl import ArbolAVL
from algoritmos.arbol_general import arbol_por_defecto
from modelos.videojuego import Videojuego

RUTA_GUARDADO = Path(__file__).resolve().parent.parent / "datos" / "juegos_preorden.json"


class SistemaUI:
    def __init__(self, catalogo):
        self._catalogo = catalogo
        self._arbol = None
        self._arbol_general = None

    def _obtener_arbol(self):
        if self._arbol is None:
            self._arbol = ArbolAVL()
            self._arbol.construir(self._catalogo.listar_todos())
        return self._arbol

    def _obtener_arbol_general(self):
        if self._arbol_general is None:
            self._arbol_general = arbol_por_defecto()
        return self._arbol_general

    def _juegos_de_categoria(self, categoria):
        """Juegos del catálogo cuyo género está en la categoría o sus subcategorías."""
        arbol = self._obtener_arbol_general()
        generos = {g.casefold() for g in arbol.nombres_en_subarbol(categoria)}
        return [
            j for j in self._catalogo.listar_todos()
            if j.get_genero().casefold() in generos
        ]

    def _explorar_categorias(self):
        arbol = self._obtener_arbol_general()
        while True:
            print("\n         EXPLORAR CATEGORÍAS")
            print("1. Ver jerarquía completa (con cantidad de juegos)")
            print("2. Buscar categoría (muestra la ruta)")
            print("3. Recorrido por niveles (BFS)")
            print("4. Recorrido preorden (DFS)")
            print("5. Ver juegos de una categoría")
            print("0. Volver al menú principal")
            subopcion = input("Opción: ")

            if subopcion == '1':
                print("\n Jerarquía de categorías (juegos del catálogo entre paréntesis):")
                print(arbol.dibujar(
                    sufijo=lambda nombre: f" ({len(self._juegos_de_categoria(nombre))} juegos)"
                ))
                print()

            elif subopcion == '2':
                categoria = input("> Categoría a buscar: ").strip()
                ruta = arbol.buscar_ruta(categoria)
                if ruta:
                    print(f"\n Ruta: {' > '.join(ruta)}\n")
                else:
                    print(f"\n La categoría '{categoria}' no existe.\n")

            elif subopcion == '3':
                print("\n Recorrido por niveles (BFS):")
                print(" → ".join(arbol.recorrido_por_niveles()))
                print()

            elif subopcion == '4':
                print("\n Recorrido preorden (DFS):")
                print(" → ".join(arbol.recorrido_preorden()))
                print()

            elif subopcion == '5':
                categoria = input("> Categoría: ").strip()
                try:
                    juegos = self._juegos_de_categoria(categoria)
                except ValueError:
                    print(f"\n La categoría '{categoria}' no existe.\n")
                    continue
                if juegos:
                    ruta = " > ".join(arbol.buscar_ruta(categoria))
                    print(f"\n Juegos en '{ruta}' ({len(juegos)}):")
                    for j in juegos:
                        print(f" - {j}")
                    print()
                else:
                    print(f"\n No hay juegos en '{categoria}'.\n")

            elif subopcion == '0':
                break
            else:
                print("\n Opción no válida.\n")

    def mostrar_menu(self):
        print("         NEXTPLAY — TERMINAL          ")
        print("1. Buscar videojuego por título")
        print("2. Filtrar videojuegos por género")
        print("3. Listar todos los videojuegos")
        print("4. Buscar por título (árbol AVL)")
        print("5. Listar en orden alfabético (recorrido inorden)")
        print("6. Agregar videojuego")
        print("7. Eliminar videojuego")
        print("8. Guardar catálogo a archivo (preorden)")
        print("9. Vaciar catálogo")
        print("10. Explorar categorías (árbol general)")
        print("0. Salir")

    def iniciar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Opción: ")

            if opcion == '1':
                titulo = input("> Ingresá el título a buscar: ")
                resultado = self._catalogo.buscar_por_titulo(titulo)
                if resultado:
                    print(f"\n Juego encontrado: {resultado}\n")
                else:
                    print("\n Juego no encontrado.\n")

            elif opcion == '2':
                genero = input("> Ingresá el género (ej. Metroidvania, Roguelike): ")
                resultados = self._catalogo.filtrar_por_genero(genero)
                if resultados:
                    print(f"\n Juegos del género '{genero}':")
                    for j in resultados:
                        print(f" - {j}")
                    print()
                else:
                    print("\n No hay juegos de ese género.\n")

            elif opcion == '3':
                print("\n Catálogo completo:")
                for j in self._catalogo.listar_todos():
                    print(f" - {j}")
                print()

            elif opcion == '4':
                arbol = self._obtener_arbol()
                titulo = input("> Ingresá el título a buscar: ")
                resultado, comparaciones = arbol.buscar_con_comparaciones(titulo)
                if resultado:
                    print(f"\n Juego encontrado: {resultado}")
                    print(f" Comparaciones realizadas: {comparaciones}\n")
                else:
                    print(f"\n Juego no encontrado ({comparaciones} comparaciones).\n")

            elif opcion == '5':
                arbol = self._obtener_arbol()
                print("\n Catálogo en orden alfabético:")
                for j in arbol.recorrido_inorder():
                    print(f" - {j}")
                print()

            elif opcion == '6':
                titulo = input("> Título: ")
                if self._catalogo.buscar_por_titulo(titulo):
                    print("\n Ya existe un juego con ese título.\n")
                else:
                    genero = input("> Género: ")
                    estudio = input("> Estudio: ")
                    try:
                        rating = float(input("> Rating (5.0 - 10.0): "))
                    except ValueError:
                        print("\n Rating inválido; se usa 0.0.\n")
                        rating = 0.0
                    juego = Videojuego(titulo, genero, estudio, rating)
                    self._catalogo.agregar_juego(juego)
                    self._obtener_arbol().insertar(juego)
                    print(f"\n '{titulo}' agregado al catálogo.\n")

            elif opcion == '7':
                titulo = input("> Título a eliminar: ")
                arbol = self._obtener_arbol()
                eliminado = self._catalogo.eliminar_por_titulo(titulo)
                if eliminado:
                    arbol.eliminar(titulo)
                    print(f"\n '{titulo}' eliminado del catálogo.\n")
                else:
                    print("\n Juego no encontrado.\n")

            elif opcion == '8':
                arbol = self._obtener_arbol()
                ruta = input(f"> Archivo de salida (Enter para '{RUTA_GUARDADO.name}'): ").strip()
                ruta = ruta or str(RUTA_GUARDADO)
                juegos = []
                for juego in arbol.recorrido_preorder():
                    juegos.append({
                        "titulo": juego.get_titulo(),
                        "genero": juego.get_genero(),
                        "estudio": juego.get_estudio(),
                        "rating": juego.get_rating(),
                    })
                with open(ruta, 'w', encoding='utf-8') as archivo:
                    json.dump(juegos, archivo, ensure_ascii=False, indent=4)
                print(f"\n Catálogo guardado (preorden) en {ruta}.\n")

            elif opcion == '9':
                confirmar = input("> ¿Eliminar TODOS los juegos? (s/N): ").strip().lower()
                if confirmar == 's':
                    self._catalogo.listar_todos().clear()
                    self._arbol = None
                    print("\n Catálogo vaciado.\n")
                else:
                    print("\n Operación cancelada.\n")

            elif opcion == '10':
                self._explorar_categorias()

            elif opcion == '0':
                print("\nSaliendo de NextPlay... ¡Hasta luego!")
                break
            else:
                print("\n Opción no válida. Intentá de nuevo.\n")
