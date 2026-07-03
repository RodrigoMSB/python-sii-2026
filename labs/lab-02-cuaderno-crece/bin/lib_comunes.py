"""Helpers compartidos por los scripts de bin/ del Lab 01.

Aquí vive la paleta de colores ANSI y las funciones de salida con el formato
que exige el curso:  [OK] / [ERROR] (+ Pista:) / [INFO]  y el resumen final
`✔|✘ N/N verificaciones correctas`.

Es 100 % biblioteca estándar (contrato C1) y se comporta bien en macOS, Linux
y Windows. Si la salida no es un terminal de verdad (por ejemplo, cuando se
redirige a un archivo), los colores se apagan solos para no ensuciar el texto.
"""

from __future__ import annotations

import os
import sys

# Windows / stdout no-consola: fuerza UTF-8 en la salida para que los símbolos del
# curso (✔, ✘, ═, emojis) no revienten con UnicodeEncodeError cuando stdout es un
# pipe o una consola cp1252 (CI, redirección). errors="replace" como red de seguridad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # pragma: no cover - stream sin reconfigure
        pass

# ─────────────────────────────────────────────────────────────────────────
#  Colores ANSI, con degradación limpia
# ─────────────────────────────────────────────────────────────────────────


def _colores_activos() -> bool:
    """Decide si conviene emitir códigos de color.

    - Si el usuario forzó color con FORCE_COLOR, obedecemos.
    - Si la salida no es un terminal interactivo (TTY), no coloreamos.
    """
    if os.environ.get("FORCE_COLOR"):
        return True
    return sys.stdout.isatty()


# En Windows moderno hay que "despertar" el soporte de secuencias ANSI de la
# consola. Este truco (os.system("")) activa el modo de procesamiento de
# escapes en cmd.exe y PowerShell sin instalar nada.
if os.name == "nt":  # pragma: no cover - depende del SO
    os.system("")

_USAR_COLOR = _colores_activos()


def _c(codigo: str) -> str:
    """Devuelve el código ANSI solo si los colores están activos."""
    return codigo if _USAR_COLOR else ""


VERDE = _c("\033[32m")
ROJO = _c("\033[31m")
AMARILLO = _c("\033[33m")
CIAN = _c("\033[36m")
NEGRITA = _c("\033[1m")
RESET = _c("\033[0m")


# ─────────────────────────────────────────────────────────────────────────
#  Contador de verificaciones (para el resumen final)
# ─────────────────────────────────────────────────────────────────────────


class Contador:
    """Lleva la cuenta de verificaciones correctas sobre el total.

    Se usa así en cada verificador:

        cont = Contador()
        if condicion:
            ok("...", cont)
        else:
            error("...", "pista", cont)
        ...
        sys.exit(resumen(cont))
    """

    def __init__(self) -> None:
        self.total = 0
        self.correctas = 0

    def suma(self, aprobada: bool) -> None:
        self.total += 1
        if aprobada:
            self.correctas += 1


# ─────────────────────────────────────────────────────────────────────────
#  Funciones de salida con formato del curso
# ─────────────────────────────────────────────────────────────────────────


def titulo(texto: str) -> None:
    """Imprime un encabezado destacado."""
    linea = "═" * len(texto)
    print(f"\n{CIAN}{NEGRITA}{texto}{RESET}")
    print(f"{CIAN}{linea}{RESET}")


def info(mensaje: str) -> None:
    """Mensaje informativo (no cuenta como verificación)."""
    print(f"{CIAN}[INFO]{RESET} {mensaje}")


def ok(mensaje: str, contador: Contador | None = None) -> None:
    """Verificación superada."""
    if contador is not None:
        contador.suma(True)
    print(f"{VERDE}[OK]{RESET} {mensaje}")


def error(mensaje: str, pista: str = "", contador: Contador | None = None) -> None:
    """Verificación fallida, con pista opcional en la línea siguiente."""
    if contador is not None:
        contador.suma(False)
    print(f"{ROJO}[ERROR]{RESET} {mensaje}")
    if pista:
        print(f"       {AMARILLO}Pista:{RESET} {pista}")


def resumen(contador: Contador) -> int:
    """Imprime el resumen final y devuelve el código de salida (0 si todo pasó)."""
    print()
    if contador.correctas == contador.total and contador.total > 0:
        print(
            f"{VERDE}{NEGRITA}✔ {contador.correctas}/{contador.total} "
            f"verificaciones correctas{RESET}"
        )
        return 0
    print(
        f"{ROJO}{NEGRITA}✘ {contador.correctas}/{contador.total} "
        f"verificaciones correctas{RESET}"
    )
    return 1
