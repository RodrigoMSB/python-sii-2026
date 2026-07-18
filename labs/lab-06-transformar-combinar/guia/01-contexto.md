# Guía 1 — El encargo del tablero

> **Objetivo:** montar el entorno (con matplotlib) y conocer las tres piezas que
> vas a cruzar, junto con el mapa del pipeline completo.

## El encargo

El censo quedó limpio (Lab 05) y el Concejo Municipal huele resultados: quiere
**EL TABLERO** — un solo cuadro que cruce lo que cada contribuyente **debe**
(censo) con lo que efectivamente **pagó** (Tesorería, junio y julio), por rubro y
tramo de deuda, con totales por donde se mire… y un gráfico.

> «Tengo el censo por un lado y los pagos por otro. Júntalos con criterio y dame el
> saldo real de este puerto — con gráfico, que el Concejo vota con los ojos.» —
> Don Arquímedes

## Montar el taller (matplotlib es la descarga más pesada del curso)

```bash
cd labs/lab-06-transformar-combinar
bash bin/00-preparar.sh          # Windows: powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
```

La primera vez descarga **matplotlib** (unos MB — ten paciencia). Meta: `✔ 11/11`
(incluye matplotlib 3.11.0 y los 3 CSV con sus conteos exactos).

## Las tres piezas

Ábrelas y míralas (REPL: `bash bin/repl.sh`):

```python
>>> import pandas as pd
>>> censo = pd.read_csv("datos/censo_limpio.csv")
>>> censo.shape
(25, 4)
>>> pd.read_csv("datos/pagos_junio.csv").shape
(12, 3)
>>> pd.read_csv("datos/pagos_julio.csv").shape
(8, 3)
```

- **`censo_limpio.csv`** — 25 patentes con su deuda. ¿Te suena? Es **tu trabajo del
  Lab 05**: el censo que limpiaste, ahora es tu **materia prima**. Así se encadenan
  los proyectos de verdad: la salida de uno es la entrada del siguiente.
- **`pagos_junio.csv`** — 12 pagos (los del Lab 04).
- **`pagos_julio.csv`** — 8 pagos nuevos.

> 🕵️ Un adelanto intrigante: en los pagos de junio hay dos códigos —`PS-1032-C` y
> `PS-1040-G`— que **no están** en el censo limpio. ¿Pagaron fantasmas? Lo
> resolverás en la Guía 3 (los **huérfanos**).

## El mapa del pipeline

Este lab es una **cadena de cuatro eslabones**. Ten el mapa a la vista:

```
   TRANSFORMAR          COMBINAR            AGREGAR             GRAFICAR
   ───────────          ────────            ───────             ────────
   map  (rubro)         concat (meses)      groupby (rubro)     matplotlib
   cut  (tramo)         merge  (deuda×pago) transform (%)       barras → PNG
   dummies (estado)     → huérfanos         crosstab / pivot
```

- **Transformar** (Guía 2): darle sentido a cada columna (la letra → rubro, el
  monto → tramo, el estado → columnas de sí/no).
- **Combinar** (Guía 3): apilar los meses (`concat`) y cruzar deuda con pagos
  (`merge`).
- **Agregar** (Guía 4): totales por grupo (`groupby`), el % dentro del grupo
  (`transform`), y los cuadros cruzados (`crosstab`, `pivot_table`).
- **Graficar** (Guía 5): el dibujito que el Concejo aprueba con los ojos.

## ✅ Checkpoint

- [ ] El preparador terminó en `✔ 11/11` (incluye matplotlib y los 3 CSV).
- [ ] Miraste las tres piezas y reconociste el censo del Lab 05 como materia prima.
- [ ] Tienes el mapa del pipeline (transformar → combinar → agregar → graficar).

Cuando esté todo ✔, sigue con **[Guía 2 — Mapear y clasificar](02-mapear-y-clasificar.md)**.
