# Desafío extra — La quinta fuente (un CSV rebelde)

> Opcional. No lo revisa el verificador; es para que domines las "perillas" de
> `read_csv`, las que te salvarán con datos ajenos en el mundo real.

Tesorería manda un **segundo** archivo, pero su sistema viejo exporta distinto:
usa **punto y coma** (`;`) como separador y **coma** como separador decimal
(estilo europeo/latino). Si lo abres con `read_csv` tal cual, pandas se confunde.

## Paso 1 — Crea el archivo a mano

Crea `salidas/pagos_tesoreria_viejo.csv` (en salidas/, que es tuyo) con este
contenido EXACTO (fíjate en los `;` y las comas decimales):

```
codigo;fecha;monto
PS-1006-G;2026-07-01;45000,50
PS-1012-G;2026-07-02;18000,00
PS-1017-G;2026-07-03;76000,75
```

## Paso 2 — Léelo con las perillas correctas

```python
import pandas as pd

# Sin perillas, pandas lee UNA sola columna llena de ; y comas: un desastre.
malo = pd.read_csv("salidas/pagos_tesoreria_viejo.csv")
print(malo.shape)        # (3, 1)  ← ¡todo apelotonado en una columna!

# Con las perillas: sep=";" (separador) y decimal="," (coma decimal)
bueno = pd.read_csv("salidas/pagos_tesoreria_viejo.csv", sep=";", decimal=",")
print(bueno.shape)                 # (3, 3)
print(bueno.dtypes["monto"])       # float64  ← ahora sí es número
print(bueno["monto"].sum())        # 139001.25
```

## Salida esperada

```
(3, 1)
(3, 3)
float64
139001.25
```

## La lección

`read_csv` tiene decenas de "perillas" (`sep`, `decimal`, `thousands`,
`encoding`, `header`, `names`, `skiprows`, …). Cuando un CSV ajeno "se ve raro"
al cargarlo, no es que pandas esté roto: es que hay que decirle **cómo** está
escrito ese archivo en particular. Dos que memorizar hoy:

- `sep=";"` → cuando el separador no es la coma.
- `decimal=","` → cuando los decimales usan coma (y, de paso, `thousands="."`
  cuando los miles usan punto, como en `"45.000"`).

> Guiño a la Pregunta 4: si Tesorería hubiera escrito `"45.000"` pensando en
> "cuarenta y cinco mil", `thousands="."` le dice a pandas que ese punto es
> separador de miles, no decimal — y lo lee como el entero `45000`.
