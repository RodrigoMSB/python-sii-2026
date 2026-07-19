"""Recuperador del Lab 06 — modo instructor / rezagado.

    uv run python bin/recuperar_lab.py

Restaura los 3 CSV si fueron alterados (git es la fuente de verdad), repone
soluciones/tablero.py → tablero.py, lo ejecuta para regenerar salidas/ (informe,
csv, xlsx y gráfico PNG), y copia plantillas/RESPUESTAS.md → RESPUESTAS.md solo si
no existe. Nunca responde el interrogatorio.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

CSVS = ["datos/censo_limpio.csv", "datos/pagos_junio.csv", "datos/pagos_julio.csv"]


def _restaurar_csvs(cont):
    en_git = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                            cwd=str(RAIZ), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if en_git.returncode != 0 or en_git.stdout.strip() != "true":
        lc.info("El lab no está dentro de un repo git: no puedo restaurar los CSV automáticamente.")
        if all((RAIZ / c).is_file() for c in CSVS):
            lc.ok("Los 3 CSV están presentes (no verificados contra git).", cont)
        else:
            lc.error("Falta algún CSV y no hay git para restaurarlo.", "Vuelve a clonar el repositorio.", cont)
        return
    res = subprocess.run(["git", "checkout", "--", *CSVS], cwd=str(RAIZ), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode == 0:
        lc.ok("Los 3 CSV restaurados a su versión oficial (git checkout).", cont)
    else:
        pista = res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "Revisa git."
        lc.error("No pude restaurar los CSV desde git.", pista, cont)


def main() -> int:
    lc.titulo("Recuperador del Lab 06")
    cont = lc.Contador()

    _restaurar_csvs(cont)

    origen = RAIZ / "soluciones" / "tablero.py"
    destino = RAIZ / "tablero.py"
    if origen.is_file():
        shutil.copyfile(origen, destino)
        lc.ok("tablero.py restaurado desde soluciones/.", cont)
    else:
        lc.error("No encuentro soluciones/tablero.py.", "¿Lab completo? Vuelve a clonar.", cont)

    if destino.is_file():
        res = subprocess.run([sys.executable, str(destino)], cwd=str(RAIZ), capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode == 0 and (RAIZ / "salidas" / "informe_tablero.txt").is_file():
            lc.ok("salidas/ (informe, tablero.csv/xlsx y saldo_por_rubro.png) regeneradas.", cont)
        else:
            pista = res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "Revisa los CSV."
            lc.error("No pude regenerar las salidas ejecutando tablero.py.", pista, cont)
    else:
        lc.error("No hay tablero.py que ejecutar.", "Falló el paso anterior.", cont)

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
        lc.info("CSV, código y salidas recuperados. El interrogatorio (RESPUESTAS.md) queda "
                "SIN responder a propósito: esa parte se gana pensando, no copiando.")
        lc.info("Ahora completa RESPUESTAS.md y corre: uv run python bin/verificar.py")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
