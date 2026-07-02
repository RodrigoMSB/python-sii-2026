"""Verificador de ENTORNO del Lab 06.

Checks estándar + bibliotecas (tolerante, incluye matplotlib) + los 3 CSV con sus
conteos exactos (25 / 12 / 8). Solo lectura. Los CSV son texto versionado: git es
la fuente de verdad.

    uv run python bin/verificar_entorno.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

VERSIONES = {"numpy": "2.5.0", "pandas": "3.0.3", "openpyxl": "3.1.5", "matplotlib": "3.11.0"}
CSVS = {"censo_limpio.csv": 25, "pagos_junio.csv": 12, "pagos_julio.csv": 8}


def _check_biblioteca(nombre, esperada, cont):
    try:
        modulo = __import__(nombre)
    except Exception:  # noqa: BLE001
        lc.error(f"No pude importar {nombre}.", "Corre el preparador: bash bin/00-preparar.sh", cont)
        return
    version = getattr(modulo, "__version__", "desconocida")
    if version == esperada:
        lc.ok(f"{nombre} {version} (correcto).", cont)
    else:
        lc.error(f"{nombre} {version}; el lab usa {esperada}.", "Sincroniza: uv sync", cont)


def main() -> int:
    lc.titulo("Verificación de entorno — Lab 06")
    cont = lc.Contador()

    mayor, menor = sys.version_info.major, sys.version_info.minor
    if (mayor, menor) == (3, 13):
        lc.ok(f"Python en ejecución: {mayor}.{menor} (correcto).", cont)
    else:
        lc.error(f"Python en ejecución: {mayor}.{menor}; el lab usa 3.13.", "Antepón siempre 'uv run'.", cont)

    ruta_uv = shutil.which("uv")
    if ruta_uv:
        lc.ok(f"uv disponible en el PATH ({ruta_uv}).", cont)
    else:
        lc.error("No encuentro 'uv' en el PATH.", "Instálalo (docs/setup-alumno.md).", cont)

    if (RAIZ / ".venv").is_dir():
        lc.ok("El entorno virtual .venv/ existe.", cont)
    else:
        lc.error("No existe el entorno virtual .venv/.", "Corre el preparador.", cont)

    esperadas = ["bin", "datos", "guia", "plantillas", "soluciones", "docs"]
    faltantes = [d for d in esperadas if not (RAIZ / d).is_dir()]
    if not faltantes:
        lc.ok("La estructura de carpetas del lab está completa.", cont)
    else:
        lc.error(f"Faltan carpetas del lab: {', '.join(faltantes)}.", "Vuelve a clonar.", cont)

    for nombre, esperada in VERSIONES.items():
        _check_biblioteca(nombre, esperada, cont)

    for nombre, esperado in CSVS.items():
        ruta = RAIZ / "datos" / nombre
        if not ruta.is_file():
            lc.error(f"Falta datos/{nombre}.", f"Restáuralo: git checkout -- datos/{nombre}", cont)
            continue
        filas = sum(1 for _ in ruta.open(encoding="utf-8")) - 1
        if filas == esperado:
            lc.ok(f"datos/{nombre} presente con {esperado} filas.", cont)
        else:
            lc.error(f"datos/{nombre} tiene {filas} filas (deberían ser {esperado}).",
                     f"Restáuralo: git checkout -- datos/{nombre}", cont)

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.info("Entorno en verde. Puedes continuar con la Guía 2.")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
