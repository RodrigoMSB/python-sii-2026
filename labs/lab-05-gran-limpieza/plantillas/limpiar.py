"""La gran limpieza — PLANTILLA para la Ruta Artesano 🛠️ (Lab 05).

Este archivo YA CORRE, pero casi no limpia nada: las funciones devuelven el censo
tal cual. Completa los seis TODO para que homogeneice, deduplique, filtre, impute
y decida los outliers con criterio.

Reglas del juego:
  - Copia este archivo a la raíz del lab con el nombre limpiar.py
        (macOS/Linux)  cp plantillas/limpiar.py limpiar.py
        (Windows)      Copy-Item plantillas\\limpiar.py limpiar.py
  - Completa los TODO EN ORDEN (1 → 6). Ejecuta seguido:  uv run python limpiar.py
  - ¿Trabado >10 min? Mira SOLO esa función en soluciones/limpiar.py.

Se ejecuta SIEMPRE desde la raíz del lab:

    uv run python limpiar.py
"""

import sys as _s
if hasattr(_s.stdout, "reconfigure"):
    _s.stdout.reconfigure(encoding="utf-8")   # Windows: imprime UTF-8 sin morir (cp1252)
    _s.stderr.reconfigure(encoding="utf-8")


from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent
CENSO = RAIZ / "datos" / "censo_patentes.csv"
SALIDAS = RAIZ / "salidas"

PATRON_CODIGO = r"PS-\d{4}-[CGT]"


def cargar_censo(ruta):
    """Lee el censo. Unifica los TRES marcadores de faltante en NaN."""
    return pd.read_csv(ruta, na_values=["", "S/I", "sin dato"], keep_default_na=True)


def homogeneizar(df):
    """Normaliza texto: estado a MAYÚSCULAS sin espacios; nombre sin bordes."""
    df = df.copy()
    # TODO 1 — Usa el accessor .str (aplica a TODA la columna de una vez):
    #   df["estado"] = df["estado"].str.strip().str.upper()
    #   df["nombre"] = df["nombre"].str.strip()
    return df


def quitar_duplicados(df):
    """Elimina filas EXACTAMENTE duplicadas. Retorna (df, cuántas quitó)."""
    df = df.copy()
    # TODO 2 — Compara len antes/después: guarda antes=len(df), aplica
    #   df = df.drop_duplicates(), y retorna (df, antes - len(df)).
    return df, 0


def filtrar_codigos(df):
    """Separa códigos con formato válido (PS-####-Y). Retorna (válidos, descartados)."""
    df = df.copy()
    # TODO 3 — Arma una máscara con la regex (ya está en PATRON_CODIGO):
    #   mascara = df["codigo"].str.fullmatch(PATRON_CODIGO)
    #   Retorna (df[mascara].copy(), df[~mascara].copy())  — ~ invierte la máscara.
    return df.copy(), df.iloc[0:0].copy()


def imputar_deuda(df):
    """Imputa las deudas faltantes con 0 y pasa la columna a entero.

    Regla de negocio (Don Arquímedes): "la deuda no informada se asume 0 y se
    marca para verificación en terreno".
    """
    df = df.copy()
    # TODO 4 — Cuenta los faltantes con df["deuda"].isna().sum() (guárdalo en
    #   'imputados'), rellena con df["deuda"] = df["deuda"].fillna(0).astype(int),
    #   y retorna (df, imputados).
    imputados = 0
    return df, imputados


def outliers_iqr(df):
    """Filas cuya deuda cae fuera de [Q1-1.5·IQR, Q3+1.5·IQR]."""
    # TODO 5 — Calcula q1 = df["deuda"].quantile(0.25), q3 = ...quantile(0.75),
    #   iqr = q3 - q1, y devuelve las filas con deuda < q1-1.5*iqr o > q3+1.5*iqr.
    return df.iloc[0:0].copy()


def outliers_z(df, umbral=3.0):
    """Filas cuya deuda tiene |z-score| mayor al umbral (std MUESTRAL, ddof=1)."""
    media = df["deuda"].mean()
    desv = df["deuda"].std()  # ddof=1 (muestral) por defecto en pandas
    z = (df["deuda"] - media) / desv
    return df[z.abs() > umbral].copy()


def vencidas_grandes(df, umbral):
    """Patentes VENCIDA con deuda sobre el umbral, usando query() (demostración)."""
    return df.query("estado == 'VENCIDA' and deuda > @umbral").copy()


def limpiar_censo(ruta, umbral_z=3.0):
    """Pipeline completo. Retorna (censo_limpio, reporte con TODAS las métricas)."""
    df = cargar_censo(ruta)
    filas_brutas = len(df)

    df = homogeneizar(df)
    df, duplicados = quitar_duplicados(df)
    df, descartados_df = filtrar_codigos(df)
    codigos_descartados = sorted(descartados_df["codigo"].tolist())
    df, imputados = imputar_deuda(df)

    iqr_df = outliers_iqr(df)
    z_df = outliers_z(df, umbral_z)
    cod_iqr = set(iqr_df["codigo"])
    cod_z = set(z_df["codigo"])

    # TODO 6 — Regla de decisión: se APARTA solo lo señalado por AMBOS métodos
    #   (consenso). Un código está "en ambos" si aparece en cod_iqr Y en cod_z:
    #   apartados = sorted(cod_iqr & cod_z)
    apartados = []

    detalle = []
    for _, fila in iqr_df.sort_values("codigo").iterrows():
        cod = fila["codigo"]
        en_z = cod in cod_z
        detalle.append({
            "codigo": cod, "nombre": fila["nombre"], "deuda": int(fila["deuda"]),
            "metodos": "por IQR y z-score" if en_z else "solo por IQR",
            "veredicto": "APARTADO" if cod in apartados else "CONSERVADO",
        })

    limpio = df[~df["codigo"].isin(apartados)].copy()
    reporte = {
        "filas_brutas": filas_brutas,
        "duplicados_eliminados": duplicados,
        "codigos_descartados": codigos_descartados,
        "deudas_imputadas": imputados,
        "outliers_iqr": sorted(cod_iqr),
        "outliers_z": sorted(cod_z),
        "apartados": apartados,
        "filas_finales": len(limpio),
        "deuda_total": int(limpio["deuda"].sum()),
        "outliers_detalle": detalle,
    }
    return limpio, reporte


def construir_informe(reporte, df_limpio):
    """Arma el informe de limpieza como una sola cadena multilinea."""
    r = reporte
    tras_dedup = r["filas_brutas"] - r["duplicados_eliminados"]
    tras_codigos = tras_dedup - len(r["codigos_descartados"])

    lineas = []
    lineas.append("INFORME DE LIMPIEZA — Censo de Patentes de Puerto Siracusa")
    lineas.append("=" * 58)
    lineas.append("Embudo de filas:")
    lineas.append(f"  Censo bruto              : {r['filas_brutas']}")
    lineas.append(f"  Tras quitar duplicados   : {tras_dedup}  (-{r['duplicados_eliminados']} exactos)")
    lineas.append(f"  Tras filtrar códigos     : {tras_codigos}  "
                  f"(-{len(r['codigos_descartados'])} malformados: {', '.join(r['codigos_descartados'])})")
    lineas.append(f"  Deudas imputadas (= 0)   : {r['deudas_imputadas']}")
    lineas.append(f"  Tras apartar outliers    : {r['filas_finales']}  (-{len(r['apartados'])})")
    lineas.append("")
    lineas.append("Outliers de deuda (los métodos proponen, el analista dispone):")
    for o in r["outliers_detalle"]:
        lineas.append(f"  {o['codigo']} ({o['nombre']}, ${o['deuda']:,}): {o['veredicto']}")
        if o["veredicto"] == "APARTADO":
            lineas.append(f"      → señalado {o['metodos']} (consenso). Error de digitación: se aparta.")
        else:
            lineas.append(f"      → señalado {o['metodos']}; el z-score no lo marca. Negocio real "
                          f"(deuda conocida desde el Lab 01): se conserva, con nota.")
    lineas.append("")
    lineas.append(f"Censo limpio : {r['filas_finales']} filas — Deuda total : ${r['deuda_total']:,} CLP")
    return "\n".join(lineas)


def main():
    limpio, reporte = limpiar_censo(CENSO)
    informe = construir_informe(reporte, limpio)
    print(informe)

    SALIDAS.mkdir(exist_ok=True)
    (SALIDAS / "informe_limpieza.txt").write_text(informe + "\n", encoding="utf-8")
    limpio.to_csv(SALIDAS / "censo_limpio.csv", index=False)
    limpio.to_excel(SALIDAS / "censo_limpio.xlsx", index=False)

    print()
    print(f"[INFO] Informe y censo limpio en: {SALIDAS}")


if __name__ == "__main__":
    main()
