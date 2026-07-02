# Guía 2 — CSV y Excel

> **Objetivo:** leer las dos primeras fuentes con pandas y adquirir el ritual de
> inspeccionar todo lo que cargas.

REPL abierto (`uv run python`), `import pandas as pd`.

## Leer el CSV de Tesorería

```python
>>> import pandas as pd
>>> pagos = pd.read_csv("datos/fuentes/pagos.csv", encoding="utf-8")
>>> pagos.head()
      codigo       fecha  monto
0  PS-1006-G  2026-06-02  45000
1  PS-1012-G  2026-06-03  18000
2  PS-1017-G  2026-06-05  76000
3  PS-1020-G  2026-06-08  33500
4  PS-1005-C  2026-06-09  92000
```

Una línea y el CSV es un DataFrame. El `encoding="utf-8"` es explícito a
propósito (contrato del curso): así los acentos nunca se rompen, aquí ni en
Windows.

### 🔮 Predice el dtype del dinero

Antes de mirar, **predice**: ¿de qué tipo crees que quedó la columna `monto`?

```python
>>> pagos.info()
```

<details>
<summary>Ver respuesta</summary>

`monto` quedó como **`int64`**: pandas vio que eran números enteros y los cargó
como enteros. `codigo` y `fecha` quedaron como `str` (texto). Que pandas adivine
bien el tipo depende de cómo esté escrito el archivo; por eso **siempre** se
inspecciona (Pregunta 4).
</details>

> 🎛️ **Las perillas de `read_csv`.** Nuestro CSV es limpio, pero los ajenos no
> siempre: `read_csv` tiene perillas para adaptarse — `sep=";"` (otro
> separador), `decimal=","` (coma decimal), `thousands="."` (punto de miles),
> `encoding=` (otra codificación). Las verás en acción en el desafío final.

## El ritual: `head`, `info`, `dtypes`

Cada vez que cargas datos, míralos antes de confiar:

```python
>>> pagos.shape
(12, 3)
>>> pagos.dtypes
codigo    str
fecha     str
monto     int64
dtype: object
>>> int(pagos["monto"].sum())
677500
```

12 pagos, $677.500 en total. Cargar sin inspeccionar es como firmar sin leer.

## Leer el Excel de Turismo

El Excel puede tener varias **hojas**; hay que decir cuál:

```python
>>> permisos = pd.read_excel("datos/fuentes/permisos_eventos.xlsx", sheet_name="Permisos")
>>> permisos.head(3)
    folio                            evento   valor
0  EV-201                   Feria del Erizo  120000
1  EV-202             Regata de la Espiral   85000
2  EV-203  Festival del Grito del Pregonero  150000
```

Por dentro, pandas usa **openpyxl** (la biblioteca que instalaste) para abrir el
`.xlsx`. Por eso era una dependencia del lab.

### 💥 Rómpelo: el nombre de la hoja importa

```python
>>> pd.read_excel("datos/fuentes/permisos_eventos.xlsx", sheet_name="permisos")
```
```
ValueError: Worksheet named 'permisos' not found
```

La hoja se llama `Permisos` (con mayúscula), no `permisos`. Como con las columnas
en el Lab 03, **las mayúsculas importan**. El error es clarísimo: "no encontré una
hoja con ese nombre".

## Sana paranoia: el $1.000.000 redondo

```python
>>> int(permisos["valor"].sum())
1000000
```

¿Un millón **exacto**? En datos reales, un número tan redondo da para
desconfiar (¿lo inventaron? ¿lo redondearon?). Verifica en dos pasos: mira los
valores uno por uno, y pídele a pandas un resumen estadístico:

```python
>>> permisos["valor"].describe()
count         8.000000
mean     125000.000000
min       75000.000000
max      200000.000000
Name: valor, dtype: float64
```

8 permisos, promedio $125.000, entre $75.000 y $200.000: cifras plausibles que
**suman** el millón. Era real; solo un bonito azar. Desconfiar y verificar dos
veces es lo que separa a un analista de una calculadora.

## ✅ Checkpoint

- [ ] Leíste `pagos.csv` con `read_csv` y confirmaste que `monto` es `int64`.
- [ ] Aplicaste el ritual `head`/`info`/`dtypes` y sumaste ($677.500).
- [ ] Leíste `permisos_eventos.xlsx` con `sheet_name="Permisos"`.
- [ ] Provocaste el error con la hoja `"permisos"` en minúscula.
- [ ] Verificaste el $1.000.000 con `describe()` (sana paranoia).

Cuando esté todo ✔, sigue con **[Guía 3 — JSON](03-json.md)**.
