# Pista Nivel 3 — Fragmentos 🧩

> *Destapa solo lo que necesites. Pedir un mapa no es perderse; es navegar.*

Fragmentos casi-completos de los pasos más duros. Cada uno deja **el último paso
para ti** (marcado `# ← COMPLETA`). No es la solución entera: es el andamio.

## Fragmento 1 — Las dos hojas del Excel

`sheet_name=None` te devuelve un **diccionario** `{nombre_hoja: DataFrame}` con
TODAS las hojas de una:

```python
hojas = pd.read_excel(ruta_xlsx, sheet_name=None)   # {"S1": df, "S2": df}
pagos = pd.concat(hojas.values(), ignore_index=True)  # apila S1 y S2
# ← COMPLETA: agrupa 'pagos' por codigo y suma 'monto' para obtener lo pagado por contribuyente
```

## Fragmento 2 — El faltante que pandas no conoce

```python
# 's/d' NO es NA por defecto de pandas: hay que declararlo
censo = pd.read_csv(ruta, na_values=["", "S/I", "s/d"])   # ← los TRES marcadores
# ← COMPLETA: homogeneiza estado (strip/upper) y nombre (strip) sobre una COPIA
```

## Fragmento 3 — El consenso de outliers

```python
q1, q3 = df["deuda"].quantile(0.25), df["deuda"].quantile(0.75)
iqr = q3 - q1
cod_iqr = set(df[(df["deuda"] < q1 - 1.5*iqr) | (df["deuda"] > q3 + 1.5*iqr)]["codigo"])
z = (df["deuda"] - df["deuda"].mean()) / df["deuda"].std()   # std muestral (ddof=1)
cod_z = set(df[z.abs() > 3.0]["codigo"])
apartados = cod_iqr & cod_z          # ∩ : solo los que marcan AMBOS
# ← COMPLETA: quédate con las filas cuyo codigo NO esté en 'apartados'
```

## Fragmento 4 — El doble (triple) merge con cinturón

```python
tablero = (censo
    .merge(contrib, on="codigo", how="left", validate="1:1")   # trae giro
    .merge(pagado,  on="codigo", how="left", validate="1:1")   # trae pagado
    .merge(multa,   on="codigo", how="left", validate="1:1"))  # trae multas
tablero["pagado"] = tablero["pagado"].fillna(0).astype(int)
tablero["multas"] = tablero["multas"].fillna(0).astype(int)
# ← COMPLETA: calcula la columna 'saldo' (recuerda: deuda + multas − pagado)
```

## Fragmento 5 — Los huérfanos (anti-join)

```python
# 'pagado' y 'multa' son los DataFrames ya agrupados por codigo
huer_pago  = pagado[~pagado["codigo"].isin(censo["codigo"])]
# ← COMPLETA: haz lo mismo para las multas huérfanas, y súmalas para el informe
```

## Fragmento 6 — El resumen a SQLite

```python
resumen = tablero.groupby("rubro", as_index=False)["saldo"].sum()
con = sqlite3.connect("salidas/gestion.db")
try:
    resumen.to_sql("resumen_anual", con, if_exists="replace", index=False)   # ← COMPLETA si falta algo
finally:
    con.close()
```

## Fragmento 7 — Un gráfico headless (C16)

```python
import matplotlib
matplotlib.use("Agg")            # ANTES de importar pyplot
import matplotlib.pyplot as plt

saldo = tablero.groupby("rubro")["saldo"].sum().sort_index()
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(saldo.index, saldo.values)
ax.set_title("Saldo anual por rubro — Puerto Siracusa")
# ← COMPLETA: etiqueta los ejes, tight_layout, savefig(dpi=150) y plt.close(fig)
#   (y haz el segundo gráfico: conteo por tramo)
```

> Con esto tienes el andamio de las partes difíciles. Ármalo, corre
> `uv run python bin/verificar.py`, y cuando llegues a `9/9`, responde la BITÁCORA
> con TUS números. La arena está contada. 🏖️
