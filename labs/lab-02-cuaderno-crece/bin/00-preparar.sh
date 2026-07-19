#!/usr/bin/env bash
export PYTHONUTF8=1  # Windows: Python imprime/lee UTF-8 sin morir (cp1252)
# ─────────────────────────────────────────────────────────────────────────
#  Preparador del Lab 02 (macOS / Linux / Windows con Git Bash)
#  Uso, desde la raíz del lab:   bash bin/00-preparar.sh
#
#  Monta el taller aislado: comprueba uv, crea/sincroniza el entorno virtual
#  con Python 3.13 y verifica que todo quedó en verde. Idempotente.
# ─────────────────────────────────────────────────────────────────────────
set -euo pipefail

if [ -t 1 ]; then
  VERDE=$'\033[32m'; ROJO=$'\033[31m'; AMARILLO=$'\033[33m'; CIAN=$'\033[36m'
  NEGRITA=$'\033[1m'; RESET=$'\033[0m'
else
  VERDE=""; ROJO=""; AMARILLO=""; CIAN=""; NEGRITA=""; RESET=""
fi

DIR_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ_LAB="$(cd "$DIR_SCRIPT/.." && pwd)"
cd "$RAIZ_LAB"

echo "${CIAN}${NEGRITA}Preparando el Lab 02 — El cuaderno crece${RESET}"
echo "${CIAN}Carpeta del lab: ${RAIZ_LAB}${RESET}"
echo

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

echo "${CIAN}[INFO]${RESET} Sincronizando el entorno (uv se encarga de traer Python 3.13)…"
uv sync
echo "${VERDE}[OK]${RESET} Entorno .venv/ listo."
echo

echo "${CIAN}[INFO]${RESET} Verificando el entorno…"
uv run python bin/verificar_entorno.py
