# Guía 3 — Combinar

> **Objetivo:** apilar los meses (`concat`) y cruzar deuda con pagos (`merge`),
> resolviendo de paso el misterio de los pagos huérfanos.

REPL abierto (`bash bin/repl.sh`).

## `concat`: apilar meses

Junio y julio tienen las **mismas columnas** (`codigo, fecha, monto`). Apilarlos es
`pd.concat`:

```python
>>> import pandas as pd
>>> jun = pd.read_csv("datos/pagos_junio.csv")
>>> jul = pd.read_csv("datos/pagos_julio.csv")
>>> pagos = pd.concat([jun, jul], ignore_index=True)
>>> len(pagos), int(pagos["monto"].sum())
(20, 1213000)
```

> ⚠️ El `ignore_index=True` importa: sin él, los índices se **repiten** (junio trae
> 0..11 y julio 0..7, y quedarías con dos filas "0", dos "1"…). `ignore_index`
> renumera de 0 a 19 de corrido.

## `merge`: cruzar dos tablas

El censo tiene una fila por contribuyente; los pagos, una por pago. Para saber
cuánto pagó cada uno, primero **agrupamos los pagos por código** (un contribuyente
puede pagar varias veces) y luego **unimos**:

```python
>>> pagado = pagos.groupby("codigo", as_index=False)["monto"].sum().rename(columns={"monto": "pagado"})
>>> censo = pd.read_csv("datos/censo_limpio.csv")
>>> tablero = censo.merge(pagado, on="codigo", how="left", validate="1:1")
```

> 🗄️ **Analogía obligatoria: dos oficinas.** Rentas tiene una **carpeta por
> contribuyente** (el censo). Tesorería tiene **boletas por contribuyente** (los
> pagos). Unir = meter cada boleta en su carpeta. `on="codigo"` es la etiqueta que
> hace calzar boleta con carpeta.

### `how=`: las tres uniones (y qué conserva cada una)

`how` decide **qué filas sobreviven**. Pruébalas sobre los mismos datos:

```python
>>> len(censo.merge(pagado, on="codigo", how="left"))    # TODO el censo
25
>>> len(censo.merge(pagado, on="codigo", how="inner"))   # solo los que están en AMBOS
16
>>> len(censo.merge(pagado, on="codigo", how="outer"))   # TODO de ambos lados
27
```

- **`left` (25):** todas las carpetas, tengan boleta o no. Las sin boleta quedan con
  `pagado = NaN` (9 contribuyentes que no pagaron).
- **`inner` (16):** solo carpetas **con** boleta. Pierdes a los 9 que no pagaron.
- **`outer` (27):** todo: las 25 carpetas + **2 boletas sin carpeta** (¡los
  huérfanos!).

> 📝 **Pregunta 2** del interrogatorio: explica los tres números con carpetas y boletas.

### `indicator=True`: ¿de dónde salió cada fila?

```python
>>> m = censo.merge(pagado, on="codigo", how="outer", indicator=True)
>>> m["_merge"].value_counts()
_merge
both          16
left_only      9
right_only     2
Name: count, dtype: int64
```

`both`: carpeta con boleta. `left_only`: carpeta sin boleta (no pagó).
**`right_only`: boleta sin carpeta — los pagos huérfanos.**

## El misterio de los huérfanos

Esas **2 boletas sin carpeta** son `PS-1032-C` (Cordelería El Nudo Firme) y
`PS-1040-G` (Jugos El Cilindro): pagaron en junio, pero **no están en el censo
limpio**. ¿De dónde salieron? Son contribuyentes que venían en los pagos del
**Lab 04** pero que no sobrevivieron al censo del Lab 05. No se botan en silencio:
van a una sección **"Pagos huérfanos (a investigar)"** del informe — plata que
llegó y hay que explicar (contrato C14: nada desaparece sin rastro).

```python
>>> huerfanos = pagado[~pagado["codigo"].isin(censo["codigo"])]
>>> huerfanos
      codigo  pagado
...  PS-1032-C   83000
...  PS-1040-G   47500
```

> 📝 **Pregunta 3:** ¿qué códigos, cuánto suman, de qué lab vienen y qué harías con esa plata?

### 💥 Rómpelo: el cinturón `validate`

¿Por qué agrupamos los pagos ANTES de unir? Porque sin agrupar hay códigos
repetidos (alguien pagó en junio Y en julio), y un merge "1 a 1" se rompe. El
parámetro `validate="1:1"` es el cinturón que lo detecta:

```python
>>> censo.merge(pagos, on="codigo", how="left", validate="1:1")   # ¡pagos SIN agrupar!
```
```
MergeError: Merge keys are not unique in right dataset; not a one-to-one merge
```

`validate` te obliga a pensar la **cardinalidad**: ¿es 1:1, 1:muchos, muchos:1? Un
merge sin `how` explícito y sin `validate` es un merge que nadie revisó — y los
merges mal hechos duplican filas en silencio. Por eso agrupamos primero (1 fila por
código) y recién ahí unimos (C17).

### 🤖 Pregúntale a la IA

> *"En pandas, ¿qué diferencia hay entre `how='left'`, `'inner'`, `'outer'` y
> `'right'` en un merge? Explícamelo con la analogía de carpetas y boletas, y
> dime en qué caso cada uno pierde información sin avisar."*

## ✅ Checkpoint

- [ ] Apilaste junio+julio con `concat` (20 filas, `ignore_index`).
- [ ] Cruzaste censo×pagos con `merge` y probaste `left`/`inner`/`outer` (25/16/27).
- [ ] Usaste `indicator=True` y encontraste los `right_only` (huérfanos).
- [ ] Identificaste los 2 huérfanos y de qué lab vienen.
- [ ] Provocaste el `MergeError` con `validate` sobre pagos sin agrupar.

Cuando esté todo ✔, sigue con **[Guía 4 — Agregar y pivotear](04-agregar-y-pivotear.md)**.
