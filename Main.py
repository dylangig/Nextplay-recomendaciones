import json
import sys

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



if __name__ == "__main__":
    mi_catalogo = Catalogo()
    mi_catalogo.cargar_desde_json('juegos.json')

    app = SistemaUI(mi_catalogo)
    app.iniciar()