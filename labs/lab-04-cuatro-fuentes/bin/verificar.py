"""Verificador del Lab 04 — el juez de las cuatro fuentes.

Se ejecuta desde la raíz del lab:

    uv run python bin/verificar.py

Solo lectura sobre tu trabajo y sobre las fuentes del curso (C1): para probar la
transacción trabaja SIEMPRE sobre COPIAS temporales, nunca sobre datos/fuentes/.
Genera además sus propias "fuentes sorpresa" en un directorio temporal (gracias
a que tus lectores reciben la ruta como parámetro — C12): si copiaste cifras
fijas, el sorpresa te delata. Blindaje anti-breakpoint (C8) como siempre.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import random
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

_BREAKPOINT = {"golpeado": False}
sys.breakpointhook = lambda *a, **k: _BREAKPOINT.__setitem__("golpeado", True)

try:
    import pandas as pd
except Exception as exc:  # pragma: no cover
    lc.error(f"No pude importar pandas: {exc}", "Corre el preparador: bash bin/00-preparar.sh")
    sys.exit(1)

FUENTES = RAIZ / "datos" / "fuentes"
SALIDAS = RAIZ / "salidas"
RUTA_PROGRAMA = RAIZ / "fuentes.py"
RUTA_RESPUESTAS = RAIZ / "RESPUESTAS.md"
MARCADOR_PENDIENTE = "(escribe aquí tu respuesta)"

FUNCIONES = ("cargar_pagos", "cargar_permisos", "cargar_multas", "cargar_contribuyentes",
             "registrar_pago", "resumen_ingresos", "exportar_resumen", "construir_informe")


# ─── Fuentes sorpresa en un directorio temporal ───────────────────────────

def _fuentes_sorpresa(tmp):
    rng = random.Random()
    npag, nper, nmul = rng.randint(4, 8), rng.randint(4, 8), rng.randint(4, 8)
    pagos = [[f"ZZ-9{rng.randint(0, 999):03d}-C", f"2026-06-{rng.randint(1, 28):02d}",
              rng.choice([10000, 25000, 50000, 80000])] for _ in range(npag)]
    permisos = [[f"EV-{rng.randint(300, 399)}", f"Evento {i}",
                 rng.choice([50000, 90000, 120000])] for i in range(nper)]
    multas = [[f"ZZ-9{rng.randint(0, 999):03d}-T", f"Motivo {i}",
               rng.choice([15000, 30000, 45000])] for i in range(nmul)]
    contrib = [[f"CC-{i:02d}", f"Contribuyente {i}", "Giro"] for i in range(5)]

    r_csv, r_xlsx, r_json, r_db = tmp / "p.csv", tmp / "p.xlsx", tmp / "m.json", tmp / "c.db"
    with r_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["codigo", "fecha", "monto"]); w.writerows(pagos)
    pd.DataFrame(permisos, columns=["folio", "evento", "valor"]).to_excel(
        r_xlsx, sheet_name="Permisos", index=False)
    with r_json.open("w", encoding="utf-8") as f:
        json.dump([{"codigo": c, "motivo": m, "monto": v} for c, m, v in multas], f, ensure_ascii=False)
    with sqlite3.connect(r_db) as con:
        con.execute("CREATE TABLE contribuyentes (codigo TEXT PRIMARY KEY, nombre TEXT, giro TEXT)")
        con.executemany("INSERT INTO contribuyentes VALUES (?,?,?)", contrib)
        con.commit()

    ref = {
        "shapes": {"pagos": (npag, 3), "permisos": (nper, 3), "multas": (nmul, 3)},
        "resumen": {
            "pagos": sum(r[2] for r in pagos),
            "permisos": sum(r[2] for r in permisos),
            "multas": sum(r[2] for r in multas),
        },
    }
    ref["resumen"]["total"] = sum(ref["resumen"][k] for k in ("pagos", "permisos", "multas"))
    return {"csv": r_csv, "xlsx": r_xlsx, "json": r_json, "db": r_db}, ref


# ─── Carga del programa ────────────────────────────────────────────────────

def cargar_programa():
    spec = importlib.util.spec_from_file_location("fuentes_alumno", RUTA_PROGRAMA)
    modulo = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(modulo)
        return modulo, None
    except BaseException as exc:  # noqa: BLE001
        return None, exc


def _llamar(func, *args):
    try:
        return True, func(*args)
    except BaseException as exc:  # noqa: BLE001
        return False, exc


def _check_carga(func, ruta, shape_esp, cols_esp, etiqueta, cont, **kw):
    if func is None:
        lc.error(f"{etiqueta}: la función no existe.", "No la renombres.", cont); return
    ok, df = _llamar(func, ruta) if not kw else _llamar(func, ruta)
    if ok and isinstance(df, pd.DataFrame) and df.shape == shape_esp and list(df.columns) == cols_esp:
        lc.ok(f"{etiqueta}: DataFrame {df.shape} con columnas {cols_esp}.", cont)
    else:
        det = f"shape={getattr(df, 'shape', None)}, cols={list(df.columns) if ok and isinstance(df, pd.DataFrame) else df}"
        lc.error(f"{etiqueta} incorrecta: {det}, se esperaba {shape_esp} y {cols_esp}.",
                 "Revisa la ruta, el motor (sheet_name en Excel) y las columnas.", cont)


def main() -> int:
    lc.titulo("Verificador del Lab 04 — Las cuatro fuentes")
    cont = lc.Contador()

    if RUTA_PROGRAMA.exists():
        lc.ok("fuentes.py está en la raíz del lab.", cont)
    else:
        lc.error("No encuentro fuentes.py en la raíz del lab.",
                 "Cópialo desde plantillas/ o soluciones/. Ver Guía 5.", cont)
        return _cerrar(cont)

    modulo, err = cargar_programa()
    if err is None:
        lc.ok("fuentes.py se cargó sin errores.", cont)
    else:
        pista = "Lee el traceback de abajo hacia arriba."
        if isinstance(err, ModuleNotFoundError):
            pista = "¿Falta pandas/openpyxl? Corre el preparador."
        lc.error(f"fuentes.py falló al cargar: {type(err).__name__}: {err}", pista, cont)
        for _ in range(7):
            lc.error("No evaluable: primero hay que poder cargar fuentes.py.",
                     "Corrige el error de carga y reejecuta.", cont)
        return _cerrar(cont)

    faltan = [n for n in FUNCIONES if not callable(getattr(modulo, n, None))]
    if not faltan:
        lc.ok("Existen las 8 funciones del lab y son invocables.", cont)
    else:
        lc.error(f"Faltan o no son funciones: {', '.join(faltan)}.", "No las renombres.", cont)

    # 4-7) cargas oficiales
    _check_carga(getattr(modulo, "cargar_pagos", None), FUENTES / "pagos.csv",
                 (12, 3), ["codigo", "fecha", "monto"], "cargar_pagos [oficial]", cont)
    _check_carga(getattr(modulo, "cargar_permisos", None), FUENTES / "permisos_eventos.xlsx",
                 (8, 3), ["folio", "evento", "valor"], "cargar_permisos [oficial]", cont)
    _check_carga(getattr(modulo, "cargar_multas", None), FUENTES / "multas.json",
                 (10, 3), ["codigo", "motivo", "monto"], "cargar_multas [oficial]", cont)
    _check_carga(getattr(modulo, "cargar_contribuyentes", None), FUENTES / "contribuyentes.db",
                 (10, 3), ["codigo", "nombre", "giro"], "cargar_contribuyentes [oficial]", cont)

    # 8) resumen oficial
    _check_resumen_oficial(modulo, cont)
    # 9) fuentes sorpresa
    _check_sorpresa(modulo, cont)
    # 10) transaccional
    _check_transaccional(modulo, cont)
    # 11) salidas
    _check_salidas(cont)

    return _cerrar(cont)


def _check_resumen_oficial(modulo, cont):
    fp, fpe, fm, fr = (getattr(modulo, n, None) for n in
                       ("cargar_pagos", "cargar_permisos", "cargar_multas", "resumen_ingresos"))
    if None in (fp, fpe, fm, fr):
        lc.error("No puedo probar resumen_ingresos (faltan funciones).", "No renombres.", cont); return
    try:
        r = fr(fp(FUENTES / "pagos.csv"), fpe(FUENTES / "permisos_eventos.xlsx"), fm(FUENTES / "multas.json"))
    except Exception as exc:  # noqa: BLE001
        lc.error(f"resumen_ingresos lanzó {type(exc).__name__}: {exc}", "Revisa las cargas y las sumas.", cont); return
    esperado = {"pagos": 677500, "permisos": 1000000, "multas": 395000, "total": 2072500}
    if isinstance(r, dict) and {k: r.get(k) for k in esperado} == esperado and all(type(r[k]) is int for k in esperado):
        lc.ok("resumen_ingresos [oficial] == {pagos:677500, permisos:1000000, multas:395000, total:2072500}.", cont)
    else:
        lc.error(f"resumen_ingresos [oficial]: obtuvo {r!r}, se esperaba {esperado} (ints nativos).",
                 "Suma la columna de monto de cada fuente con .sum() y envuélvela en int().", cont)


def _check_sorpresa(modulo, cont):
    with tempfile.TemporaryDirectory() as d:
        rutas, ref = _fuentes_sorpresa(Path(d))
        try:
            dp = modulo.cargar_pagos(rutas["csv"])
            dpe = modulo.cargar_permisos(rutas["xlsx"])
            dm = modulo.cargar_multas(rutas["json"])
            r = modulo.resumen_ingresos(dp, dpe, dm)
        except Exception as exc:  # noqa: BLE001
            lc.error(f"Fuentes sorpresa: una función lanzó {type(exc).__name__}: {exc}",
                     "Tus lectores deben leer la ruta que reciben, no una fija.", cont)
            return
        problemas = []
        if getattr(dp, "shape", None) != ref["shapes"]["pagos"]:
            problemas.append("cargar_pagos")
        if getattr(dpe, "shape", None) != ref["shapes"]["permisos"]:
            problemas.append("cargar_permisos")
        if getattr(dm, "shape", None) != ref["shapes"]["multas"]:
            problemas.append("cargar_multas")
        if not (isinstance(r, dict) and {k: r.get(k) for k in ref["resumen"]} == ref["resumen"]):
            problemas.append("resumen_ingresos")
        if not problemas:
            lc.ok("Fuentes sorpresa (temporales, aleatorias): cargas y resumen coinciden con la referencia.", cont)
        else:
            lc.error("Fuentes sorpresa: fallan " + ", ".join(problemas) + ".",
                     "Si el oficial pasó pero el sorpresa no, dejaste valores fijos. Lee la ruta que te pasan.", cont)


def _check_transaccional(modulo, cont):
    func = getattr(modulo, "registrar_pago", None)
    if func is None:
        lc.error("registrar_pago no existe.", "No la renombres.", cont); return
    with tempfile.TemporaryDirectory() as d:
        copia = Path(d) / "c.db"
        shutil.copyfile(FUENTES / "contribuyentes.db", copia)  # copia: nunca la original
        ok_val, r_val = _llamar(func, copia, "PS-1006-G", "2026-06-30", 22000)  # existe
        n1 = _contar(copia)
        ok_inv, r_inv = _llamar(func, copia, "PS-9999-X", "2026-06-30", 5000)   # no existe
        n2 = _contar(copia)
        if ok_val and r_val is True and n1 == 1 and ok_inv and r_inv is False and n2 == 1:
            lc.ok("Transacción: válido→True (fila registrada); inválido→False (rollback, la tabla NO crece).", cont)
        else:
            lc.error(f"Transacción incorrecta: válido→{r_val if ok_val else 'error'} (filas={n1}), "
                     f"inválido→{r_inv if ok_inv else 'error'} (filas={n2}). Esperado True/1 y False/1.",
                     "Valida que el código exista; si no, rollback y return False; si sí, INSERT + commit.", cont)


def _contar(ruta_bd):
    con = sqlite3.connect(ruta_bd)
    try:
        try:
            return con.execute("SELECT COUNT(*) FROM pagos_registrados").fetchone()[0]
        except sqlite3.OperationalError:
            return 0
    finally:
        con.close()


def _check_salidas(cont):
    informe = SALIDAS / "informe_fuentes.txt"
    problemas = []
    if not (informe.exists() and "2,072,500" in informe.read_text(encoding="utf-8")):
        problemas.append("informe_fuentes.txt con 2,072,500")
    for nombre in ("resumen.csv", "resumen.xlsx", "resumen.json"):
        if not (SALIDAS / nombre).exists():
            problemas.append(nombre)
    try:
        pd.read_csv(SALIDAS / "resumen.csv")
        pd.read_excel(SALIDAS / "resumen.xlsx")
    except Exception:  # noqa: BLE001
        problemas.append("csv/xlsx legibles")
    gestion = SALIDAS / "gestion.db"
    if gestion.exists():
        con = sqlite3.connect(gestion)
        try:
            con.execute("SELECT * FROM resumen_mensual").fetchall()
        except Exception:  # noqa: BLE001
            problemas.append("gestion.db/resumen_mensual")
        finally:
            con.close()
    else:
        problemas.append("gestion.db")

    if not problemas:
        lc.ok("salidas/ tiene el informe ($2,072,500) y los 4 exportados (csv, xlsx, json, gestion.db).", cont)
    else:
        lc.error("Faltan/mal en salidas: " + ", ".join(problemas) + ".",
                 "Ejecuta uv run python fuentes.py para generar el informe y las exportaciones.", cont)


def _cerrar(cont):
    if not RUTA_RESPUESTAS.exists():
        lc.error("No encuentro RESPUESTAS.md en la raíz del lab.",
                 "Copia el interrogatorio y respóndelo: cp plantillas/RESPUESTAS.md RESPUESTAS.md.", cont)
    else:
        pend = RUTA_RESPUESTAS.read_text(encoding="utf-8").count(MARCADOR_PENDIENTE)
        if pend == 0:
            lc.ok("RESPUESTAS.md está completo (sin respuestas pendientes).", cont)
        else:
            lc.error(f"RESPUESTAS.md tiene {pend} respuesta(s) sin contestar.",
                     f"Reemplaza cada '{MARCADOR_PENDIENTE}' por tu explicación.", cont)

    if _BREAKPOINT["golpeado"]:
        print()
        lc.info("Detecté un breakpoint() en tu código y lo neutralicé para no colgarme (C8). "
                "Quítalo de fuentes.py antes de entregar.")

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.titulo("Don Arquímedes reparte el informe a las oficinas")
        print(
            "Don Arquímedes mira los cuatro archivos exportados y se ríe: «Cada oficina\n"
            "recibe el informe en su propio dialecto. Y la base de datos, por fin, sin\n"
            "miedo: lo que se timbra queda, lo que falla se anula. Buen trabajo, analista.»\n"
        )
        print(
            f"{lc.CIAN}Próxima jornada — Lab 05:{lc.RESET} hasta ahora los datos llegaron\n"
            "ordenaditos. Se acabó: en el Módulo 3 llegan SUCIOS —espacios, mayúsculas,\n"
            "nulos, duplicados, fechas en tres formatos—. La gran limpieza te espera.\n"
            "Nos vemos en el mesón."
        )
    return codigo


if __name__ == "__main__":
    sys.exit(main())
