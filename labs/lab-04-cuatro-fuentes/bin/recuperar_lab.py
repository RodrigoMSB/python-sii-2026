"""Recuperador del Lab 04 — modo instructor / rezagado.

    uv run python bin/recuperar_lab.py

Reconstruye TODO lo necesario, en orden:
  1. Regenera las cuatro fuentes (datos/fuentes/) desde la semilla — por si
     alguna se corrompió. La generación es determinista (bytes idénticos).
  2. Copia soluciones/fuentes.py → fuentes.py (raíz) y lo ejecuta para regenerar
     salidas/.
  3. Copia plantillas/RESPUESTAS.md → RESPUESTAS.md SOLO si no existe.

Nunca responde el interrogatorio.
"""

from __future__ import annotations

import shutil
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

FUENTES = RAIZ / "datos" / "fuentes"


def _leible(nombre):
    """Devuelve True si la fuente existe y se puede leer; False si falta o está corrupta."""
    ruta = FUENTES / nombre
    if not ruta.exists():
        return False
    try:
        import pandas as pd
        if nombre.endswith(".csv"):
            pd.read_csv(ruta)
        elif nombre.endswith(".xlsx"):
            pd.read_excel(ruta, sheet_name="Permisos")
        elif nombre.endswith(".json"):
            with ruta.open(encoding="utf-8") as f:
                json.load(f)
        elif nombre.endswith(".db"):
            con = sqlite3.connect(ruta)
            try:
                con.execute("SELECT COUNT(*) FROM contribuyentes").fetchone()
            finally:
                con.close()
        return True
    except Exception:  # noqa: BLE001 - cualquier fallo de lectura = corrupta
        return False


def _limpiar_corruptas():
    """Borra las fuentes presentes pero corruptas para que el generador las reponga.

    Regla (H-04): la cura de una fuente corrupta-pero-presente es borrar el archivo
    dañado y regenerar. El generador en modo por defecto solo repone lo que falta,
    así que primero eliminamos lo que no se puede leer.
    """
    borradas = []
    for nombre in ("pagos.csv", "permisos_eventos.xlsx", "multas.json", "contribuyentes.db"):
        ruta = FUENTES / nombre
        if ruta.exists() and not _leible(nombre):
            ruta.unlink()
            borradas.append(nombre)
    return borradas


def main() -> int:
    lc.titulo("Recuperador del Lab 04")
    cont = lc.Contador()

    # 1) Reponer fuentes: borrar las corruptas (H-04) y regenerar lo que falte.
    corruptas = _limpiar_corruptas()
    if corruptas:
        lc.info(f"Fuentes corruptas detectadas y eliminadas para reponerlas: {', '.join(corruptas)}.")
    gen = subprocess.run([sys.executable, str(RAIZ / "bin" / "generar_fuentes.py")],
                         cwd=str(RAIZ), capture_output=True, text=True)
    if gen.returncode == 0:
        lc.ok("Fuentes verificadas y repuestas en datos/fuentes/ (csv, xlsx, json, db).", cont)
    else:
        pista = gen.stderr.strip().splitlines()[-1] if gen.stderr.strip() else "Revisa openpyxl."
        lc.error("No pude reponer las fuentes.", pista, cont)

    # 2) Reponer fuentes.py y regenerar salidas.
    origen = RAIZ / "soluciones" / "fuentes.py"
    destino = RAIZ / "fuentes.py"
    if origen.is_file():
        shutil.copyfile(origen, destino)
        lc.ok("fuentes.py restaurado desde soluciones/.", cont)
    else:
        lc.error("No encuentro soluciones/fuentes.py.", "¿Lab completo? Vuelve a clonar.", cont)

    if destino.is_file():
        res = subprocess.run([sys.executable, str(destino)], cwd=str(RAIZ),
                             capture_output=True, text=True)
        if res.returncode == 0 and (RAIZ / "salidas" / "informe_fuentes.txt").is_file():
            lc.ok("salidas/informe_fuentes.txt y exportaciones regenerados.", cont)
        else:
            pista = res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "Revisa las fuentes."
            lc.error("No pude regenerar las salidas ejecutando fuentes.py.", pista, cont)
    else:
        lc.error("No hay fuentes.py que ejecutar.", "Falló el paso anterior.", cont)

    # 3) Interrogatorio.
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
        lc.info("Fuentes, código y salidas recuperados. El interrogatorio (RESPUESTAS.md) queda "
                "SIN responder a propósito: esa parte se gana pensando, no copiando.")
        lc.info("Ahora completa RESPUESTAS.md y corre: uv run python bin/verificar.py")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
