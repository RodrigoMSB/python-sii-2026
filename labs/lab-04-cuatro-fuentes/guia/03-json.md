# Guía 3 — JSON

> **Objetivo:** leer la tercera fuente por sus **dos caminos** (stdlib y pandas)
> y entender cuándo conviene cada uno.

REPL abierto (`uv run python`).

## Anatomía de un JSON

Abre `datos/fuentes/multas.json` en tu editor. Verás algo así:

```json
[
  {
    "codigo": "PS-1007-T",
    "motivo": "Operar sin señalética de seguridad",
    "monto": 25000
  },
  {
    "codigo": "PS-1013-C",
    "motivo": "Venta fuera de horario autorizado",
    "monto": 50000
  }
]
```

Es **texto** con una estructura estricta: una **lista** `[...]` de **objetos**
`{...}`, cada objeto con pares `"clave": valor`. Si conoces los diccionarios y
listas de Python, ya sabes leer JSON: es casi lo mismo.

## Camino 1 — `json.load` (stdlib): el puente dict → DataFrame

```python
>>> import json
>>> with open("datos/fuentes/multas.json", encoding="utf-8") as f:
...     multas = json.load(f)
...
>>> type(multas)
<class 'list'>
>>> multas[0]
{'codigo': 'PS-1007-T', 'motivo': 'Operar sin señalética de seguridad', 'monto': 25000}
```

### 🔮 Predice antes de ejecutar

¿Qué **tipo Python** crees que devolvió `json.load`? (mira el `[...]` del
archivo). Ya lo viste arriba: una **`list`** de **`dict`**. `json.load` traduce
el texto JSON a objetos Python normales: `[]`→list, `{}`→dict, `"..."`→str,
números→int/float. Y una lista de dicts, pandas la convierte en tabla de una:

```python
>>> import pandas as pd
>>> df = pd.DataFrame(multas)
>>> df.shape
(10, 3)
>>> int(df["monto"].sum())
395000
```

> 📝 **Pregunta 3:** anota qué tipo te devolvió `json.load`.

## Camino 2 — `pd.read_json` (directo)

pandas también lee JSON de un tirón, sin pasar por `json.load`:

```python
>>> df2 = pd.read_json("datos/fuentes/multas.json")
>>> df2.shape
(10, 3)
```

Mismo resultado. Entonces, ¿cuál usar?

| Camino | Cuándo conviene |
|--------|-----------------|
| `json.load` (stdlib) | Cuando necesitas **inspeccionar o transformar** los datos ANTES de armar la tabla (filtrar, renombrar, aplanar objetos anidados). Ves los dicts en crudo. |
| `pd.read_json` | Cuando el JSON **ya tiene forma tabular** (lista de objetos planos) y solo quieres la tabla, sin escalas. |

En este lab la solución usa `json.load` para que **veas el puente** dict→DataFrame
con tus propios ojos. En datos anidados de verdad, ese control extra es oro.

## 💥 Rómpelo: un JSON con una coma de más

El JSON es estricto con su sintaxis. Vamos a romperlo **en una copia** (jamás la
fuente original):

```bash
cp datos/fuentes/multas.json salidas/multas_roto.json
```
Abre `salidas/multas_roto.json` y **agrega una coma** después del último objeto,
justo antes del `]` de cierre (una coma "colgante"). Guárdalo e intenta leerlo:

```python
>>> import json
>>> with open("salidas/multas_roto.json", encoding="utf-8") as f:
...     json.load(f)
...
```
```
json.decoder.JSONDecodeError: Expecting value: line 42 column 3 (char 980)
```

`JSONDecodeError` — y te dice **línea y columna** exactas del problema. Es el
error más honesto del ecosistema: no adivina, no "arregla" silenciosamente, te
manda directo al carácter culpable. Ve a esa línea, quita la coma colgante y
volverá a cargar. (La fuente original sigue intacta: solo rompiste tu copia.)

## ✅ Checkpoint

- [ ] Leíste `multas.json` con `json.load` y viste que da una `list` de `dict`.
- [ ] Convertiste esa lista en DataFrame y sumaste ($395.000).
- [ ] Leíste lo mismo con `pd.read_json` y entendiste cuándo usar cada camino.
- [ ] Rompiste una COPIA del JSON y leíste el `JSONDecodeError` (línea y columna).

Cuando esté todo ✔, sigue con **[Guía 4 — Base de datos](04-base-de-datos.md)**.
