"""Generador de fuentes binarias del Capstone (H-04).

Construye desde la semilla (datos/fuentes_semilla.py):
  - datos/fuentes/pagos_anuales.xlsx  (dos hojas: "S1" y "S2")
  - datos/fuentes/contribuyentes.db   (SQLite, tabla contribuyentes)

    uv run python bin/generar_fuentes.py            # solo lo que falta
    uv run python bin/generar_fuentes.py --force    # reconstruye todo

Doctrina H-04: el .xlsx no es byte-determinista, así que por defecto se regenera
SOLO lo que falta (con las dos presentes es un no-op y no ensucia git). Para
reponer un binario corrupto: bórralo y regenera. Única herramienta autorizada a
escribir en datos/fuentes/.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

from datos.fuentes_semilla import PAGOS_S1, PAGOS_S2, CONTRIBUYENTES_BD  # noqa: E402

CARPETA = RAIZ / "datos" / "fuentes"
RUTA_XLSX = CARPETA / "pagos_anuales.xlsx"
RUTA_DB = CARPETA / "contribuyentes.db"


def generar_xlsx():
    import pandas as pd
    s1 = pd.DataFrame(PAGOS_S1, columns=["codigo", "fecha", "monto"])
    s2 = pd.DataFrame(PAGOS_S2, columns=["codigo", "fecha", "monto"])
    with pd.ExcelWriter(RUTA_XLSX, engine="openpyxl") as w:
        s1.to_excel(w, sheet_name="S1", index=False)
        s2.to_excel(w, sheet_name="S2", index=False)


def generar_db():
    if RUTA_DB.exists():
        RUTA_DB.unlink()
    # C11: `with sqlite3.connect(...)` es transaccional, NO cierra la conexión
    # (queda prohibido como mecanismo de cierre en todo el curso; ver H-07).
    con = sqlite3.connect(RUTA_DB)
    try:
        con.execute("CREATE TABLE contribuyentes ("
                    "codigo TEXT PRIMARY KEY, nombre TEXT NOT NULL, giro TEXT NOT NULL)")
        con.executemany("INSERT INTO contribuyentes (codigo, nombre, giro) VALUES (?, ?, ?)",
                        CONTRIBUYENTES_BD)
        con.commit()
    finally:
        con.close()


def main() -> int:
    lc.titulo("Generador de fuentes — Capstone El Arenario")
    CARPETA.mkdir(parents=True, exist_ok=True)
    forzar = "--force" in sys.argv
    cont = lc.Contador()

    for etiqueta, funcion, ruta in (
        ("pagos_anuales.xlsx", generar_xlsx, RUTA_XLSX),
        ("contribuyentes.db", generar_db, RUTA_DB),
    ):
        if ruta.exists() and not forzar:
            lc.ok(f"{etiqueta} ya está (no la toco).", cont)
            continue
        try:
            funcion()
            lc.ok(f"{etiqueta} generado.", cont)
        except Exception as exc:  # noqa: BLE001
            lc.error(f"No pude generar {etiqueta}: {exc}", "¿openpyxl instalado? Corre el preparador.", cont)

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.info(f"Fuentes binarias en: {CARPETA}")
        if not forzar:
            lc.info("Se regeneró solo lo que faltaba. Para reconstruir todo: --force")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
