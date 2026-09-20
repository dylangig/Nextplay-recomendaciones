# Informe — NextPlay: Búsqueda por título con tres estrategias

## 1. Objetivo

Resolver una misma necesidad crítica del sistema —*encontrar un videojuego por su título*— con al menos tres estrategias distintas, medir su comportamiento con distintos tamaños de entrada y analizar su complejidad usando notación Ω, Θ y O. La tercera estrategia, un **árbol binario de búsqueda**, agrega además alta/baja de juegos en tiempo logarítmico, un requerimiento que la búsqueda binaria sobre arreglo ordenado no puede sostener.

## 2. Estrategias implementadas

### Estrategia A — Búsqueda lineal (secuencial)
Recorre el catálogo comparando el título buscado contra cada elemento, uno por uno. Es la que ya usaba `Catalogo.buscar_por_titulo`. No exige ningún orden ni estructura previa.

- Se implementa en `estrategias.py::busqueda_lineal`.
- **Mejor caso Ω(1):** el título coincide con el primer elemento.
- **Caso promedio Θ(n):** en promedio recorre n/2 posiciones.
- **Peor caso O(n):** el título es el último o no existe (recorre todo).

### Estrategia B — Búsqueda binaria
Requiere que el catálogo esté **ordenado por título**. Compara el título buscado contra el elemento del medio y descarta la mitad restante en cada comparación.

- Índice: `estrategias.py::preparar_indice_binario` ordena el catálogo una vez (Timsort, O(n log n)).
- Se implementa en `estrategias.py::busqueda_binaria`.
- **Mejor caso Ω(1):** el título coincide con el elemento medio en la primera comparación.
- **Caso promedio Θ(log n):** en n = 1.000.000 bastan ≈ 20 comparaciones.
- **Peor caso O(log n):** la búsqueda siempre reduce el espacio a la mitad.
- **Limitación:** todo cambio del catálogo (alta o baja) exige re-ordenar o desplazar elementos, O(n), además de re-indexar.

### Estrategia C — Árbol binario de búsqueda
Mantiene los juegos en un **ABB ordenado por título** (clave en minúsculas), implementado en `arbol.py`. La búsqueda recorre la raíz y decide ir a la izquierda o a la derecha según la comparación, recorriendo la altura del árbol.

- Construcción: `estrategias.py::construir_arbol` inserta los juegos uno a uno.
- Búsqueda: `estrategias.py::busqueda_arbol` → `ArbolBinario.buscar`.
- **Alta/baja dinámicas:** `insertar` y `eliminar` (impares: sin hijos, un hijo, dos hijos con sucesor inorden) en tiempo igual que la búsqueda.
- **Recorridos usados como funcionalidad real:**
  - *inorden* → listar el catálogo en orden alfabético (`Menu 6`).
  - *preorden* → serializar/guardar el catálogo a archivo para reconstruir el mismo árbol (`Menu 9`).
  - *postorden* → vaciar el catálogo liberando hijos antes que padres (`Menu 10`).
- **Mejor caso Ω(1):** el título coincide con la raíz.
- **Caso promedio Θ(log n):** con inserción en orden aleatorio el árbol queda balanceado en expectativa (altura ≈ log₂ n).
- **Peor caso O(n):** con inserciones en orden ascendente el árbol degenera en lista enlazada.

## 3. Análisis de complejidad

| Operación                      | Ω (mejor) | Θ (promedio) | O (peor)   |
|--------------------------------|-----------|--------------|------------|
| Búsqueda lineal                | Ω(1)      | Θ(n)         | O(n)       |
| Búsqueda binaria               | Ω(1)      | Θ(log n)     | O(log n)   |
| Búsqueda en árbol              | Ω(1)      | Θ(log n)     | O(n) (*)   |
| Inserción en árbol             | Ω(1)      | Θ(log n)     | O(n) (*)   |
| Eliminación en árbol           | Ω(1)      | Θ(log n)     | O(n) (*)   |
| Recorrido inorder/preorder/postorder | Θ(n) | Θ(n)         | Θ(n)       |
| Ordenamiento previo (única vez)| Ω(n)      | Θ(n log n)   | O(n log n) |
| Construcción del árbol (única) | Ω(n)      | Θ(n log n)   | O(n²)(*)   |

(*) Peor caso del ABB sin balancear: si los títulos se insertan ordenados, el árbol degenera en lista y todas las operaciones pasan a O(n). Un árbol autobalanceado (AVL) garantiza O(log n) también en el peor caso.

## 4. Metodología de medición

- **Datos:** `generar_datos.py` genera catálogos con títulos únicos y desordenados (orden aleatorio) de 100 a 1.000.000 de juegos —por eso el ABB resultante queda equilibrado en la práctica—.
- **Instrumento:** `benchmark.py` usa `time.perf_counter()`; toma la **mediana de 5 rondas**; cada ronda ejecuta un lote de consultas proporcional al costo estimado y desactiva el *garbage collector* durante la medición.
- **Escenarios por tamaño:**
  - *Mejor caso:* buscar el primer título del catálogo.
  - *Promedio:* buscar el título de la posición central.
  - *Peor caso:* buscar el último título.
  - *No encontrado:* buscar un título inexistente.
  - *Pagos únicos:* `ordenamiento` (índice binario) y `construccion_arbol` (n inserciones).

Los valores son **segundos por consulta individual** (las dos últimas columnas son pagos únicos al construir cada índice).

## 5. Resultados

| Tamaño   | Lineal (mejor) | Lineal (prom.) | Lineal (peor) | Lineal (ausente) | Binaria | Árbol  | Ordenamiento (única) | Construcción árbol (única) |
|----------|----------------|----------------|----------------|------------------|---------|--------|----------------------|----------------------------|
| 100      | ≈0             | 0,000008       | 0,000018       | 0,000013         | 0,000001| 0,000001| 0,000136            | 0,000208                   |
| 1.000    | ≈0             | 0,000078       | 0,000153       | 0,000159         | 0,000003| 0,000001| 0,000459            | 0,001242                   |
| 10.000   | ≈0             | 0,000609       | 0,001361       | 0,001127         | 0,000002| 0,000001| 0,007686            | 0,023762                   |
| 100.000  | ≈0             | 0,014348       | 0,028095       | 0,027358         | 0,000002| 0,000001| 0,083882            | 0,371207                   |
| 1.000.000| ≈0             | 0,199569       | 0,409817       | 0,450176         | 0,000004| 0,000004| 2,389559            | 9,494401                   |

*(Los mismos valores están en `resultados.csv`.)*

## 6. Análisis de resultados

- **La búsqueda lineal crece proporcionalmente con n.** Entre 1.000 y 1.000.000 de elementos el peor caso pasa de 0,000153 s a 0,410 s: Es el comportamiento O(n) esperado.
- **Binaria y árbol son prácticamente constantes** en el rango medido (1 a 4 µs): sus ≈log₂(n) comparaciones pasan de ~7 (n=100) a ~20 (n=1.000.000). Empíricamente ambas confirman Θ(log n) en promedio; el árbol no degrada porque el dato de entrada llega desordenado.
- **El árbol empata a la binaria en búsqueda** (ambas recorren una rama de log n nodos) pero **agrega tres ventajas que el arreglo no tiene**: alta y baja en O(log n) sin re-ordenar todo, listado alfabético sin sort adicional (inorden) y serialización pensada para reconstruir la misma estructura (preorden).
- **Costo de construcción:** insertar n títulos (9,49 s en 1M) es más caro que el Ordenamiento de Timsort (2,39 s). Es un **pago único** y se amortiza cuando el catálogo cambia a menudo: cada alta/baja incremental es ~µs, contra O(n) del arreglo ordenado.
- **Peor caso teórico del ABB:** si los títulos se dieran de alta en orden alfabético, el árbol degeneraría en lista y la búsqueda pasaría a O(n). El benchmark no lo muestra porque los datos de entrada están desordenados.

## 7. Conclusión

- **Catálogos pequeños (≤ 1.000) y sin actualizaciones:** la lineal conviene por simplicidad y por no exigir estructura.
- **Catálogos grandes y estáticos:** binaria sobre arreglo ordenado es la más simple y el ordenamiento único se amortiza.
- **Catálogos grandes y dinámicos (altas/bajas constantes):** el **árbol binario de búsqueda es la estrategia superior**, porque mantiene búsqueda O(log n) promedio y además permite insertar, eliminar y listar en orden sin el costo O(n) de re-ordenar el arreglo por cada cambio. Este era exactamente el vacío del TP2.
- **Evolución recomendada:** sustituir el ABB por un **AVL**, que con rotaciones garantiza O(log n) también en el peor caso, eliminando la degeneración que sufre el árbol simple con inserciones ordenadas.