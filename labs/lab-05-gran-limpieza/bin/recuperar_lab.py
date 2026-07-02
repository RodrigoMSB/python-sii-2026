"""Recuperador del Lab 05 — modo instructor / rezagado.

    uv run python bin/recuperar_lab.py

Reconstruye lo necesario, en orden:
  1. Restaura el censo (datos/censo_patentes.csv) si fue alterado. El censo es
     texto VERSIONADO: la fuente de verdad es git, así que se restaura con
     `git checkout -- ...`. Decisión documentada: si el lab no está dentro de un
     repo git (caso raro), se avisa y se continúa (no hay copia de respaldo
     interna para no duplicar el dataset).
  2. Copia soluciones/limpiar.py → limpiar.py y lo ejecuta para regenerar salidas/.
  3. Copia plantillas/RESPUESTAS.md → RESPUESTAS.md SOLO si no existe.

Nunca responde el interrogatorio.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

CENSO_REL = "datos/censo_patentes.csv"


def _restaurar_censo(cont):
    censo = RAIZ / CENSO_REL
    esta_en_git = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                                 cwd=str(RAIZ), capture_output=True, text=True)
    if esta_en_git.returncode != 0 or esta_en_git.stdout.strip() != "true":
        lc.info("El lab no está dentro de un repo git: no puedo restaurar el censo automáticamente.")
        if censo.is_file():
            lc.ok("El censo está presente (no se pudo verificar contra git).", cont)
        else:
            lc.error("Falta el censo y no hay git para restaurarlo.", "Vuelve a clonar el repositorio.", cont)
        return
    res = subprocess.run(["git", "checkout", "--", CENSO_REL], cwd=str(RAIZ),
                         capture_output=True, text=True)
    if res.returncode == 0:
        lc.ok("Censo restaurado a la versión oficial (git checkout).", cont)
    else:
        pista = res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "Revisa el estado de git."
        lc.error("No pude restaurar el censo desde git.", pista, cont)


def main() -> int:
    lc.titulo("Recuperador del Lab 05")
    cont = lc.Contador()

    _restaurar_censo(cont)

    origen = RAIZ / "soluciones" / "limpiar.py"
    destino = RAIZ / "limpiar.py"
    if origen.is_file():
        shutil.copyfile(origen, destino)
        lc.ok("limpiar.py restaurado desde soluciones/.", cont)
    else:
        lc.error("No encuentro soluciones/limpiar.py.", "¿Lab completo? Vuelve a clonar.", cont)

    if destino.is_file():
        res = subprocess.run([sys.executable, str(destino)], cwd=str(RAIZ),
                             capture_output=True, text=True)
        if res.returncode == 0 and (RAIZ / "salidas" / "informe_limpieza.txt").is_file():
            lc.ok("salidas/informe_limpieza.txt y censo_limpio.* regenerados.", cont)
        else:
            pista = res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "Revisa el censo."
            lc.error("No pude regenerar las salidas ejecutando limpiar.py.", pista, cont)
    else:
        lc.error("No hay limpiar.py que ejecutar.", "Falló el paso anterior.", cont)

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
        lc.info("Censo, código y salidas recuperados. El interrogatorio (RESPUESTAS.md) queda "
                "SIN responder a propósito: esa parte se gana pensando, no copiando.")
        lc.info("Ahora completa RESPUESTAS.md y corre: uv run python bin/verificar.py")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
