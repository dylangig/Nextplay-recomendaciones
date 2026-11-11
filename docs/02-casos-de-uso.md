# 02 — Casos de uso

> Actor principal: **Usuario** (persona usando la terminal de NextPlay).
> Diagrama en notación UML informal (draw.io / Excalidraw / ASCII).

## 1. Diagrama de casos de uso

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         NEXTPLAY (sistema)                              │
│                                                                          │
│   ┌─────────────────────┐        ┌──────────────────────────┐           │
│   │ Buscar videojuego   │        │ Ver Top N (heap)         │           │
│   │ (lineal / AVL)      │        └──────────────────────────┘           │
│   └─────────────────────┘        ┌──────────────────────────┐           │
│   ┌─────────────────────┐        │ Explorar categorías      │           │
│   │ Filtrar por género  │        │  (árbol general)         │           │
│   └─────────────────────┘        └──────────────────────────┘           │
│   ┌─────────────────────┐        ┌──────────────────────────┐           │
│   │ Listar / orden      │        │ Buscar categoría (ruta)  │           │
│   │ alfabético (AVL)    │        └──────────────────────────┘           │
│   └─────────────────────┘        ┌──────────────────────────┐           │
│   ┌─────────────────────┐        │ Ver juegos relacionados  │           │
│   │ Agregar / eliminar  │        │ (grafo)                  │           │
│   └─────────────────────┘        └──────────────────────────┘           │
│   ┌─────────────────────┐        ┌──────────────────────────┐           │
│   │ Exportar catálogo   │        │ Cercano (BFS) /          │           │
│   │ (preorden)          │        │ explorar red (DFS)       │           │
│   └─────────────────────┘        └──────────────────────────┘           │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                 ▲
                 │  usa
            ┌─────────┐
            │ Usuario │
            └─────────┘
```

## 2. Descripción de casos de uso

### CU01 — Buscar videojuego por título

| | |
|---|---|
| **Actor** | Usuario |
| **Precondición** | El catálogo está cargado desde `datos/juegos.json` |
| **Flujo principal** | 1. El usuario elige la opción de búsqueda. 2. El sistema solicita el título. 3. El usuario ingresa el título. 4. El sistema busca (lineal o sobre el AVL) y muestra el juego con su género, estudio y rating. |
| **Flujo alternativo** | Si no se encuentra, el sistema informa "Juego no encontrado" (en el AVL, junto con las comparaciones realizadas). |
| **Postcondición** | Ninguna (solo lectura). |

### CU02 — Ver Top N mejores evaluados

| | |
|---|---|
| **Actor** | Usuario |
| **Precondición** | El catálogo está cargado y contiene al menos un juego |
| **Flujo principal** | 1. El usuario elige la opción "Top N". 2. El sistema solicita cuántos elementos mostrar (Enter = 10). 3. El usuario ingresa N. 4. El sistema construye la MaxHeap con `heapify` [O(K)] y extrae N elementos [O(log K) c/u]. 5. Muestra el ranking con medallas 🥇🥈🥉 y rating. |
| **Flujo alternativo** | Si N ≤ 0, informa el error. Si el catálogo está vacío, informa que no hay datos. Si N > tamaño del catálogo, muestra todos los disponibles. |

### CU03 — Explorar categorías (árbol general)

| | |
|---|---|
| **Actor** | Usuario |
| **Precondición** | El árbol de jerarquía está construido (`JERARQUIA_GENEROS`) |
| **Flujo principal** | 1. El usuario elige "Explorar categorías". 2. El sistema muestra el submenú. 3. El usuario elige "Ver jerarquía". 4. El sistema dibuja el árbol ASCII con la cantidad de juegos del catálogo en cada categoría. |
| **Flujo alternativo** | También permite: buscar categoría (muestra la ruta raíz → categoría), recorridos BFS/preorden, y listar los juegos de una categoría. Si la categoría no existe, lo informa. |

### CU04 — Buscar categoría y ver su ruta

| | |
|---|---|
| **Actor** | Usuario |
| **Precondición** | El árbol general está construido |
| **Flujo principal** | 1. El usuario elige "Buscar categoría". 2. Ingresa un nombre (ej. `metroidvania`, sin distinguir mayúsculas). 3. El sistema busca con DFS y muestra `Videojuegos > Aventura > Metroidvania`. |
| **Flujo alternativo** | Si no existe, informa "La categoría 'X' no existe". |

### CU05 — Filtrar por género

| | |
|---|---|
| **Actor** | Usuario |
| **Precondición** | El catálogo está cargado |
| **Flujo principal** | 1. El usuario elige "Filtrar por género". 2. Ingresa el género (ej. `Roguelike`). 3. El sistema recorre la lista y muestra los juegos coincidentes. |
| **Flujo alternativo** | Si no hay coincidencias, informa "No hay juegos de ese género". |

### CU06 — Agregar / eliminar videojuego

| | |
|---|---|
| **Actor** | Usuario |
| **Precondición** | El sistema está en el menú principal |
| **Flujo principal (alta)** | 1. Elige "Agregar videojuego". 2. Ingresa título, género, estudio y rating. 3. El sistema valida que el título no exista. 4. Agrega a la lista del catálogo **e inserta en el AVL**. 5. Confirma la alta. |
| **Flujo principal (baja)** | 1. Elige "Eliminar videojuego". 2. Ingresa el título. 3. El sistema elimina de la lista **y del AVL**. 4. Confirma la eliminación. |
| **Flujo alternativo** | Alta con título duplicado o baja con título inexistente: informa y no modifica nada. |

### CU07 — Ver juegos relacionados

| | |
|---|---|
| **Actor** | Usuario |
| **Precondición** | El catálogo está cargado (el grafo se construye en cada consulta) |
| **Flujo principal** | 1. Elige "Juegos relacionados". 2. Ingresa el título de un juego. 3. El sistema construye el grafo, lista sus vértices vecinos (comparten género o estudio) ordenados por afinidad. |
| **Flujo alternativo** | Si el juego no existe o no tiene vecinos, lo informa. |

### CU08 — Consulta BFS / DFS sobre la red

| | |
|---|---|
| **Actor** | Usuario |
| **Precondición** | El catálogo está cargado |
| **Flujo principal (BFS)** | 1. Elige "Juego relacionado más cercano (BFS)". 2. Ingresa un juego. 3. El sistema ejecuta BFS y devuelve el alcanzable más cercano (menos aristas; empate → mayor rating). |
| **Flujo principal (DFS)** | 1. Elige "Explorar toda la red en profundidad (DFS)". 2. Ingresa un juego. 3. El sistema ejecuta DFS y muestra la componente conexa completa en orden de visita. |
| **Flujo alternativo** | Si el juego no tiene conexiones, lo informa. |
