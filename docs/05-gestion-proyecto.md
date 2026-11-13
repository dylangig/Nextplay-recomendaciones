# 05 — Gestión de proyecto

## 1. Metodología

Trabajamos con un **Scrum simplificado** adaptado al calendario de la cátedra:

| Elemento | Cómo lo aplicamos |
|---|---|
| **Sprint** | 1 sprint = 1 TP (entrega incremental). Cada sprint cierra con su PR mergeado en `main`. |
| **Backlog** | Pila de tareas por TP (historias de usuario + tareas técnicas) en el tablero. |
| **Daily / coordinación** | Comunicación por el grupo del curso + revisiones en los PR de GitHub. |
| **Review** | Todo trabajo entra a `main` vía **pull request revisado por otro integrante** (flujo profesional). |
| **Retro** | Breve cierre de cada sprint: qué salió bien, qué mejorar, y actualización del estado en el README. |

### Tablero

🔗 **GitHub Projects:** _[pegar aquí el link del tablero — ver sección 3]_

Columnas mínimas: **Backlog → En progreso → En revisión → Hecho**.

## 2. Historias de usuario (una por entrega)

| Sprint / TP | Historia de usuario | Criterios de aceptación |
|---|---|---|
| **TP1** | *"Como usuario quiero cargar un catálogo de videojuegos y buscar/filtrar/listar para no depender de archivos sueltos."* | Carga desde JSON; buscar, filtrar y listar funcionan en la terminal. |
| **TP2** | *"Como usuario quiero que la búsqueda por título sea rápida con catálogos grandes."* | Dos estrategias implementadas; benchmark de 100 a 1.000.000 con tabla y análisis O/Ω/Θ en el informe. |
| **TP3** | *"Como usuario quiero encontrar títulos en O(log n) usando un árbol."* | BST con inserción, búsqueda y recorridos; integrado al menú; comparado contra la lineal. |
| **TP4** | *"Como usuario quiero que la búsqueda no se degenere si los datos llegan ordenados."* | AVL con 4 rotaciones; experimento BST vs AVL con datos ordenados/inversos/aleatorios; conclusión técnica. |
| **TP5** | *"Como usuario quiero explorar las categorías de juegos como una jerarquía."* | Árbol general con los 25 géneros reales; búsqueda con ruta; recorridos; opción 'Explorar categorías'; versión 3. |
| **TP6** | *"Como usuario quiero ver el Top 10 de juegos mejor rankeados para decidir rápido qué jugar."* | MaxHeap manual (sin `heapq`); ranking con medallas en menos de 1 s; coincide con el `sort()` de referencia; versión 4. |
| **TP7** | *"Como usuario quiero saber qué juegos están relacionados con uno que me gustó."* | Grafo justificado (vértices/aristas/tipo/representación); lista de adyacencia; consulta de vecinos; versión 5. |
| **TP8** | *"Como usuario quiero saber qué juego relacionado está más cerca y poder explorar toda la red."* | BFS y DFS implementados; 2 casos de uso reales; análisis de complejidad O(V+E); versión 6. |

## 3. Cómo crear el tablero (5 minutos)

1. Entrar al repositorio en GitHub → pestaña **Projects** → **New project** → **Board**.
2. Nombre: `NextPlay — Tablero de entregas`.
3. Crear las columnas (vistas de tabla o kanban): `Backlog`, `En progreso`, `En revisión`, `Hecho`.
4. Crear una tarjeta por historia de usuario de la tabla anterior (o importarlas desde las issues).
5. Pegar el link del tablero arriba, en la sección 1.

> Alternativa: [Trello](https://trello.com) con las mismas cuatro columnas (la cátedra lo acepta como ejemplo).

## 4. Evidencia del uso del tablero

- Cada TP tiene su **branch** (`feature/tp_N`) y su **PR** en GitHub: `#4` (TP2), `#5` (TP3), `#6` (TP5), etc.
- El historial de commits refleja la evolución incremental (no está todo subido de una sola vez).
- El `main` se mantiene funcional en cada entrega (verificado con `python -m unittest discover -s tests`).
