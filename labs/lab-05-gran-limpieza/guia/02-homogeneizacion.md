# Guía 2 — Homogeneización

> **Objetivo:** unificar el texto desordenado y convertir los faltantes disfrazados
> en `NaN` de verdad. Dos herramientas: el accessor `.str` y `na_values`.

REPL abierto (`bash bin/repl.sh`), `import pandas as pd`.

## El accessor `.str`: una operación, toda la columna

Recuerda del Lab 01 que un texto sabe hacer `.strip()`, `.upper()`, `.title()`.
En pandas, el accessor **`.str`** aplica esos métodos a **toda la columna de una
vez**, sin bucles:

```python
>>> df = pd.read_csv("datos/censo_patentes.csv")
>>> df["estado"] = df["estado"].str.strip().str.upper()
>>> df["nombre"] = df["nombre"].str.strip()
```

`.str.strip()` quita los espacios de los bordes (adiós ` VENCIDA ` y `vigente `);
`.str.upper()` lleva todo a MAYÚSCULAS. El momento de la verdad:

```python
>>> df["estado"].value_counts()
estado
VENCIDA       14
VIGENTE       11
SUSPENDIDA     5
Name: count, dtype: int64
```

**De 10 variantes a 3.** Ese salto de `value_counts` antes/después es el momento
de satisfacción del lab: el desorden del practicante, ordenado en dos líneas.

### 💥 Rómpelo: por qué el filtro "no encontraba" nada

Antes de homogeneizar, intenta filtrar las vigentes a mano:

```python
>>> crudo = pd.read_csv("datos/censo_patentes.csv")
>>> (crudo["estado"] == "VIGENTE").sum()
```

Te dará **menos** de las que hay realmente, porque `vigente`, `Vigente` y
`vigente ` **no** son iguales a `"VIGENTE"` para Python:

```python
>>> "VIGENTE" == "vigente "
False
```

Un espacio o una minúscula y el filtro las ignora en silencio — el error más
traicionero, porque **no avisa**: simplemente cuenta mal. Por eso se homogeneiza
**antes** de filtrar. (Guarda esto para la Pregunta 1.)

## Los faltantes disfrazados: `na_values`

En la Guía 1 viste que `deuda` llegó como texto porque los faltantes venían como
`S/I`, `sin dato` o celda vacía. Le decimos a `read_csv` que trate esos tres
marcadores como **ausente** (`NaN`):

```python
>>> df = pd.read_csv("datos/censo_patentes.csv",
...                  na_values=["", "S/I", "sin dato"])
>>> df["deuda"].dtype
dtype('float64')
>>> df["deuda"].isna().sum()
3
```

Ahora `deuda` es numérica (`float64`, porque el `NaN` obliga a decimales) y pandas
sabe que faltan **3** valores. Unificar los marcadores de faltante es el primer
paso para poder tratarlos.

## Tratar los faltantes: `fillna` vs `dropna`

Hay dos caminos, y elegir es una **decisión de negocio**, no técnica:

```python
>>> df["deuda"].fillna(0)       # RELLENAR con un valor (aquí, 0)
>>> df.dropna(subset=["deuda"]) # BORRAR las filas con deuda faltante
```

- `dropna` **borra** las filas incompletas. Sirve si un dato faltante hace la fila
  inútil.
- `fillna` **rellena** con un valor que tú decides. Sirve si puedes asumir algo
  razonable.

En este lab seguimos la **regla de Don Arquímedes**: *"la deuda no informada se
asume 0 y se marca para verificación en terreno"*. Es decir, `fillna(0)` — pero
con la conciencia de que 0 **no es la verdad**, es una decisión trazable (por eso
el pipeline la cuenta). El riesgo: si esas patentes sí debían, subestimamos la
morosidad. Ese trade-off es la Pregunta 4.

## ✅ Checkpoint

- [ ] Homogeneizaste `estado` con `.str.strip().str.upper()` (10 → 3) y `nombre`.
- [ ] Viste por qué un filtro fallaba antes de homogeneizar (espacios/mayúsculas).
- [ ] Cargaste con `na_values` y confirmaste `deuda` float con 3 NaN.
- [ ] Entendiste `fillna` vs `dropna` y la regla de negocio del lab.

Cuando esté todo ✔, sigue con **[Guía 3 — Duplicados y filtrado](03-duplicados-y-filtrado.md)**.
