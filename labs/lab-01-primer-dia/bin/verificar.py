"""Verificador del Lab 01 — el juez del triaje.

Se ejecuta desde la raíz del lab:

    uv run python bin/verificar.py

Es de SOLO LECTURA sobre tu trabajo (contrato C1): mira tu triaje.py, tus
salidas y tu RESPUESTAS.md, pero jamás los modifica. Y es 100 % biblioteca
estándar.

Tiene su propia implementación de referencia de las tres funciones (así no hay
números mágicos que mantener) y, además, un "cuaderno sorpresa" aleatorio que
cambia en cada ejecución: si tu código funciona de verdad, dará bien con el
cuaderno oficial Y con el sorpresa. Si copiaste los números a mano, el sorpresa
te delata.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

# La raíz del lab es la carpeta que contiene a bin/. La ponemos primera en el
# path para poder importar 'datos' y cargar el triaje.py del alumno igual que
# lo haría Python al ejecutarlo desde ahí.
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402  (después de ajustar sys.path)

RUTA_TRIAJE = RAIZ / "triaje.py"
RUTA_INFORME = RAIZ / "salidas" / "informe_triaje.txt"
RUTA_RESPUESTAS = RAIZ / "RESPUESTAS.md"
MARCADOR_PENDIENTE = "(escribe aquí tu respuesta)"

FUNCIONES = ("contar_vigentes", "codigos_vencidas", "deuda_total")


# ─────────────────────────────────────────────────────────────────────────
#  Implementación de referencia (la verdad contra la que comparamos)
# ─────────────────────────────────────────────────────────────────────────


def ref_contar_vigentes(patentes):
    return sum(1 for p in patentes if p[2] == "VIGENTE")


def ref_codigos_vencidas(patentes):
    return [p[0] for p in patentes if p[2] == "VENCIDA"]


def ref_deuda_total(patentes):
    return sum(p[3] for p in patentes)


# ─────────────────────────────────────────────────────────────────────────
#  Cuaderno sorpresa (anti-loro): distinto en cada corrida
# ─────────────────────────────────────────────────────────────────────────


def generar_cuaderno_sorpresa():
    """Devuelve una lista de 6 a 10 patentes aleatorias.

    Usa random.Random() SIN semilla fija: cambia entre ejecuciones a propósito.
    """
    rng = random.Random()
    estados = ["VIGENTE", "VENCIDA", "SUSPENDIDA"]
    rubros = ["C", "G", "T"]
    posibles_deudas = [0, 0, 12000, 27500, 44000, 90000, 133000, 251000, 380000]

    cuantas = rng.randint(6, 10)
    patentes = []
    for i in range(cuantas):
        codigo = f"ZZ-9{rng.randint(0, 999):03d}-{rng.choice(rubros)}"
        nombre = f"Contribuyente Sorpresa {i + 1}"
        estado = rng.choice(estados)
        deuda = rng.choice(posibles_deudas)
        patentes.append([codigo, nombre, estado, deuda])
    return patentes


# ─────────────────────────────────────────────────────────────────────────
#  Carga del triaje.py del alumno (blindada contra cualquier excepción)
# ─────────────────────────────────────────────────────────────────────────


def cargar_triaje():
    """Carga triaje.py como módulo. Devuelve (modulo, error_o_None)."""
    spec = importlib.util.spec_from_file_location("triaje_alumno", RUTA_TRIAJE)
    modulo = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(modulo)
        return modulo, None
    except BaseException as exc:  # noqa: BLE001 - queremos atrapar TODO
        return None, exc


def _comparar(nombre_cuaderno, obtenido, esperado, cont, pista):
    """Compara obtenido vs esperado y emite [OK]/[ERROR] con valores visibles."""
    if obtenido == esperado:
        lc.ok(f"{nombre_cuaderno}: obtuvo {obtenido!r} (correcto)", cont)
    else:
        lc.error(
            f"{nombre_cuaderno}: obtuvo {obtenido!r}, se esperaba {esperado!r}",
            pista,
            cont,
        )


def main() -> int:
    lc.titulo("Verificador del Lab 01 — Triaje de patentes")

    try:
        from datos.cuaderno import PATENTES as CUADERNO_OFICIAL
    except Exception as exc:  # pragma: no cover
        lc.error(
            f"No pude leer el cuaderno oficial (datos/cuaderno.py): {exc}",
            "¿Estás ejecutando desde la raíz del lab? Prueba: uv run python bin/verificar.py",
        )
        return 1

    cont = lc.Contador()

    # ── 1) triaje.py existe en la raíz ────────────────────────────────────
    if RUTA_TRIAJE.exists():
        lc.ok("triaje.py está en la raíz del lab.", cont)
    else:
        lc.error(
            "No encuentro triaje.py en la raíz del lab.",
            "Cópialo desde plantillas/ (Artesano) o soluciones/ (Explorador). "
            "Ver Guía 5, paso de copia.",
            cont,
        )
        # Sin triaje no hay nada más que revisar en el código; igual reportamos
        # los checks de archivos para dar un total estable.
        return _cerrar(cont, _checks_archivos(cont, CUADERNO_OFICIAL))

    # ── 2) se importa sin explotar ────────────────────────────────────────
    modulo, err = cargar_triaje()
    if err is None:
        lc.ok("triaje.py se cargó sin errores.", cont)
    else:
        tipo = type(err).__name__
        lc.error(
            f"triaje.py falló al cargar: {tipo}: {err}",
            "Lee el traceback de ABAJO hacia arriba: la última línea dice el "
            "tipo de error y el mensaje. Un SyntaxError suele apuntar la línea "
            "siguiente a la del problema (revisa los dos puntos ':' y la sangría).",
            cont,
        )
        # No se pudo cargar: los checks 3..9 no se pueden evaluar → cuentan mal.
        for _ in range(7):
            lc.error(
                "No evaluable: primero hay que poder cargar triaje.py.",
                "Corrige el error de carga de arriba y vuelve a ejecutar.",
                cont,
            )
        return _cerrar(cont, _checks_archivos(cont, CUADERNO_OFICIAL))

    # ── 3) las tres funciones existen y son invocables ────────────────────
    faltan = [n for n in FUNCIONES if not callable(getattr(modulo, n, None))]
    if not faltan:
        lc.ok("Existen las funciones contar_vigentes, codigos_vencidas y deuda_total.", cont)
    else:
        lc.error(
            f"Faltan o no son funciones: {', '.join(faltan)}.",
            "No renombres las funciones: los nombres deben ser exactos.",
            cont,
        )

    f_vig = getattr(modulo, "contar_vigentes", None)
    f_ven = getattr(modulo, "codigos_vencidas", None)
    f_deu = getattr(modulo, "deuda_total", None)

    sorpresa = generar_cuaderno_sorpresa()

    # ── 4-6) contra el cuaderno OFICIAL ───────────────────────────────────
    lc.info("Comparando contra el cuaderno OFICIAL (24 patentes)…")
    _eval_funcion(
        f_vig, CUADERNO_OFICIAL, ref_contar_vigentes,
        "contar_vigentes [oficial]",
        "¿Comparas el estado con == \"VIGENTE\" exacto (mayúsculas)?",
        cont,
    )
    _eval_funcion(
        f_ven, CUADERNO_OFICIAL, ref_codigos_vencidas,
        "codigos_vencidas [oficial]",
        "Debes agregar con .append el código de las patentes \"VENCIDA\", en orden.",
        cont,
    )
    _eval_funcion(
        f_deu, CUADERNO_OFICIAL, ref_deuda_total,
        "deuda_total [oficial]",
        "La deuda se suma para TODAS las patentes, sin filtrar por estado.",
        cont,
    )

    # ── 7-9) contra el cuaderno SORPRESA (anti-loro) ──────────────────────
    lc.info(f"Comparando contra un cuaderno SORPRESA aleatorio ({len(sorpresa)} patentes)…")
    _eval_funcion(
        f_vig, sorpresa, ref_contar_vigentes,
        "contar_vigentes [sorpresa]",
        "Si aquí falla pero el oficial pasó, quizá devolviste un número fijo. "
        "Cuenta de verdad recorriendo la lista.",
        cont,
    )
    _eval_funcion(
        f_ven, sorpresa, ref_codigos_vencidas,
        "codigos_vencidas [sorpresa]",
        "Si aquí falla pero el oficial pasó, quizá devolviste una lista fija. "
        "Recorre y filtra la lista que te pasan.",
        cont,
    )
    _eval_funcion(
        f_deu, sorpresa, ref_deuda_total,
        "deuda_total [sorpresa]",
        "Si aquí falla pero el oficial pasó, quizá devolviste un total fijo. "
        "Suma la deuda de la lista que te pasan.",
        cont,
    )

    # ── 10-12) checks de archivos ─────────────────────────────────────────
    return _cerrar(cont, _checks_archivos(cont, CUADERNO_OFICIAL))


def _eval_funcion(func, patentes, referencia, etiqueta, pista, cont):
    """Ejecuta la función del alumno de forma segura y compara con la referencia."""
    esperado = referencia(patentes)
    if func is None:
        lc.error(f"{etiqueta}: la función no existe.", "No renombres las funciones.", cont)
        return
    try:
        obtenido = func(patentes)
    except Exception as exc:  # noqa: BLE001
        lc.error(
            f"{etiqueta}: la función lanzó {type(exc).__name__}: {exc}",
            pista,
            cont,
        )
        return
    _comparar(etiqueta, obtenido, esperado, cont, pista)


def _checks_archivos(cont, cuaderno_oficial):
    """Checks 10, 11 y 12 (informe y RESPUESTAS). Devuelve True si todo pasó."""
    # ── 10) el informe existe ─────────────────────────────────────────────
    if RUTA_INFORME.exists():
        lc.ok("salidas/informe_triaje.txt existe.", cont)
        informe_txt = RUTA_INFORME.read_text(encoding="utf-8")
    else:
        lc.error(
            "No existe salidas/informe_triaje.txt.",
            "Genera el informe ejecutando el triaje: uv run python triaje.py",
            cont,
        )
        informe_txt = ""

    # ── 11) el informe trae la deuda total correcta ───────────────────────
    deuda_ok = str(ref_deuda_total(cuaderno_oficial))
    if informe_txt and deuda_ok in informe_txt:
        lc.ok(f"El informe reporta la deuda total correcta (${deuda_ok} CLP).", cont)
    else:
        lc.error(
            "El informe no contiene la deuda total correcta.",
            "Puede estar desactualizado: vuelve a ejecutar uv run python triaje.py "
            "DESPUÉS de corregir tus funciones.",
            cont,
        )

    # ── 12) el interrogatorio está respondido ─────────────────────────────
    if not RUTA_RESPUESTAS.exists():
        lc.error(
            "No encuentro RESPUESTAS.md en la raíz del lab.",
            "Copia el interrogatorio y respóndelo con tus palabras: "
            "cp plantillas/RESPUESTAS.md RESPUESTAS.md (Windows: Copy-Item).",
            cont,
        )
    else:
        texto = RUTA_RESPUESTAS.read_text(encoding="utf-8")
        pendientes = texto.count(MARCADOR_PENDIENTE)
        if pendientes == 0:
            lc.ok("RESPUESTAS.md está completo (sin respuestas pendientes).", cont)
        else:
            lc.error(
                f"RESPUESTAS.md tiene {pendientes} respuesta(s) sin contestar.",
                f"Reemplaza cada '{MARCADOR_PENDIENTE}' por tu propia explicación.",
                cont,
            )

    return cont.correctas == cont.total


def _cerrar(cont, _todo_ok):
    """Imprime el resumen y, si todo pasó, el mensaje de Don Arquímedes."""
    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.titulo("Don Arquímedes archiva tu informe")
        print(
            "Don Arquímedes toma tu informe, lo mira por encima de sus anteojos y\n"
            "asiente despacio: «Patente por patente, número por número. Así se hace\n"
            "el trabajo en Rentas, joven analista.»\n"
        )
        print(
            f"{lc.CIAN}Próxima jornada — Lab 02:{lc.RESET} el municipio te pasará miles de\n"
            "patentes en una planilla de verdad. Ahí cambiaremos las listas por\n"
            "pandas… pero el 'recorrer y filtrar' que aprendiste hoy será exactamente\n"
            "lo mismo, solo que más rápido. Nos vemos en el mesón."
        )
    return codigo


if __name__ == "__main__":
    sys.exit(main())
