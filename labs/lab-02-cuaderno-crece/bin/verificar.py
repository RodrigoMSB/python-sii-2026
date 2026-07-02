"""Verificador del Lab 02 — el juez de la consolidación.

Se ejecuta desde la raíz del lab:

    uv run python bin/verificar.py

Solo lectura sobre tu trabajo (C1) y 100 % stdlib. Trae su propia implementación
de referencia y un "archivador sorpresa" aleatorio (cambia cada corrida) que
siempre incluye deudas sucias y un código duplicado: si tu código funciona de
verdad, da bien con el archivador oficial Y con el sorpresa.

Blindaje anti-breakpoint (C8): si por error dejaste un breakpoint() en tu
consolidar.py, este verificador NO se queda colgado en el depurador; lo
neutraliza y te avisa.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

# ── Blindaje C8: neutralizamos breakpoint() ANTES de cargar nada del alumno ──
# Si el alumno olvidó un breakpoint(), en vez de abrir pdb (y colgar el
# verificador para siempre), solo lo anotamos y seguimos.
_BREAKPOINT = {"golpeado": False}


def _breakpoint_neutralizado(*args, **kwargs):
    _BREAKPOINT["golpeado"] = True


sys.breakpointhook = _breakpoint_neutralizado

RUTA_PROGRAMA = RAIZ / "consolidar.py"
RUTA_INFORME = RAIZ / "salidas" / "informe_consolidacion.txt"
RUTA_RESPUESTAS = RAIZ / "RESPUESTAS.md"
MARCADOR_PENDIENTE = "(escribe aquí tu respuesta)"

FUNCIONES = ("normalizar_deuda", "crear_ficha", "consolidar", "deuda_por_rubro")
RUBROS = ["C", "G", "T"]


# ─────────────────────────────────────────────────────────────────────────
#  Implementación de referencia (la verdad contra la que comparamos)
# ─────────────────────────────────────────────────────────────────────────


class _RefInvalido(ValueError):
    pass


def _ref_normalizar(texto):
    try:
        return int(texto.replace(".", ""))
    except ValueError:
        raise _RefInvalido(f"deuda no numérica ('{texto}')") from None


def _ref_crear_ficha(reg):
    return {
        "codigo": reg["codigo"],
        "nombre": reg["nombre"],
        "estado": reg["estado"],
        "deuda": _ref_normalizar(reg["deuda"]),
        "rubro": reg["codigo"][-1],
    }


def _ref_consolidar(registros):
    fichero, rechazos = {}, []
    for reg in registros:
        codigo = reg["codigo"]
        try:
            ficha = _ref_crear_ficha(reg)
        except _RefInvalido as e:
            rechazos.append((codigo, str(e)))
            continue
        if codigo in fichero:
            rechazos.append((codigo, "código duplicado"))
            continue
        fichero[codigo] = ficha
    return fichero, rechazos


def _ref_deuda_por_rubro(fichero):
    tot = {}
    for f in fichero.values():
        tot[f["rubro"]] = tot.get(f["rubro"], 0) + f["deuda"]
    return tot


# ─────────────────────────────────────────────────────────────────────────
#  Archivador sorpresa (anti-loro): distinto en cada corrida
# ─────────────────────────────────────────────────────────────────────────


def generar_archivador_sorpresa():
    """8–12 registros brutos: garantiza ≥1 deuda no numérica, ≥1 duplicado y
    deudas con puntos de miles. Sin semilla fija: cambia entre ejecuciones."""
    rng = random.Random()
    rubros = ["C", "G", "T"]
    estados = ["VIGENTE", "VENCIDA", "SUSPENDIDA"]
    no_numericas = ["S/I", "pendiente", "sin dato"]
    valores = [0, 12000, 27500, 38000, 47500, 64000, 83000, 121000, 154000, 205000, 290000]

    n = rng.randint(7, 11)
    regs = []
    for i in range(n):
        codigo = f"ZZ-9{rng.randint(0, 999):03d}-{rng.choice(rubros)}"
        v = rng.choice(valores)
        deuda = "0" if v == 0 else f"{v:,}".replace(",", ".")  # p. ej. 38000 -> "38.000"
        regs.append({"codigo": codigo, "nombre": f"Sorpresa {i + 1}",
                     "estado": rng.choice(estados), "deuda": deuda})

    # Garantía 1: al menos una deuda no numérica (en un índice != 0).
    regs[rng.randrange(1, n)]["deuda"] = rng.choice(no_numericas)
    # Garantía 2: un duplicado del código de regs[0] (que es numérico/válido),
    # con datos DISTINTOS, para probar que "gana el primero".
    regs.append({"codigo": regs[0]["codigo"], "nombre": regs[0]["nombre"] + " (bis)",
                 "estado": "SUSPENDIDA", "deuda": "99.000"})
    return regs


# ─────────────────────────────────────────────────────────────────────────
#  Carga del consolidar.py del alumno
# ─────────────────────────────────────────────────────────────────────────


def cargar_programa():
    spec = importlib.util.spec_from_file_location("consolidar_alumno", RUTA_PROGRAMA)
    modulo = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(modulo)
        return modulo, None
    except BaseException as exc:  # noqa: BLE001
        return None, exc


def _llamar(func, *args):
    """Llama a una función del alumno de forma segura. Devuelve (ok, valor_o_exc)."""
    try:
        return True, func(*args)
    except BaseException as exc:  # noqa: BLE001
        return False, exc


def main() -> int:
    lc.titulo("Verificador del Lab 02 — Consolidación del archivador")

    try:
        from datos.archivador import REGISTROS_BRUTOS as OFICIAL
    except Exception as exc:  # pragma: no cover
        lc.error(f"No pude leer datos/archivador.py: {exc}",
                 "¿Ejecutas desde la raíz del lab? uv run python bin/verificar.py")
        return 1

    cont = lc.Contador()

    # ── 1) consolidar.py existe ───────────────────────────────────────────
    if RUTA_PROGRAMA.exists():
        lc.ok("consolidar.py está en la raíz del lab.", cont)
    else:
        lc.error("No encuentro consolidar.py en la raíz del lab.",
                 "Cópialo desde plantillas/ (Artesano) o soluciones/ (Explorador). Ver Guía 5.",
                 cont)
        return _cerrar(cont, OFICIAL)

    # ── 2) se importa sin explotar ────────────────────────────────────────
    modulo, err = cargar_programa()
    if err is None:
        lc.ok("consolidar.py se cargó sin errores.", cont)
    else:
        tipo = type(err).__name__
        lc.error(f"consolidar.py falló al cargar: {tipo}: {err}",
                 "Lee el traceback de ABAJO hacia arriba. Un SyntaxError suele apuntar "
                 "la línea siguiente a la del problema (revisa ':' y sangría).",
                 cont)
        for _ in range(6):  # checks 3..8 no evaluables
            lc.error("No evaluable: primero hay que poder cargar consolidar.py.",
                     "Corrige el error de carga de arriba y reejecuta.", cont)
        return _cerrar(cont, OFICIAL)

    # ── 3) funciones y clase existen ──────────────────────────────────────
    faltan = [n for n in FUNCIONES if not callable(getattr(modulo, n, None))]
    clase = getattr(modulo, "RegistroInvalido", None)
    clase_ok = isinstance(clase, type) and issubclass(clase, ValueError)
    if not faltan and clase_ok:
        lc.ok("Existen las 4 funciones y la clase RegistroInvalido (subclase de ValueError).", cont)
    else:
        problemas = []
        if faltan:
            problemas.append("faltan funciones: " + ", ".join(faltan))
        if not clase_ok:
            problemas.append("RegistroInvalido no existe o no hereda de ValueError")
        lc.error("; ".join(problemas) + ".", "No renombres funciones ni la clase.", cont)

    f_norm = getattr(modulo, "normalizar_deuda", None)
    f_cons = getattr(modulo, "consolidar", None)
    f_rub = getattr(modulo, "deuda_por_rubro", None)

    # ── 4) normalizar_deuda numérica ──────────────────────────────────────
    _check_normalizar_numerica(f_norm, cont)

    # ── 5) normalizar_deuda("S/I") lanza RegistroInvalido ─────────────────
    _check_normalizar_invalida(f_norm, clase, cont)

    # ── 6) consolidar con el archivador OFICIAL ───────────────────────────
    _check_consolidar_oficial(f_cons, OFICIAL, cont)

    # ── 7) deuda_por_rubro OFICIAL ────────────────────────────────────────
    _check_rubro_oficial(f_rub, OFICIAL, cont)

    # ── 8) consolidar + deuda_por_rubro con archivador SORPRESA ───────────
    _check_sorpresa(f_cons, f_rub, cont)

    # ── 9 y 10) archivos ──────────────────────────────────────────────────
    return _cerrar(cont, OFICIAL)


def _check_normalizar_numerica(f_norm, cont):
    if f_norm is None:
        lc.error("normalizar_deuda no existe.", "No la renombres.", cont)
        return
    ok1, v1 = _llamar(f_norm, "154.000")
    ok2, v2 = _llamar(f_norm, "0")
    if ok1 and ok2 and v1 == 154000 and v2 == 0:
        lc.ok("normalizar_deuda convierte bien ('154.000'→154000, '0'→0).", cont)
    else:
        obt = f"'154.000'→{v1!r}, '0'→{v2!r}" if ok1 and ok2 else f"lanzó {v1 if not ok1 else v2}"
        lc.error(f"normalizar_deuda no convierte bien: {obt}.",
                 "Quita los puntos con .replace('.', '') y usa int().", cont)


def _check_normalizar_invalida(f_norm, clase, cont):
    if f_norm is None or clase is None:
        lc.error("No puedo probar normalizar_deuda('S/I').",
                 "Deben existir normalizar_deuda y la clase RegistroInvalido.", cont)
        return
    try:
        resultado = f_norm("S/I")
        lc.error(f"normalizar_deuda('S/I') NO lanzó excepción (devolvió {resultado!r}).",
                 "Cuando int() falle, relanza como RegistroInvalido.", cont)
    except Exception as exc:  # noqa: BLE001
        if isinstance(exc, clase):
            lc.ok("normalizar_deuda('S/I') lanza RegistroInvalido.", cont)
        else:
            lc.error(f"normalizar_deuda('S/I') lanzó {type(exc).__name__}, no RegistroInvalido.",
                     "Captura el ValueError de int() y relánzalo como RegistroInvalido.", cont)


def _check_consolidar_oficial(f_cons, oficial, cont):
    if f_cons is None:
        lc.error("consolidar no existe.", "No la renombres.", cont)
        return
    ok, res = _llamar(f_cons, oficial)
    if not ok:
        lc.error(f"consolidar(oficial) lanzó {type(res).__name__}: {res}",
                 "El proceso NO debe morir por un registro malo: usa try/except RegistroInvalido.",
                 cont)
        return
    try:
        fichero, rechazos = res
    except (TypeError, ValueError):
        lc.error("consolidar no devolvió (fichero, rechazos).", "Debe retornar una tupla de dos.", cont)
        return
    codigos_rech = [c for c, _ in rechazos] if _es_lista_de_pares(rechazos) else []
    dup_rechazado = "PS-1026-C" in codigos_rech
    if len(fichero) == 15 and len(rechazos) == 3 and dup_rechazado and "PS-1026-C" in fichero:
        lc.ok("consolidar(oficial): 15 fichas, 3 rechazos y el duplicado PS-1026-C fue rechazado (gana el primero).", cont)
    else:
        lc.error(
            f"consolidar(oficial): fichas={len(fichero)} (esperado 15), "
            f"rechazos={len(rechazos)} (esperado 3), duplicado_rechazado={dup_rechazado}.",
            "Rechaza deudas no numéricas y los códigos ya vistos (in sobre el dict).",
            cont)


def _check_rubro_oficial(f_rub, oficial, cont):
    if f_rub is None:
        lc.error("deuda_por_rubro no existe.", "No la renombres.", cont)
        return
    fichero, _ = _ref_consolidar(oficial)  # usamos referencia para aislar la función
    ok, res = _llamar(f_rub, fichero)
    esperado = {"C": 338000, "G": 260000, "T": 444000}
    if ok and res == esperado:
        lc.ok(f"deuda_por_rubro(oficial) == {esperado}.", cont)
    else:
        obt = res if ok else f"lanzó {type(res).__name__}"
        lc.error(f"deuda_por_rubro(oficial): obtuvo {obt!r}, se esperaba {esperado!r}.",
                 "Acumula por rubro con totales.get(rubro, 0) + ficha['deuda'].", cont)


def _check_sorpresa(f_cons, f_rub, cont):
    if f_cons is None or f_rub is None:
        lc.error("No puedo probar el archivador sorpresa.", "Deben existir consolidar y deuda_por_rubro.", cont)
        return
    sorpresa = generar_archivador_sorpresa()
    ref_fichero, ref_rech = _ref_consolidar(sorpresa)
    ref_rub = _ref_deuda_por_rubro(ref_fichero)

    ok_c, res_c = _llamar(f_cons, sorpresa)
    if not ok_c:
        lc.error(f"consolidar(sorpresa) lanzó {type(res_c).__name__}: {res_c}",
                 "Con datos sucios reales, el proceso debe rechazar sin morir (try/except).", cont)
        return
    try:
        stu_fichero, stu_rech = res_c
    except (TypeError, ValueError):
        lc.error("consolidar(sorpresa) no devolvió (fichero, rechazos).", "Debe retornar una tupla de dos.", cont)
        return

    stu_codes = sorted(stu_fichero.keys()) if isinstance(stu_fichero, dict) else None
    ref_codes = sorted(ref_fichero.keys())
    ok_rub, stu_rub = _llamar(f_rub, ref_fichero)

    problemas = []
    if stu_fichero != ref_fichero:
        problemas.append(f"fichero difiere (tú {stu_codes} vs esperado {ref_codes})")
    if not ok_rub or stu_rub != ref_rub:
        problemas.append(f"deuda_por_rubro difiere (tú {stu_rub if ok_rub else type(stu_rub).__name__} vs {ref_rub})")
    if not problemas:
        lc.ok(f"Archivador sorpresa ({len(sorpresa)} registros): consolidación y rubros coinciden con la referencia.", cont)
    else:
        lc.error("Archivador sorpresa: " + "; ".join(problemas) + ".",
                 "Si el oficial pasó pero el sorpresa no, probablemente dejaste valores fijos. "
                 "Procesa la lista que te pasan.", cont)


def _es_lista_de_pares(x):
    return isinstance(x, list) and all(isinstance(t, tuple) and len(t) == 2 for t in x)


def _check_informe_y_respuestas(cont, oficial):
    # ── 9) informe existe + deuda total en formato con comas ──────────────
    total_ref = _ref_deuda_por_rubro(_ref_consolidar(oficial)[0])
    esperado = sum(total_ref.values())  # 1042000
    # Decisión documentada: buscamos la cifra en formato con separador de miles
    # de Python (coma), tal como la escribe el informe con {:,}. Como respaldo,
    # normalizamos separadores (quitamos , y .) por si el alumno usó otro estilo.
    formato_coma = f"{esperado:,}"  # "1,042,000"
    if RUTA_INFORME.exists():
        lc.ok("salidas/informe_consolidacion.txt existe.", cont)
        texto = RUTA_INFORME.read_text(encoding="utf-8")
    else:
        lc.error("No existe salidas/informe_consolidacion.txt.",
                 "Genera el informe: uv run python consolidar.py", cont)
        texto = ""

    texto_norm = texto.replace(",", "").replace(".", "")
    if texto and (formato_coma in texto or str(esperado) in texto_norm):
        lc.ok(f"El informe reporta la deuda total consolidada correcta (${formato_coma} CLP).", cont)
    else:
        lc.error("El informe no contiene la deuda total consolidada correcta.",
                 "Puede estar desactualizado: reejecuta uv run python consolidar.py tras corregir. "
                 "Recuerda el formato con separador de miles ({:,}).", cont)

    # ── 10) interrogatorio respondido ─────────────────────────────────────
    if not RUTA_RESPUESTAS.exists():
        lc.error("No encuentro RESPUESTAS.md en la raíz del lab.",
                 "Copia el interrogatorio y respóndelo: cp plantillas/RESPUESTAS.md RESPUESTAS.md "
                 "(Windows: Copy-Item).", cont)
    else:
        pendientes = RUTA_RESPUESTAS.read_text(encoding="utf-8").count(MARCADOR_PENDIENTE)
        if pendientes == 0:
            lc.ok("RESPUESTAS.md está completo (sin respuestas pendientes).", cont)
        else:
            lc.error(f"RESPUESTAS.md tiene {pendientes} respuesta(s) sin contestar.",
                     f"Reemplaza cada '{MARCADOR_PENDIENTE}' por tu propia explicación.", cont)


def _cerrar(cont, oficial):
    _check_informe_y_respuestas(cont, oficial)

    if _BREAKPOINT["golpeado"]:
        print()
        lc.info("Detecté un breakpoint() en tu código y lo neutralicé para no colgarme (C8). "
                "Quítalo de consolidar.py antes de entregar: el depurador es para explorar, "
                "no para dejarlo puesto.")

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.titulo("Don Arquímedes revisa la consolidación")
        print(
            "Don Arquímedes hojea el informe, se detiene en los rechazados y sonríe:\n"
            "«Lo que no sirve, afuera; y con razón anotada. Así se ordena un archivo,\n"
            "joven analista. El cuaderno creció, y usted con él.»\n"
        )
        print(
            f"{lc.CIAN}Próxima jornada — Lab 03:{lc.RESET} el puerto quiere ESTADÍSTICAS —\n"
            "promedios, máximos, percentiles de deuda sobre miles de patentes. Ahí\n"
            "entra NumPy y los números empiezan a volar. Nos vemos en el mesón."
        )
    return codigo


if __name__ == "__main__":
    sys.exit(main())
