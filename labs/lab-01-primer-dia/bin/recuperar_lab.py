"""Recuperador del Lab 01 — modo instructor / rezagado.

¿Llegaste tarde, se te enredó todo o el instructor necesita dejar el lab en un
estado conocido? Esta herramienta reconstruye el CÓDIGO y las SALIDAS a partir
de la solución oficial:

    uv run python bin/recuperar_lab.py

Es el ÚNICO script del lab que escribe archivos, y solo hace tres cosas:
  1. Copia soluciones/triaje.py → triaje.py (en la raíz).
  2. Ejecuta el triaje para regenerar salidas/informe_triaje.txt.
  3. Copia plantillas/RESPUESTAS.md → RESPUESTAS.md, pero SOLO si no existe
     (si ya lo empezaste, lo respeta y no lo pisa).

Lo que JAMÁS hace: responder el interrogatorio por ti. Recuperar el código es
gratis; recuperar la comprensión, jamás.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402


def main() -> int:
    lc.titulo("Recuperador del Lab 01")
    cont = lc.Contador()

    # ── 1) Reponer triaje.py desde la solución ────────────────────────────
    origen_triaje = RAIZ / "soluciones" / "triaje.py"
    destino_triaje = RAIZ / "triaje.py"
    if origen_triaje.is_file():
        shutil.copyfile(origen_triaje, destino_triaje)
        lc.ok("triaje.py restaurado desde soluciones/.", cont)
    else:
        lc.error(
            "No encuentro soluciones/triaje.py.",
            "¿Está completo el lab? Vuelve a clonar el repositorio.",
            cont,
        )

    # ── 2) Regenerar salidas/ ejecutando el triaje ────────────────────────
    if destino_triaje.is_file():
        resultado = subprocess.run(
            [sys.executable, str(destino_triaje)],
            cwd=str(RAIZ),
            capture_output=True,
            text=True, encoding="utf-8", errors="replace")
        if resultado.returncode == 0 and (RAIZ / "salidas" / "informe_triaje.txt").is_file():
            lc.ok("salidas/informe_triaje.txt regenerado.", cont)
        else:
            lc.error(
                "No pude regenerar el informe ejecutando el triaje.",
                (resultado.stderr.strip().splitlines()[-1]
                 if resultado.stderr.strip() else "Revisa datos/cuaderno.py."),
                cont,
            )
    else:
        lc.error("No hay triaje.py que ejecutar.", "Falló el paso anterior.", cont)

    # ── 3) Copiar el interrogatorio SOLO si no existe ─────────────────────
    origen_resp = RAIZ / "plantillas" / "RESPUESTAS.md"
    destino_resp = RAIZ / "RESPUESTAS.md"
    if destino_resp.exists():
        lc.ok("RESPUESTAS.md ya existía: lo respeto, no lo piso.", cont)
        lc.info("Tus respuestas quedan intactas.")
    elif origen_resp.is_file():
        shutil.copyfile(origen_resp, destino_resp)
        lc.ok("RESPUESTAS.md copiado (en blanco, para que lo respondas).", cont)
    else:
        lc.error(
            "No encuentro plantillas/RESPUESTAS.md.",
            "¿Está completo el lab? Vuelve a clonar el repositorio.",
            cont,
        )

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.info(
            "Código y salidas recuperados. El interrogatorio (RESPUESTAS.md) queda "
            "a propósito SIN responder: esa parte se gana pensando, no copiando."
        )
        lc.info("Ahora completa RESPUESTAS.md y corre: uv run python bin/verificar.py")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
