"""Verificador de ENTORNO del Capstone.

Checks estándar + bibliotecas + las 4 fuentes (censo 31, multas 10, xlsx con
hojas S1/S2, db consultable). Solo lectura.

    uv run python bin/verificar_entorno.py
"""

from __future__ import annotations

import json
import shutil
import sqlite3
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

VERSIONES = {"numpy": "2.5.0", "pandas": "3.0.3", "openpyxl": "3.1.5", "matplotlib": "3.11.0"}


def _check_biblioteca(nombre, esperada, cont):
    try:
        modulo = __import__(nombre)
    except Exception:  # noqa: BLE001
        lc.error(f"No pude importar {nombre}.", "Corre el preparador: bash bin/00-preparar.sh", cont)
        return
    v = getattr(modulo, "__version__", "desconocida")
    if v == esperada:
        lc.ok(f"{nombre} {v} (correcto).", cont)
    else:
        lc.error(f"{nombre} {v}; el capstone usa {esperada}.", "Sincroniza: uv sync", cont)


def main() -> int:
    lc.titulo("Verificación de entorno — Capstone El Arenario")
    cont = lc.Contador()

    mayor, menor = sys.version_info.major, sys.version_info.minor
    if (mayor, menor) == (3, 13):
        lc.ok(f"Python en ejecución: {mayor}.{menor} (correcto).", cont)
    else:
        lc.error(f"Python en ejecución: {mayor}.{menor}; el capstone usa 3.13.", "Antepón 'uv run'.", cont)

    ruta_uv = shutil.which("uv")
    if ruta_uv:
        lc.ok(f"uv disponible en el PATH ({ruta_uv}).", cont)
    else:
        lc.error("No encuentro 'uv' en el PATH.", "Instálalo (docs/setup-alumno.md).", cont)

    if (RAIZ / ".venv").is_dir():
        lc.ok("El entorno virtual .venv/ existe.", cont)
    else:
        lc.error("No existe el entorno virtual .venv/.", "Corre el preparador.", cont)

    esperadas = ["bin", "escenario", "pistas", "datos", "plantillas", "soluciones", "docs"]
    faltantes = [d for d in esperadas if not (RAIZ / d).is_dir()]
    if not faltantes:
        lc.ok("La estructura de carpetas del capstone está completa.", cont)
    else:
        lc.error(f"Faltan carpetas: {', '.join(faltantes)}.", "Vuelve a clonar.", cont)

    for nombre, esperada in VERSIONES.items():
        _check_biblioteca(nombre, esperada, cont)

    # Fuentes de texto
    censo = RAIZ / "datos" / "censo_anual.csv"
    if censo.is_file() and sum(1 for _ in censo.open(encoding="utf-8")) - 1 == 31:
        lc.ok("datos/censo_anual.csv presente con 31 filas.", cont)
    else:
        lc.error("datos/censo_anual.csv ausente o con conteo distinto de 31.",
                 "Restáuralo: git checkout -- datos/censo_anual.csv", cont)

    multas = RAIZ / "datos" / "multas.json"
    try:
        n = len(json.load(multas.open(encoding="utf-8")))
        _ok = n == 10
    except Exception:  # noqa: BLE001
        _ok = False
    if _ok:
        lc.ok("datos/multas.json presente con 10 multas.", cont)
    else:
        lc.error("datos/multas.json ausente o inválido.", "git checkout -- datos/multas.json", cont)

    # Fuentes binarias
    xlsx = RAIZ / "datos" / "fuentes" / "pagos_anuales.xlsx"
    try:
        import pandas as pd
        hojas = pd.ExcelFile(xlsx).sheet_names
        _ok = set(hojas) >= {"S1", "S2"}
    except Exception:  # noqa: BLE001
        _ok = False
    if _ok:
        lc.ok("datos/fuentes/pagos_anuales.xlsx presente con hojas S1 y S2.", cont)
    else:
        lc.error("Falta o está mal datos/fuentes/pagos_anuales.xlsx.",
                 "Genéralo: uv run python bin/generar_fuentes.py", cont)

    db = RAIZ / "datos" / "fuentes" / "contribuyentes.db"
    try:
        con = sqlite3.connect(db); con.execute("SELECT COUNT(*) FROM contribuyentes").fetchone(); con.close()
        _ok = True
    except Exception:  # noqa: BLE001
        _ok = False
    if _ok:
        lc.ok("datos/fuentes/contribuyentes.db presente y consultable.", cont)
    else:
        lc.error("Falta o está mal datos/fuentes/contribuyentes.db.",
                 "Genéralo: uv run python bin/generar_fuentes.py", cont)

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.info("Entorno en verde. Lee escenario/ESCENARIO.md y a contar la arena.")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
