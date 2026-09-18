import json
import random

random.seed(42)

GENEROS = ["Metroidvania", "Plataformas", "Roguelike", "Shooter", "RPG", "Estrategia", "Puzzle", "Deportes"]
ESTUDIOS = ["Team Cherry", "Supergiant Games", "Motion Twin", "Moon Studios", "Maddy Makes Games", "Valve", "Bethesda", "Nintendo"]

TAMANOS = [100, 1000, 10000]


def generar_catalogo(cantidad):
    juegos = []
    for i in range(cantidad):
        juegos.append({
            "titulo": f"Juego_{i:06d}",
            "genero": random.choice(GENEROS),
            "estudio": random.choice(ESTUDIOS),
            "rating": round(random.uniform(5.0, 10.0), 1),
        })
    random.shuffle(juegos)
    return juegos


def main():
    for cantidad in TAMANOS:
        ruta = f"datos_{cantidad}.json"
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(generar_catalogo(cantidad), archivo, ensure_ascii=False, indent=2)
        print(f"Generado: {ruta}")


if __name__ == "__main__":
    main()