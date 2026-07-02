# Desafío extra — El rubro estrella

> Opcional. No lo revisa el verificador; es para que sientas el poder de una
> línea de NumPy.

Don Arquímedes tiene una corazonada: "el Turismo se despertó en el segundo
semestre". Quiere el dato duro: **¿qué rubro creció más, en porcentaje, entre
Junio y Diciembre?**

## Una línea de NumPy

`m[5]` es la fila de Junio (índice 5) y `m[11]` la de Diciembre (índice 11).
Ambas son arrays de 3 rubros. El crecimiento porcentual, elemento a elemento:

```python
import numpy as np
from soluciones.panorama import construir_matriz  # o pega tu construir_matriz
from datos.recaudacion import RUBROS

m = construir_matriz()
crecimiento = (m[11] - m[5]) / m[5] * 100     # % de cambio por rubro, vectorizado

for rubro, pct in zip(RUBROS, crecimiento):
    print(f"{rubro}: {pct:.1f}%")
```

## Salida esperada

```
C: 20.7%
G: 65.6%
T: 289.3%
```

**El rubro estrella es Turismo (T): +289,3 %.** Pasó de $280.000 en Junio a
$1.090.000 en Diciembre. La corazonada de Don Arquímedes era correcta: el puerto
se llena de turistas en verano y eso se ve en la recaudación.

## Lo que acabas de hacer

`(m[11] - m[5]) / m[5] * 100` operó sobre los **tres rubros a la vez**, sin un
solo bucle. Eso es **broadcasting** y **vectorización**: restas dos arrays,
divides por otro y multiplicas por un escalar, y NumPy lo aplica celda a celda.
En listas de Python habrías necesitado un `for`; aquí es una línea que se lee
como la fórmula matemática.

> Guiño: `np.argmax(crecimiento)` te daría directamente la POSICIÓN del rubro
> estrella (2 → Turismo). Pruébalo.
