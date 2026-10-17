# Informe — NextPlay: Búsqueda por título con dos estrategias

## 1. Objetivo

Resolver una misma necesidad crítica del sistema —*encontrar un videojuego por su título*— con al menos dos estrategias distintas, medir su comportamiento con distintos tamaños de entrada y analizar su complejidad usando notación Ω, Θ y O.

## 2. Estrategias implementadas

### Estrategia A — Búsqueda lineal (secuencial)
Recorre el catálogo comparando el título buscado contra cada elemento, uno por uno. Es la que ya usaba `Catalogo.buscar_por_titulo`. No exige ningún orden ni estructura previa.

- Se implementa en `algoritmos/busqueda.py::busqueda_lineal`.
- **Mejor caso Ω(1):** el título coincide con el primer elemento.
- **Caso promedio Θ(n):** en promedio recorre n/2 posiciones.
- **Peor caso O(n):** el título es el último o no existe (recorre todo).

### Estrategia B — Búsqueda binaria
Requiere que el catálogo esté **ordenado por título**. Compara el título buscado contra el elemento del medio y descarta la mitad restante en cada comparación.

- Índice: `algoritmos/busqueda.py::preparar_indice_binario` ordena el catálogo una vez (Timsort, O(n log n)).
- Se implementa en `algoritmos/busqueda.py::busqueda_binaria`.
- **Mejor caso Ω(1):** el título coincide con el elemento medio en la primera comparación.
- **Caso promedio Θ(log n):** en n = 1.000.000 bastan ≈ 20 comparaciones.
- **Peor caso O(log n):** la búsqueda siempre reduce el espacio a la mitad.

## 3. Análisis de complejidad

| Estrategia               | Ω (mejor)   | Θ (promedio) | O (peor)    |
|--------------------------|-------------|--------------|-------------|
| Búsqueda lineal          | Ω(1)        | Θ(n)         | O(n)        |
| Búsqueda binaria         | Ω(1)        | Θ(log n)     | O(log n)    |
| Ordenamiento previo (*)  | Ω(n)        | Θ(n log n)   | O(n log n)  |

(*) Solo requerido por la estrategia binaria. En Python el ordenamiento usa Timsort, cuyo mejor caso sobre datos ya ordenados es Ω(n).

## 4. Metodología de medición

- **Datos:** `algoritmos/generar_datos.py` genera catálogos con títulos únicos y desordenados de 100, 1.000, 10.000, 100.000 y 1.000.000 de juegos (formato idéntico a `datos/juegos.json`).
- **Instrumento:** `tests/benchmark.py` usa `time.perf_counter()`; toma la **mediana de 5 rondas**; cada ronda ejecuta un lote de consultas proporcional al costo estimado (para mantener constante el volumen de trabajo) y desactiva el *garbage collector* durante la medición.
- **Escenarios por tamaño:**
  - *Mejor caso:* buscar el primer título del catálogo.
  - *Promedio:* buscar el título de la posición central (n/2 comparaciones).
  - *Peor caso:* buscar el último título.
  - *No encontrado:* buscar un título inexistente (peor caso real de la lineal).
  - *Ordenamiento:* tiempo de preparar el índice binario una sola vez.

Los valores son **segundos por consulta individual** (excepto la columna de ordenamiento, que es un pago único al construir el índice).

## 5. Resultados

| Tamaño   | Lineal (mejor) | Lineal (prom.) | Lineal (peor) | Lineal (ausente) | Binaria       | Ordenamiento (única vez) |
|----------|----------------|----------------|----------------|------------------|---------------|--------------------------|
| 100      | ≈0             | 0,000005       | 0,000008       | 0,000009         | 0,000001      | 0,000048                 |
| 1.000    | ≈0             | 0,000041       | 0,000085       | 0,000077         | 0,000001      | 0,000347                 |
| 10.000   | ≈0             | 0,000578       | 0,001083       | 0,000851         | 0,000002      | 0,005830                 |
| 100.000  | ≈0             | 0,005334       | 0,009897       | 0,008817         | 0,000004      | 0,097969                 |
| 1.000.000| ≈0             | 0,052015       | 0,114923       | 0,094450         | 0,000004      | 1,566838                 |



## 6. Análisis de resultados

- **La búsqueda lineal crece proporcionalmente con n.** Entre 1.000 y 1.000.000 de elementos el peor caso pasa de 0,000085 s a 0,115 s: **×1.350** de tiempo para **×1.000** de datos. Es el comportamiento O(n) esperado: 10x datos ≈ 10x tiempo.
- **La búsqueda binaria es prácticamente constante.** Se mantiene entre 1 y 4 microsegundos en todo el rango, porque sus ≈log₂(n) comparaciones pasan de ~7 (n=100) a ~20 (n=1.000.000). Empíricamente confirma Θ(log n).
- **Aceleración en el peor caso:** con 1.000.000 de elementos, la binaria es ≈ **28.700 veces más rápida** que la lineal (0,115 s vs. 0,000004 s por consulta).
- **Costo del ordenamiento:** crece más que lineal (típico n log n: de 48 µs a 1,57 s) pero es un **pago único**; se amortiza desde la primera búsqueda en catálogos grandes.

## 7. Conclusión

- **Catálogos pequeños (≤ 1.000):** ambas estrategias son indistinguibles en la práctica; la lineal conviene por simplicidad y por no exigir orden.
- **Catálogos grandes y con muchas consultas (caso típico de un sistema de recomendación):** la **búsqueda binaria es claramente superior**. El ordenamiento único O(n log n) se amortiza en segundos.
- **Limitación de la binaria:** exige mantener el catálogo ordenado. Si el sistema cambia de juegos con mucha frecuencia (altas/bajas constantes), cada modificación cuesta O(n) (insertar y mantener orden) y puede convenir la lineal o un índice por tabla de hash (O(1) promedio, a considerar como tercera estrategia).
- **Recomendación:** adoptar la búsqueda binaria sobre un catálogo ordenado como operación estándar de búsqueda por título, manteniendo la lineal solo como respaldo ante errores o catálogos en construcción.

## 8. El árbol también puede enfermarse: desbalance y AVL

### 8.1 El problema: el BST no se balancea solo

El árbol binario de búsqueda (BST) de la estrategia anterior (`algoritmos/arbol.py`) ofrece búsqueda en O(log n) **solo si el árbol está balanceado**. Pero un BST común no impone ninguna condición de forma: el orden de inserción decide la altura.

Si los datos llegan **ya ordenados** (por ejemplo, insertar títulos en orden alfabético), cada clave nueva es mayor que todas las anteriores y se encadena siempre a la derecha. El resultado deja de ser un árbol y degenera en una **lista enlazada**: altura = n − 1, y cada búsqueda recorre hasta n nodos. Es el caso patológico que motiva esta sección.

### 8.2 La solución: árbol AVL

Un **árbol AVL** (`algoritmos/arbol_avl.py`) es un BST que mantiene como invariante que, en cada nodo, la diferencia de altura entre subárbol derecho e izquierdo (el *factor de balance*) nunca supera 1 en valor absoluto. Tras cada inserción o eliminación se recalcula la altura y, si algún nodo se desbalancea, se aplica una **rotación** que reorganiza ese subárbol sin romper el orden inorden (la propiedad BST se conserva).

Se implementan las cuatro rotaciones clásicas:

| Situación (según factor de balance) | Rotación |
|---|---|
| Desbalance a la izquierda con hijo izquierdo izquierdo | simple a la derecha |
| Desbalance a la derecha con hijo derecho derecho | simple a la izquierda |
| Desbalance a la izquierda con hijo izquierdo derecho | doble izquierda-derecha |
| Desbalance a la derecha con hijo derecho izquierdo | doble derecha-izquierda |

Gracias al rebalanceo, la altura de un AVL con n nodos está acotada por **h ≤ 1,44 · log₂(n + 2) − 0,328**, de modo que la búsqueda, la inserción y la eliminación son siempre **O(log n) en el peor caso**, sin importar el orden de llegada de los datos.

### 8.3 Metodología del experimento

El script `tests/experimento_desbalance.py` construye ambos árboles con el **mismo dataset** y los compara en cuatro escenarios:

1. **`ordenado`** — títulos sintéticos insertados en orden creciente (peor caso del BST).
2. **`inverso`** — en orden decreciente (peor caso por el otro lado).
3. **`aleatorio`** — mismo dataset barajado con semilla fija (caso promedio).
4. **`reales_ordenado` / `reales_desordenado`** — los 100 títulos reales de `datos/juegos.json`, ordenados y desordenados.

Métricas registradas por cada par (estructura, escenario):

- **altura** del árbol y **altura mínima teórica** `⌊log₂ n⌋`;
- **comparaciones de búsqueda en el peor caso** (título inexistente menor y mayor que todos);
- **comparaciones promedio** sobre una muestra de claves;
- **tiempo de construcción** (mediana de 5 rondas) y **tiempo de búsqueda** por consulta.

Se ejecuta con:

```bash
python -m tests.experimento_desbalance 100 1000 10000
```

### 8.4 Resultados

| Escenario | n | Estructura | Altura | Alt. mín. | Cmp. peor | Cmp. prom. | T. constr. (s) | T. búsq. (s) |
|---|---|---|---|---|---|---|---|---|
| ordenado  | 100   | BST | 99   | 6  | 100   | 50,5  | 0,000805 | 0,000010 |
| ordenado  | 100   | AVL | 6    | 6  | 7     | 5,8   | 0,001084 | 0,000001 |
| ordenado  | 1.000 | BST | 999  | 9  | 1.000 | 498,5 | 0,068988 | 0,000112 |
| ordenado  | 1.000 | AVL | 9    | 9  | 10    | 9,0   | 0,013170 | 0,000002 |
| ordenado  | 10.000| BST | 9.999| 13 | 10.000| 4.976,0 | 6,078943 | 0,001211 |
| ordenado  | 10.000| AVL | 13   | 13 | 14    | 13,4  | 0,129872 | 0,000001 |
| inverso   | 10.000| BST | 9.999| 13 | 10.000| 4.976,0 | 4,343115 | 0,001855 |
| inverso   | 10.000| AVL | 13   | 13 | 14    | 13,4  | 0,133903 | 0,000002 |
| aleatorio | 1.000 | BST | 20   | 9  | 11    | 12,0  | 0,001653 | 0,000001 |
| aleatorio | 1.000 | AVL | 11   | 9  | 10    | 9,0   | 0,011834 | 0,000002 |
| aleatorio | 10.000| BST | 31   | 13 | 16    | 16,4  | 0,029380 | 0,000002 |
| aleatorio | 10.000| AVL | 15   | 13 | 14    | 12,6  | 0,158052 | 0,000002 |
| reales_ordenado    | 100 | BST | 99 | 6 | 100 | 50,5 | 0,000563 | 0,000011 |
| reales_ordenado    | 100 | AVL | 6  | 6 | 7   | 5,8  | 0,000582 | 0,000001 |
| reales_desordenado | 100 | BST | 13 | 6 | 5   | 7,4  | 0,000106 | 0,000001 |
| reales_desordenado | 100 | AVL | 7  | 6 | 7   | 5,9  | 0,000464 | 0,000001 |

### 8.5 Análisis de resultados

- **El BST ordenado degenera en lista enlazada.** Con 10.000 títulos en orden alfabético la altura es 9.999 (frente a una mínima de 13): exactamente el comportamiento O(n) predicho. La búsqueda peor caso exige 10.000 comparaciones y, en promedio, 4.976 —prácticamente n/2—. El mini ejemplo del enunciado queda confirmado.
- **El AVL no depende del orden de inserción.** En el mismo escenario ordenado su altura es 13, la mínima teórica, con 14 comparaciones en el peor caso y ~13,4 en promedio: Θ(log n) garantizado. La cota teórica también se respeta en todos los casos (para n = 10.000, 1,44·log₂(10.002) ≈ 19 > 13).
- **En datos aleatorios el BST "tiene suerte".** Con 10.000 claves barajadas su altura es 31 y el peor caso 16 comparaciones, lejos del desastre ordenado, pero sin ninguna garantía: una permutación desafortunada lo degrada otra vez. El AVL, en cambio, acota la altura en 15 sin importar la permutación.
- **La construcción es el único terreno donde el BST compite.** Con datos aleatorios el BST construye más rápido (0,029 s vs. 0,158 s en n = 10.000), porque no paga rotaciones. Pero con datos ordenados su construcción es **cuadrática** (cada inserción recorre la cadena creciente: 6,08 s vs. los 0,13 s del AVL). El AVL es, entonces, más lento solo cuando el BST tiene la suerte de no degenerar.
- **La ventaja del AVL se dispara con n.** En el peor caso ordenado, cada búsqueda pasa de 0,001211 s (BST) a 0,000001 s (AVL): alrededor de **1.000 veces más rápida** con solo 10.000 claves, y la brecha crece linealmente con n.
- **Con el catálogo real (100 títulos) pasa lo mismo a menor escala:** ordenado, el BST alcanza altura 99 y 50,5 comparaciones promedio, mientras el AVL se queda en 6 y 5,8. Desordenado, la diferencia se achica pero el AVL sigue siendo el más predecible.

### 8.6 Conclusión técnica

- **Por qué importa el balance:** la promesa de O(log n) de un árbol de búsqueda **no es una propiedad del BST, sino de su forma**. Un BST sin balanceo solo la cumple si los datos llegan en un orden favorable; ordenados, degrada a O(n) y pierde toda la ventaja frente a una lista.
- **Qué aporta el AVL:** garantiza el O(log n) en el peor caso para búsqueda, inserción y eliminación, a cambio de un costo constante por operación (rotaciones) y un poco más de memoria por nodo (campo de altura). Es la estructura adecuada cuando el catálogo **cambia con frecuencia** y no se puede controlar el orden de las altas.
- **Decisión para NextPlay:** el sistema usa el **AVL como estructura de búsqueda del catálogo dinámico** (`ui/terminal.py`), porque combina altas/bajas frecuentes con la garantía de búsqueda rápida. El BST común se conserva en `algoritmos/arbol.py` únicamente como referencia didáctica y base de comparación en el experimento.
- **Limitación y alternativa:** el AVL es más rígido que otras estructuras auto-balanceadas; cuando las búsquedas dominan sobre las escrituras, un **árbol rojo-negro** (menos rotaciones por inserción) o una **tabla de hash** (O(1) promedio) pueden ser mejores opciones a evaluar como próximas estrategias.