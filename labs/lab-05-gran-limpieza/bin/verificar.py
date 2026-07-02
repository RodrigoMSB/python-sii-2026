"""Verificador del Lab 05 — el juez de la limpieza.

Se ejecuta desde la raíz del lab:

    uv run python bin/verificar.py

Solo lectura sobre tu trabajo. Trae su propia implementación de referencia del
pipeline y genera un "censo sorpresa" (CSV con mugre aleatoria en un directorio
temporal) para probar que tu limpieza funciona de verdad, no con números fijos.
Cuartiles con quantile y std muestral (ddof=1), como manda C15. Blindaje
anti-breakpoint (C8).
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

CENSO = RAIZ / "datos" / "censo_patentes.csv"
SALIDAS = RAIZ / "salidas"
RUTA_PROGRAMA = RAIZ / "limpiar.py"
RUTA_RESPUESTAS = RAIZ / "RESPUESTAS.md"
MARCADOR = "(escribe aquí tu respuesta)"
PATRON = r"PS-\d{4}-[CGT]"

FUNCIONES = ("cargar_censo", "homogeneizar", "quitar_duplicados", "filtrar_codigos",
             "imputar_deuda", "outliers_iqr", "outliers_z", "vencidas_grandes",
             "limpiar_censo", "construir_informe")


# ─── Referencia ────────────────────────────────────────────────────────────

def _ref_steps(ruta, umbral_z=3.0):
    """Devuelve los DataFrames intermedios y las métricas de referencia."""
    df0 = pd.read_csv(ruta, na_values=["", "S/I", "sin dato"], keep_default_na=True)
    df = df0.copy()
    df["estado"] = df["estado"].str.strip().str.upper()
    df["nombre"] = df["nombre"].str.strip()
    homog = df.copy()
    n = len(df); df = df.drop_duplicates(); dedup = df.copy(); dup = n - len(df)
    mask = df["codigo"].str.fullmatch(PATRON)
    desc = sorted(df[~mask]["codigo"].tolist()); df = df[mask].copy(); filtrado = df.copy()
    imp = int(df["deuda"].isna().sum()); df["deuda"] = df["deuda"].fillna(0).astype(int)
    imputado = df.copy()
    q1 = df["deuda"].quantile(0.25); q3 = df["deuda"].quantile(0.75); iqr = q3 - q1
    ciqr = set(df[(df["deuda"] < q1 - 1.5 * iqr) | (df["deuda"] > q3 + 1.5 * iqr)]["codigo"])
    m = df["deuda"].mean(); s = df["deuda"].std(); z = (df["deuda"] - m) / s
    cz = set(df[z.abs() > umbral_z]["codigo"])
    apart = sorted(ciqr & cz)
    limpio = df[~df["codigo"].isin(apart)].copy()
    metr = {
        "filas_brutas": len(df0), "duplicados_eliminados": dup, "codigos_descartados": desc,
        "deudas_imputadas": imp, "outliers_iqr": sorted(ciqr), "outliers_z": sorted(cz),
        "apartados": apart, "filas_finales": len(limpio), "deuda_total": int(limpio["deuda"].sum()),
    }
    return {"df0": df0, "homog": homog, "dedup": dedup, "filtrado": filtrado,
            "imputado": imputado, "limpio": limpio, "metr": metr}


def _censo_sorpresa(ruta):
    rng = random.Random()
    variantes = ["VIGENTE", "vigente", " VIGENTE ", "VENCIDA", "vencida", "Vencida ", "SUSPENDIDA", "suspendida"]
    faltantes = ["", "S/I", "sin dato"]
    filas = []
    n = rng.randint(8, 12)
    for i in range(n):
        filas.append([f"PS-{rng.randint(2000, 2999)}-{rng.choice('CGT')}", f"Negocio {i}",
                      rng.choice(variantes), str(rng.choice([0, 15000, 30000, 60000, 90000, 120000]))])
    mediana = 60000
    filas.append([f"PS-{rng.randint(2000, 2999)}-C", "Outlier Digitación",
                  rng.choice(["VENCIDA", "vencida"]), str(mediana * 50)])       # outlier extremo
    filas.append([f"ZZ-{rng.randint(100, 999)}", "Codigo Malo", "VIGENTE", "20000"])  # malformado
    filas[rng.randrange(n)][3] = rng.choice(faltantes)                          # 1 faltante
    filas.append(list(filas[0]))                                               # 1 duplicado exacto
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["codigo", "nombre", "estado", "deuda"]); w.writerows(filas)


# ─── Carga ─────────────────────────────────────────────────────────────────

def cargar_programa():
    spec = importlib.util.spec_from_file_location("limpiar_alumno", RUTA_PROGRAMA)
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
    lc.titulo("Verificador del Lab 05 — La gran limpieza")
    cont = lc.Contador()

    if RUTA_PROGRAMA.exists():
        lc.ok("limpiar.py está en la raíz del lab.", cont)
    else:
        lc.error("No encuentro limpiar.py en la raíz del lab.", "Cópialo desde plantillas/ o soluciones/. Ver Guía 5.", cont)
        return _cerrar(cont)

    modulo, err = cargar_programa()
    if err is None:
        lc.ok("limpiar.py se cargó sin errores.", cont)
    else:
        pista = "Lee el traceback de abajo hacia arriba."
        if isinstance(err, ModuleNotFoundError):
            pista = "¿Falta pandas? Corre el preparador."
        lc.error(f"limpiar.py falló al cargar: {type(err).__name__}: {err}", pista, cont)
        for _ in range(9):
            lc.error("No evaluable: primero hay que poder cargar limpiar.py.", "Corrige el error y reejecuta.", cont)
        return _cerrar(cont)

    faltan = [n for n in FUNCIONES if not callable(getattr(modulo, n, None))]
    if not faltan:
        lc.ok("Existen las 10 funciones del pipeline y son invocables.", cont)
    else:
        lc.error(f"Faltan o no son funciones: {', '.join(faltan)}.", "No las renombres.", cont)

    ref = _ref_steps(CENSO)
    g = lambda n: getattr(modulo, n, None)  # noqa: E731

    # 4) cargar_censo
    ok, df = _llamar(g("cargar_censo"), CENSO) if g("cargar_censo") else (False, None)
    if ok and isinstance(df, pd.DataFrame) and df.shape == (30, 4) and str(df["deuda"].dtype).startswith("float") and int(df["deuda"].isna().sum()) == 3:
        lc.ok("cargar_censo: 30×4, deuda float con 3 NaN (na_values aplicado).", cont)
    else:
        det = f"shape={getattr(df, 'shape', None)}, dtype={df['deuda'].dtype if ok and isinstance(df, pd.DataFrame) else df}"
        lc.error(f"cargar_censo incorrecto: {det}.", "Usa na_values=['', 'S/I', 'sin dato']; deuda debe quedar float con 3 NaN.", cont)

    # 5) homogeneizar
    ok, dh = _llamar(g("homogeneizar"), ref["df0"]) if g("homogeneizar") else (False, None)
    if ok and isinstance(dh, pd.DataFrame) and set(dh["estado"].unique()) == {"VIGENTE", "VENCIDA", "SUSPENDIDA"} and \
            not dh["nombre"].str.startswith(" ").any() and not dh["nombre"].str.endswith(" ").any():
        lc.ok("homogeneizar: estado ∈ {VIGENTE, VENCIDA, SUSPENDIDA} y nombre sin espacios de borde.", cont)
    else:
        got = sorted(dh["estado"].unique().tolist()) if ok and isinstance(dh, pd.DataFrame) else dh
        lc.error(f"homogeneizar incorrecto: estados={got}.", "Aplica .str.strip().str.upper() al estado y .str.strip() al nombre.", cont)

    # 6) quitar_duplicados
    ok, res = _llamar(g("quitar_duplicados"), ref["homog"]) if g("quitar_duplicados") else (False, None)
    if ok and isinstance(res, tuple) and len(res) == 2 and len(res[0]) == 28 and res[1] == 2:
        lc.ok("quitar_duplicados: 28 filas y contador 2.", cont)
    else:
        lc.error(f"quitar_duplicados incorrecto: {(len(res[0]), res[1]) if ok and isinstance(res, tuple) else res}, se esperaba (28, 2).",
                 "drop_duplicates() y retorna cuántas quitaste (len antes - después).", cont)

    # 7) filtrar_codigos
    ok, res = _llamar(g("filtrar_codigos"), ref["dedup"]) if g("filtrar_codigos") else (False, None)
    if ok and isinstance(res, tuple) and len(res) == 2 and len(res[0]) == 26 and \
            sorted(res[1]["codigo"].tolist()) == ["PS-999", "XX-1050-G"]:
        lc.ok("filtrar_codigos: 26 válidos y descartados {PS-999, XX-1050-G}.", cont)
    else:
        det = (len(res[0]), sorted(res[1]["codigo"].tolist())) if ok and isinstance(res, tuple) else res
        lc.error(f"filtrar_codigos incorrecto: {det}.", "Máscara con str.fullmatch(PATRON_CODIGO); ~ invierte.", cont)

    # 8) imputar_deuda
    ok, res = _llamar(g("imputar_deuda"), ref["filtrado"]) if g("imputar_deuda") else (False, None)
    if ok and isinstance(res, tuple) and res[1] == 3 and int(res[0]["deuda"].isna().sum()) == 0 and \
            str(res[0]["deuda"].dtype).startswith("int"):
        lc.ok("imputar_deuda: 3 imputados, 0 NaN restantes, deuda entera.", cont)
    else:
        lc.error(f"imputar_deuda incorrecto: {res if not ok else (res[1], str(res[0]['deuda'].dtype))}.",
                 "Cuenta isna().sum(), fillna(0).astype(int).", cont)

    # 9) outliers
    problemas = []
    ok, di = _llamar(g("outliers_iqr"), ref["imputado"]) if g("outliers_iqr") else (False, None)
    if not (ok and set(di["codigo"]) == {"PS-1022-T", "PS-1046-C"}):
        problemas.append(f"IQR={sorted(di['codigo']) if ok else 'error'} (esperado PS-1022-T, PS-1046-C)")
    ok, dz = _llamar(g("outliers_z"), ref["imputado"]) if g("outliers_z") else (False, None)
    if not (ok and set(dz["codigo"]) == {"PS-1046-C"}):
        problemas.append(f"z={sorted(dz['codigo']) if ok else 'error'} (esperado PS-1046-C)")
    if not problemas:
        lc.ok("outliers_iqr → {PS-1022-T, PS-1046-C}; outliers_z → {PS-1046-C}.", cont)
    else:
        lc.error("outliers: " + "; ".join(problemas) + ".", "IQR usa quantile(.25/.75); z usa std muestral (ddof=1).", cont)

    # 10) vencidas_grandes
    ok, dv = _llamar(g("vencidas_grandes"), ref["limpio"], 100000) if g("vencidas_grandes") else (False, None)
    esperado_vg = set(ref["limpio"].query("estado == 'VENCIDA' and deuda > 100000")["codigo"])
    if ok and set(dv["codigo"]) == esperado_vg:
        lc.ok(f"vencidas_grandes(limpio, 100000) == {sorted(esperado_vg)}.", cont)
    else:
        lc.error(f"vencidas_grandes incorrecto: {sorted(dv['codigo']) if ok else dv}, se esperaba {sorted(esperado_vg)}.",
                 "Usa query(\"estado == 'VENCIDA' and deuda > @umbral\").", cont)

    # 11) pipeline oficial
    _check_pipeline(g("limpiar_censo"), CENSO, ref["metr"], "oficial", exacto=True, cont=cont)
    # 12) censo sorpresa
    with tempfile.TemporaryDirectory() as d:
        rs = Path(d) / "sorpresa.csv"
        _censo_sorpresa(rs)
        _check_pipeline(g("limpiar_censo"), rs, _ref_steps(rs)["metr"], "sorpresa", exacto=False, cont=cont)

    # 13) salidas
    _check_salidas(cont)

    return _cerrar(cont)


def _check_pipeline(func, ruta, metr, etiqueta, exacto, cont):
    if func is None:
        lc.error(f"limpiar_censo no existe (check {etiqueta}).", "No la renombres.", cont); return
    ok, res = _llamar(func, ruta)
    if not (ok and isinstance(res, tuple) and len(res) == 2):
        lc.error(f"limpiar_censo [{etiqueta}] no devolvió (df, reporte): {res if not ok else type(res)}.",
                 "Debe retornar (censo_limpio, reporte).", cont); return
    df, rep = res
    claves = ["filas_brutas", "duplicados_eliminados", "codigos_descartados", "deudas_imputadas",
              "outliers_iqr", "outliers_z", "apartados", "filas_finales", "deuda_total"]
    faltan = [k for k in claves if k not in (rep or {})]
    if faltan:
        lc.error(f"limpiar_censo [{etiqueta}]: al reporte le faltan claves: {faltan}.",
                 "El reporte debe contabilizar TODO (C14).", cont); return
    difieren = [k for k in claves if rep[k] != metr[k]]
    if not difieren:
        extra = f" ({metr['filas_finales']} filas, ${metr['deuda_total']:,})" if exacto else ""
        lc.ok(f"limpiar_censo [{etiqueta}]: pipeline y reporte coinciden con la referencia{extra}.", cont)
    else:
        muestra = {k: (rep[k], metr[k]) for k in difieren[:3]}
        lc.error(f"limpiar_censo [{etiqueta}] difiere en {difieren}: {muestra}.",
                 "Si el oficial pasó pero el sorpresa no, quizá dejaste valores fijos. Procesa el censo que te pasan.", cont)


def _check_salidas(cont):
    inf = SALIDAS / "informe_limpieza.txt"
    problemas = []
    if not (inf.exists() and "3,107,500" in inf.read_text(encoding="utf-8") and "30" in inf.read_text(encoding="utf-8")):
        problemas.append("informe con 3,107,500 y el embudo")
    for nombre in ("censo_limpio.csv", "censo_limpio.xlsx"):
        ruta = SALIDAS / nombre
        try:
            leido = pd.read_csv(ruta) if nombre.endswith(".csv") else pd.read_excel(ruta)
            if len(leido) != 25:
                problemas.append(f"{nombre} debe tener 25 filas (tiene {len(leido)})")
        except Exception:  # noqa: BLE001
            problemas.append(f"{nombre} ausente o ilegible")
    if not problemas:
        lc.ok("salidas/: informe ($3,107,500, embudo 30→25) y censo_limpio.csv/.xlsx de 25 filas.", cont)
    else:
        lc.error("Faltan/mal en salidas: " + "; ".join(problemas) + ".",
                 "Ejecuta uv run python limpiar.py para generar informe y censo limpio.", cont)


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
        lc.info("Detecté un breakpoint() en tu código y lo neutralicé para no colgarme (C8). Quítalo de limpiar.py.")

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.titulo("Don Arquímedes revisa el censo limpio")
        print(
            "Don Arquímedes recorre el informe con el dedo, se detiene en los veredictos\n"
            "de los outliers y sonríe: «Nada se botó sin razón anotada. Buceo Fondo Claro\n"
            "sigue en el registro; el dedo dormido, afuera. Así se limpia, joven analista.»\n"
        )
        print(
            f"{lc.CIAN}Próxima jornada — Lab 06:{lc.RESET} el censo limpio ya no estará solo.\n"
            "En el Módulo 3 aprenderás a TRANSFORMAR y COMBINAR: cruzar el censo con los\n"
            "pagos, los permisos y las multas. El merge te espera. Nos vemos en el mesón."
        )
    return codigo


if __name__ == "__main__":
    sys.exit(main())
