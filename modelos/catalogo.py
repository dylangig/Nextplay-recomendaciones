import json

from modelos.videojuego import Videojuego


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