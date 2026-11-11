# 04 — Diagrama de conexión entre estructuras (datos)

> Este diagrama muestra **cómo fluyen y se conectan las estructuras de datos** del sistema,
> no solo las clases. Es la pieza central de la parte técnica de la defensa (§8.3).

## 1. Vista general del flujo de datos

```
                      ┌─────────────────────────┐
                      │   datos/juegos.json      │
                      │  (100 juegos reales)     │
                      └────────────┬────────────┘
                                   │ carga (json)
                                   ▼
                      ┌─────────────────────────┐
                      │  Catalogo._juegos        │
                      │  list[Videojuego]        │  ◄── fuente de verdad
                      └────────────┬────────────┘
                                   │
        ┌──────────────┬───────────┼───────────┬──────────────┐
        │              │           │           │              │
        ▼              ▼           │           ▼              ▼
┌──────────────┐ ┌──────────────┐  │   ┌──────────────┐ ┌──────────────┐
│  ArbolAVL    │ │ArbolGeneral  │  │   │  MaxHeap     │ │   Grafo      │
│ (por título) │ │(categorías)  │  │   │  (por rating)│ │(relaciones)  │
│  O(log n)    │ │   O(n)       │  │   │  O(K) build  │ │  O(V+E)      │
└──────┬───────┘ └──────┬───────┘  │   └──────┬───────┘ └──────┬───────┘
       │                │          │           │                │
       │                │          │           │                │
       ▼                ▼          │           ▼                ▼
┌────────────┐  ┌──────────────┐   │   ┌──────────────┐  ┌──────────────┐
│ Buscar por │  │ Explorar     │   │   │ Top-N        │  │ BFS / DFS    │
│ título     │  │ categorías   │   │   │ Recomendador │  │ (TP8)        │
│ (opc. 4)   │  │ (opc. 11)    │   │   │ (opc. 10)    │  │ (TP7/8)      │
└────────────┘  └──────────────┘   │   └──────────────┘  └──────────────┘
                                   │
                                   │ lista (búsqueda lineal, filtrado,
                                   │        altas/bajas, exportación)
                                   ▼
                      ┌─────────────────────────┐
                      │      SistemaUI          │
                      │   ui/terminal.py        │
                      │   (menú principal)      │
                      └─────────────────────────┘
```

## 2. Qué consulta cada funcionalidad

| Funcionalidad (opc. menú) | Estructura que la resuelve | Complejidad clave |
|---|---|---|
| 1. Buscar por título (lineal) | `Catalogo._juegos` (lista) | O(n) |
| 2. Filtrar por género | `Catalogo._juegos` (lista) | O(n) |
| 3. Listar todos | `Catalogo._juegos` (lista) | O(n) |
| 4. Buscar por título (AVL) | `ArbolAVL` | **O(log n)** |
| 5. Orden alfabético | `ArbolAVL` inorden | Θ(n) |
| 6/7. Agregar / eliminar | `Catalogo` (lista) **+** `ArbolAVL` (sincronizados) | O(log n) el árbol |
| 8. Exportar preorden | `ArbolAVL` preorder | Θ(n) |
| 10. Top N (heap) | `MaxHeap` vía `Recomendador` | **O(K + n log K)** |
| 11. Explorar categorías | `ArbolGeneral` + conteos sobre el catálogo | O(n) |
| 12.1 Juegos relacionados | `Grafo` (lista de adyacencia) | O(V²) build + O(grado) |
| 12.2 Más cercano (BFS) | `Grafo.bfs()` | **O(V + E)** |
| 12.3 Explorar red (DFS) | `Grafo.dfs()` | **O(V + E)** |

## 3. Conexiones en código (imports reales)

```
main.py
  ├── modelos.catalogo.Catalogo ────── lee ──► datos/juegos.json
  ├── servicios.recomendador.Recomendador
  │        ├── estructuras.heap.MaxHeap ◄── usa para obtener_top_n()
  │        └── algoritmos.grafo.Grafo ◄── construye en cada consulta (TP7)
  └── ui.terminal.SistemaUI
           ├── Catalogo                (lista + búsqueda lineal + filtros)
           ├── Recomendador            (Top-N, relacionados, BFS, DFS)
           ├── algoritmos.arbol_avl.ArbolAVL      (búsqueda por título)
           └── algoritmos.arbol_general.ArbolGeneral  (jerarquía de categorías)
                 └── JERARQUIA_GENEROS (dict de los 25 géneros reales)
```

## 4. Ciclo de vida de los datos (altas y bajas)

```
 usuario ingresa alta (opc. 6)
        │
        ├──► Catalogo.agregar_juego()      → lista.append
        └──► ArbolAVL.insertar()           → rotaciones si hace falta
                                             (ambos quedan sincronizados)

 usuario ingresa baja (opc. 7)
        │
        ├──► Catalogo.eliminar_por_titulo()  → lista.remove
        └──► ArbolAVL.eliminar()             → rebalanceo

 ranking Top-N (opc. 10) siempre se recalcula desde la lista actual:
        Catalogo.listar_todos() ──heapify O(K)──► MaxHeap ──n pops──► Top-N
        (el heap es desechable: no se almacena entre consultas)
```

> **Nota de diseño (para la defensa):** el heap es *desechable por consulta* porque el
> catálogo es pequeño y dinámico; reconstruirlo en O(K) es más barato que mantenerlo
> sincronizado ante cada alta/baja. El AVL, en cambio, sí se mantiene incremental porque
> se consulta mucho (búsquedas) y las rotaciones cuestan O(1).

## 5. Grafo y recorridos (TP7 / TP8)

```
  Catalogo.listar_todos()
        │  vértice = juego
        │  arista (no dirigida, pesada) si comparten género O estudio
        ▼
     Grafo._adyacencia = {juego: [(vecino, peso), ...]}   (lista de adyacencia)
        │
        ├── vecinos(j)          → "juegos relacionados"        (opc. 12.1)
        ├── bfs(origen)         → el más cercano en aristas    (opc. 12.2)
        └── dfs(origen)         → explorar la red en profundidad (opc. 12.3)
```

- **Vértice** = juego · **Arista** no dirigida si comparten género o estudio · **Peso** = `1/(1+|Δrating|)` ∈ (0,1].
- **Construcción:** `Recomendador.construir_grafo()` compara todos los pares **O(V²)** y se recrea en cada consulta (más barato que sincronizar ante altas/bajas).
- **Recorridos:** BFS con cola (`deque`) descubre primero lo más cercano; DFS con pila explícita cubre la componente en profundidad; ambos **O(V + E)** con conjunto de visitados.
