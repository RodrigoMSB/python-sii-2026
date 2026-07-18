# Guía 1 — La planilla del Concejo

> **Objetivo:** montar el taller (¡ahora con bibliotecas!) y entender de una vez
> por qué existe NumPy: para hacer en una línea lo que antes eran bucles.

## El encargo

Don Arquímedes entra apurado, con una planilla en la mano:

> «Me pidieron en el Concejo el **panorama anual** del puerto: doce meses, tres
> rubros, y lo quieren "con totales por donde se mire" —por mes, por rubro, el
> mejor mes, los meses flojos—. Yo lo intenté con las listas que me enseñó,
> pero se me hizo un enredo de bucles. Tiene que haber una forma más… derecha.»

La hay. Se llama **NumPy**, y después su prima **pandas**. Con ellas, "totales
por donde se mire" son operaciones de una línea.

## Montar el taller (ojo: ahora descarga bibliotecas)

Este es el **primer lab con dependencias externas**. La primera vez, el
preparador descargará numpy y pandas (necesita Internet unos segundos).

**macOS/Linux:**
```bash
cd labs/lab-03-numeros-del-puerto
bash bin/00-preparar.sh
```
**Windows:**
```powershell
cd labs\lab-03-numeros-del-puerto
powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
```

**Salida esperada (la primera vez; puede variar):**
```
[INFO] Descargando las bibliotecas del lab (solo la primera vez, requiere Internet)…
Downloading numpy ...
Downloading pandas ...
[OK] Entorno .venv/ listo con numpy y pandas.
...
[OK] numpy 2.5.0 (correcto).
[OK] pandas 3.0.3 (correcto).

✔ 7/7 verificaciones correctas
```

La segunda vez ya no descarga nada (queda cacheado). ¿Falla la descarga por red
o antivirus? Revisa [`../docs/troubleshooting.md`](../docs/troubleshooting.md).

## ¿Por qué NumPy? La demo que lo explica todo

Abre el REPL: `bash bin/repl.sh`. Trae la planilla y suma el total de **cada mes**,
primero a la antigua (con bucle) y luego a la NumPy:

```python
>>> from datos.recaudacion import RECAUDACION
>>> # A la antigua: recorrer fila por fila sumando
>>> totales = []
>>> for fila in RECAUDACION:
...     totales.append(sum(fila))
...
>>> totales[:3]
[8650000, 8800000, 7960000]
```

Ahora con NumPy:

```python
>>> import numpy as np
>>> m = np.array(RECAUDACION)
>>> m.sum(axis=1)[:3]
array([8650000, 8800000, 7960000])
```

Mismo resultado. Pero fíjate: `m.sum(axis=1)` es **una línea**, sin bucle, sin
lista intermedia. Y sobre millones de datos, además, es muchísimo más rápido.

> 📣 **Analogía: el pregonero.** El bucle es un cobrador que va **timbre por
> timbre**, casa por casa, anotando cada patente. NumPy es el **pregonero** que
> se para en la esquina y le cobra a **toda la cuadra de un solo grito**. Mismo
> cobro, un gesto en vez de cien. A eso se le llama **vectorización**: operar
> sobre todo el arreglo de una vez, en lugar de elemento por elemento.

## Saluda a las dos bibliotecas

```python
>>> import numpy as np
>>> import pandas as pd
>>> np.__version__
'2.5.0'
>>> pd.__version__
'3.0.3'
```

`np` y `pd` son los apodos de rigor (los verás así en todo tutorial del mundo).
NumPy manda en los **números en bloque** (matrices); pandas, en las **tablas con
nombres** (lo verás en la Guía 4).

## ✅ Checkpoint

- [ ] El preparador terminó en `✔ 7/7` (incluye numpy 2.5.0 y pandas 3.0.3).
- [ ] Sumaste los totales mensuales con bucle y con `m.sum(axis=1)`: mismo resultado.
- [ ] Importaste `numpy as np` y `pandas as pd` y viste sus versiones.

Cuando esté todo ✔, sigue con **[Guía 2 — Arrays](02-arrays.md)**.
