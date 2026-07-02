"""Transformar y combinar — PLANTILLA para la Ruta Artesano 🛠️ (Lab 06).

Este archivo YA CORRE, pero el tablero miente: sin rubros, sin tramos, sin pagos
cruzados y sin gráfico. Completa los seis TODO para armar el tablero del Concejo.

Reglas del juego:
  - Copia este archivo a la raíz del lab con el nombre tablero.py
        (macOS/Linux)  cp plantillas/tablero.py tablero.py
        (Windows)      Copy-Item plantillas\\tablero.py tablero.py
  - Completa los TODO EN ORDEN (1 → 6). Ejecuta seguido:  uv run python tablero.py
  - ¿Trabado >10 min? Mira SOLO esa función en soluciones/tablero.py.

Se ejecuta SIEMPRE desde la raíz del lab:

    uv run python tablero.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")            # C16: backend headless ANTES de importar pyplot
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "datos"
SALIDAS = RAIZ / "salidas"

RUBRO_NOMBRE = {"C": "Comercio", "G": "Gastronomía", "T": "Turismo"}
BINS_DEUDA = [-1, 0, 100_000, 300_000, 10**9]
LABELS_DEUDA = ["Sin deuda", "Baja", "Media", "Alta"]


def cargar_censo(ruta):
    return pd.read_csv(ruta, encoding="utf-8")


def cargar_pagos(ruta):
    return pd.read_csv(ruta, encoding="utf-8")


def agregar_rubro(df):
    """Agrega la columna 'rubro' traduciendo la última letra del código."""
    df = df.copy()
    # TODO 1 — La última letra del código es el rubro. Tradúcela con map y el dict:
    #   df["rubro"] = df["codigo"].str[-1].map(RUBRO_NOMBRE)
    df["rubro"] = "(sin rubro)"
    return df


def clasificar_deuda(df):
    """Agrega la columna 'tramo' discretizando la deuda con pd.cut."""
    df = df.copy()
    # TODO 2 — Discretiza la deuda en tramos con pd.cut (los bordes y etiquetas ya
    #   están en BINS_DEUDA y LABELS_DEUDA):
    #   df["tramo"] = pd.cut(df["deuda"], bins=BINS_DEUDA, labels=LABELS_DEUDA)
    df["tramo"] = "(sin tramo)"
    return df


def dummies_estado(df):
    """Variables dummy (one-hot) del estado. dtype bool (lo moderno de pandas)."""
    return pd.get_dummies(df["estado"])


def consolidar_pagos(df_junio, df_julio):
    """Apila los pagos de los dos meses. ignore_index para no repetir índices."""
    # TODO 3 — Apila junio y julio con pd.concat([...], ignore_index=True).
    #   Sin ignore_index, los índices se repiten (0..n en cada mes).
    return df_junio


def construir_tablero(censo, pagos):
    """Cruza deuda (censo) con pagos. Retorna (tablero, huérfanos)."""
    censo = censo.copy()
    pagado = pagos.groupby("codigo", as_index=False)["monto"].sum().rename(
        columns={"monto": "pagado"})
    # TODO 4 — Une el censo con lo pagado. merge LEFT conserva TODO el censo aunque
    #   no haya pagado (C17: how y validate explícitos):
    #     tablero = censo.merge(pagado, on="codigo", how="left", validate="1:1")
    #     tablero["pagado"] = tablero["pagado"].fillna(0).astype(int)
    #   (¿qué pasaría con how="inner"? Pruébalo antes de decidir.)
    tablero = censo.copy()
    tablero["pagado"] = 0
    tablero["saldo"] = tablero["deuda"] - tablero["pagado"]
    huerfanos = pagado[~pagado["codigo"].isin(censo["codigo"])].copy()
    return tablero, huerfanos


def resumen_por_rubro(tablero):
    """Suma deuda, pagado y saldo por rubro."""
    return tablero.groupby("rubro", as_index=False)[["deuda", "pagado", "saldo"]].sum()


def pct_dentro_del_rubro(tablero):
    """Agrega 'pct_rubro': qué % de la deuda de su rubro representa cada fila."""
    tablero = tablero.copy()
    # TODO 5 — transform devuelve una serie del MISMO LARGO que el df (a diferencia
    #   de agg, que colapsa). Así puedes dividir fila a fila:
    #     total_rubro = tablero.groupby("rubro")["deuda"].transform("sum")
    #     tablero["pct_rubro"] = (tablero["deuda"] / total_rubro * 100).round(1)
    tablero["pct_rubro"] = 0.0
    return tablero


def tabla_cruzada(tablero):
    """Conteo cruzado estado × rubro."""
    return pd.crosstab(tablero["estado"], tablero["rubro"])


def pivote_deuda(tablero):
    """Pivote de deuda: rubro (filas) × estado (columnas), sumada."""
    return tablero.pivot_table(values="deuda", index="rubro", columns="estado",
                               aggfunc="sum", fill_value=0)


def graficar_saldo(tablero, ruta_png):
    """Gráfico de barras del saldo por rubro. Headless (C16): Agg + savefig + close."""
    resumen = tablero.groupby("rubro")["saldo"].sum().sort_index()
    # TODO 6 — Cinco líneas de matplotlib:
    #   fig, ax = plt.subplots(figsize=(7, 4.5))
    #   ax.bar(resumen.index, resumen.values, color="#2a6f97")
    #   ax.set_title("Saldo por rubro — Puerto Siracusa")
    #   ax.set_xlabel("Rubro"); ax.set_ylabel("Saldo pendiente (CLP)")
    #   fig.tight_layout(); fig.savefig(ruta_png, dpi=150); plt.close(fig)
    #   OJO (C16): jamás plt.show() en un script — cuelga y no sirve headless.
    return None


def construir_informe(tablero, resumen, huerfanos):
    total_deuda = int(tablero["deuda"].sum())
    total_pagado = int(tablero["pagado"].sum())
    total_saldo = int(tablero["saldo"].sum())
    tramos = tablero["tramo"].value_counts().sort_index()
    sin_pago = int((tablero["pagado"] == 0).sum())

    lineas = []
    lineas.append("TABLERO DEL CONCEJO — Dirección de Rentas de Puerto Siracusa")
    lineas.append("=" * 58)
    lineas.append(f"{'Deuda total':<20}: ${total_deuda:,} CLP")
    lineas.append(f"{'Pagado total':<20}: ${total_pagado:,} CLP")
    lineas.append(f"{'Saldo pendiente':<20}: ${total_saldo:,} CLP")
    lineas.append(f"{'Sin pago alguno':<20}: {sin_pago} contribuyentes")
    lineas.append("")
    lineas.append("Contribuyentes por tramo de deuda:")
    for tramo, n in tramos.items():
        lineas.append(f"  {tramo:<10}: {n}")
    lineas.append("")
    lineas.append("Saldo por rubro:")
    for _, fila in resumen.sort_values("rubro").iterrows():
        lineas.append(f"  {fila['rubro']:<12}: deuda ${int(fila['deuda']):,}  "
                      f"pagado ${int(fila['pagado']):,}  saldo ${int(fila['saldo']):,}")
    lineas.append("")
    lineas.append("Pagos huérfanos (a investigar — pagaron pero no están en el censo):")
    for _, fila in huerfanos.iterrows():
        lineas.append(f"  {fila['codigo']}: ${int(fila['pagado']):,}")
    lineas.append(f"  Total huérfano: ${int(huerfanos['pagado'].sum()) if len(huerfanos) else 0:,} CLP")
    return "\n".join(lineas)


def main():
    censo = agregar_rubro(cargar_censo(DATOS / "censo_limpio.csv"))
    censo = clasificar_deuda(censo)
    pagos = consolidar_pagos(cargar_pagos(DATOS / "pagos_junio.csv"),
                             cargar_pagos(DATOS / "pagos_julio.csv"))

    tablero, huerfanos = construir_tablero(censo, pagos)
    resumen = resumen_por_rubro(tablero)
    informe = construir_informe(tablero, resumen, huerfanos)
    print(informe)

    SALIDAS.mkdir(exist_ok=True)
    (SALIDAS / "informe_tablero.txt").write_text(informe + "\n", encoding="utf-8")
    tablero.to_csv(SALIDAS / "tablero.csv", index=False)
    tablero.to_excel(SALIDAS / "tablero.xlsx", index=False)
    graficar_saldo(tablero, SALIDAS / "saldo_por_rubro.png")

    print()
    print(f"[INFO] Tablero, informe y gráfico en: {SALIDAS}")


if __name__ == "__main__":
    main()
