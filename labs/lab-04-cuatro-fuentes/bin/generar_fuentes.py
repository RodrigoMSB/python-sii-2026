"""Generador de las cuatro fuentes — "la imprenta del lab".

Construye datos/fuentes/ a partir de la semilla (datos/fuentes_semilla.py):

    uv run python bin/generar_fuentes.py

Produce:
  - pagos.csv               (CSV UTF-8, con encabezado)
  - permisos_eventos.xlsx   (Excel, hoja "Permisos")
  - multas.json             (JSON UTF-8, indentado, ensure_ascii=False)
  - contribuyentes.db       (SQLite, tabla contribuyentes)

Es idempotente: borra y reconstruye todo desde cero en cada corrida. Es la
ÚNICA herramienta autorizada a escribir en datos/fuentes/ (para el alumno esos
archivos son de SOLO LECTURA). El recuperador lo invoca para reponer fuentes
corrompidas.

Decisión documentada: el CSV se escribe con el módulo `csv` de la stdlib (para
mostrar la escritura "a mano"); el XLSX con pandas+openpyxl; el JSON con `json`
stdlib; la BD con `sqlite3` stdlib.
"""

from __future__ import annotations

import csv
import json
import sqlite3
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

from datos.fuentes_semilla import (  # noqa: E402
    PAGOS_CSV, PERMISOS_XLSX, MULTAS_JSON, CONTRIBUYENTES_BD,
)

CARPETA = RAIZ / "datos" / "fuentes"
RUTA_CSV = CARPETA / "pagos.csv"
RUTA_XLSX = CARPETA / "permisos_eventos.xlsx"
RUTA_JSON = CARPETA / "multas.json"
RUTA_DB = CARPETA / "contribuyentes.db"


def generar_csv():
    with RUTA_CSV.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["codigo", "fecha", "monto"])
        escritor.writerows(PAGOS_CSV)


def generar_xlsx():
    import pandas as pd
    df = pd.DataFrame(PERMISOS_XLSX, columns=["folio", "evento", "valor"])
    df.to_excel(RUTA_XLSX, sheet_name="Permisos", index=False)


def generar_json():
    objetos = [{"codigo": c, "motivo": m, "monto": v} for c, m, v in MULTAS_JSON]
    with RUTA_JSON.open("w", encoding="utf-8") as f:
        json.dump(objetos, f, ensure_ascii=False, indent=2)


def generar_db():
    if RUTA_DB.exists():
        RUTA_DB.unlink()  # regeneración desde cero
    with sqlite3.connect(RUTA_DB) as con:
        con.execute(
            "CREATE TABLE contribuyentes ("
            "codigo TEXT PRIMARY KEY, nombre TEXT NOT NULL, giro TEXT NOT NULL)"
        )
        con.executemany(
            "INSERT INTO contribuyentes (codigo, nombre, giro) VALUES (?, ?, ?)",
            CONTRIBUYENTES_BD,
        )
        con.commit()


def main() -> int:
    lc.titulo("Generador de fuentes — Lab 04")
    CARPETA.mkdir(parents=True, exist_ok=True)
    cont = lc.Contador()

    for etiqueta, funcion, ruta in (
        ("pagos.csv", generar_csv, RUTA_CSV),
        ("permisos_eventos.xlsx", generar_xlsx, RUTA_XLSX),
        ("multas.json", generar_json, RUTA_JSON),
        ("contribuyentes.db", generar_db, RUTA_DB),
    ):
        try:
            funcion()
            lc.ok(f"{etiqueta} generado.", cont)
        except Exception as exc:  # noqa: BLE001
            lc.error(f"No pude generar {etiqueta}: {exc}",
                     "¿Está instalado openpyxl? Corre bash bin/00-preparar.sh", cont)

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.info(f"Las cuatro fuentes están en: {CARPETA}")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
