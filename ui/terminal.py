class SistemaUI:
    def __init__(self, catalogo):
        self._catalogo = catalogo

    def mostrar_menu(self):
        print("         NEXTPLAY — TERMINAL          ")
        print("1. Buscar videojuego por título")
        print("2. Filtrar videojuegos por género")
        print("3. Listar todos los videojuegos")
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

            elif opcion == '0':
                print("\nSaliendo de NextPlay... ¡Hasta luego!")
                break
            else:
                print("\n Opción no válida. Intentá de nuevo.\n")