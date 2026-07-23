#!/usr/bin/env bash
export PYTHONUTF8=1  # Windows: Python imprime/lee UTF-8 sin morir (cp1252)
export UV_NATIVE_TLS=1  # Redes corporativas (SII): usa los certificados del sistema
# ─────────────────────────────────────────────────────────────────────────
#  Preparador del Lab 01 (macOS / Linux / Windows con Git Bash)
#  Uso, desde la raíz del lab:   bash bin/00-preparar.sh
#
#  Monta el "taller aislado": comprueba uv, crea/sincroniza el entorno virtual
#  con Python 3.13 y verifica que todo quedó en verde. Es idempotente: puedes
#  correrlo las veces que quieras; no duplica nada.
# ─────────────────────────────────────────────────────────────────────────
set -euo pipefail

# Colores (se apagan si la salida no es un terminal)
if [ -t 1 ]; then
  VERDE=$'\033[32m'; ROJO=$'\033[31m'; AMARILLO=$'\033[33m'; CIAN=$'\033[36m'
  NEGRITA=$'\033[1m'; RESET=$'\033[0m'
else
  VERDE=""; ROJO=""; AMARILLO=""; CIAN=""; NEGRITA=""; RESET=""
fi

# Nos paramos SIEMPRE en la raíz del lab (la carpeta que contiene a bin/),
# sin importar desde dónde se invoque el script.
DIR_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ_LAB="$(cd "$DIR_SCRIPT/.." && pwd)"
cd "$RAIZ_LAB"

echo "${CIAN}${NEGRITA}Preparando el Lab 01 — El primer día en Rentas${RESET}"
echo "${CIAN}Carpeta del lab: ${RAIZ_LAB}${RESET}"
echo

# ── 1) ¿Está uv instalado? ────────────────────────────────────────────────
if ! command -v uv >/dev/null 2>&1; then
  echo "${ROJO}[ERROR]${RESET} No encuentro 'uv' en el PATH."
  echo "       ${AMARILLO}Pista:${RESET} instala uv y vuelve a intentar. Elige una:"
  echo "         • Homebrew:  brew install uv"
  echo "         • Script:    curl -LsSf https://astral.sh/uv/install.sh | sh"
  echo "       Cierra y reabre la terminal después de instalar."
  echo "       Más ayuda en docs/setup-alumno.md y docs/troubleshooting.md."
  exit 1
fi
echo "${VERDE}[OK]${RESET} uv encontrado: $(command -v uv)"

# ── 2) Crear / sincronizar el entorno virtual con Python 3.13 ─────────────
echo "${CIAN}[INFO]${RESET} Sincronizando el entorno (uv se encarga de traer Python 3.13)…"
uv sync
echo "${VERDE}[OK]${RESET} Entorno .venv/ listo."
echo

# ── 3) Verificar que el entorno quedó en verde ────────────────────────────
echo "${CIAN}[INFO]${RESET} Verificando el entorno…"
uv run python bin/verificar_entorno.py
