"""Triaje de patentes — PLANTILLA para la Ruta Artesano 🛠️ (Lab 01).

Este archivo YA CORRE tal cual, pero miente: todas las cuentas dan cero o
vacío. Tu trabajo es completar los cinco TODO para que diga la verdad.

Reglas del juego:
  - Copia este archivo a la raíz del lab con el nombre triaje.py
        (macOS/Linux)  cp plantillas/triaje.py triaje.py
        (Windows)      Copy-Item plantillas\\triaje.py triaje.py
  - Completa los TODO EN ORDEN (1 → 5). Después de cada uno puedes ejecutar
        uv run python triaje.py
    y ver cómo el informe se va corrigiendo.
  - ¿Trabado más de 10 minutos en una función? Abre soluciones/triaje.py,
    mira SOLO esa función, ciérrala y escríbela de memoria. No copies el archivo
    entero: recuperar el código es gratis; recuperar la comprensión, jamás.

Se ejecuta SIEMPRE desde la raíz del lab:

    uv run python triaje.py
"""

import sys as _s
if hasattr(_s.stdout, "reconfigure"):
    _s.stdout.reconfigure(encoding="utf-8")   # Windows: imprime UTF-8 sin morir (cp1252)
    _s.stderr.reconfigure(encoding="utf-8")


from pathlib import Path

from datos.cuaderno import PATENTES

# ─── Constantes de posición ───────────────────────────────────────────────
# Cada patente es una lista [codigo, nombre, estado, deuda]. Les ponemos nombre
# a las posiciones para no escribir números mágicos y no equivocarnos de columna.
POS_CODIGO = 0
POS_NOMBRE = 1
POS_ESTADO = 2
POS_DEUDA = 3


def contar_vigentes(patentes):
    """Devuelve cuántas patentes están en estado 'VIGENTE'."""
    total = 0
    # TODO 1 — Recorre 'patentes' con un for. Dentro, usa un if para preguntar
    #          si patente[POS_ESTADO] es igual a "VIGENTE"; si lo es, súmale 1
    #          a 'total'.
    #          Pista: la comparación de igualdad se escribe con == (doble igual).
    #          Ojo: "VIGENTE" en mayúsculas y exacto, tal como está en el cuaderno.
    return total


def codigos_vencidas(patentes):
    """Devuelve la lista de códigos cuyo estado es 'VENCIDA', en orden."""
    vencidas = []
    # TODO 2 — Recorre 'patentes'. Cuando el estado sea "VENCIDA", agrega el
    #          código (patente[POS_CODIGO]) a la lista 'vencidas'.
    #          Pista: para agregar al final de una lista se usa vencidas.append(...)
    return vencidas


def deuda_total(patentes):
    """Suma la deuda de TODAS las patentes (vigentes, vencidas y suspendidas)."""
    total = 0
    # TODO 3 — Recorre 'patentes' y ve sumando patente[POS_DEUDA] a 'total'.
    #          Pista: aquí NO hay if. Se suman TODAS, deban o no deban.
    #          Es un "acumulador": total = total + patente[POS_DEUDA]
    return total


def construir_informe(patentes):
    """Arma el texto del informe de triaje como una sola cadena multilinea."""
    n = len(patentes)
    v = contar_vigentes(patentes)
    vencidas = codigos_vencidas(patentes)
    t = deuda_total(patentes)

    lineas = []
    lineas.append("INFORME DE TRIAJE — Dirección de Rentas de Puerto Siracusa")
    lineas.append("=" * 58)
    # TODO 4 — Agrega las CUATRO líneas del resumen usando f-strings y las
    #          variables n, v, vencidas y t. Deben quedar EXACTAMENTE así
    #          (respeta los espacios para que las columnas queden alineadas):
    #              Patentes registradas : {n}
    #              Patentes vigentes    : {v}
    #              Patentes vencidas    : {len(vencidas)}
    #              Deuda total          : ${t} CLP
    #          Pista: cada línea es un lineas.append(f"...")
    lineas.append("")
    lineas.append("Detalle de patentes vencidas:")
    # TODO 5 — Recorre la lista 'vencidas' con un for y, por cada 'codigo',
    #          agrega una línea con el formato "  - {codigo}" (dos espacios,
    #          guion, espacio, código).
    #          Pista: lineas.append(f"  - {codigo}")
    return "\n".join(lineas)


def main():
    informe = construir_informe(PATENTES)
    print(informe)

    # Guardamos una copia en disco para dejar constancia del triaje.
    # pathlib + UTF-8: rutas portables y acentos que no se rompen.
    salidas = Path("salidas")
    salidas.mkdir(exist_ok=True)
    destino = salidas / "informe_triaje.txt"
    destino.write_text(informe + "\n", encoding="utf-8")

    print()
    print(f"[INFO] Informe archivado en: {destino}")


if __name__ == "__main__":
    main()
