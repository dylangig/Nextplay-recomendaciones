# NextPlay -- Sistema de Recomendacion de Videojuegos

> Trabajo Practico Integrador -- Estructuras de Datos (UNaB)
> Aplicacion de consola para la busqueda, filtrado y recomendacion eficiente de videojuegos utilizando estructuras de datos avanzadas.
>
> Version del entregable: **v5 (TP7 -- Grafo de relaciones)**

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

4. Ejecutar el experimento de desbalance BST vs. AVL:
   ```bash
   python -m tests.experimento_desbalance 100 1000 10000
   ```

5. Ejecutar los tests unitarios (árbol general y heap):
   ```bash
   python -m unittest discover -s tests -v
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
│   ├── arbol.py            # arbol binario de busqueda (BST)
│   ├── arbol_avl.py        # arbol AVL (busqueda con balanceo)
│   ├── arbol_general.py    # arbol general n-ario (jerarquia de categorias)
│   ├── grafo.py            # grafo no dirigido pesado (lista de adyacencia)
│   └── generar_datos.py    # generacion de catalogos sinteticos para benchmarking
├── estructuras/
│   └── heap.py             # MaxHeap manual (sin heapq) para rankings
├── servicios/
│   └── recomendador.py      # logica de negocio: Top-N con heap
├── ui/
│   └── terminal.py         # interfaz por consola
├── datos/
│   └── juegos.json         # catalogo de videojuegos
├── tests/
│   ├── benchmark.py            # benchmark de las estrategias de busqueda
│   ├── experimento_desbalance.py  # experimento BST vs. AVL
│   ├── test_arbol_general.py   # tests unitarios del arbol general
│   ├── test_heap.py            # tests unitarios de la heap y el Top-N
│   └── test_grafo.py           # tests unitarios del grafo y relacionados
├── docs/
│   ├── 01-requerimientos.md    # requerimientos funcionales y no funcionales
│   ├── 02-casos-de-uso.md      # diagrama y descripcion de casos de uso
│   ├── 03-diagrama-clases.md   # clases de dominio, estructuras y relaciones
│   ├── 04-diagrama-datos.md    # conexion entre estructuras (flujo de datos)
│   ├── 05-gestion-proyecto.md  # tablero GitHub Projects y metodologia
│   ├── Informe.md              # analisis de complejidad y resultados (TP2-TP8)
│   └── capturas/               # capturas de pantalla de la demo
├── main.py                 # punto de entrada
└── README.md
```

---

## 5. Documentación

| Documento | Contenido |
|---|---|
| [docs/01-requerimientos.md](docs/01-requerimientos.md) | Requerimientos funcionales (RF) y no funcionales (RNF), alcance |
| [docs/02-casos-de-uso.md](docs/02-casos-de-uso.md) | Diagrama UML y descripción de los casos de uso |
| [docs/03-diagrama-clases.md](docs/03-diagrama-clases.md) | Clases de dominio y estructuras, con relaciones |
| [docs/04-diagrama-datos.md](docs/04-diagrama-datos.md) | Conexión entre estructuras (flujo de datos) |
| [docs/05-gestion-proyecto.md](docs/05-gestion-proyecto.md) | Tablero, sprints e historias de usuario |
| [docs/Informe.md](docs/Informe.md) | Análisis de complejidad, benchmarks y experimentos |

---

### Estado actual :
TP 1 - Objetos y clases: Modelo e interfaz inicial.
TP 2 - Estrategias de busqueda: lineal vs binaria con benchmark e informe.
TP 3 - Implemetancion de Arbol de busqueda
TP 4 - Arbol AVL: rotaciones, balanceo y experimento de desbalance.
TP 5 - Arbol general (n-ario): jerarquia de generos, recorridos y explorador de categorias en terminal (version 3).
TP 6 - Heap (cola de prioridad): MaxHeap manual, ranking Top-N por rating con el servicio Recomendador (version 4).
TP 7 - Grafo de relaciones: no dirigido y pesado (comparten genero o estudio), lista de adyacencia, consulta de juegos relacionados (version 5).
