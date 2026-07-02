"""El Arenario — SOLUCIÓN DE REFERENCIA (instructor).

Informe Anual de Rentas de Puerto Siracusa: depura el censo, cruza deudas con
pagos (dos semestres) y multas, calcula saldos, resume, grafica e informa —
dejando rastro de cada decisión y explicando los hallazgos (incluidos los saldos
negativos, el giro final del curso).

Esta es la implementación de REFERENCIA con la que se validan los productos. El
alumno construye la suya con estructura libre; lo que se mide son los archivos de
salidas/ (contrato C18).

    uv run python arenario.py
"""

import json
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")            # C16
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "datos"
FUENTES = DATOS / "fuentes"
SALIDAS = RAIZ / "salidas"
GRAFICOS = SALIDAS / "graficos"

PATRON = r"PS-\d{4}-[CGT]"
RUBRO = {"C": "Comercio", "G": "Gastronomía", "T": "Turismo"}
BINS = [-1, 0, 100_000, 300_000, 10**9]
LABELS = ["Sin deuda", "Baja", "Media", "Alta"]
MARCADORES_FALTANTE = ["", "S/I", "s/d"]     # H-05: 's/d', no 'N/A'


# ─── Depuración (reglas oficiales del curso) ───────────────────────────────

def depurar_censo(ruta):
    """Depura el censo anual. Retorna (censo_depurado, reporte_del_embudo)."""
    df = pd.read_csv(ruta, na_values=MARCADORES_FALTANTE, keep_default_na=True)
    brutas = len(df)
    df = df.copy()
    df["estado"] = df["estado"].str.strip().str.upper()
    df["nombre"] = df["nombre"].str.strip()

    n = len(df); df = df.drop_duplicates(); duplicados = n - len(df)     # gana el primero
    mask = df["codigo"].str.fullmatch(PATRON)
    codigos_descartados = sorted(df[~mask]["codigo"].tolist())
    df = df[mask].copy()
    imputados = int(df["deuda"].isna().sum())
    df["deuda"] = df["deuda"].fillna(0).astype(int)

    q1, q3 = df["deuda"].quantile(0.25), df["deuda"].quantile(0.75)
    iqr = q3 - q1
    cod_iqr = set(df[(df["deuda"] < q1 - 1.5 * iqr) | (df["deuda"] > q3 + 1.5 * iqr)]["codigo"])
    z = (df["deuda"] - df["deuda"].mean()) / df["deuda"].std()
    cod_z = set(df[z.abs() > 3.0]["codigo"])
    apartados = sorted(cod_iqr & cod_z)          # consenso: solo lo señalado por AMBOS

    depurado = df[~df["codigo"].isin(apartados)].copy()
    reporte = {
        "brutas": brutas, "duplicados": duplicados, "codigos_descartados": codigos_descartados,
        "imputados": imputados, "outliers_iqr": sorted(cod_iqr), "outliers_z": sorted(cod_z),
        "apartados": apartados, "depuradas": len(depurado),
    }
    return depurado, reporte


# ─── Carga de las otras fuentes ────────────────────────────────────────────

def cargar_pagos(ruta_xlsx):
    """Lee las dos hojas (S1, S2) del Excel y las apila."""
    hojas = pd.read_excel(ruta_xlsx, sheet_name=None)     # dict {hoja: df}
    return pd.concat(hojas.values(), ignore_index=True)


def cargar_multas(ruta_json):
    with open(ruta_json, encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))


def cargar_contribuyentes(ruta_db):
    con = sqlite3.connect(ruta_db)
    try:
        return pd.read_sql("SELECT codigo, giro FROM contribuyentes", con)
    finally:
        con.close()


# ─── Tablero anual ─────────────────────────────────────────────────────────

def construir_tablero(censo, pagos, multas, contrib):
    """Cruza deuda × pagos × multas × giro. Retorna (tablero, huérfanos)."""
    censo = censo.copy()
    censo["rubro"] = censo["codigo"].str[-1].map(RUBRO)
    censo["tramo"] = pd.cut(censo["deuda"], bins=BINS, labels=LABELS)

    pagado = pagos.groupby("codigo", as_index=False)["monto"].sum().rename(columns={"monto": "pagado"})
    multa = multas.groupby("codigo", as_index=False)["monto"].sum().rename(columns={"monto": "multas"})

    t = (censo
         .merge(contrib, on="codigo", how="left", validate="1:1")
         .merge(pagado, on="codigo", how="left", validate="1:1")
         .merge(multa, on="codigo", how="left", validate="1:1"))
    t["pagado"] = t["pagado"].fillna(0).astype(int)
    t["multas"] = t["multas"].fillna(0).astype(int)
    t["saldo"] = t["deuda"] + t["multas"] - t["pagado"]
    t = t[["codigo", "nombre", "estado", "deuda", "rubro", "tramo", "giro", "pagado", "multas", "saldo"]]

    huer_pago = pagado[~pagado["codigo"].isin(censo["codigo"])].copy()
    huer_multa = multa[~multa["codigo"].isin(censo["codigo"])].copy()
    return t, (huer_pago, huer_multa)


# ─── Gráficos (headless, C16) ──────────────────────────────────────────────

def graficar(tablero):
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    saldo = tablero.groupby("rubro")["saldo"].sum().sort_index()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(saldo.index, saldo.values, color="#2a6f97")
    ax.set_title("Saldo anual por rubro — Puerto Siracusa")
    ax.set_xlabel("Rubro"); ax.set_ylabel("Saldo (CLP)")
    fig.tight_layout(); fig.savefig(GRAFICOS / "saldo_por_rubro.png", dpi=150); plt.close(fig)

    tramos = tablero["tramo"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(tramos.index.astype(str), tramos.values, color="#c9803a")
    ax.set_title("Contribuyentes por tramo de deuda")
    ax.set_xlabel("Tramo"); ax.set_ylabel("Cantidad")
    fig.tight_layout(); fig.savefig(GRAFICOS / "tramos_de_deuda.png", dpi=150); plt.close(fig)


# ─── Informe ───────────────────────────────────────────────────────────────

def construir_informe(tablero, reporte, huerfanos):
    huer_pago, huer_multa = huerfanos
    total_deuda = int(tablero["deuda"].sum())
    total_pagado = int(tablero["pagado"].sum())
    total_multas = int(tablero["multas"].sum())
    total_saldo = int(tablero["saldo"].sum())
    al_dia = int((tablero["saldo"] <= 0).sum())
    morosos = int((tablero["saldo"] > 0).sum())
    tramos = tablero["tramo"].value_counts().sort_index()
    por_rubro = tablero.groupby("rubro")["saldo"].sum()
    negativos = tablero[tablero["saldo"] < 0]

    tras_dedup = reporte["brutas"] - reporte["duplicados"]
    tras_cod = tras_dedup - len(reporte["codigos_descartados"])

    L = []
    L.append("INFORME ANUAL DE RENTAS — Puerto Siracusa")
    L.append("=" * 58)
    L.append("Embudo de depuración:")
    L.append(f"  Censo bruto              : {reporte['brutas']}")
    L.append(f"  Tras quitar duplicados   : {tras_dedup}  (-{reporte['duplicados']})")
    L.append(f"  Tras filtrar códigos     : {tras_cod}  (-{len(reporte['codigos_descartados'])}: "
             f"{', '.join(reporte['codigos_descartados'])})")
    L.append(f"  Deudas imputadas (= 0)   : {reporte['imputados']}")
    L.append(f"  Outlier apartado         : {', '.join(reporte['apartados'])}  "
             f"(IQR marcó {reporte['outliers_iqr']}; z marcó {reporte['outliers_z']}; "
             f"consenso solo {reporte['apartados']})")
    L.append(f"  Censo depurado           : {reporte['depuradas']}")
    L.append("")
    L.append("Totales del año:")
    L.append(f"  {'Deuda':<10}: ${total_deuda:,} CLP")
    L.append(f"  {'Pagado':<10}: ${total_pagado:,} CLP")
    L.append(f"  {'Multas':<10}: ${total_multas:,} CLP")
    L.append(f"  {'SALDO':<10}: ${total_saldo:,} CLP")
    L.append(f"  Al día (saldo ≤ 0): {al_dia}    Morosos (saldo > 0): {morosos}")
    L.append("")
    L.append("Contribuyentes por tramo de deuda:")
    for tramo, n in tramos.items():
        L.append(f"  {tramo:<10}: {n}")
    L.append("")
    L.append("Saldo por rubro:")
    for rubro in ["Comercio", "Gastronomía", "Turismo"]:
        L.append(f"  {rubro:<12}: ${int(por_rubro.get(rubro, 0)):,} CLP")
    L.append("")
    L.append("Huérfanos (llegaron pero no están en el censo depurado):")
    for _, f in huer_pago.iterrows():
        L.append(f"  Pago  {f['codigo']}: ${int(f['pagado']):,}")
    for _, f in huer_multa.iterrows():
        L.append(f"  Multa {f['codigo']}: ${int(f['multas']):,}")
    L.append("")
    L.append("Hallazgos del analista:")
    L.append(f"  Se detectaron {len(negativos)} saldos NEGATIVOS (pagó más de lo que debe):")
    for _, f in negativos.sort_values("codigo").iterrows():
        L.append(f"    {f['codigo']} ({f['nombre']}): saldo ${int(f['saldo']):,} "
                 f"(deuda ${int(f['deuda']):,} + multas ${int(f['multas']):,} − pagado ${int(f['pagado']):,})")
    L.append("  Dos causas: (1) SOBREPAGOS — contribuyentes que pagaron en ambos semestres;")
    L.append("  (2) CONSECUENCIA DE LA IMPUTACIÓN — a quien tenía deuda no informada se le")
    L.append("  imputó 0, y su pago posterior lo dejó en negativo (p. ej. PS-1044-C: deuda")
    L.append("  'S/I' → 0, pagó $25.000 → saldo −$25.000). Recomendación al Concejo: verificar")
    L.append("  en terreno los saldos negativos por imputación antes de devolver dinero.")
    return "\n".join(L)


# ─── Persistencia ──────────────────────────────────────────────────────────

def escribir_productos(censo, tablero, informe):
    SALIDAS.mkdir(exist_ok=True)
    censo[["codigo", "nombre", "estado", "deuda"]].to_csv(SALIDAS / "censo_depurado.csv", index=False)
    tablero.to_csv(SALIDAS / "tablero_anual.csv", index=False)
    tablero.to_excel(SALIDAS / "tablero_anual.xlsx", index=False)
    (SALIDAS / "informe_anual.txt").write_text(informe + "\n", encoding="utf-8")
    resumen = tablero.groupby("rubro", as_index=False)["saldo"].sum()
    con = sqlite3.connect(SALIDAS / "gestion.db")
    try:
        resumen.to_sql("resumen_anual", con, if_exists="replace", index=False)
    finally:
        con.close()


def main():
    censo, reporte = depurar_censo(DATOS / "censo_anual.csv")
    pagos = cargar_pagos(FUENTES / "pagos_anuales.xlsx")
    multas = cargar_multas(DATOS / "multas.json")
    contrib = cargar_contribuyentes(FUENTES / "contribuyentes.db")

    tablero, huerfanos = construir_tablero(censo, pagos, multas, contrib)
    informe = construir_informe(tablero, reporte, huerfanos)
    print(informe)

    escribir_productos(censo, tablero, informe)
    graficar(tablero)
    print()
    print(f"[INFO] Informe anual y productos en: {SALIDAS}")


if __name__ == "__main__":
    main()
