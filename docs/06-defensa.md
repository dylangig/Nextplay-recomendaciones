# 06 — Guion de defensa (Demo Day)

> 7–10 minutos. Esta guía resume qué decir en cada bloque y las respuestas
> a las preguntas típicas de la cátedra (Parte X de la consigna).

## 8.1 Presentación — 1 minuto

**"¿Qué problema resuelve nuestro sistema?"**

> NextPlay resuelve el problema de *no saber qué jugar después de terminar
> un buen juego*. Es un sistema de recomendación de videojuegos por
> terminal: carga un catálogo real de 100 juegos y permite buscarlos,
> filtrarlos, explorarlos por categorías, rankearlos y descubrir juegos
> relacionados — usando estructuras de datos eficientes en cada consulta.

Datos duros: 100 juegos · 25 géneros · 51 tests · 6 entregas incrementales.

## 8.2 Demo — 3 minutos

Orden sugerido (usar `docs/capturas/` como apoyo):

1. **Buscar** (opc. 4): título en el AVL + comparaciones mostradas.
2. **Top N** (opc. 10): ranking con heap → *"O(K + n log K), sin ordenar el dataset"*.
3. **Explorar categorías** (opc. 11): jerarquía ASCII con conteos reales (suman 100).
4. **Grafo** (opc. 12): relacionados de Hades → BFS (más cercano) → DFS (red entera).
5. **Alta/baja** (opc. 6/7): se mantienen lista y AVL sincronizados.

## 8.3 Parte técnica — 3 minutos

### "¿Dónde está cada cosa?" (ubicaciones exactas)

| Pregunta | Respuesta |
|---|---|
| ¿Dónde está el árbol? | `algoritmos/arbol.py` (BST), `arbol_avl.py` (AVL, **el que usa la UI**), `arbol_general.py` (n-ario de categorías) |
| ¿Dónde el heap? | `estructuras/heap.py` — `MaxHeap` **maneada a mano, sin `heapq`**; usada en `servicios/recomendador.py::obtener_top_n()` |
| ¿Dónde el grafo? | `algoritmos/grafo.py` — lista de adyacencia, no dirigido y pesado; construido en `Recomendador.construir_grafo()` |
| ¿Dónde se usa BFS? | `Grafo.bfs()` → `Recomendador.juego_mas_cercano()` → opción **12.2** (el juego relacionado más cercano) |
| ¿Dónde se usa DFS? | `Grafo.dfs()` → `Recomendador.explorar_red()` → opción **12.3** (explorar toda la red) |

### Complejidades clave

| Operación | Complejidad | Dónde |
|---|---|---|
| Búsqueda por título (AVL) | **O(log n)** peor caso (garantizado por balance) | `arbol_avl.py` |
| Top-N con heap | **O(K + n log K)** vs O(K log K) de `sort()` | `heap.py` + `recomendador.py` |
| Explorar categorías / recorridos | O(n) — jerarquía chica (28 nodos) | `arbol_general.py` |
| Construir el grafo | O(V²) comparaciones (V = 100) | `recomendador.py` |
| BFS / DFS | **O(V + E)** | `grafo.py` |
| Búsqueda lineal (referencia) | O(n) | `busqueda.py` |

### "¿Por qué cada estructura?" (la pregunta clave)

- **Árbol AVL:** *"porque buscamos por título de forma frecuente y queremos evitar que, con datos ordenados, el BST degrade a O(n). El experimento del TP4 lo demuestra: 9.999 de altura (BST) vs 13 (AVL) con 10.000 títulos ordenados."*
- **Árbol general:** *"porque la taxonomía de géneros no es binaria: una categoría tiene N subcategorías. Un BST forzaría claves artificiales."*
- **Heap:** *"porque el sistema consulta constantemente los mejores N; heapify construye en O(K) lineal y solo pagamos log por cada extracción. Ordenar todo sería O(K log K) completo para leer 10 elementos."*
- **Grafo:** *"porque las relaciones entre juegos son muchos-a-muchos (comparten género o estudio) y eso no es una jerarquía: solo un grafo lo representa sin mentir."*
- **Lista de adyacencia:** *"grafo disperso: 100 vértices, cientos de aristas. O(V+E) memoria vs O(V²) de la matriz (10.000 celdas, 90% vacías)."*
- **BFS vs DFS:** *"BFS para 'el más cercano' porque garantiza el camino con menos aristas; DFS para 'explorar toda la red' porque cubre la componente completa en profundidad."*

### Mostrar el diagrama de conexión (docs/04-diagrama-datos.md)

> JSON → catálogo (lista) → [AVL por título | Árbol general por categorías | Heap por rating | Grafo por relaciones] → Recomendador → terminal.

## 8.4 Desafío sorpresa — preguntas probables

**"Agreguen 100.000 elementos y vuelvan a buscar."**
> `generar_datos.py` ya lo hace: correr `python -m tests.benchmark 100000`. La binaria sigue en microsegundos; el AVL mantiene O(log n) ≈ 17 niveles.

**"¿Qué pasa si el dataset fuera 100 veces más grande?"**
> Las estructuras clave son logarítmicas o lineales controladas: AVL O(log n) → +7 niveles; heap O(K + n log K) crece linealmente; BFS/DFS O(V+E). Nada se degrada a cuadrático.

**"¿Por qué un heap y no ordenar todo?"**
> Porque solo pedimos n << K elementos. Ordenar paga O(K log K) aunque pidas 10; el heap construye en O(K) y cobra log solo por extracción.

**"¿Qué representa el costo en el grafo / camino mínimo?"**
> El peso es afinidad `1/(1+|Δrating|)` ∈ (0,1], siempre positivo. Si se pidiera camino mínimo, el costo sería `1 − afinidad` y entraría Dijkstra (el TP9 salió, pero el grafo ya está preparado).

**"¿Qué ocurriría si un árbol se desbalancea?"**
> Ver §8 del Informe: degrada a O(n). El AVL lo evita con rotaciones (4 casos) manteniendo altura ≤ 1,44·log₂(n+2).

## 9. Checklist rápido antes de exponer

- [ ] `python -m unittest discover -s tests` → **51 OK**
- [ ] `python main.py` recorriendo todas las opciones
- [ ] Saber explicar: encapsulamiento (TP1), O/Ω/Θ (TP2), BST vs secuencial (TP3), rotaciones AVL (TP4), n-ario (TP5), heap (TP6), grafo (TP7), BFS/DFS (TP8)
- [ ] Revisar `docs/04-diagrama-datos.md` (lo van a pedir en la defensa)
- [ ] Los tres integrantes deben poder explicar cualquier parte (defensa individual)
