"""Verificador de ENTORNO del Lab 02.

Comprueba que el taller esté montado antes de trabajar: versión de Python, uv,
entorno virtual, estructura de carpetas y los datasets en su sitio. Solo lectura,
100 % stdlib.

    uv run python bin/verificar_entorno.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402


def main() -> int:
    lc.titulo("Verificación de entorno — Lab 02")
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
        lc.error(f"Faltan carpetas del lab: {', '.join(faltantes)}.",
                 "¿Descargaste el lab completo? Vuelve a clonar.", cont)

    datasets = ["archivador.py", "cuaderno.py"]
    faltan_datos = [d for d in datasets if not (RAIZ / "datos" / d).is_file()]
    if not faltan_datos:
        lc.ok("Los datasets (datos/archivador.py y datos/cuaderno.py) están presentes.", cont)
    else:
        lc.error(f"Faltan datasets: {', '.join(faltan_datos)}.",
                 "Son los datos del lab; sin ellos nada funciona. Vuelve a clonar.", cont)

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.info("Entorno en verde. Puedes continuar con la Guía 2.")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
