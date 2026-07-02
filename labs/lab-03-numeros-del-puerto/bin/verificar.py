"""Verificador del Lab 03 — el juez del panorama.

Se ejecuta desde la raíz del lab:

    uv run python bin/verificar.py

Solo lectura sobre tu trabajo (C1) y corre dentro del entorno del lab (puede
usar numpy/pandas). Trae implementación de referencia propia y dos datasets
sorpresa (una matriz aleatoria y un mini-cuaderno aleatorio): si tu código
funciona de verdad, da bien con los oficiales Y con los sorpresa.

Los floats se comparan con tolerancia (np.allclose / np.isclose), nunca con ==
(contrato C10). Blindaje anti-breakpoint (C8) como en el Lab 02.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

_BREAKPOINT = {"golpeado": False}
sys.breakpointhook = lambda *a, **k: _BREAKPOINT.__setitem__("golpeado", True)

try:
    import numpy as np
    import pandas as pd
except Exception as exc:  # pragma: no cover
    lc.error(f"No pude importar numpy/pandas: {exc}",
             "Corre el preparador: bash bin/00-preparar.sh (descarga las bibliotecas).")
    sys.exit(1)

RUTA_PROGRAMA = RAIZ / "panorama.py"
RUTA_INFORME = RAIZ / "salidas" / "informe_panorama.txt"
RUTA_RESPUESTAS = RAIZ / "RESPUESTAS.md"
MARCADOR_PENDIENTE = "(escribe aquí tu respuesta)"

FUNCIONES = ("construir_matriz", "recaudacion_por_mes", "recaudacion_por_rubro",
             "mes_record", "meses_bajo_umbral", "proyectar_reajuste",
             "cuaderno_a_dataframe", "resumen_vencidas")


# ─── Referencia ────────────────────────────────────────────────────────────

def _ref_por_mes(m):
    return m.sum(axis=1)


def _ref_por_rubro(m):
    return m.sum(axis=0)


def _ref_mes_record(m, meses):
    return meses[int(np.argmax(m.sum(axis=1)))]


def _ref_bajo(m, umbral, meses):
    pm = m.sum(axis=1)
    return [meses[i] for i in range(len(pm)) if pm[i] < umbral]


def _ref_vencidas(filas):
    ven = [f for f in filas if f[2] == "VENCIDA"]
    return len(ven), sum(f[3] for f in ven)


# ─── Datasets sorpresa ─────────────────────────────────────────────────────

def _matriz_sorpresa():
    rng = random.Random()
    filas = [[rng.randint(2_000_000, 5_000_000),
              rng.randint(1_500_000, 4_000_000),
              rng.randint(200_000, 1_500_000)] for _ in range(12)]
    return np.array(filas)


def _cuaderno_sorpresa():
    rng = random.Random()
    estados = ["VIGENTE", "VENCIDA", "SUSPENDIDA"]
    n = rng.randint(6, 10)
    return [[f"ZZ-9{rng.randint(0, 999):03d}-{rng.choice('CGT')}", f"Sorpresa {i + 1}",
             rng.choice(estados), rng.choice([0, 50000, 120000, 300000])] for i in range(n)]


# ─── Carga ─────────────────────────────────────────────────────────────────

def cargar_programa():
    spec = importlib.util.spec_from_file_location("panorama_alumno", RUTA_PROGRAMA)
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
    lc.titulo("Verificador del Lab 03 — El panorama del puerto")

    try:
        from datos.recaudacion import MESES, RECAUDACION
        from datos.cuaderno import PATENTES
    except Exception as exc:  # pragma: no cover
        lc.error(f"No pude leer los datasets: {exc}", "¿Ejecutas desde la raíz del lab?")
        return 1

    oficial = np.array(RECAUDACION)
    cont = lc.Contador()

    # 1) existe
    if RUTA_PROGRAMA.exists():
        lc.ok("panorama.py está en la raíz del lab.", cont)
    else:
        lc.error("No encuentro panorama.py en la raíz del lab.",
                 "Cópialo desde plantillas/ o soluciones/. Ver Guía 5.", cont)
        return _cerrar(cont, oficial, MESES, PATENTES)

    # 2) importa
    modulo, err = cargar_programa()
    if err is None:
        lc.ok("panorama.py se cargó sin errores.", cont)
    else:
        tipo = type(err).__name__
        pista = "Lee el traceback de abajo hacia arriba."
        if isinstance(err, ModuleNotFoundError):
            pista = "¿Falta numpy/pandas? Corre el preparador: bash bin/00-preparar.sh"
        lc.error(f"panorama.py falló al cargar: {tipo}: {err}", pista, cont)
        for _ in range(7):
            lc.error("No evaluable: primero hay que poder cargar panorama.py.",
                     "Corrige el error de carga y reejecuta.", cont)
        return _cerrar(cont, oficial, MESES, PATENTES)

    # 3) funciones
    faltan = [n for n in FUNCIONES if not callable(getattr(modulo, n, None))]
    if not faltan:
        lc.ok("Existen las 8 funciones del panorama y son invocables.", cont)
    else:
        lc.error(f"Faltan o no son funciones: {', '.join(faltan)}.", "No las renombres.", cont)

    g = lambda n: getattr(modulo, n, None)  # noqa: E731

    # 4) construir_matriz shape + dtype
    ok, m = _llamar(g("construir_matriz")) if g("construir_matriz") else (False, None)
    if ok and isinstance(m, np.ndarray) and m.shape == (12, 3) and np.issubdtype(m.dtype, np.integer):
        lc.ok("construir_matriz(): matriz 12×3 de enteros.", cont)
    else:
        detalle = f"shape={getattr(m, 'shape', None)}, dtype={getattr(m, 'dtype', type(m).__name__)}" if ok else f"lanzó {m}"
        lc.error(f"construir_matriz() incorrecta: {detalle}.", "Debe ser np.array(RECAUDACION), 12×3 int.", cont)

    # 5) por_mes oficial
    _cmp_array(g("recaudacion_por_mes"), oficial, _ref_por_mes(oficial),
               "recaudacion_por_mes [oficial]", "Suma a lo ancho: matriz.sum(axis=1).", cont)
    # 6) por_rubro oficial
    _cmp_array(g("recaudacion_por_rubro"), oficial, _ref_por_rubro(oficial),
               "recaudacion_por_rubro [oficial]", "Suma a lo largo: matriz.sum(axis=0).", cont)

    # 7) agregaciones oficiales (mes récord + umbral + reajuste)
    _check_agregaciones(modulo, oficial, MESES, "oficial",
                        esperado_record="Diciembre",
                        esperado_bajo=["Junio", "Julio"], umbral=6_500_000,
                        esperado_reajuste=94_307_200, cont=cont)

    # 8) sorpresa (a): matriz aleatoria
    ms = _matriz_sorpresa()
    _check_sorpresa_matriz(modulo, ms, MESES, cont)

    # 9) DataFrame + resumen_vencidas oficial
    _check_dataframe_oficial(modulo, cont)

    # 10) sorpresa (b): resumen_vencidas con mini-cuaderno
    _check_sorpresa_cuaderno(modulo, cont)

    return _cerrar(cont, oficial, MESES, PATENTES)


def _cmp_array(func, matriz, esperado, etiqueta, pista, cont):
    if func is None:
        lc.error(f"{etiqueta}: la función no existe.", pista, cont)
        return
    ok, obt = _llamar(func, matriz)
    if ok and isinstance(obt, np.ndarray) and np.array_equal(obt, esperado):
        lc.ok(f"{etiqueta}: {obt.tolist()} (correcto).", cont)
    else:
        muestra = obt.tolist() if ok and isinstance(obt, np.ndarray) else (obt if ok else f"lanzó {obt}")
        lc.error(f"{etiqueta}: obtuvo {muestra}, se esperaba {esperado.tolist()}.", pista, cont)


def _check_agregaciones(modulo, m, meses, etiq, esperado_record, esperado_bajo, umbral, esperado_reajuste, cont):
    problemas = []
    ok, rec = _llamar(modulo.mes_record, m)
    if not (ok and rec == esperado_record):
        problemas.append(f"mes_record={rec if ok else 'error'} (esperado {esperado_record})")
    ok, bajo = _llamar(modulo.meses_bajo_umbral, m, umbral)
    if not (ok and list(bajo) == esperado_bajo):
        problemas.append(f"meses_bajo_umbral={bajo if ok else 'error'} (esperado {esperado_bajo})")
    ok, proy = _llamar(modulo.proyectar_reajuste, m, 0.04)
    reajuste_ok = ok and hasattr(proy, "sum") and np.isclose(float(proy.sum()), esperado_reajuste)
    if not reajuste_ok:
        val = float(proy.sum()) if ok and hasattr(proy, "sum") else "error"
        problemas.append(f"reajuste.sum()={val} (esperado ≈{esperado_reajuste})")
    if not problemas:
        lc.ok(f"Agregaciones [{etiq}]: mes récord, meses bajo umbral y reajuste correctos.", cont)
    else:
        lc.error(f"Agregaciones [{etiq}]: " + "; ".join(problemas) + ".",
                 "argmax da la posición; la máscara compara con el umbral; el reajuste es m*(1+tasa).", cont)


def _check_sorpresa_matriz(modulo, ms, meses, cont):
    rng = random.Random()
    umbral = int((ms.sum(axis=1).min() + ms.sum(axis=1).max()) / 2)
    problemas = []
    for nombre, ref in (("recaudacion_por_mes", _ref_por_mes(ms)),
                        ("recaudacion_por_rubro", _ref_por_rubro(ms))):
        ok, obt = _llamar(getattr(modulo, nombre), ms)
        if not (ok and isinstance(obt, np.ndarray) and np.array_equal(obt, ref)):
            problemas.append(nombre)
    ok, rec = _llamar(modulo.mes_record, ms)
    if not (ok and rec == _ref_mes_record(ms, meses)):
        problemas.append("mes_record")
    ok, bajo = _llamar(modulo.meses_bajo_umbral, ms, umbral)
    if not (ok and list(bajo) == _ref_bajo(ms, umbral, meses)):
        problemas.append("meses_bajo_umbral")
    ok, proy = _llamar(modulo.proyectar_reajuste, ms, 0.075)
    if not (ok and hasattr(proy, "sum") and np.allclose(np.asarray(proy), ms * 1.075)):
        problemas.append("proyectar_reajuste")
    if not problemas:
        lc.ok("Matriz sorpresa aleatoria: las 5 operaciones coinciden con la referencia.", cont)
    else:
        lc.error("Matriz sorpresa: fallan " + ", ".join(problemas) + ".",
                 "Si el oficial pasó pero el sorpresa no, quizá devolviste valores fijos. "
                 "Opera sobre la matriz que te pasan.", cont)


def _check_dataframe_oficial(modulo, cont):
    ok, df = _llamar(modulo.cuaderno_a_dataframe)
    cols_ok = ok and isinstance(df, pd.DataFrame) and list(df.columns) == ["codigo", "nombre", "estado", "deuda"] and df.shape == (24, 4)
    if not cols_ok:
        detalle = f"shape={getattr(df, 'shape', None)}, cols={list(df.columns) if ok and isinstance(df, pd.DataFrame) else df}"
        lc.error(f"cuaderno_a_dataframe() incorrecto: {detalle}.",
                 "Debe ser pd.DataFrame(PATENTES, columns=['codigo','nombre','estado','deuda']).", cont)
        return
    ok2, res = _llamar(modulo.resumen_vencidas, df)
    tipos_ok = ok2 and isinstance(res, tuple) and len(res) == 2 and all(type(x) is int for x in res)
    if tipos_ok and res == (8, 976000):
        lc.ok("cuaderno_a_dataframe() 24×4 y resumen_vencidas() == (8, 976000) con ints nativos.", cont)
    else:
        lc.error(f"resumen_vencidas(oficial): obtuvo {res!r}, se esperaba (8, 976000) como ints nativos.",
                 "Filtra df[df['estado']=='VENCIDA'] y envuelve cantidad y suma en int().", cont)


def _check_sorpresa_cuaderno(modulo, cont):
    filas = _cuaderno_sorpresa()
    df = pd.DataFrame(filas, columns=["codigo", "nombre", "estado", "deuda"])
    ref = _ref_vencidas(filas)
    ok, res = _llamar(modulo.resumen_vencidas, df)
    if ok and tuple(res) == ref:
        lc.ok(f"Cuaderno sorpresa ({len(filas)} patentes): resumen_vencidas coincide con la referencia.", cont)
    else:
        lc.error(f"Cuaderno sorpresa: resumen_vencidas obtuvo {res if ok else 'error'}, se esperaba {ref}.",
                 "No devuelvas cifras fijas: filtra el DataFrame que te pasan.", cont)


def _check_informe_y_respuestas(cont, oficial):
    total = int(oficial.sum())
    if RUTA_INFORME.exists():
        lc.ok("salidas/informe_panorama.txt existe.", cont)
        texto = RUTA_INFORME.read_text(encoding="utf-8")
    else:
        lc.error("No existe salidas/informe_panorama.txt.",
                 "Genera el informe: uv run python panorama.py", cont)
        texto = ""
    if texto and f"{total:,}" in texto and "Diciembre" in texto:
        lc.ok(f"El informe contiene la recaudación total (${total:,}) y el mes récord (Diciembre).", cont)
    else:
        lc.error("El informe no contiene las cifras esperadas (90,680,000 y Diciembre).",
                 "Reejecuta uv run python panorama.py tras corregir. Formato con {:,}.", cont)

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


def _cerrar(cont, oficial, meses, patentes):
    _check_informe_y_respuestas(cont, oficial)
    if _BREAKPOINT["golpeado"]:
        print()
        lc.info("Detecté un breakpoint() en tu código y lo neutralicé para no colgarme (C8). "
                "Quítalo de panorama.py antes de entregar.")
    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.titulo("Don Arquímedes lleva el panorama al Concejo")
        print(
            "Don Arquímedes revisa los totales, asiente y guarda el informe en su\n"
            "carpeta de cuero: «Doce meses, tres rubros, y todo cuadra al peso. Con\n"
            "esto el Concejo me come de la mano, joven analista.»\n"
        )
        print(
            f"{lc.CIAN}Próxima jornada — Lab 04:{lc.RESET} hasta ahora los datos te llegaban\n"
            "cómodos, como módulos de Python. Se acabó la comodidad: en el Lab 04 los\n"
            "datos llegan en ARCHIVOS de verdad (CSV, Excel, JSON) y hasta una base de\n"
            "datos. Las cuatro fuentes te esperan. Nos vemos en el mesón."
        )
    return codigo


if __name__ == "__main__":
    sys.exit(main())
