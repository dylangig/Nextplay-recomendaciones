# NextPlay -- Sistema de Recomendacion de Videojuegos

> Trabajo Practico Integrador -- Estructuras de Datos (UNaB)
> Aplicacion de consola para la busqueda, filtrado y recomendacion eficiente de videojuegos utilizando estructuras de datos avanzadas.

---

## 1. Descripcion del Proyecto

NextPlay es un sistema interactivo por linea de comandos disenado para ayudar a los jugadores a descubrir nuevos videojuegos segun sus gustos, generos preferidos o titulos ya jugados. 

El proyecto resuelve el problema de los jugadores que terminan un videojuego y no saben que comprar o jugar a continuacion sin arriesgarse a gastar dinero en titulos que no encajan con sus preferencias. La aplicacion carga datos reales del dominio de videojuegos e implementa estructuras de datos eficientes para procesar las busquedas y recomendaciones.

---

## 2. Integrantes del Equipo

Dylan Gigena Diaz

Nicolás Costantini

Franco Steg

---

## 3. Instrucciones de Instalacion y Ejecucion

### Requisitos Previos
* Tener instalado Python 3.8 o superior.
* Contar con Git para la clonacion del repositorio.

### Pasos para Ejecutar

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/dylangig/Nextplay-recomendaciones
   cd NextPlay-Recomendaciones
2. Ejecutar la aplicacion desde la terminal:
   ```bash
   python main.py
   ```
   Los datos se cargan desde `datos/juegos.json`.

3. Ejecutar el benchmark de estrategias de busqueda:
   ```bash
   python -m tests.benchmark 100 1000
   ```

---

## 4. Estructura del Proyecto

```
Nextplay-recomendaciones/
├── modelos/
│   ├── videojuego.py       # entidad Videojuego
│   └── catalogo.py         # Catalogo (carga JSON, busqueda y filtros)
├── algoritmos/
│   ├── busqueda.py         # busqueda lineal, binaria y preparacion del indice
│   └── generar_datos.py    # generacion de catalogos sinteticos para benchmarking
├── ui/
│   └── terminal.py         # interfaz por consola
├── datos/
│   └── juegos.json         # catalogo de videojuegos
├── tests/
│   └── benchmark.py        # benchmark de las estrategias de busqueda
├── docs/
│   └── Informe.md          # analisis de complejidad y resultados
├── main.py                 # punto de entrada
└── README.md
```

---

### Estado actual :
TP 1 - Objetos y clases: Modelo e interfaz inicial.
TP 2 - Estrategias de busqueda: lineal vs binaria con benchmark e informe.