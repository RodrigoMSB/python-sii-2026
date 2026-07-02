# Guía 2 — Mapear y clasificar

> **Objetivo:** transformar columnas para que digan algo: la letra del código →
> nombre del rubro, el monto → tramo de deuda, el estado → columnas de sí/no.

REPL abierto (`uv run python`), con el censo cargado.

## `map`: el timbre traductor

La última letra del código es el rubro (`C`, `G`, `T`), pero al Concejo esas
siglas no le dicen nada. `Series.map` traduce **cada valor** según un diccionario:

```python
>>> import pandas as pd
>>> censo = pd.read_csv("datos/censo_limpio.csv")
>>> censo["rubro"] = censo["codigo"].str[-1].map({"C": "Comercio", "G": "Gastronomía", "T": "Turismo"})
>>> censo["rubro"].value_counts()
rubro
Gastronomía    11
Comercio        8
Turismo         6
Name: count, dtype: int64
```

`censo["codigo"].str[-1]` saca la última letra (accessor `.str`, Guía del Lab 05);
`.map(dict)` la cambia por el nombre completo.

> 🏷️ **Analogía obligatoria: el timbre traductor de la oficina de partes.** Entra
> un documento con una sigla, el funcionario le estampa el nombre completo con su
> timbre, y sale legible. `map` es ese timbre: entra `G`, sale `Gastronomía`.

### 🔮 Predice: ¿y si aparece una letra que no está en el diccionario?

```python
>>> pd.Series(["C", "G", "X"]).map({"C": "Comercio", "G": "Gastronomía", "T": "Turismo"})
```

<details>
<summary>Ver respuesta</summary>

`X` se convierte en **`NaN`**: `map` deja como faltante todo lo que **no esté** en
el diccionario. Es una buena red de seguridad — si mañana llega un rubro nuevo sin
traducir, no se disfraza de otro: aparece como NaN y lo notas.
</details>

## `cut`: clasificar en tramos

El Concejo quiere saber "¿cuántos deben poco y cuántos deben una fortuna?".
`pd.cut` **discretiza** un número continuo en **tramos** con nombre:

```python
>>> bins = [-1, 0, 100000, 300000, 10**9]
>>> labels = ["Sin deuda", "Baja", "Media", "Alta"]
>>> censo["tramo"] = pd.cut(censo["deuda"], bins=bins, labels=labels)
>>> censo["tramo"].value_counts().sort_index()
tramo
Sin deuda     4
Baja         11
Media         7
Alta          3
Name: count, dtype: int64
```

Los **bins** son los bordes: `(-1, 0]` → "Sin deuda", `(0, 100000]` → "Baja",
`(100000, 300000]` → "Media", `(300000, 10⁹]` → "Alta". (Los "tramos de impuesto"
del mundo real: la analogía es literal aquí 😄.)

### 💥 Rómpelo: ¿en qué tramo cae EXACTAMENTE 100.000?

Predícelo y comprueba:

```python
>>> pd.cut([100000], bins=bins, labels=labels)[0]
```

<details>
<summary>Ver respuesta</summary>

Cae en **"Baja"**. Por defecto `cut` usa el **borde derecho incluyente**: el
intervalo es `(0, 100000]`, así que 100.000 pertenece a "Baja", no a "Media". Si
quisieras lo contrario, existe `right=False`. Saber de qué lado cae un borde
**exacto** evita errores de clasificación que nadie nota hasta que alguien reclama.
</details>

> 📝 **Pregunta 1** del interrogatorio: ¿en qué tramo cayó el $100.000 y por qué?

## `get_dummies`: de categoría a columnas de sí/no

Las máquinas (y los modelos estadísticos) no entienden `"VENCIDA"`; entienden
números. `pd.get_dummies` convierte una columna categórica en varias columnas de
**verdadero/falso**, una por categoría:

```python
>>> pd.get_dummies(censo["estado"]).head(3)
   SUSPENDIDA  VENCIDA  VIGENTE
0       False    False     True
1       False     True    False
2       False     True    False
>>> pd.get_dummies(censo["estado"]).dtypes.iloc[0]
dtype('bool')
```

Cada patente queda con un `True` en su estado y `False` en el resto (one-hot). El
`dtype` es **`bool`** — lo moderno de pandas (antes era `uint8`). ¿Para qué sirve?
Es la antesala de los modelos: cuando en el curso avanzado alimentes datos a un
algoritmo, así es como entran las categorías.

## ✅ Checkpoint

- [ ] Tradujiste la letra a rubro con `map` (Gastronomía 11, Comercio 8, Turismo 6).
- [ ] Viste qué hace `map` con un valor fuera del diccionario (NaN).
- [ ] Clasificaste la deuda en tramos con `cut` (4/11/7/3).
- [ ] Comprobaste en qué tramo cae exactamente $100.000 (Baja, borde derecho).
- [ ] Generaste dummies del estado (dtype bool).

Cuando esté todo ✔, sigue con **[Guía 3 — Combinar](03-combinar.md)**.
