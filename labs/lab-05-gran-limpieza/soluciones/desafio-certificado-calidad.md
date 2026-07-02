# Desafío extra — El certificado de calidad

> Opcional. No lo revisa el verificador; es para que aprendas a **medir la mugre
> antes de limpiarla** (el diagnóstico que todo analista hace primero).

Don Arquímedes quiere, antes de aprobar cualquier limpieza, un **certificado de
calidad** del censo bruto: un vistazo rápido de qué tan sucio viene. Escribe una
función que reciba el censo **crudo** (sin limpiar) y devuelva tres indicadores.

## La función

```python
import pandas as pd

def certificado_calidad(ruta):
    # Cargamos con los marcadores de faltante unificados en NaN,
    # para poder MEDIR la completitud real.
    df = pd.read_csv(ruta, na_values=["", "S/I", "sin dato"])

    # 1) % de completitud por columna (notna = no faltante).
    completitud = (df.notna().mean() * 100).round(1).to_dict()

    # 2) Variantes crudas de 'estado' (antes de homogeneizar).
    variantes_estado = int(df["estado"].nunique())

    # 3) Candidatos a duplicado por código (aparecen más de una vez).
    dup_mask = df["codigo"].duplicated(keep=False)
    candidatos_dup = sorted(df[dup_mask]["codigo"].unique().tolist())

    return {
        "completitud": completitud,
        "variantes_estado": variantes_estado,
        "candidatos_duplicado": candidatos_dup,
    }

from pathlib import Path
print(certificado_calidad(Path("datos/censo_patentes.csv")))
```

## Salida esperada

```
{'completitud': {'codigo': 100.0, 'nombre': 100.0, 'estado': 100.0, 'deuda': 90.0},
 'variantes_estado': 10,
 'candidatos_duplicado': ['PS-1005-C', 'PS-1020-G']}
```

## Lectura del certificado

- **Completitud:** `deuda` está al **90 %** (3 de 30 celdas faltan). Las otras
  columnas, completas. Ese 90 % es exactamente lo que tu pipeline tuvo que imputar.
- **Variantes de estado: 10** — el desorden del practicante, medido. Tras
  homogeneizar quedarán 3.
- **Candidatos a duplicado:** `PS-1005-C` y `PS-1020-G` aparecen más de una vez.
  Ojo con la palabra "candidatos": `duplicated(keep=False)` marca **todas** las
  apariciones de un código repetido, pero eso no siempre significa fila idéntica
  (podrían diferir en deuda — ahí decidirías con `subset` y `keep`). En este censo
  sí son exactas, y por eso `drop_duplicates()` se las lleva.

## La lección

Un buen analista **mide antes de tocar**. Este certificado es el "antes"; el
informe de limpieza es el "después". Entre ambos, cada decisión quedó escrita.
