"""Arnés común de la Suite de Pruebas del Curso — 100 % stdlib, multiplataforma.

Reproduce el flujo feliz del alumno (E01) de CADA lab en una COPIA temporal, sin
tocar jamás el repositorio (contrato P1). Invoca los verificadores certificados de
cada lab; no duplica sus cifras de control (las llama).

Contratos P1–P5 (ver SPEC-009):
  P1  el repo jamás se ensucia (copia a tempdir, limpieza con try/finally).
  P2  100 % stdlib, pathlib, subprocess con listas (nunca shell=True), utf-8 +
      errors=replace, timeouts en todo subproceso, ANSI activado en Windows.
  P4  salida [OK]/[ERROR]+pista/[INFO], resumen N/N, exit 0 solo si todo pasa.
  P5  se prueba a sí mismo: modo sabotaje que AFIRMA que una prueba puede fallar.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parent.parent
REPORTES = RAIZ_REPO / "pruebas" / "_reportes"
MARCADOR = "(escribe aquí tu respuesta)"
TIMEOUT = 600  # segundos por paso (anti-cuelgue, P2)

# ─── Colores ANSI (con degradación y despertar de Windows) ─────────────────
if os.name == "nt":  # pragma: no cover
    os.system("")
_TTY = sys.stdout.isatty() or bool(os.environ.get("FORCE_COLOR"))


def _c(code: str) -> str:
    return code if _TTY else ""


VERDE, ROJO, AMARILLO, CIAN = _c("\033[32m"), _c("\033[31m"), _c("\033[33m"), _c("\033[36m")
NEGRITA, RESET = _c("\033[1m"), _c("\033[0m")


def titulo(t: str) -> None:
    print(f"\n{CIAN}{NEGRITA}{t}{RESET}")
    print(f"{CIAN}{'═' * len(t)}{RESET}")


def info(m: str) -> None:
    print(f"{CIAN}[INFO]{RESET} {m}")


def ok(m: str) -> None:
    print(f"{VERDE}[OK]{RESET} {m}")


def error(m: str, pista: str = "") -> None:
    print(f"{ROJO}[ERROR]{RESET} {m}")
    if pista:
        print(f"       {AMARILLO}Pista:{RESET} {pista}")


# ─── Subprocesos portables (P2) ────────────────────────────────────────────

def correr(args, cwd, timeout=TIMEOUT):
    """Ejecuta una lista de argumentos (nunca shell=True). Devuelve el resultado
    con stdout/stderr decodificados en utf-8 tolerante."""
    try:
        return subprocess.run(
            args, cwd=str(cwd), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        salida = (exc.stdout or "") + (exc.stderr or "")
        return subprocess.CompletedProcess(args, 124, salida, f"TIMEOUT tras {timeout}s")


# ─── Copia aislada del lab (P1) ────────────────────────────────────────────

# Solo entorno y salidas. OJO: ignore_patterns matchea por BASENAME en cualquier
# nivel, así que NO se listan los scripts (triaje.py, etc.): eso borraría también
# soluciones/ y plantillas/, que SÍ deben copiarse.
_IGNORAR = shutil.ignore_patterns(".venv", "__pycache__", "*.pyc", ".pytest_cache", "salidas")


def copiar_lab(carpeta: str) -> Path:
    """Copia labs/<carpeta> a un directorio temporal, ignorando entorno y
    artefactos del alumno. El repo no se toca."""
    origen = RAIZ_REPO / "labs" / carpeta
    destino = Path(tempfile.mkdtemp(prefix=f"prueba-{carpeta}-")) / carpeta
    shutil.copytree(origen, destino, ignore=_IGNORAR)
    return destino


def rellenar_marcadores(ruta: Path) -> int:
    """Reemplaza cada marcador pendiente por texto de prueba. Devuelve cuántos."""
    texto = ruta.read_text(encoding="utf-8")
    n = texto.count(MARCADOR)
    i = 0
    while MARCADOR in texto:
        i += 1
        texto = texto.replace(MARCADOR, f"Respuesta de prueba {i}.", 1)
    ruta.write_text(texto, encoding="utf-8")
    return n


def _guardar_reporte(copia: Path, carpeta: str, etapa: str, r):
    """Al fallar, copia salidas/ y el log del subproceso a pruebas/_reportes/."""
    try:
        dst = REPORTES / carpeta
        dst.mkdir(parents=True, exist_ok=True)
        salidas = copia / "salidas"
        if salidas.is_dir():
            shutil.copytree(salidas, dst / "salidas", dirs_exist_ok=True)
        log = [f"# Fallo en etapa: {etapa}", ""]
        if r is not None:
            log += [f"returncode: {r.returncode}", "", "--- stdout ---", r.stdout or "",
                    "--- stderr ---", r.stderr or ""]
        (dst / "log.txt").write_text("\n".join(log), encoding="utf-8")
    except Exception:  # noqa: BLE001 - un reporte que falla no debe romper la suite
        pass


# ─── El flujo por lab (reproduce E01) ──────────────────────────────────────

def ejecutar_flujo(flujo: dict, sabotear: bool = False):
    """Ejecuta el flujo feliz del alumno en una copia temporal.

    Devuelve (aprobado: bool, detalle: str, segundos: float). Con sabotear=True
    elimina la solución del lab en la copia (para el autochequeo P5).
    """
    carpeta = flujo["carpeta"]
    t0 = time.monotonic()
    copia = copiar_lab(carpeta)

    def fin(aprobado, detalle, etapa=None, r=None):
        if not aprobado:
            _guardar_reporte(copia, carpeta, etapa or detalle, r)
        shutil.rmtree(copia.parent, ignore_errors=True)
        return aprobado, detalle, time.monotonic() - t0

    if sabotear:
        (copia / "soluciones" / flujo["script"]).unlink(missing_ok=True)

    # 1) Preparar (uv sync respeta el uv.lock del lab)
    r = correr(["uv", "sync"], cwd=copia)
    if r.returncode != 0:
        return fin(False, "uv sync falló", "uv sync", r)

    # 2) Verificar entorno
    r = correr(["uv", "run", "python", "bin/verificar_entorno.py"], cwd=copia)
    if r.returncode != 0:
        return fin(False, "verificar_entorno no dio verde", "verificar_entorno", r)

    # 3) El alumno resuelve (recuperador: solución + salidas)
    r = correr(["uv", "run", "python", "bin/recuperar_lab.py"], cwd=copia)
    if r.returncode != 0:
        return fin(False, "recuperar_lab falló (¿solución ausente?)", "recuperar_lab", r)

    # 5) Anti-adorno: el verificador DEBE reclamar el interrogatorio (exit 1)
    r = correr(["uv", "run", "python", "bin/verificar.py"], cwd=copia)
    if r.returncode == 0:
        return fin(False, "el verificador pasó SIN interrogatorio (adorno verde)", "anti-adorno", r)

    # 4) Rellenar el interrogatorio (RESPUESTAS.md o BITACORA.md)
    resp = copia / flujo["respuestas"]
    if not resp.exists():
        plantilla = copia / "plantillas" / flujo["respuestas"]
        if not plantilla.exists():
            return fin(False, f"no encuentro {flujo['respuestas']} ni su plantilla", "interrogatorio")
        shutil.copyfile(plantilla, resp)
    if rellenar_marcadores(resp) == 0:
        return fin(False, f"no había marcadores en {flujo['respuestas']}", "interrogatorio")

    # 6) Veredicto final
    r = correr(["uv", "run", "python", "bin/verificar.py"], cwd=copia)
    if r.returncode != 0:
        return fin(False, "el verificador final no dio verde", "veredicto", r)
    if "verificaciones correctas" not in r.stdout or "✔" not in r.stdout:
        return fin(False, "la salida del verificador no confirma N/N", "veredicto", r)

    # Cifras insignia en el informe del lab
    informe = copia / flujo["informe"]
    txt = informe.read_text(encoding="utf-8", errors="replace") if informe.exists() else ""
    faltan = [s for s in flujo["insignia"] if s not in txt]
    if faltan:
        return fin(False, f"faltan cifras insignia {faltan} en {flujo['informe']}", "insignia")

    return fin(True, "flujo del alumno en verde", None)
