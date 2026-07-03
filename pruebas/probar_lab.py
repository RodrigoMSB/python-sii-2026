"""Prueba UN lab del curso, reproduciendo el flujo feliz del alumno.

    uv run --no-project python pruebas/probar_lab.py lab-03
    uv run --no-project python pruebas/probar_lab.py lab-05-gran-limpieza

Exit 0 solo si el lab pasa de punta a punta.
"""

import sys

import lib_pruebas as lp
from flujos import FLUJOS, resolver


def main() -> int:
    if len(sys.argv) != 2:
        lp.info("Uso: probar_lab.py <lab>   (p. ej. lab-03 o capstone)")
        lp.info("Labs disponibles: " + ", ".join(f["carpeta"] for f in FLUJOS))
        return 2
    flujo = resolver(sys.argv[1])
    if flujo is None:
        lp.error(f"No reconozco el lab '{sys.argv[1]}'.",
                 "Usa uno de: " + ", ".join(f["carpeta"] for f in FLUJOS))
        return 2

    lp.titulo(f"Prueba — {flujo['titulo']}")
    lp.info("Copiando el lab a un directorio temporal (el repo no se toca)…")
    aprobado, detalle, seg = lp.ejecutar_flujo(flujo)
    print()
    if aprobado:
        lp.ok(f"{flujo['titulo']}: {detalle} ({seg:.0f}s)")
        print(f"\n{lp.VERDE}{lp.NEGRITA}✔ 1/1 pruebas correctas{lp.RESET}")
        return 0
    lp.error(f"{flujo['titulo']}: {detalle} ({seg:.0f}s)",
             "Revisa pruebas/_reportes/ para el log y las salidas capturadas.")
    print(f"\n{lp.ROJO}{lp.NEGRITA}✘ 0/1 pruebas correctas{lp.RESET}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
