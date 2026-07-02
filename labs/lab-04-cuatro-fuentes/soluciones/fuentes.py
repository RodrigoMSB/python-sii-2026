"""Las cuatro fuentes — SOLUCIÓN OFICIAL (Lab 04).

Lee las cuatro fuentes del mes (cada oficina en su dialecto), registra un pago
en la base de datos de forma TRANSACCIONAL (commit si todo va bien, rollback si
algo falla), consolida el resumen de ingresos y lo exporta de vuelta en los
cuatro formatos.

Regla de oro del lab: datos/fuentes/ es de SOLO LECTURA. Todo lo que este
programa produce —incluida la copia de trabajo de la base de datos— va a
salidas/. Nunca tocamos las fuentes originales.

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
    return pd.read_csv(ruta, encoding="utf-8")


def cargar_permisos(ruta):
    """Lee el Excel de Turismo, hoja 'Permisos'. [folio, evento, valor]."""
    return pd.read_excel(ruta, sheet_name="Permisos")


def cargar_multas(ruta):
    """Lee el JSON de multas por el camino stdlib: json.load -> DataFrame."""
    with open(ruta, encoding="utf-8") as f:
        objetos = json.load(f)          # una LISTA de dicts
    return pd.DataFrame(objetos)         # pandas la traga entera


def cargar_contribuyentes(ruta):
    """Lee la tabla contribuyentes de la BD SQLite. Cierre garantizado (C11)."""
    con = sqlite3.connect(ruta)
    try:
        return pd.read_sql("SELECT codigo, nombre, giro FROM contribuyentes", con)
    finally:
        con.close()


# ─── El corazón transaccional ─────────────────────────────────────────────

def registrar_pago(ruta_bd, codigo, fecha, monto):
    """Registra un pago en pagos_registrados, SOLO si el código existe.

    Transacción: si el contribuyente existe -> INSERT + commit (retorna True).
    Si NO existe -> rollback y retorna False (no queda "media boleta").
    """
    con = sqlite3.connect(ruta_bd)
    try:
        con.execute(
            "CREATE TABLE IF NOT EXISTS pagos_registrados "
            "(codigo TEXT, fecha TEXT, monto INTEGER)"
        )
        existe = con.execute(
            "SELECT 1 FROM contribuyentes WHERE codigo = ?", (codigo,)
        ).fetchone()
        if existe is None:
            con.rollback()              # nada se registra
            return False
        con.execute(
            "INSERT INTO pagos_registrados (codigo, fecha, monto) VALUES (?, ?, ?)",
            (codigo, fecha, monto),
        )
        con.commit()                    # el "timbre": recién ahora es oficial
        return True
    except Exception:
        con.rollback()                  # ante cualquier error, anular todo
        return False
    finally:
        con.close()


# ─── Consolidación y exportación ──────────────────────────────────────────

def resumen_ingresos(pagos, permisos, multas):
    """Resumen de ingresos por fuente y total. Ints nativos."""
    total_pagos = int(pagos["monto"].sum())
    total_permisos = int(permisos["valor"].sum())
    total_multas = int(multas["monto"].sum())
    return {
        "pagos": total_pagos,
        "permisos": total_permisos,
        "multas": total_multas,
        "total": total_pagos + total_permisos + total_multas,
    }


def exportar_resumen(resumen, carpeta_salidas):
    """Exporta el resumen a los cuatro formatos dentro de carpeta_salidas."""
    carpeta = Path(carpeta_salidas)
    carpeta.mkdir(exist_ok=True)
    df = pd.DataFrame(
        [("pagos", resumen["pagos"]), ("permisos", resumen["permisos"]),
         ("multas", resumen["multas"]), ("total", resumen["total"])],
        columns=["fuente", "monto"],
    )
    df.to_csv(carpeta / "resumen.csv", index=False)
    df.to_excel(carpeta / "resumen.xlsx", index=False)
    df.to_json(carpeta / "resumen.json", orient="records", indent=2, force_ascii=False)
    con = sqlite3.connect(carpeta / "gestion.db")
    try:
        df.to_sql("resumen_mensual", con, if_exists="replace", index=False)
    finally:
        con.close()


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
    _ = cargar_contribuyentes(FUENTES / "contribuyentes.db")  # se carga para el informe/inspección

    SALIDAS.mkdir(exist_ok=True)
    # Copia de trabajo de la BD (jamás tocamos la fuente original).
    bd_trabajo = SALIDAS / "registro.db"
    shutil.copyfile(FUENTES / "contribuyentes.db", bd_trabajo)

    hoy = datetime.date.today().isoformat()
    pago_ok = registrar_pago(bd_trabajo, "PS-1031-G", hoy, 22000)          # existe -> True
    pago_rechazado = registrar_pago(bd_trabajo, "PS-9999-X", hoy, 5000)    # no existe -> False

    resumen = resumen_ingresos(pagos, permisos, multas)
    informe = construir_informe(resumen, pago_ok, pago_rechazado)
    print(informe)

    (SALIDAS / "informe_fuentes.txt").write_text(informe + "\n", encoding="utf-8")
    exportar_resumen(resumen, SALIDAS)

    print()
    print(f"[INFO] Informe y exportaciones en: {SALIDAS}")


if __name__ == "__main__":
    main()
