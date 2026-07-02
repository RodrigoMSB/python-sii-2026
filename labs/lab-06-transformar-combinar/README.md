# Lab 06 — Transformar y combinar 📊

> Módulo 3 (segunda parte) · ~2,0 horas · el pipeline completo del analista:
> transformar, combinar, agregar y **graficar** · añade matplotlib.

## El encargo

El censo quedó limpio (Lab 05) y el Concejo quiere **EL TABLERO**: un cuadro que
cruce lo que cada contribuyente **debe** (censo) con lo que **pagó** (Tesorería,
junio + julio), por rubro y tramo, con totales por donde se mire y un gráfico.

> «Júntalos con criterio y dame el saldo real del puerto — con gráfico, que el
> Concejo vota con los ojos.» — Don Arquímedes

Construirás `tablero.py`: transforma (map/cut/dummies), combina (concat/merge),
agrega (groupby/transform/crosstab/pivot) y grafica (matplotlib), entregando el
tablero del Concejo con cada peso cuadrado.

## Qué vas a aprender

**Transformar:** `map` (dict), `pd.cut` (tramos), `get_dummies`. **Combinar:**
`concat` (apilar), `merge` (`how`, `validate`, huérfanos, `indicator`).
**Agregar:** `groupby`, la diferencia `agg` vs **`transform`**, `crosstab`,
`pivot_table`. **Graficar:** matplotlib básico headless (Agg, `savefig`).

## Dos rutas, un mismo verificador

| Ruta | Para quién | Qué haces |
|------|------------|-----------|
| 🛠️ **Artesano** | Quiero escribir el código | Completas los 6 `TODO` de `plantillas/tablero.py`. |
| 🔎 **Explorador** | Quiero entender leyendo y probando | Ejecutas `soluciones/tablero.py`, con las demos de merge y la modificación de la Pregunta 5. |

## La regla de la casa (sobre la IA) 🤖

La IA está **invitada**: que te explique un `merge` o un `transform`. Pero el
interrogatorio pregunta por lo que pasó en **TU** terminal (el borde del tramo, las
tres uniones, los huérfanos): eso se entiende, no se copia.

## Contrato clave del lab (C16)

Los gráficos se dibujan **headless**: `matplotlib.use("Agg")` antes de importar
pyplot, salida solo por `savefig`, y **jamás** `plt.show()` en un script (cuelga en
terminales sin interfaz gráfica). En Jupyter usarías `show()`; en un script, no.

## Prerrequisitos

- **`uv`** (trae Python 3.13). Instalación:
  [`../../docs/setup-alumno.md`](../../docs/setup-alumno.md).
- **Internet** la primera vez (matplotlib es la descarga más pesada del curso).
- Se recomienda haber hecho los Labs 01–05 (el censo limpio y los pagos vienen de
  ahí; los huérfanos son un hilo narrativo del Lab 04).

Problemas: [`docs/troubleshooting.md`](docs/troubleshooting.md).

## Mapa de las guías

1. **[Guía 1 — El encargo del tablero](guia/01-contexto.md)** — entorno, las 3
   piezas y el mapa del pipeline.
2. **[Guía 2 — Mapear y clasificar](guia/02-mapear-y-clasificar.md)** — `map`,
   `cut`, `get_dummies`.
3. **[Guía 3 — Combinar](guia/03-combinar.md)** — `concat`, `merge` (las tres
   uniones, `validate`, huérfanos).
4. **[Guía 4 — Agregar y pivotear](guia/04-agregar-y-pivotear.md)** — `groupby`,
   `transform`, `crosstab`, `pivot_table`.
5. **[Guía 5 — El tablero](guia/05-tablero.md)** — matplotlib, armar `tablero.py` y
   verificar.

## Verifica tu trabajo

Desde la raíz del lab (`labs/lab-06-transformar-combinar/`):

```bash
uv run python bin/verificar.py
```

Meta: `✔ 14/14 verificaciones correctas`. El verificador es de **solo lectura**,
prueba con datos oficiales y **sorpresa** (mini-censo + pagos con huérfano), valida
que el PNG exista y sea válido, y neutraliza cualquier `breakpoint()` olvidado.

## Para el instructor 🧑‍🏫

- **Recuperar a un rezagado:** `uv run python bin/recuperar_lab.py` (restaura los 3
  CSV con `git checkout`, repone `tablero.py`, regenera salidas y gráfico).
- **Cifras de control:** rubros G/C/T = 11/8/6 · tramos 4/11/7/3 · concat 20 pagos
  $1.213.000 · tablero 25 filas, 9 sin pago, pagado $1.082.500, **saldo
  $2.025.000** · huérfanos {PS-1032-C, PS-1040-G} = $130.500 · saldo por rubro
  C/G/T = 601k/99k/1325k · Buceo = 34% de la deuda de Turismo.
- **Dependencias:** numpy 2.5.0, pandas 3.0.3, openpyxl 3.1.5, **matplotlib 3.11.0**.
- Los 3 CSV son texto versionado (git es la fuente de verdad). `bin/` solo lectura
  (salvo `recuperar_lab.py`); gráficos headless con Agg (C16); merges con `how` y
  `validate` explícitos (C17); sin `breakpoint()` en soluciones/plantillas/bin (C8).
