"""Verificador del Lab 06 — el juez del tablero.

Se ejecuta desde la raíz del lab:

    uv run python bin/verificar.py

Solo lectura. Trae implementación de referencia del pipeline y genera datasets
sorpresa (mini-censo + dos meses de pagos con al menos un huérfano) en un
directorio temporal, para probar que tu tablero funciona de verdad. Floats con
tolerancia (C10). Blindaje anti-breakpoint (C8). El gráfico se valida por el PNG
que deja tu tablero.py (Agg, headless — C16).
"""

from __future__ import annotations

import csv
import importlib.util
import random
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

DATOS = RAIZ / "datos"
SALIDAS = RAIZ / "salidas"
RUTA_PROGRAMA = RAIZ / "tablero.py"
RUTA_RESPUESTAS = RAIZ / "RESPUESTAS.md"
MARCADOR = "(escribe aquí tu respuesta)"
RUBRO = {"C": "Comercio", "G": "Gastronomía", "T": "Turismo"}
BINS = [-1, 0, 100_000, 300_000, 10**9]
LABELS = ["Sin deuda", "Baja", "Media", "Alta"]

FUNCIONES = ("cargar_censo", "cargar_pagos", "agregar_rubro", "clasificar_deuda",
             "dummies_estado", "consolidar_pagos", "construir_tablero",
             "resumen_por_rubro", "pct_dentro_del_rubro", "tabla_cruzada",
             "pivote_deuda", "graficar_saldo")


# ─── Referencia ────────────────────────────────────────────────────────────

def _ref_tablero(censo, pagos):
    censo = censo.copy()
    censo["rubro"] = censo["codigo"].str[-1].map(RUBRO)
    pagado = pagos.groupby("codigo", as_index=False)["monto"].sum().rename(columns={"monto": "pagado"})
    t = censo.merge(pagado, on="codigo", how="left", validate="1:1")
    t["pagado"] = t["pagado"].fillna(0).astype(int)
    t["saldo"] = t["deuda"] - t["pagado"]
    huer = pagado[~pagado["codigo"].isin(censo["codigo"])].copy()
    return t, huer


def _ref_metrics(censo, jun, jul):
    pagos = pd.concat([jun, jul], ignore_index=True)
    t, huer = _ref_tablero(censo, pagos)
    return {
        "concat_filas": len(pagos), "concat_total": int(pagos["monto"].sum()),
        "tablero_filas": len(t), "pagado_total": int(t["pagado"].sum()),
        "saldo_total": int(t["saldo"].sum()), "sin_pago": int((t["pagado"] == 0).sum()),
        "huerfanos": sorted(huer["codigo"].tolist()), "huerfanos_suma": int(huer["pagado"].sum()),
        "saldo_por_rubro": t.groupby("rubro")["saldo"].sum().round(2).to_dict(),
    }


def _censo_sorpresa_files(d):
    rng = random.Random()
    estados = ["VIGENTE", "VENCIDA", "SUSPENDIDA"]
    n = rng.randint(8, 12)
    codigos = [f"PS-{2000 + i}-{rng.choice('CGT')}" for i in range(n)]
    censo = [[c, f"Negocio {i}", rng.choice(estados), rng.choice([0, 20000, 90000, 250000, 480000])]
             for i, c in enumerate(codigos)]
    r_censo, r_jun, r_jul = d / "censo.csv", d / "jun.csv", d / "jul.csv"
    with r_censo.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["codigo", "nombre", "estado", "deuda"]); w.writerows(censo)

    def _pagos(ruta, k):
        filas = [[rng.choice(codigos), "2026-06-01", rng.choice([10000, 30000, 50000])] for _ in range(k)]
        with ruta.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f); w.writerow(["codigo", "fecha", "monto"]); w.writerows(filas)
    _pagos(r_jun, rng.randint(3, 5)); _pagos(r_jul, rng.randint(3, 5))
    # garantía: al menos un huérfano (código que NO está en el censo)
    with r_jul.open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([f"ZZ-9{rng.randint(0, 999):03d}-C", "2026-07-01", 99000])
    return r_censo, r_jun, r_jul


# ─── Carga ─────────────────────────────────────────────────────────────────

def cargar_programa():
    spec = importlib.util.spec_from_file_location("tablero_alumno", RUTA_PROGRAMA)
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


def main() -> int:
    lc.titulo("Verificador del Lab 06 — El tablero del Concejo")
    cont = lc.Contador()

    if RUTA_PROGRAMA.exists():
        lc.ok("tablero.py está en la raíz del lab.", cont)
    else:
        lc.error("No encuentro tablero.py en la raíz del lab.", "Cópialo desde plantillas/ o soluciones/. Ver Guía 5.", cont)
        return _cerrar(cont)

    modulo, err = cargar_programa()
    if err is None:
        lc.ok("tablero.py se cargó sin errores (Agg headless, sin ventanas).", cont)
    else:
        pista = "¿Falta pandas/matplotlib? Corre el preparador." if isinstance(err, ModuleNotFoundError) else "Lee el traceback de abajo hacia arriba."
        lc.error(f"tablero.py falló al cargar: {type(err).__name__}: {err}", pista, cont)
        for _ in range(11):
            lc.error("No evaluable: primero hay que poder cargar tablero.py.", "Corrige el error y reejecuta.", cont)
        return _cerrar(cont)

    faltan = [n for n in FUNCIONES if not callable(getattr(modulo, n, None))]
    if not faltan:
        lc.ok("Existen las 12 funciones del pipeline y son invocables.", cont)
    else:
        lc.error(f"Faltan o no son funciones: {', '.join(faltan)}.", "No las renombres.", cont)

    g = lambda n: getattr(modulo, n, None)  # noqa: E731
    censo0 = pd.read_csv(DATOS / "censo_limpio.csv")
    jun = pd.read_csv(DATOS / "pagos_junio.csv")
    jul = pd.read_csv(DATOS / "pagos_julio.csv")
    ref_censo = censo0.copy(); ref_censo["rubro"] = ref_censo["codigo"].str[-1].map(RUBRO)
    ref_censo["tramo"] = pd.cut(ref_censo["deuda"], bins=BINS, labels=LABELS)
    ref_tab, ref_huer = _ref_tablero(censo0, pd.concat([jun, jul], ignore_index=True))
    ref_tab["rubro"] = ref_tab["codigo"].str[-1].map(RUBRO)
    metr = _ref_metrics(censo0, jun, jul)

    # 4) agregar_rubro
    _cmp(lambda: {k: int(v) for k, v in g("agregar_rubro")(censo0)["rubro"].value_counts().items()},
         {"Gastronomía": 11, "Comercio": 8, "Turismo": 6}, "agregar_rubro [rubros]",
         "rubro = codigo.str[-1].map(dict).", cont)
    # 5) clasificar_deuda
    _cmp(lambda: {k: int(v) for k, v in g("clasificar_deuda")(censo0)["tramo"].value_counts().sort_index().items()},
         {"Sin deuda": 4, "Baja": 11, "Media": 7, "Alta": 3}, "clasificar_deuda [tramos]",
         "pd.cut con los bins y labels dados; ordena por índice.", cont)
    # 6) dummies_estado
    _check_dummies(g("dummies_estado"), censo0, cont)
    # 7) consolidar_pagos
    _check_concat(g("consolidar_pagos"), jun, jul, cont)
    # 8) construir_tablero
    _check_tablero(g("construir_tablero"), ref_censo, pd.concat([jun, jul], ignore_index=True), metr, cont)
    # 9) resumen + pct
    _check_resumen_pct(modulo, ref_tab, cont)
    # 10) crosstab
    _cmp_df(g("tabla_cruzada"), ref_tab, pd.crosstab(ref_tab["estado"], ref_tab["rubro"]),
            "tabla_cruzada (crosstab)", cont)
    # 11) pivote
    _cmp_df(g("pivote_deuda"), ref_tab,
            ref_tab.pivot_table(values="deuda", index="rubro", columns="estado", aggfunc="sum", fill_value=0),
            "pivote_deuda (pivot_table)", cont)
    # 12) sorpresa
    _check_sorpresa(modulo, cont)
    # 13) salidas
    _check_salidas(cont)

    return _cerrar(cont)


def _cmp(fn, esperado, etiqueta, pista, cont):
    try:
        obt = fn()
    except Exception as exc:  # noqa: BLE001
        lc.error(f"{etiqueta}: lanzó {type(exc).__name__}: {exc}", pista, cont); return
    if obt == esperado:
        lc.ok(f"{etiqueta}: {obt}.", cont)
    else:
        lc.error(f"{etiqueta}: obtuvo {obt}, se esperaba {esperado}.", pista, cont)


def _cmp_df(func, tablero, esperado, etiqueta, cont):
    if func is None:
        lc.error(f"{etiqueta}: la función no existe.", "No la renombres.", cont); return
    ok, obt = _llamar(func, tablero)
    try:
        igual = ok and obt.equals(esperado)
    except Exception:  # noqa: BLE001
        igual = False
    if igual:
        lc.ok(f"{etiqueta}: coincide con la referencia.", cont)
    else:
        lc.error(f"{etiqueta}: no coincide con la referencia.",
                 "Revisa índices/columnas (crosstab: estado×rubro; pivote: rubro×estado, fill_value=0).", cont)


def _check_dummies(func, censo, cont):
    if func is None:
        lc.error("dummies_estado no existe.", "No la renombres.", cont); return
    ok, d = _llamar(func, censo)
    sumas = {c: int(d[c].sum()) for c in d.columns} if ok and hasattr(d, "columns") else None
    es_bool = ok and hasattr(d, "dtypes") and all(str(t) == "bool" for t in d.dtypes)
    if sumas == {"SUSPENDIDA": 5, "VENCIDA": 10, "VIGENTE": 10} and es_bool:
        lc.ok("dummies_estado: sumas {S:5, V:10, Vig:10} y dtype bool.", cont)
    else:
        lc.error(f"dummies_estado: sumas={sumas}, bool={es_bool}.", "pd.get_dummies(df['estado']).", cont)


def _check_concat(func, jun, jul, cont):
    if func is None:
        lc.error("consolidar_pagos no existe.", "No la renombres.", cont); return
    ok, df = _llamar(func, jun, jul)
    if ok and len(df) == 20 and int(df["monto"].sum()) == 1_213_000:
        lc.ok("consolidar_pagos: 20 filas, total $1,213,000.", cont)
    else:
        lc.error(f"consolidar_pagos: {(len(df), int(df['monto'].sum())) if ok else df}, se esperaba (20, 1213000).",
                 "pd.concat([junio, julio], ignore_index=True).", cont)


def _check_tablero(func, censo, pagos, metr, cont):
    if func is None:
        lc.error("construir_tablero no existe.", "No la renombres.", cont); return
    ok, res = _llamar(func, censo, pagos)
    if not (ok and isinstance(res, tuple) and len(res) == 2):
        lc.error(f"construir_tablero no devolvió (tablero, huérfanos): {res if not ok else type(res)}.",
                 "Debe retornar (tablero, huerfanos).", cont); return
    t, huer = res
    checks = (len(t) == 25 and int(t["pagado"].sum()) == 1_082_500 and int(t["saldo"].sum()) == 2_025_000
              and int((t["pagado"] == 0).sum()) == 9
              and sorted(huer["codigo"].tolist()) == ["PS-1032-C", "PS-1040-G"]
              and int(huer["pagado"].sum()) == 130_500)
    if checks:
        lc.ok("construir_tablero: 25 filas, pagado $1,082,500, saldo $2,025,000, 9 sin pago; huérfanos {PS-1032-C, PS-1040-G} = $130,500.", cont)
    else:
        lc.error(f"construir_tablero: filas={len(t)}, pagado={int(t['pagado'].sum())}, saldo={int(t['saldo'].sum())}, "
                 f"sin_pago={int((t['pagado']==0).sum())}, huérfanos={sorted(huer['codigo'].tolist())}.",
                 "merge how='left' validate='1:1'; agrupa los pagos por código antes.", cont)


def _check_resumen_pct(modulo, ref_tab, cont):
    problemas = []
    ok, r = _llamar(modulo.resumen_por_rubro, ref_tab)
    if ok:
        d = {row["rubro"]: int(row["saldo"]) for _, row in r.iterrows()}
        if d != {"Comercio": 601000, "Gastronomía": 99000, "Turismo": 1325000}:
            problemas.append(f"resumen saldo {d}")
    else:
        problemas.append("resumen lanzó error")
    ok, p = _llamar(modulo.pct_dentro_del_rubro, ref_tab)
    try:
        pct = float(p[p["codigo"] == "PS-1022-T"]["pct_rubro"].iloc[0])
        if abs(pct - 34.0) > 0.1:
            problemas.append(f"pct Buceo {pct}")
    except Exception:  # noqa: BLE001
        problemas.append("pct_dentro_del_rubro sin columna pct_rubro")
    if not problemas:
        lc.ok("resumen_por_rubro (saldo C/G/T = 601k/99k/1325k) y pct de Buceo = 34.0%.", cont)
    else:
        lc.error("resumen/pct: " + "; ".join(problemas) + ".",
                 "groupby suma por rubro; pct con transform('sum').", cont)


def _check_sorpresa(modulo, cont):
    with tempfile.TemporaryDirectory() as dd:
        d = Path(dd)
        rc, rj, rl = _censo_sorpresa_files(d)
        try:
            censo = modulo.agregar_rubro(modulo.cargar_censo(rc))
            censo = modulo.clasificar_deuda(censo)
            pagos = modulo.consolidar_pagos(modulo.cargar_pagos(rj), modulo.cargar_pagos(rl))
            t, huer = modulo.construir_tablero(censo, pagos)
        except Exception as exc:  # noqa: BLE001
            lc.error(f"Sorpresa: el pipeline lanzó {type(exc).__name__}: {exc}",
                     "Tus funciones deben procesar los datos que reciben, no fijos.", cont)
            return
        ref = _ref_metrics(pd.read_csv(rc), pd.read_csv(rj), pd.read_csv(rl))
        obt = {"tablero_filas": len(t), "saldo_total": int(t["saldo"].sum()),
               "sin_pago": int((t["pagado"] == 0).sum()),
               "huerfanos": sorted(huer["codigo"].tolist()), "huerfanos_suma": int(huer["pagado"].sum())}
        esp = {k: ref[k] for k in obt}
        if obt == esp:
            lc.ok(f"Datasets sorpresa: pipeline coincide con la referencia ({len(t)} filas, {len(huer)} huérfano/s).", cont)
        else:
            lc.error(f"Datasets sorpresa: obtuvo {obt}, se esperaba {esp}.",
                     "Si el oficial pasó pero el sorpresa no, dejaste valores fijos. Procesa lo que te pasan.", cont)


def _check_salidas(cont):
    problemas = []
    inf = SALIDAS / "informe_tablero.txt"
    if not (inf.exists() and "2,025,000" in inf.read_text(encoding="utf-8") and "huérfanos" in inf.read_text(encoding="utf-8").lower()):
        problemas.append("informe con 2,025,000 y sección de huérfanos")
    for nombre in ("tablero.csv", "tablero.xlsx"):
        try:
            leido = pd.read_csv(SALIDAS / nombre) if nombre.endswith(".csv") else pd.read_excel(SALIDAS / nombre)
            if len(leido) != 25:
                problemas.append(f"{nombre} debe tener 25 filas")
        except Exception:  # noqa: BLE001
            problemas.append(f"{nombre} ausente/ilegible")
    png = SALIDAS / "saldo_por_rubro.png"
    if not png.exists():
        problemas.append("saldo_por_rubro.png ausente")
    elif png.stat().st_size < 5000:
        problemas.append(f"el PNG pesa {png.stat().st_size} bytes (<5KB: ¿figura vacía?)")
    elif png.read_bytes()[:4] != b"\x89PNG":
        problemas.append("saldo_por_rubro.png no es un PNG válido")
    if not problemas:
        lc.ok("salidas/: informe ($2,025,000 + huérfanos), tablero.csv/xlsx de 25 filas y saldo_por_rubro.png válido.", cont)
    else:
        lc.error("Faltan/mal en salidas: " + "; ".join(problemas) + ".",
                 "Ejecuta uv run python tablero.py para generar informe, tablero y gráfico.", cont)


def _cerrar(cont):
    if not RUTA_RESPUESTAS.exists():
        lc.error("No encuentro RESPUESTAS.md en la raíz del lab.",
                 "Copia el interrogatorio y respóndelo: cp plantillas/RESPUESTAS.md RESPUESTAS.md.", cont)
    else:
        pend = RUTA_RESPUESTAS.read_text(encoding="utf-8").count(MARCADOR)
        if pend == 0:
            lc.ok("RESPUESTAS.md está completo (sin respuestas pendientes).", cont)
        else:
            lc.error(f"RESPUESTAS.md tiene {pend} respuesta(s) sin contestar.",
                     f"Reemplaza cada '{MARCADOR}' por tu explicación.", cont)

    if _BREAKPOINT["golpeado"]:
        print()
        lc.info("Detecté un breakpoint() en tu código y lo neutralicé para no colgarme (C8). Quítalo de tablero.py.")

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.titulo("El Concejo vota con los ojos")
        print(
            "Don Arquímedes proyecta tu gráfico en la sala del Concejo. Los concejales,\n"
            "que jamás leen tablas, asienten al ver las barras. «Aprobado», dicen. «Con\n"
            "esto sí se entiende dónde está la plata del puerto.» Bien hecho, analista.\n"
        )
        print(
            f"{lc.CIAN}Se acerca el capstone:{lc.RESET} el Concejo aprobó el tablero. Ahora Don\n"
            "Arquímedes quiere TODO junto — el informe anual del puerto, de cabo a rabo.\n"
            "Se acerca El Arenario. 🏖️"
        )
    return codigo


if __name__ == "__main__":
    sys.exit(main())
