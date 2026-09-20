import json
import os
import sys

from arbol import ArbolBinario
from estrategias import busqueda_binaria, preparar_indice_binario

sys.stdout.reconfigure(encoding='utf-8')

#Clases 

class Videojuego:
    def __init__(self, titulo, genero, estudio, rating):
        self._titulo = titulo
        self._genero = genero
        self._estudio = estudio
        self._rating = rating

    def get_titulo(self):
        return self._titulo
        
    def get_genero(self):
        return self._genero
        
    def get_rating(self):
        return self._rating

    def __repr__(self):
        return f"{self._titulo} ({self._genero}) - Estudio: {self._estudio}  {self._rating}"


class Catalogo:
    def __init__(self):
        self._juegos = []

    def cargar_desde_json(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                for item in datos:
                    juego = Videojuego(item['titulo'], item['genero'], item['estudio'], item['rating'])
                    self._juegos.append(juego)
            print(f" Se cargaron {len(self._juegos)} juegos exitosamente.\n")
        except FileNotFoundError:
            print(f" Error: No se encontró el archivo {ruta_archivo}")


    def buscar_por_titulo(self, titulo_buscado):
        for juego in self._juegos:
            if juego.get_titulo().lower() == titulo_buscado.lower():
                return juego
        return None

    def agregar_juego(self, juego):
        self._juegos.append(juego)

    def eliminar_por_titulo(self, titulo):
        for i, juego in enumerate(self._juegos):
            if juego.get_titulo().lower() == titulo.lower():
                del self._juegos[i]
                return juego
        return None

    def listar_todos(self):
        return self._juegos

    def filtrar_por_genero(self, genero_buscado):
        resultados = []
        for juego in self._juegos:
            if juego.get_genero().lower() == genero_buscado.lower():
                resultados.append(juego)
        return resultados


#Interfaz por terminal

class SistemaUI:
    def __init__(self, catalogo):
        self._catalogo = catalogo
        self._catalogo_ordenado = None
        self._titulos_ordenados = None
        self._arbol = None

    def _obtener_arbol(self):
        if self._arbol is None:
            self._arbol = ArbolBinario()
            self._arbol.construir(self._catalogo.listar_todos())
        return self._arbol

    def mostrar_menu(self):
        print("         NEXTPLAY — TERMINAL          ")
        print("1. Buscar videojuego por título (secuencial)")
        print("2. Filtrar videojuegos por género")
        print("3. Listar todos los videojuegos")
        print("4. Buscar por título (búsqueda binaria)")
        print("5. Buscar por título (árbol binario)")
        print("6. Listar en orden alfabético (recorrido inorden)")
        print("7. Agregar videojuego")
        print("8. Eliminar videojuego")
        print("9. Guardar catálogo a archivo")
        print("10. Vaciar catálogo")
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
                if self._titulos_ordenados is None:
                    self._catalogo_ordenado, self._titulos_ordenados = preparar_indice_binario(self._catalogo.listar_todos())
                titulo = input("> Ingresá el título a buscar: ")
                resultado = busqueda_binaria(self._catalogo_ordenado, self._titulos_ordenados, titulo)
                if resultado:
                    print(f"\n Juego encontrado: {resultado}\n")
                else:
                    print("\n Juego no encontrado.\n")

            elif opcion == '5':
                arbol = self._obtener_arbol()
                titulo = input("> Ingresá el título a buscar: ")
                resultado = arbol.buscar(titulo)
                if resultado:
                    print(f"\n Juego encontrado: {resultado}\n")
                else:
                    print("\n Juego no encontrado.\n")

            elif opcion == '6':
                arbol = self._obtener_arbol()
                print("\n Catálogo en orden alfabético:")
                for j in arbol.recorrido_inorder():
                    print(f" - {j}")
                print()

            elif opcion == '7':
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

            elif opcion == '8':
                titulo = input("> Título a eliminar: ")
                arbol = self._obtener_arbol()
                eliminado = self._catalogo.eliminar_por_titulo(titulo)
                if eliminado:
                    arbol.eliminar(titulo)
                    print(f"\n '{titulo}' eliminado del catálogo.\n")
                else:
                    print("\n Juego no encontrado.\n")

            elif opcion == '9':
                arbol = self._obtener_arbol()
                ruta = input("> Archivo de salida (Enter para 'juegos_preorden.json'): ").strip()
                ruta = ruta or 'juegos_preorden.json'
                juegos = [{
                    "titulo": j.get_titulo(),
                    "genero": j.get_genero(),
                    "estudio": j._estudio,
                    "rating": j.get_rating(),
                } for j in arbol.recorrido_preorder()]
                with open(ruta, 'w', encoding='utf-8') as archivo:
                    json.dump(juegos, archivo, ensure_ascii=False, indent=4)
                print(f"\n Catálogo guardado (preorden) en {ruta}.\n")

            elif opcion == '10':
                arbol = self._obtener_arbol()
                confirmar = input("> ¿Eliminar TODOS los juegos? (s/N): ").strip().lower()
                if confirmar == 's':
                    for j in arbol.recorrido_postorder():
                        self._catalogo.eliminar_por_titulo(j.get_titulo())
                    arbol.vaciar()
                    self._arbol = None
                    print("\n Catálogo vaciado.\n")
                else:
                    print("\n Operación cancelada.\n")

            elif opcion == '0':
                print("\nSaliendo de NextPlay... ¡Hasta luego!")
                break
            else:
                print("\n Opción no válida. Intentá de nuevo.\n")



if __name__ == "__main__":
    mi_catalogo = Catalogo()
    ruta_catalogo = 'juegos.json' if os.path.exists('juegos.json') else 'Juegos.json'
    mi_catalogo.cargar_desde_json(ruta_catalogo)

    app = SistemaUI(mi_catalogo)
    app.iniciar()