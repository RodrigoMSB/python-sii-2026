"""Recuperador del Capstone — SOLO INSTRUCTOR / DEMOSTRACIÓN.

    uv run python bin/recuperar_lab.py

⚠️ ADVERTENCIA: en el capstone, ejecutar el recuperador NO certifica al alumno.
Reconstruye los productos desde la solución de REFERENCIA solo para demostración
(mostrar en clase cómo debería verse el resultado). La nota la pone el relator con
la rúbrica; el examen se aprueba construyendo, no recuperando. La BITÁCORA jamás se
toca.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

TEXTO = ["datos/censo_anual.csv", "datos/multas.json"]


def _restaurar_fuentes(cont):
    en_git = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                            cwd=str(RAIZ), capture_output=True, text=True)
    if en_git.returncode == 0 and en_git.stdout.strip() == "true":
        subprocess.run(["git", "checkout", "--", *TEXTO], cwd=str(RAIZ), capture_output=True, text=True)
        lc.ok("Fuentes de texto restauradas (git checkout).", cont)
    else:
        lc.info("Sin git: no restauro las fuentes de texto automáticamente.")
    # binarios: regenerar lo que falte (solo-faltantes, H-04)
    gen = subprocess.run([sys.executable, str(RAIZ / "bin" / "generar_fuentes.py")],
                         cwd=str(RAIZ), capture_output=True, text=True)
    if gen.returncode == 0:
        lc.ok("Fuentes binarias verificadas/repuestas (xlsx, db).", cont)
    else:
        lc.error("No pude reponer las fuentes binarias.", "Revisa openpyxl.", cont)


def main() -> int:
    lc.titulo("Recuperador del Capstone (SOLO INSTRUCTOR)")
    print()
    lc.info("⚠️  Esto reconstruye los productos desde la REFERENCIA para DEMOSTRACIÓN.")
    lc.info("⚠️  En el capstone el rescate NO certifica: la rúbrica del relator manda.")
    print()
    cont = lc.Contador()

    _restaurar_fuentes(cont)

    origen = RAIZ / "soluciones" / "arenario.py"
    destino = RAIZ / "arenario.py"
    if origen.is_file():
        shutil.copyfile(origen, destino)
        lc.ok("arenario.py (referencia) copiado a la raíz.", cont)
    else:
        lc.error("No encuentro soluciones/arenario.py.", "¿Capstone completo? Vuelve a clonar.", cont)

    if destino.is_file():
        res = subprocess.run([sys.executable, str(destino)], cwd=str(RAIZ), capture_output=True, text=True)
        if res.returncode == 0 and (RAIZ / "salidas" / "informe_anual.txt").is_file():
            lc.ok("Productos de DEMOSTRACIÓN regenerados en salidas/.", cont)
        else:
            pista = res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "Revisa las fuentes."
            lc.error("No pude regenerar los productos.", pista, cont)
    else:
        lc.error("No hay arenario.py que ejecutar.", "Falló el paso anterior.", cont)

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.info("Productos de demostración listos. La BITÁCORA queda intacta (el alumno la responde).")
        lc.info("Recuerda: esto es para MOSTRAR, no para certificar.")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
