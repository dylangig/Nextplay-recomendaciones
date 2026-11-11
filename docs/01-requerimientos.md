# 01 — Requerimientos del sistema

> **Proyecto:** NextPlay — Sistema de recomendación de videojuegos
> **Versión de referencia:** v4 (TP6) · Documento vivo, se actualiza con cada etapa.

## 1. Requerimientos funcionales

### Catálogo y búsqueda

| Código | Requerimiento |
|---|---|
| **RF01** | El sistema debe poder **buscar un videojuego por título** (búsqueda lineal sobre la lista y búsqueda sobre el árbol AVL, mostrando la cantidad de comparaciones realizadas). |
| **RF02** | El sistema debe poder **filtrar videojuegos por género**. |
| **RF03** | El sistema debe **listar todos los videojuegos** del catálogo y mostrarlos en **orden alfabético** (recorrido inorden del AVL). |
| **RF04** | El sistema debe permitir **agregar y eliminar videojuegos** (alta/baja), manteniendo sincronizados la lista del catálogo y el árbol AVL. |
| **RF05** | El sistema debe **cargar los datos desde un archivo JSON** (`datos/juegos.json`) y **exportar el catálogo** a otro archivo JSON (en preorden). |

### Jerarquía de categorías (árbol general)

| Código | Requerimiento |
|---|---|
| **RF06** | El sistema debe presentar la **jerarquía de categorías** del dominio (Videojuegos → géneros → subgéneros) como un árbol visual, con la **cantidad de juegos** del catálogo en cada categoría. |
| **RF07** | El sistema debe permitir **buscar una categoría** y mostrar su **ruta completa desde la raíz** (ej. `Videojuegos > Aventura > Metroidvania`), sin distinguir mayúsculas/minúsculas. |
| **RF08** | El sistema debe listar **los juegos que pertenecen a una categoría** (incluyendo sus subcategorías). |
| **RF09** | El sistema debe exponer los **recorridos del árbol general**: por niveles (BFS) y preorden (DFS). |

### Ranking y prioridades (heap)

| Código | Requerimiento |
|---|---|
| **RF10** | El sistema debe mostrar el **Top-N de juegos mejor evaluados** (prioridad = rating), en orden descendente, con medallas para los primeros puestos. |
| **RF11** | El ranking debe calcularse con una **heap binaria implementada por el equipo** (sin `heapq`), sin ordenar el catálogo completo. |

### Relaciones entre juegos (grafo) — TP7

| Código | Requerimiento |
|---|---|
| **RF12** | El sistema debe modelar **relaciones entre juegos** en un grafo: dos juegos están conectados si comparten género o comparten estudio. |
| **RF13** | El sistema debe permitir consultar los **juegos relacionados** a uno dado (ordenados por afinidad). |

### Exploración de la red (BFS / DFS) — TP8

| Código | Requerimiento |
|---|---|
| **RF14** | El sistema debe poder responder **¿cuál es el juego relacionado más cercano a X?** usando **BFS** (camino con menos aristas; empate resuelto por mayor rating). |
| **RF15** | El sistema debe poder **explorar en profundidad** toda la red conectada con un juego usando **DFS**. |

### Transversal

| Código | Requerimiento |
|---|---|
| **RF16** | Toda la interacción se realiza por **interfaz de terminal** (menú numerado). |
| **RF17** | El sistema debe conservar **todas las funcionalidades** de etapas anteriores (cada TP se suma al anterior). |

## 2. Requerimientos no funcionales

| Código | Requerimiento |
|---|---|
| **RNF01** | La búsqueda por título sobre el árbol AVL debe resolverse en **O(log n) en el peor caso** (garantía de balance AVL). |
| **RNF02** | El sistema debe soportar **al menos 1.000 elementos** sin degradación perceptible; el benchmark mide hasta 1.000.000. |
| **RNF03** | El Top-N debe costar **O(K + n log K)** (heapify + extracciones), evitando el O(K log K) de ordenar el dataset completo. |
| **RNF04** | Sin dependencias externas: **Python 3.8+ y solo librería estándar** (`json` para datos sí; prohibido `heapq` y librerías de grafos). |
| **RNF05** | Manejo de **casos borde**: operaciones sobre estructuras vacías con mensajes claros (`IndexError` controlado, entradas inválidas informadas). |
| **RNF06** | **Toda estructura incorporada debe tener utilidad real** en el sistema (nada de estructuras de juguete). |
| **RNF07** | El código debe estar **organizado por capas** (`modelos/`, `algoritmos/`, `estructuras/`, `servicios/`, `ui/`, `tests/`, `docs/`), documentado y con pruebas unitarias. |
| **RNF08** | El `main` del repositorio debe mantenerse **siempre en un estado funcional**; el trabajo se integra mediante branches + pull requests. |

## 3. Alcance

**Dentro del alcance:**
- Catálogo de videojuegos con datos reales (100 títulos) + generación sintética para benchmarks.
- Búsqueda, filtrado, alta/baja, jerarquía de categorías, ranking Top-N, relaciones entre juegos y exploración BFS/DFS.
- Interfaz de terminal, documentación completa y pruebas automatizadas.

**Fuera de alcance (explícito):**
- **No** se implementa autenticación de usuarios ni perfiles.
- **No** hay interfaz gráfica (solo terminal).
- **No** se integra Telegram (opcional de la cátedra).
- **No** se implementan caminos mínimos (Dijkstra): la entrega TP9 fue eliminada por la cátedra; el grafo se diseña pesado como preparación por si se solicita en la defensa.
- **No** hay persistencia de datos entre ejecuciones (la exportación JSON es manual).
- **No** se usan servicios externos ni bases de datos.
