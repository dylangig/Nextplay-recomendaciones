import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from modelos.catalogo import Catalogo
from ui.terminal import SistemaUI

RUTA_DATOS = Path(__file__).resolve().parent / "datos" / "juegos.json"


def main():
    mi_catalogo = Catalogo()
    mi_catalogo.cargar_desde_json(RUTA_DATOS)

    app = SistemaUI(mi_catalogo)
    app.iniciar()


if __name__ == "__main__":
    main()