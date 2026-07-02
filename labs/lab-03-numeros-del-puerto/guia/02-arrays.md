# Guía 2 — Arrays de NumPy

> **Objetivo:** manejar la matriz de recaudación: crearla, medirla, cortarla y
> sacarle totales por eje.

REPL abierto (`uv run python`), con `import numpy as np`.

## De lista de listas a matriz

```python
>>> import numpy as np
>>> from datos.recaudacion import RECAUDACION, MESES, RUBROS
>>> m = np.array(RECAUDACION)
>>> m
array([[4120000, 3380000, 1150000],
       [3950000, 3610000, 1240000],
       ...
       [4490000, 3560000, 1090000]])
```

Es la misma planilla del Lab 01/02 (lista de listas), pero ahora es un
**ndarray**: un bloque de números con superpoderes.

> 🔢 **Sobre los guiones bajos:** en `datos/recaudacion.py` los números se
> escriben `4_120_000`. Python **ignora** los `_`; son solo para que TÚ leas de
> un vistazo que son millones. `4_120_000 == 4120000` es `True`.

## Medir el array: `shape`, `dtype`, `ndim`

```python
>>> m.shape
(12, 3)
>>> m.dtype
dtype('int64')
>>> m.ndim
2
```

- `shape` → **la forma**: 12 filas × 3 columnas.
- `dtype` → **el tipo** de los datos (enteros de 64 bits).
- `ndim` → **cuántas dimensiones** (2: una tabla).

> 🗄️ **Analogía del archivador.** `shape (12, 3)` es como decir "el archivador
> tiene **12 cajones** y cada cajón, **3 carpetas**". La primera dimensión son
> los cajones (meses); la segunda, las carpetas (rubros).

## Indexación y slicing en 2D

Se accede con `[fila, columna]`:

```python
>>> m[0, 0]        # Enero, Comercio
4120000
>>> m[0]           # toda la fila de Enero (los 3 rubros)
array([4120000, 3380000, 1150000])
>>> m[:, 2]        # TODA la columna 2 (Turismo, los 12 meses)
array([1150000, 1240000,  760000,  410000,  330000,  280000,
        350000,  390000,  540000,  690000,  880000, 1090000])
```

`m[:, 2]` se lee: "todas las filas (`:`), columna 2". Es la serie del **Turismo**
mes a mes — y cuenta la historia estacional del puerto (alto en verano, casi
cero en invierno).

### 🔮 Predice antes de ejecutar

¿Qué crees que devuelve `m[5, 2]`? (pista: fila 5, columna 2). Anota tu
predicción y ejecuta:

```python
>>> m[5, 2]
```

<details>
<summary>Ver respuesta</summary>

Devuelve `280000`: la fila 5 es **Junio** (se cuenta desde 0) y la columna 2 es
**Turismo**. Es la recaudación turística de Junio, el punto más bajo del año —
pleno invierno en el puerto.
</details>

## Agregaciones por eje: la regla que lo cambia todo

`sum`, `mean`, `max` pueden colapsar el array por un **eje** (`axis`):

```python
>>> m.sum()            # sin axis: el total de TODO
90680000
>>> m.sum(axis=1)      # por fila -> un total por MES (12 números)
array([8650000, 8800000, 7960000, 7000000, 6570000, 6150000,
       6350000, 6680000, 7280000, 7820000, 8280000, 9140000])
>>> m.sum(axis=0)      # por columna -> un total por RUBRO (3 números)
array([48480000, 34090000,  8110000])
```

> 🧭 **Regla mnemotécnica (memorízala): `axis` es el eje QUE COLAPSA.**
> - `axis=1` colapsa las **columnas** → te queda un número por **fila** (por mes).
> - `axis=0` colapsa las **filas** → te queda un número por **columna** (por rubro).
>
> Se siente al revés al principio; por eso la regla. El eje que pones es el que
> **desaparece**.

`max` y `argmax` te dan el mejor y **dónde** está el mejor:

```python
>>> por_mes = m.sum(axis=1)
>>> por_mes.max()          # el mayor total mensual
9140000
>>> por_mes.argmax()       # la POSICIÓN de ese mayor (no el valor)
11
>>> MESES[por_mes.argmax()]
'Diciembre'
```

`argmax` devuelve el **índice** (11), no el valor. Combinado con `MESES`, te da
el **mes récord**. Ese es exactamente el TODO 3 de tu programa.

## 💥 Rómpelo: pide una fila que no existe

```python
>>> m[12, 0]
```
```
IndexError: index 12 is out of bounds for axis 0 with size 12
```

Última línea: `IndexError` — el eje 0 tiene tamaño 12 (índices 0 a 11), y pediste
el 12. Otra vez el clásico de contar desde 0: hay 12 meses, pero el último es el
índice **11**.

## ✅ Checkpoint

- [ ] Creaste la matriz y consultaste `shape`, `dtype`, `ndim`.
- [ ] Sacaste una fila (`m[0]`), la columna del Turismo (`m[:, 2]`) y `m[5, 2]`.
- [ ] Entendiste la regla "`axis` es el eje que colapsa" con `sum(axis=0/1)`.
- [ ] Usaste `argmax` para encontrar el mes récord.
- [ ] Provocaste el `IndexError` con `m[12, 0]`.

Cuando esté todo ✔, sigue con **[Guía 3 — Vectorización](03-vectorizacion.md)**.
