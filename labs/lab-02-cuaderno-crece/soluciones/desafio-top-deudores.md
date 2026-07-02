# Desafío extra — El podio de deudores (top 3)

> Opcional. No lo revisa el verificador; es para que te lleves el gesto de
> "ordenar por un criterio y quedarte con los primeros", que usarás sin parar.

Don Arquímedes quiere un **podio**: las 3 patentes que más deben del fichero
consolidado. En el Lab 01 lo habrías hecho con un bucle acumulador; ahora que
tienes diccionarios, funciones y lambdas, sale en tres líneas.

## La idea: ordenar por deuda y cortar los primeros 3

```python
from consolidar import consolidar
from datos.archivador import REGISTROS_BRUTOS

fichero, _ = consolidar(REGISTROS_BRUTOS)

# fichero.values() son las fichas (dicts). Las ordenamos por su "deuda",
# de mayor a menor, con una lambda que dice "la llave de orden es la deuda".
ordenadas = sorted(fichero.values(), key=lambda ficha: ficha["deuda"], reverse=True)

# Y nos quedamos con las 3 primeras usando slicing (como en el Lab 01).
podio = ordenadas[:3]

for puesto, ficha in enumerate(podio, start=1):
    print(f"{puesto}. {ficha['nombre']} ({ficha['codigo']}): ${ficha['deuda']:,} CLP")
```

## Salida esperada

```
1. Miradores del Istmo (PS-1030-T): $290,000 CLP
2. Tornería El Eje (PS-1038-C): $205,000 CLP
3. Paseos Corriente Austral (PS-1027-T): $154,000 CLP
```

## Las tres piezas, nombradas

- **`sorted(..., key=lambda ...)`** — la `lambda` es una mini-función anónima:
  `lambda ficha: ficha["deuda"]` significa "para ordenar, fíjate en la deuda".
  `sorted` no toca el fichero; devuelve una lista nueva ordenada.
- **`reverse=True`** — de mayor a menor (sin él, el podio saldría al revés).
- **`[:3]`** — slicing: los tres primeros. Cambia el 3 y tienes top 5, top 10…

## Guiño al futuro

Esto que hiciste con `sorted` + `lambda` + slicing es, otra vez, el abuelo de lo
que en pandas será `df.nlargest(3, "deuda")`. Mismo concepto, una línea. Entender
la versión a mano hoy hace que la de mañana no sea magia.
