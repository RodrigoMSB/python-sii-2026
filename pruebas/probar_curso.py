"""Suite de Pruebas del Curso — corre las 7 unidades reproduciendo E01.

    uv run --no-project python pruebas/probar_curso.py            # todo el curso
    uv run --no-project python pruebas/probar_curso.py --lab lab-04
    uv run --no-project python pruebas/probar_curso.py --desde lab-05
    uv run --no-project python pruebas/probar_curso.py --listar
    uv run --no-project python pruebas/probar_curso.py --autocheck   # se prueba a sí misma (P5)

Exit 0 solo si TODO pasa. El repositorio nunca se ensucia (P1): se verifica al final
que `git status` quedó idéntico.
"""

import subprocess
import sys

import lib_pruebas as lp
from flujos import FLUJOS, resolver


def _git_status():
    r = subprocess.run(["git", "status", "--porcelain"], cwd=str(lp.RAIZ_REPO),
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def _autocheck() -> int:
    """P5: sabotea una copia (borra la solución) y AFIRMA que la prueba FALLA."""
    lp.titulo("Autochequeo de la suite (P5) — ¿puede fallar?")
    lp.info("Saboteo el Lab 01 (borro su solución) y exijo que la prueba lo detecte…")
    flujo = FLUJOS[0]
    aprobado, detalle, seg = lp.ejecutar_flujo(flujo, sabotear=True)
    print()
    if not aprobado:
        lp.ok(f"Sabotaje detectado — la prueba falló como se esperaba ({detalle}).")
        print(f"\n{lp.VERDE}{lp.NEGRITA}✔ 1/1 autochequeos correctos{lp.RESET}")
        print(f"{lp.CIAN}Una suite que puede fallar es una suite que prueba de verdad.{lp.RESET}")
        return 0
    lp.error("¡El sabotaje NO fue detectado! La suite pasó con la solución borrada.",
             "La suite es un adorno verde: revisa el arnés. ESTO ES UN BUG DE LA SUITE.")
    print(f"\n{lp.ROJO}{lp.NEGRITA}✘ 0/1 autochequeos correctos{lp.RESET}")
    return 1


def main() -> int:
    args = sys.argv[1:]

    if "--listar" in args:
        lp.titulo("Unidades del curso")
        for i, f in enumerate(FLUJOS, 1):
            print(f"  {i}. {f['carpeta']:<28} {f['titulo']}")
        return 0

    if "--autocheck" in args:
        return _autocheck()

    # Selección de flujos
    flujos = FLUJOS
    if "--lab" in args:
        f = resolver(args[args.index("--lab") + 1])
        if not f:
            lp.error("Lab no reconocido.", "Prueba --listar."); return 2
        flujos = [f]
    elif "--desde" in args:
        f = resolver(args[args.index("--desde") + 1])
        if not f:
            lp.error("Lab no reconocido.", "Prueba --listar."); return 2
        flujos = FLUJOS[FLUJOS.index(f):]

    estado_antes = _git_status()

    lp.titulo("Suite de Pruebas del Curso — Puerto Siracusa")
    lp.info(f"Reproduciendo el flujo del alumno en {len(flujos)} unidad(es). "
            "La primera corrida descarga bibliotecas; las siguientes usan caché.")
    lp.info("El repositorio no se toca: cada lab se prueba en una copia temporal.\n")

    resultados = []
    for f in flujos:
        print(f"{lp.NEGRITA}▶ {f['titulo']}{lp.RESET}")
        aprobado, detalle, seg = lp.ejecutar_flujo(f)
        (lp.ok if aprobado else lp.error)(f"{detalle} ({seg:.0f}s)")
        resultados.append((f, aprobado, seg))
        print()

    # Tabla resumen
    lp.titulo("Resumen")
    correctas = 0
    for f, aprobado, seg in resultados:
        marca = f"{lp.VERDE}CUMPLE{lp.RESET}" if aprobado else f"{lp.ROJO}FALLA {lp.RESET}"
        print(f"  {marca}  {f['titulo']:<40} {seg:6.0f}s")
        correctas += 1 if aprobado else 0
    total = len(resultados)

    # Higiene del repo (P1)
    estado_despues = _git_status()
    repo_limpio = estado_antes is not None and estado_antes == estado_despues
    print()
    if repo_limpio:
        lp.ok("Higiene: el repositorio quedó idéntico (git status sin cambios).")
    else:
        lp.error("Higiene: el repositorio cambió durante la suite.",
                 "Alguna prueba escribió fuera de su copia temporal (viola P1).")

    print()
    exito = correctas == total and repo_limpio
    color = lp.VERDE if exito else lp.ROJO
    marca = "✔" if exito else "✘"
    print(f"{color}{lp.NEGRITA}{marca} {correctas}/{total} pruebas correctas"
          f"{'' if repo_limpio else ' (+ repo sucio)'}{lp.RESET}")
    return 0 if exito else 1


if __name__ == "__main__":
    sys.exit(main())
