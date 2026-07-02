"""Panorama anual — SOLUCIÓN OFICIAL (Lab 03).

Entrega dos cosas para el Concejo Municipal:
  1. El panorama de recaudación del puerto (12 meses × 3 rubros) con NumPy:
     totales por mes, por rubro, mes récord, meses flojos y una proyección de
     reajuste. Todo con operaciones vectorizadas (sin bucles a mano).
  2. Un resumen de morosidad del cuaderno de patentes (del Lab 01), ahora como
     un DataFrame de pandas.

Se ejecuta SIEMPRE desde la raíz del lab:

    uv run python panorama.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

from datos.recaudacion import MESES, RUBROS, RECAUDACION
from datos.cuaderno import PATENTES

NOMBRE_RUBRO = {"C": "Comercio", "G": "Gastronomía", "T": "Turismo"}


# ─── NumPy: el panorama de recaudación ────────────────────────────────────

def construir_matriz():
    """Convierte la planilla (lista de listas) en una matriz NumPy 12×3."""
    return np.array(RECAUDACION)


def recaudacion_por_mes(matriz):
    """Total recaudado en cada mes: suma a lo ancho (colapsa las columnas)."""
    return matriz.sum(axis=1)


def recaudacion_por_rubro(matriz):
    """Total recaudado por cada rubro: suma a lo largo (colapsa las filas)."""
    return matriz.sum(axis=0)


def mes_record(matriz):
    """Nombre del mes con mayor recaudación total."""
    por_mes = recaudacion_por_mes(matriz)
    return MESES[int(np.argmax(por_mes))]


def meses_bajo_umbral(matriz, umbral):
    """Nombres de los meses cuya recaudación total quedó por debajo del umbral."""
    por_mes = recaudacion_por_mes(matriz)
    mascara = por_mes < umbral          # array de True/False, uno por mes
    return [MESES[i] for i, esta_bajo in enumerate(mascara) if esta_bajo]


def proyectar_reajuste(matriz, tasa):
    """Proyecta la recaudación aplicando un reajuste (p. ej. 0.04 = 4 %)."""
    return matriz * (1 + tasa)          # broadcasting: el escalar toca cada celda


# ─── pandas: la morosidad del cuaderno ────────────────────────────────────

def cuaderno_a_dataframe():
    """Convierte el cuaderno de patentes (Lab 01) en un DataFrame."""
    return pd.DataFrame(PATENTES, columns=["codigo", "nombre", "estado", "deuda"])


def resumen_vencidas(df):
    """Devuelve (cantidad_de_vencidas, deuda_total_vencida) como ints nativos."""
    vencidas = df[df["estado"] == "VENCIDA"]
    return int(len(vencidas)), int(vencidas["deuda"].sum())


# ─── Informe ──────────────────────────────────────────────────────────────

def construir_informe(matriz, df, umbral):
    """Arma el texto del panorama anual como una sola cadena multilinea."""
    total = int(matriz.sum())
    por_rubro = recaudacion_por_rubro(matriz)
    por_mes = recaudacion_por_mes(matriz)
    mes = mes_record(matriz)
    total_record = int(por_mes.max())
    bajo = meses_bajo_umbral(matriz, umbral)
    cant_vencidas, deuda_vencida = resumen_vencidas(df)

    lineas = []
    lineas.append("PANORAMA ANUAL — Dirección de Rentas de Puerto Siracusa")
    lineas.append("=" * 58)
    lineas.append(f"{'Recaudación total anual':<25}: ${total:,} CLP")
    lineas.append(f"{'Mes récord':<25}: {mes} (${total_record:,})")
    lineas.append(f"{'Meses bajo umbral':<25}: {', '.join(bajo)}")
    lineas.append("")
    lineas.append("Recaudación por rubro:")
    for i, rubro in enumerate(RUBROS):
        lineas.append(f"  {rubro} ({NOMBRE_RUBRO[rubro]}): ${int(por_rubro[i]):,} CLP")
    lineas.append("")
    lineas.append("Morosidad del cuaderno:")
    lineas.append(f"  Patentes vencidas: {cant_vencidas}")
    lineas.append(f"  Deuda vencida    : ${deuda_vencida:,} CLP")

    return "\n".join(lineas)


def main():
    matriz = construir_matriz()
    df = cuaderno_a_dataframe()
    informe = construir_informe(matriz, df, umbral=6_500_000)
    print(informe)

    salidas = Path("salidas")
    salidas.mkdir(exist_ok=True)
    destino = salidas / "informe_panorama.txt"
    destino.write_text(informe + "\n", encoding="utf-8")

    print()
    print(f"[INFO] Informe archivado en: {destino}")


if __name__ == "__main__":
    main()
