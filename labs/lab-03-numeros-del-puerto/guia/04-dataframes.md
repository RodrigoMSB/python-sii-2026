# Guía 4 — DataFrames de pandas

> **Objetivo:** dar el salto de "matriz de números" a "tabla con nombres". Aquí
> te reencuentras con el cuaderno de patentes del Lab 01, ahora con esteroides.

REPL abierto, `import pandas as pd`.

## El puente: una matriz con nombres

NumPy es genial con números puros, pero la matriz de recaudación no sabía que la
columna 2 era "Turismo": tú tenías que recordarlo. **pandas** le pone **nombres**
a filas y columnas. Su pieza chica es la `Series` (una columna con etiquetas):

```python
>>> import pandas as pd
>>> pd.Series([13, 8, 3], index=["vigentes", "vencidas", "suspendidas"])
vigentes       13
vencidas        8
suspendidas     3
dtype: int64
```

Y su pieza estrella es el **DataFrame**: una tabla completa.

## El cuaderno del Lab 01, ahora como DataFrame

```python
>>> from datos.cuaderno import PATENTES
>>> df = pd.DataFrame(PATENTES, columns=["codigo", "nombre", "estado", "deuda"])
>>> df.head()
      codigo                        nombre     estado   deuda
0  PS-1001-G         Pescadería La Miríada    VIGENTE       0
1  PS-1002-C  Ferretería El Tornillo Feliz    VIGENTE       0
2  PS-1003-G          Cocinería Doña Eureka    VENCIDA  185000
3  PS-1004-T          Hostal Vista al Faro    VIGENTE       0
4  PS-1005-C          Abarrotes El Arenario    VENCIDA   92000
```

La misma lista de listas del Lab 01, pero ahora es una **tabla de verdad**:
columnas con nombre, filas numeradas. Mírala con lupa:

```python
>>> df.shape
(24, 4)
>>> df.dtypes
codigo    str
nombre    str
estado    str
deuda     int64
dtype: object
```

> 🆕 **Detalle de pandas 3:** fíjate que las columnas de texto salen como
> `str`. En pandas 2 y en tutoriales viejos verías `object` ahí. Es un cambio
> reciente (pandas 3.0): el texto ahora tiene su propio tipo `str`. Si un
> tutorial te muestra `object`, no te asustes: es la versión antigua.

`df.info()` te da un resumen completo (filas, columnas, tipos, memoria); pruébalo.

## Seleccionar: `loc` (etiqueta) vs `iloc` (posición)

Dos formas de sacar una fila, y la diferencia es fina pero importa:

```python
>>> df.iloc[6]        # la fila en la POSICIÓN 6 (la séptima)
codigo            PS-1007-T
nombre    Kayaks Bahía Serena
estado           SUSPENDIDA
deuda                 310000
Name: 6, dtype: object
>>> df.loc[6, "nombre"]   # por ETIQUETA de fila (6) y columna ("nombre")
'Kayaks Bahía Serena'
```

> 🔎 **Analogía.** `iloc` es "dame la fila **número 7** del archivador" (posición
> física). `loc` es "dame la fila **etiquetada 6**" (su nombre). Ahora mismo
> coinciden porque las filas están numeradas 0, 1, 2… Pero si **reordenas** la
> tabla, la etiqueta viaja pegada a su fila y la posición no. Guarda esto: es la
> Pregunta 4.

## Filtrado booleano (lo mismo que las máscaras, con nombres)

Igual que las máscaras de NumPy, pero legible:

```python
>>> vencidas = df[df["estado"] == "VENCIDA"]
>>> vencidas.shape
(8, 4)
>>> int(vencidas["deuda"].sum())
976000
```

`df[df["estado"] == "VENCIDA"]` se lee "del df, las filas donde estado es
VENCIDA". 8 patentes, $976.000 de deuda: justo lo que pide `resumen_vencidas`.

## Columna derivada

Puedes crear columnas nuevas a partir de otras, sin bucles:

```python
>>> df["con_deuda"] = df["deuda"] > 0
>>> df[["codigo", "deuda", "con_deuda"]].head(3)
      codigo   deuda  con_deuda
0  PS-1001-G       0      False
1  PS-1002-C       0      False
2  PS-1003-G  185000       True
```

## Resúmenes automáticos: `value_counts` y `describe`

```python
>>> df["estado"].value_counts()
estado
VIGENTE       13
VENCIDA        8
SUSPENDIDA     3
Name: count, dtype: int64
>>> df["deuda"].describe()
count        24.000000
mean      97916.666667
std      ...
min           0.000000
max      520000.000000
Name: deuda, dtype: float64
```

`value_counts()` cuenta cuántas veces aparece cada valor; `describe()` te da
media, mínimo, máximo y percentiles de un tirón. Dos líneas, un panorama.

## 💥 Rómpelo: una mayúscula de más

```python
>>> df["Estado"]
```
```
KeyError: 'Estado'
```

`KeyError: 'Estado'` — no existe esa columna. La tuya se llama `estado`, en
minúscula. En pandas, como en todo Python, **las mayúsculas importan**. El 90 %
de los `KeyError` con DataFrames son exactamente esto: un nombre de columna mal
escrito.

## ✅ Checkpoint

- [ ] Creaste un DataFrame desde `PATENTES` con `columns=`.
- [ ] Miraste `head`, `shape`, `dtypes` (y viste el `str` de pandas 3).
- [ ] Sacaste una fila con `iloc[6]` y entendiste `loc` vs `iloc`.
- [ ] Filtraste las vencidas y sumaste su deuda (8, $976.000).
- [ ] Creaste una columna derivada y probaste `value_counts`/`describe`.
- [ ] Provocaste el `KeyError` con `df["Estado"]`.

Cuando esté todo ✔, sigue con **[Guía 5 — El panorama](05-panorama.md)**.
