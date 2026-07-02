"""Panorama anual — PLANTILLA para la Ruta Artesano 🛠️ (Lab 03).

Este archivo YA CORRE, pero casi todos los totales dan cero: las funciones
esperan que tú las completes. Rellena los seis TODO para que el panorama diga
la verdad.

Reglas del juego:
  - Copia este archivo a la raíz del lab con el nombre panorama.py
        (macOS/Linux)  cp plantillas/panorama.py panorama.py
        (Windows)      Copy-Item plantillas\\panorama.py panorama.py
  - Completa los TODO EN ORDEN (1 → 6) y ejecuta seguido:
        uv run python panorama.py
  - ¿Trabado >10 min en una función? Mira SOLO esa en soluciones/panorama.py.

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
    """Total recaudado en cada mes (12 números)."""
    # TODO 1 — Suma cada FILA (los 3 rubros de un mes). En NumPy eso es sumar
    #          "a lo ancho": matriz.sum(axis=1).
    #          Pista: axis es el eje que COLAPSA; axis=1 colapsa las columnas.
    return np.zeros(matriz.shape[0], dtype=int)


def recaudacion_por_rubro(matriz):
    """Total recaudado por cada rubro (3 números, orden C, G, T)."""
    # TODO 2 — Suma cada COLUMNA (los 12 meses de un rubro): matriz.sum(axis=0).
    #          Pista: axis=0 colapsa las filas (los meses).
    return np.zeros(matriz.shape[1], dtype=int)


def mes_record(matriz):
    """Nombre del mes con mayor recaudación total."""
    por_mes = recaudacion_por_mes(matriz)
    # TODO 3 — Encuentra la POSICIÓN del mayor con np.argmax(por_mes) y úsala
    #          para indexar MESES.
    #          Pista: np.argmax da el ÍNDICE (0..11), no el valor.
    return MESES[0]


def meses_bajo_umbral(matriz, umbral):
    """Nombres de los meses cuya recaudación total quedó por debajo del umbral."""
    por_mes = recaudacion_por_mes(matriz)
    # TODO 4 — Compara por_mes con el umbral: (por_mes < umbral) da un array de
    #          True/False, uno por mes. Recorre y quédate con los nombres cuyo
    #          valor sea True.
    #          Pista: [MESES[i] for i, bajo in enumerate(por_mes < umbral) if bajo]
    return []


def proyectar_reajuste(matriz, tasa):
    """Proyecta la recaudación aplicando un reajuste (p. ej. 0.04 = 4 %)."""
    return matriz * (1 + tasa)          # broadcasting: el escalar toca cada celda


# ─── pandas: la morosidad del cuaderno ────────────────────────────────────

def cuaderno_a_dataframe():
    """Convierte el cuaderno de patentes (Lab 01) en un DataFrame."""
    return pd.DataFrame(PATENTES, columns=["codigo", "nombre", "estado", "deuda"])


def resumen_vencidas(df):
    """Devuelve (cantidad_de_vencidas, deuda_total_vencida) como ints nativos."""
    # TODO 5 — Filtra las filas con estado "VENCIDA": df[df["estado"] == "VENCIDA"].
    #          Devuelve (cantidad, suma de la columna "deuda"), envolviendo ambos
    #          en int(...) para que sean enteros nativos de Python.
    return 0, 0


# ─── Informe ──────────────────────────────────────────────────────────────

def construir_informe(matriz, df, umbral):
    """Arma el texto del panorama anual como una sola cadena multilinea."""
    total = int(matriz.sum())
    por_rubro = recaudacion_por_rubro(matriz)
    por_mes = recaudacion_por_mes(matriz)
    mes = mes_record(matriz)
    total_record = int(por_mes.max()) if por_mes.size else 0
    bajo = meses_bajo_umbral(matriz, umbral)
    cant_vencidas, deuda_vencida = resumen_vencidas(df)

    lineas = []
    lineas.append("PANORAMA ANUAL — Dirección de Rentas de Puerto Siracusa")
    lineas.append("=" * 58)
    # TODO 6 — Agrega las TRES líneas del resumen con f-strings (usa {:,} para el
    #          separador de miles). Deben quedar EXACTAMENTE así (respeta espacios):
    #              f"{'Recaudación total anual':<25}: ${total:,} CLP"
    #              f"{'Mes récord':<25}: {mes} (${total_record:,})"
    #              f"{'Meses bajo umbral':<25}: {', '.join(bajo)}"
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
