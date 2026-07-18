#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────
#  Abre el REPL de Python del lab.
#  Uso, desde la raíz del lab:   bash bin/repl.sh
#
#  En Windows (Git Bash) el REPL interactivo necesita 'winpty' para mostrar
#  el prompt >>> correctamente. Este script lo detecta y lo usa solo si hace
#  falta; en macOS/Linux abre el REPL directo. Un mismo comando en todos lados.
# ─────────────────────────────────────────────────────────────────────────
set -euo pipefail

# Nos paramos SIEMPRE en la raíz del lab (la carpeta que contiene a bin/).
DIR_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ_LAB="$(cd "$DIR_SCRIPT/.." && pwd)"
cd "$RAIZ_LAB"

# winpty solo existe en Git Bash (Windows). Si está, lo usamos; si no, directo.
if command -v winpty >/dev/null 2>&1; then
  winpty uv run python
else
  uv run python
fi
