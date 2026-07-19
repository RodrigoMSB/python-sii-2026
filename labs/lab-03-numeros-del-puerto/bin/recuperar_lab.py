"""Recuperador del Lab 03 — modo instructor / rezagado.

Reconstruye código y salidas desde la solución oficial:

    uv run python bin/recuperar_lab.py

Único script del lab que escribe. Copia soluciones/panorama.py → raíz, ejecuta
el programa para regenerar salidas/, y copia el interrogatorio SOLO si no
existe. Nunca responde RESPUESTAS.md.
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
    lc.titulo("Recuperador del Lab 03")
    cont = lc.Contador()

    origen = RAIZ / "soluciones" / "panorama.py"
    destino = RAIZ / "panorama.py"
    if origen.is_file():
        shutil.copyfile(origen, destino)
        lc.ok("panorama.py restaurado desde soluciones/.", cont)
    else:
        lc.error("No encuentro soluciones/panorama.py.", "¿Lab completo? Vuelve a clonar.", cont)

    if destino.is_file():
        resultado = subprocess.run([sys.executable, str(destino)], cwd=str(RAIZ),
                                    capture_output=True, text=True, encoding="utf-8", errors="replace")
        if resultado.returncode == 0 and (RAIZ / "salidas" / "informe_panorama.txt").is_file():
            lc.ok("salidas/informe_panorama.txt regenerado.", cont)
        else:
            pista = (resultado.stderr.strip().splitlines()[-1]
                     if resultado.stderr.strip() else "Revisa que numpy/pandas estén instalados (preparador).")
            lc.error("No pude regenerar el informe ejecutando el programa.", pista, cont)
    else:
        lc.error("No hay panorama.py que ejecutar.", "Falló el paso anterior.", cont)

    origen_resp = RAIZ / "plantillas" / "RESPUESTAS.md"
    destino_resp = RAIZ / "RESPUESTAS.md"
    if destino_resp.exists():
        lc.ok("RESPUESTAS.md ya existía: lo respeto, no lo piso.", cont)
        lc.info("Tus respuestas quedan intactas.")
    elif origen_resp.is_file():
        shutil.copyfile(origen_resp, destino_resp)
        lc.ok("RESPUESTAS.md copiado (en blanco, para que lo respondas).", cont)
    else:
        lc.error("No encuentro plantillas/RESPUESTAS.md.", "¿Lab completo? Vuelve a clonar.", cont)

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.info("Código y salidas recuperados. El interrogatorio (RESPUESTAS.md) queda a "
                "propósito SIN responder: esa parte se gana pensando, no copiando.")
        lc.info("Ahora completa RESPUESTAS.md y corre: uv run python bin/verificar.py")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
