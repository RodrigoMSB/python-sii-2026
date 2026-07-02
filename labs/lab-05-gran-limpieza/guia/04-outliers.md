# Guía 4 — Outliers

> **Objetivo:** detectar valores extremos por DOS métodos (IQR y z-score),
> descubrir que **no siempre coinciden**, y aprender la lección más importante del
> lab: los métodos proponen, el analista dispone.

REPL abierto; ten el censo cargado, homogeneizado, deduplicado, con códigos
filtrados y deudas imputadas (las 26 filas del pipeline hasta aquí).

## `describe` como radar

```python
>>> df["deuda"].describe()
```

El `max` de **9.999.999** brilla al lado de una mediana de decenas de miles. Un
outlier grita en `describe`. Pero "grita" no es "culpable": hay que **medir** cuán
lejos está, y decidir.

## Método 1 — IQR (rango intercuartílico)

Los **cuartiles** parten los datos en cuatro. Q1 deja abajo el 25 %; Q3, el 75 %.
El **IQR** = Q3 − Q1 es el "ancho típico" del grueso de los datos. Un valor es
outlier si cae más de **1,5 · IQR** por fuera de esa caja:

```python
>>> q1 = df["deuda"].quantile(0.25)
>>> q3 = df["deuda"].quantile(0.75)
>>> iqr = q3 - q1
>>> q1, q3, iqr
(29000.0, 200000.0, 171000.0)
>>> limite_sup = q3 + 1.5 * iqr
>>> limite_sup
456500.0
>>> df[df["deuda"] > limite_sup]["codigo"].tolist()
['PS-1022-T', 'PS-1046-C']
```

> 🎣 **Analogía obligatoria: la vara del pescador.** El pescador conoce el tamaño
> típico del cardumen. Lo que mide **fuera de su vara** lo aparta para
> **revisarlo** — no para botarlo: podría ser el **pez récord** de su vida… o una
> **bota** enganchada. IQR es esa vara: te dice qué revisar, no qué descartar.

IQR acusa a **dos**: `PS-1022-T` (520.000) y `PS-1046-C` (9.999.999).

## Método 2 — z-score (desviaciones respecto a la media)

El **z-score** mide a cuántas **desviaciones estándar** está un valor de la media.
Regla común: |z| > 3 es sospechoso. Ojo con la desviación: usamos la **muestral**
(`std()` de pandas, `ddof=1`).

```python
>>> media = df["deuda"].mean()
>>> desv = df["deuda"].std()          # muestral (ddof=1), NO el módulo statistics
>>> z = (df["deuda"] - media) / desv
>>> df[z.abs() > 3]["codigo"].tolist()
['PS-1046-C']
```

> ⚠️ **La trampa de `statistics` (C15).** El módulo `statistics` de la stdlib y
> pandas calculan la desviación de formas distintas por defecto (población vs
> muestra), y los cuartiles de `statistics.quantiles` no coinciden con
> `Series.quantile`. Mezclarlos da números que "casi" cuadran y te vuelven loco.
> **Quédate con pandas** para todo el análisis.

### 🔮 Predice antes de ejecutar

Antes de correr el z-score, **predice**: ¿marcará también a `PS-1022-T` (520.000)?

<details>
<summary>Ver respuesta</summary>

**No.** El z-score de `PS-1022-T` es ≈ 0,01 — casi en la media, porque el gigante
de 9.999.999 infló tanto la media y la desviación que 520.000 quedó "cerca". El
z-score solo marca a `PS-1046-C` (z ≈ 4,9). **IQR acusa a dos; z-score, a uno.**
</details>

## El desacuerdo y la investigación

Los métodos no coinciden. ¿Quién tiene razón? **Ninguno solo.** Aquí entra el
analista:

- **`PS-1022-T` — Buceo Fondo Claro, 520.000.** ¿Te suena? Es un **viejo conocido**:
  aparece desde el Lab 01 con esa misma deuda. Tiene **historia**. Es un negocio
  real que simplemente debe bastante. IQR lo señaló por grande, pero **no es un
  error** → se **CONSERVA** (con una nota, para no olvidarlo).
- **`PS-1046-C` — Distribuidora El Quintal, 9.999.999.** No tiene historia en
  ningún lab. Nueve millones novecientos noventa y nueve mil novecientos noventa y
  nueve: siete nueves, el clásico **dedo dormido sobre el teclado**. Ambos métodos
  lo marcan → es un **error de digitación** → se **APARTA**.

La regla de decisión del pipeline: **se aparta solo lo que señalan AMBOS métodos**
(el consenso). Lo que marca solo IQR se conserva, con nota.

> **Los métodos proponen; el analista dispone — y todo veredicto queda escrito.**

Esa última frase (todo queda escrito) es el contrato C14: cada outlier, conservado
o apartado, va al reporte con su razón. Limpiar sin dejar rastro está prohibido.

## ✅ Checkpoint

- [ ] Calculaste Q1, Q3, IQR y el límite superior; IQR marcó `PS-1022-T` y `PS-1046-C`.
- [ ] Calculaste el z-score (std muestral) y viste que marca solo `PS-1046-C`.
- [ ] Predijiste (y confirmaste) que el z-score NO marca a Buceo Fondo Claro.
- [ ] Entendiste el veredicto de cada outlier y por qué el analista decide.

Cuando esté todo ✔, sigue con **[Guía 5 — El pipeline](05-pipeline.md)**.
