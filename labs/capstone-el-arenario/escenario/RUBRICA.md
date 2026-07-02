# Rúbrica del Capstone — El Arenario

> Para el **relator**. El verificador comprueba la exactitud (máquina); esta
> rúbrica pondera lo que una máquina no ve (criterio, código, comunicación). Cada
> criterio se califica en un nivel; el puntaje ponderado se convierte a nota.

## Los cuatro criterios

| Criterio | Peso | Qué mide |
|----------|:----:|----------|
| **Exactitud verificada** | 40 % | Verificador en verde: los 6 productos presentes y las cifras de control exactas. |
| **Calidad del pipeline** | 25 % | Código legible: funciones con nombre claro, sin mutación (C13), decisiones con rastro (C14), merges con cinturón (C17), separación de etapas. |
| **Informe y visualizaciones** | 20 % | Informe legible en español, hallazgos **explicados** (no solo listados), gráficos correctos y titulados. |
| **Bitácora del analista** | 15 % | Las 5 defensas respondidas con resultados propios, criterio y honestidad técnica. |

## Escala por criterio

Cada criterio se puntúa en uno de cuatro niveles:

| Nivel | % | |
|-------|:-:|-|
| **Excelente** | 100 | |
| **Logrado** | 75 | |
| **Básico** | 50 | |
| **Insuficiente** | 0 | |

### Descriptores

**Exactitud verificada**
- *Excelente (100):* `✔ 9/9` en el verificador.
- *Logrado (75):* 7–8 de 9 checks; falla algo menor (un gráfico, la BITÁCORA).
- *Básico (50):* 4–6 checks; el censo depurado y el tablero base cuadran.
- *Insuficiente (0):* menos de 4 checks; los productos centrales no cuadran.

**Calidad del pipeline**
- *Excelente:* funciones cortas y nombradas por lo que hacen; sin mutar los
  DataFrames recibidos; cada descarte contabilizado; merges con `how`/`validate`.
- *Logrado:* pipeline claro con 1–2 descuidos (una mutación, un merge sin validate).
- *Básico:* funciona pero es difícil de seguir (todo en un bloque, nombres opacos).
- *Insuficiente:* no se entiende, copia-pega sin criterio, o no corre.

**Informe y visualizaciones**
- *Excelente:* el informe se lee como un documento del Concejo; los hallazgos
  (saldos negativos) se **explican con causa**; los dos gráficos están titulados
  y son correctos.
- *Logrado:* informe completo pero con hallazgos apenas listados; gráficos ok.
- *Básico:* informe mínimo; falta la explicación de hallazgos o un gráfico.
- *Insuficiente:* sin informe legible o sin gráficos válidos.

**Bitácora del analista**
- *Excelente:* las 5 respuestas usan los números propios, distinguen las dos causas
  de saldo negativo y proponen recomendaciones sensatas.
- *Logrado:* 4–5 respondidas con criterio; alguna superficial.
- *Básico:* respondidas a medias o genéricas (sin números propios).
- *Insuficiente:* sin responder o copiadas sin entender.

## Del puntaje a la nota (escala 1,0–7,0)

1. **Puntaje ponderado** `P` (0–100): suma de (nivel% × peso) de los 4 criterios.
   > Ejemplo: Exactitud 100·0,40 + Calidad 75·0,25 + Informe 75·0,20 + Bitácora
   > 50·0,15 = 40 + 18,75 + 15 + 7,5 = **81,25**.

2. **Conversión a nota** con 60 % de exigencia (aprueba con 4,0):
   - Si `P ≥ 60`:  `nota = 4,0 + (P − 60) / 40 × 3,0`
   - Si `P < 60`:  `nota = 1,0 + P / 60 × 3,0`
   > Con `P = 81,25` → `nota = 4,0 + (21,25/40)×3 = 4,0 + 1,59 = ` **5,6**.

3. **Aprobación del curso:** nota ≥ **4,0** (equivale a `P ≥ 60`).

| Puntaje P | Nota | |
|:---------:|:----:|-|
| 100 | 7,0 | Excelencia |
| 80 | 5,5 | |
| 60 | 4,0 | Aprueba (mínimo) |
| 40 | 3,0 | Reprueba |
| 0 | 1,0 | |

> El relator registra el nivel de cada criterio, calcula `P`, aplica la fórmula y
> deja la nota con una línea de retroalimentación por criterio. La exactitud pesa
> 40 %, pero **no basta**: un informe sin explicar y una bitácora vacía bajan la
> nota aunque el verificador esté verde.
