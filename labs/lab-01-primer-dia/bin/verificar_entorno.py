"""Verificador de ENTORNO del Lab 01.

Comprueba que el taller esté montado antes de empezar a trabajar: la versión
de Python correcta, uv disponible, el entorno virtual creado y la estructura
de carpetas y datos en su sitio. Es de solo lectura y 100 % stdlib.

Lo llama el preparador (bin/00-preparar), pero también puedes correrlo tú:

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
    lc.titulo("Verificación de entorno — Lab 01")
    cont = lc.Contador()

    # ── 1) Python 3.13 en ejecución ───────────────────────────────────────
    mayor, menor = sys.version_info.major, sys.version_info.minor
    if (mayor, menor) == (3, 13):
        lc.ok(f"Python en ejecución: {mayor}.{menor} (correcto).", cont)
    else:
        lc.error(
            f"Python en ejecución: {mayor}.{menor}; el lab usa 3.13.",
            "No ejecutes con el Python del sistema. Antepón siempre 'uv run': "
            "uv run python bin/verificar_entorno.py",
            cont,
        )

    # ── 2) uv disponible en el PATH ───────────────────────────────────────
    ruta_uv = shutil.which("uv")
    if ruta_uv:
        lc.ok(f"uv disponible en el PATH ({ruta_uv}).", cont)
    else:
        lc.error(
            "No encuentro 'uv' en el PATH.",
            "Instálalo siguiendo docs/troubleshooting.md o docs/setup-alumno.md, "
            "y cierra y reabre la terminal.",
            cont,
        )

    # ── 3) El entorno virtual existe ──────────────────────────────────────
    if (RAIZ / ".venv").is_dir():
        lc.ok("El entorno virtual .venv/ existe.", cont)
    else:
        lc.error(
            "No existe el entorno virtual .venv/.",
            "Corre el preparador: bash bin/00-preparar.sh (macOS/Linux) o "
            "powershell -ExecutionPolicy Bypass -File bin\\00-preparar.ps1 (Windows).",
            cont,
        )

    # ── 4) La estructura de carpetas está completa ────────────────────────
    esperadas = ["bin", "datos", "guia", "plantillas", "soluciones", "docs"]
    faltantes = [d for d in esperadas if not (RAIZ / d).is_dir()]
    if not faltantes:
        lc.ok("La estructura de carpetas del lab está completa.", cont)
    else:
        lc.error(
            f"Faltan carpetas del lab: {', '.join(faltantes)}.",
            "¿Descargaste el lab completo? Vuelve a clonar el repositorio.",
            cont,
        )

    # ── 5) El cuaderno de datos está presente ─────────────────────────────
    if (RAIZ / "datos" / "cuaderno.py").is_file():
        lc.ok("El cuaderno de datos (datos/cuaderno.py) está presente.", cont)
    else:
        lc.error(
            "No encuentro datos/cuaderno.py.",
            "Es el padrón oficial del lab; sin él nada funciona. Vuelve a clonar.",
            cont,
        )

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.info("Entorno en verde. Puedes continuar con la Guía 2.")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
