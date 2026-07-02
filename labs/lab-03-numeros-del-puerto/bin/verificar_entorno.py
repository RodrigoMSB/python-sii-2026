"""Verificador de ENTORNO del Lab 03.

Checks del Lab 01 + verificación TOLERANTE de las bibliotecas del lab
(numpy/pandas). Puede ejecutarse ANTES de `uv sync` sin morir: si las
bibliotecas no están, lo reporta con una pista (no revienta con traceback).

    uv run python bin/verificar_entorno.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

# Versiones pineadas del lab (deben coincidir con pyproject.toml).
NUMPY_ESPERADA = "2.5.0"
PANDAS_ESPERADA = "3.0.3"


def _check_biblioteca(nombre, esperada, cont):
    """Import tolerante + comparación de versión."""
    try:
        modulo = __import__(nombre)
    except Exception:  # noqa: BLE001 - import puede fallar de varias formas
        lc.error(f"No pude importar {nombre}.",
                 "Corre el preparador para instalar las bibliotecas: bash bin/00-preparar.sh "
                 "(macOS/Linux) o el .ps1 en Windows.", cont)
        return
    version = getattr(modulo, "__version__", "desconocida")
    if version == esperada:
        lc.ok(f"{nombre} {version} (correcto).", cont)
    else:
        lc.error(f"{nombre} {version}; el lab usa {esperada}.",
                 "Sincroniza el entorno con: uv sync", cont)


def main() -> int:
    lc.titulo("Verificación de entorno — Lab 03")
    cont = lc.Contador()

    mayor, menor = sys.version_info.major, sys.version_info.minor
    if (mayor, menor) == (3, 13):
        lc.ok(f"Python en ejecución: {mayor}.{menor} (correcto).", cont)
    else:
        lc.error(f"Python en ejecución: {mayor}.{menor}; el lab usa 3.13.",
                 "Antepón siempre 'uv run': uv run python bin/verificar_entorno.py", cont)

    ruta_uv = shutil.which("uv")
    if ruta_uv:
        lc.ok(f"uv disponible en el PATH ({ruta_uv}).", cont)
    else:
        lc.error("No encuentro 'uv' en el PATH.",
                 "Instálalo (docs/setup-alumno.md) y reabre la terminal.", cont)

    if (RAIZ / ".venv").is_dir():
        lc.ok("El entorno virtual .venv/ existe.", cont)
    else:
        lc.error("No existe el entorno virtual .venv/.",
                 "Corre el preparador: bash bin/00-preparar.sh (o el .ps1 en Windows).", cont)

    esperadas = ["bin", "datos", "guia", "plantillas", "soluciones", "docs"]
    faltantes = [d for d in esperadas if not (RAIZ / d).is_dir()]
    if not faltantes:
        lc.ok("La estructura de carpetas del lab está completa.", cont)
    else:
        lc.error(f"Faltan carpetas del lab: {', '.join(faltantes)}.", "Vuelve a clonar.", cont)

    datasets = ["recaudacion.py", "cuaderno.py"]
    faltan_datos = [d for d in datasets if not (RAIZ / "datos" / d).is_file()]
    if not faltan_datos:
        lc.ok("Los datasets (datos/recaudacion.py y datos/cuaderno.py) están presentes.", cont)
    else:
        lc.error(f"Faltan datasets: {', '.join(faltan_datos)}.", "Vuelve a clonar.", cont)

    # Bibliotecas del lab (tolerante)
    _check_biblioteca("numpy", NUMPY_ESPERADA, cont)
    _check_biblioteca("pandas", PANDAS_ESPERADA, cont)

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.info("Entorno en verde. Puedes continuar con la Guía 2.")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
