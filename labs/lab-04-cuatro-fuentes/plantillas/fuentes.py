"""Las cuatro fuentes — PLANTILLA para la Ruta Artesano 🛠️ (Lab 04).

Este archivo YA CORRE, pero no lee nada de verdad: las cargas devuelven tablas
vacías y el resumen da cero. Completa los seis TODO para que lea las cuatro
fuentes, registre el pago transaccionalmente y exporte el resumen.

Reglas del juego:
  - Copia este archivo a la raíz del lab con el nombre fuentes.py
        (macOS/Linux)  cp plantillas/fuentes.py fuentes.py
        (Windows)      Copy-Item plantillas\\fuentes.py fuentes.py
  - Completa los TODO EN ORDEN (1 → 6). Ejecuta seguido:  uv run python fuentes.py
  - ¿Trabado >10 min? Mira SOLO esa función en soluciones/fuentes.py.
  - Recuerda: datos/fuentes/ es de SOLO LECTURA. Todo lo tuyo va a salidas/.

Se ejecuta SIEMPRE desde la raíz del lab:

    uv run python fuentes.py
"""

import datetime
import json
import shutil
import sqlite3
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent
FUENTES = RAIZ / "datos" / "fuentes"
SALIDAS = RAIZ / "salidas"


# ─── Lectores (reciben la ruta como parámetro — C12) ──────────────────────

def cargar_pagos(ruta):
    """Lee el CSV de Tesorería. Devuelve un DataFrame [codigo, fecha, monto]."""
    # TODO 1 — pandas lee un CSV en una línea: pd.read_csv(ruta, encoding="utf-8").
    #          Devuélvelo. (Quien escribió bien el CSV te hizo el 90 % del trabajo.)
    return pd.DataFrame(columns=["codigo", "fecha", "monto"])


def cargar_permisos(ruta):
    """Lee el Excel de Turismo, hoja 'Permisos'. [folio, evento, valor]."""
    # TODO 2 — pd.read_excel(ruta, sheet_name="Permisos"). Ojo: el nombre de la
    #          hoja va EXACTO ("Permisos", con mayúscula).
    return pd.DataFrame(columns=["folio", "evento", "valor"])


def cargar_multas(ruta):
    """Lee el JSON de multas por el camino stdlib: json.load -> DataFrame."""
    # TODO 3 — Abre el archivo con open(ruta, encoding="utf-8"), usa json.load(f)
    #          para obtener una LISTA de dicts, y pásala a pd.DataFrame(...).
    return pd.DataFrame(columns=["codigo", "motivo", "monto"])


def cargar_contribuyentes(ruta):
    """Lee la tabla contribuyentes de la BD SQLite. Cierre garantizado (C11)."""
    con = sqlite3.connect(ruta)
    try:
        return pd.read_sql("SELECT codigo, nombre, giro FROM contribuyentes", con)
    finally:
        con.close()


# ─── El corazón transaccional ─────────────────────────────────────────────

def registrar_pago(ruta_bd, codigo, fecha, monto):
    """Registra un pago SOLO si el código existe. Transaccional (commit/rollback)."""
    con = sqlite3.connect(ruta_bd)
    try:
        con.execute(
            "CREATE TABLE IF NOT EXISTS pagos_registrados "
            "(codigo TEXT, fecha TEXT, monto INTEGER)"
        )
        # TODO 4 — El grande. Sigue este guion:
        #   1) Averigua si el código existe en contribuyentes:
        #        existe = con.execute("SELECT 1 FROM contribuyentes WHERE codigo = ?",
        #                             (codigo,)).fetchone()
        #   2) Si NO existe -> con.rollback() y return False (no queda media boleta).
        #   3) Si existe -> INSERT en pagos_registrados (codigo, fecha, monto),
        #        luego con.commit() (el "timbre") y return True.
        #   Pista: envuélvelo de modo que, ante cualquier error, hagas con.rollback().
        return False
    except Exception:
        con.rollback()
        return False
    finally:
        con.close()


# ─── Consolidación y exportación ──────────────────────────────────────────

def resumen_ingresos(pagos, permisos, multas):
    """Resumen de ingresos por fuente y total. Ints nativos."""
    # TODO 5 — Suma la columna de monto de cada DataFrame (pagos["monto"],
    #          permisos["valor"], multas["monto"]) con .sum(), envuelto en int().
    #          Devuelve un dict con claves "pagos", "permisos", "multas", "total".
    return {"pagos": 0, "permisos": 0, "multas": 0, "total": 0}


def exportar_resumen(resumen, carpeta_salidas):
    """Exporta el resumen a los cuatro formatos dentro de carpeta_salidas."""
    carpeta = Path(carpeta_salidas)
    carpeta.mkdir(exist_ok=True)
    df = pd.DataFrame(
        [("pagos", resumen["pagos"]), ("permisos", resumen["permisos"]),
         ("multas", resumen["multas"]), ("total", resumen["total"])],
        columns=["fuente", "monto"],
    )
    # TODO 6 — Exporta el MISMO df a los cuatro formatos:
    #   df.to_csv(carpeta / "resumen.csv", index=False)
    #   df.to_excel(carpeta / "resumen.xlsx", index=False)
    #   df.to_json(carpeta / "resumen.json", orient="records", indent=2, force_ascii=False)
    #   y a SQLite: abre sqlite3.connect(carpeta / "gestion.db") y usa
    #     df.to_sql("resumen_mensual", con, if_exists="replace", index=False)
    #   (cierra la conexión con try/finally).
    return None


def construir_informe(resumen, pago_ok, pago_rechazado):
    """Arma el informe de ingresos del mes como una sola cadena."""
    lineas = []
    lineas.append("INGRESOS DEL MES — Dirección de Rentas de Puerto Siracusa")
    lineas.append("=" * 58)
    lineas.append(f"{'Pagos (Tesorería)':<22}: ${resumen['pagos']:,} CLP")
    lineas.append(f"{'Permisos (Turismo)':<22}: ${resumen['permisos']:,} CLP")
    lineas.append(f"{'Multas (sistema)':<22}: ${resumen['multas']:,} CLP")
    lineas.append("-" * 58)
    lineas.append(f"{'TOTAL':<22}: ${resumen['total']:,} CLP")
    lineas.append("")
    lineas.append("Registro transaccional:")
    lineas.append(f"  Pago válido   : {'ACEPTADO (commit)' if pago_ok else 'RECHAZADO'}")
    lineas.append(f"  Pago inválido : {'ACEPTADO' if pago_rechazado else 'RECHAZADO (rollback — código inexistente)'}")
    return "\n".join(lineas)


def main():
    pagos = cargar_pagos(FUENTES / "pagos.csv")
    permisos = cargar_permisos(FUENTES / "permisos_eventos.xlsx")
    multas = cargar_multas(FUENTES / "multas.json")
    _ = cargar_contribuyentes(FUENTES / "contribuyentes.db")

    SALIDAS.mkdir(exist_ok=True)
    bd_trabajo = SALIDAS / "registro.db"
    shutil.copyfile(FUENTES / "contribuyentes.db", bd_trabajo)

    hoy = datetime.date.today().isoformat()
    pago_ok = registrar_pago(bd_trabajo, "PS-1031-G", hoy, 22000)
    pago_rechazado = registrar_pago(bd_trabajo, "PS-9999-X", hoy, 5000)

    resumen = resumen_ingresos(pagos, permisos, multas)
    informe = construir_informe(resumen, pago_ok, pago_rechazado)
    print(informe)

    (SALIDAS / "informe_fuentes.txt").write_text(informe + "\n", encoding="utf-8")
    exportar_resumen(resumen, SALIDAS)

    print()
    print(f"[INFO] Informe y exportaciones en: {SALIDAS}")


if __name__ == "__main__":
    main()
