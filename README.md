# NextPlay -- Sistema de Recomendacion de Videojuegos

> Trabajo Practico Integrador -- Estructuras de Datos (UNaB)
> Aplicacion de consola para la busqueda, filtrado y recomendacion eficiente de videojuegos utilizando estructuras de datos avanzadas.
>
> Version del entregable: **v3 (TP5 -- Arbol general)**

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

5. Ejecutar los tests unitarios del arbol general:
   ```bash
   python -m unittest tests.test_arbol_general -v
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
│   └── generar_datos.py    # generacion de catalogos sinteticos para benchmarking
├── ui/
│   └── terminal.py         # interfaz por consola
├── datos/
│   └── juegos.json         # catalogo de videojuegos
├── tests/
│   ├── benchmark.py            # benchmark de las estrategias de busqueda
│   ├── experimento_desbalance.py  # experimento BST vs. AVL
│   └── test_arbol_general.py   # tests unitarios del arbol general
├── docs/
│   └── Informe.md          # analisis de complejidad y resultados
├── main.py                 # punto de entrada
└── README.md
```

---

### Estado actual :
TP 1 - Objetos y clases: Modelo e interfaz inicial.
TP 2 - Estrategias de busqueda: lineal vs binaria con benchmark e informe.
TP 3 - Implemetancion de Arbol de busqueda
TP 4 - Arbol AVL: rotaciones, balanceo y experimento de desbalance.
TP 5 - Arbol general (n-ario): jerarquia de generos, recorridos y explorador de categorias en terminal (version 3).
