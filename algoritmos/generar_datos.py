import random

from modelos.videojuego import Videojuego

random.seed(42)

GENEROS = ["Metroidvania", "Plataformas", "Roguelike", "Shooter", "RPG", "Estrategia", "Puzzle", "Deportes"]
ESTUDIOS = ["Team Cherry", "Supergiant Games", "Motion Twin", "Moon Studios", "Maddy Makes Games", "Valve", "Bethesda", "Nintendo"]


def generar_catalogo(cantidad):
    juegos = []
    for i in range(cantidad):
        juegos.append(Videojuego(
            titulo=f"Juego_{i:06d}",
            genero=random.choice(GENEROS),
            estudio=random.choice(ESTUDIOS),
            rating=round(random.uniform(5.0, 10.0), 1),
        ))
    random.shuffle(juegos)
    return juegos