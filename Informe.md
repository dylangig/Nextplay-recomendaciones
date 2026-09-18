# Informe — NextPlay: Búsqueda por título con dos estrategias

## 1. Objetivo

Resolver una misma necesidad crítica del sistema —*encontrar un videojuego por su título*— con al menos dos estrategias distintas, medir su comportamiento con distintos tamaños de entrada y analizar su complejidad usando notación Ω, Θ y O.

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

## 3. Análisis de complejidad

| Estrategia               | Ω (mejor)   | Θ (promedio) | O (peor)    |
|--------------------------|-------------|--------------|-------------|
| Búsqueda lineal          | Ω(1)        | Θ(n)         | O(n)        |
| Búsqueda binaria         | Ω(1)        | Θ(log n)     | O(log n)    |
| Ordenamiento previo (*)  | Ω(n)        | Θ(n log n)   | O(n log n)  |

(*) Solo requerido por la estrategia binaria. En Python el ordenamiento usa Timsort, cuyo mejor caso sobre datos ya ordenados es Ω(n).

## 4. Metodología de medición

- **Datos:** `generar_datos.py` genera catálogos con títulos únicos y desordenados de 100, 1.000, 10.000, 100.000 y 1.000.000 de juegos (formato idéntico a `Juegos.json`).
- **Instrumento:** `benchmark.py` usa `time.perf_counter()`; toma la **mediana de 5 rondas**; cada ronda ejecuta un lote de consultas proporcional al costo estimado (para mantener constante el volumen de trabajo) y desactiva el *garbage collector* durante la medición.
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

*(Los mismos valores están en `resultados.csv`.)*

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