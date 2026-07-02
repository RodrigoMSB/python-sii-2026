"""Triaje de patentes — SOLUCIÓN OFICIAL (Lab 01).

Este es el programa terminado. Léelo si vas por la Ruta Explorador 🔎 o si te
trabaste más de 10 minutos por la Ruta Artesano 🛠️ (mira SOLO la función que
te falta, cierra el archivo y escríbela de memoria).

Todo aquí es de principiante a propósito: solo listas, for, if y f-strings.
Nada de diccionarios ni comprensiones (eso llega en el Lab 02).

Se ejecuta SIEMPRE desde la raíz del lab:

    uv run python triaje.py
"""

from pathlib import Path

from datos.cuaderno import PATENTES

# ─── Constantes de posición ───────────────────────────────────────────────
# Cada patente es una lista [codigo, nombre, estado, deuda]. En vez de escribir
# números mágicos como patente[2] por todo el código (¿qué era el 2?), les
# ponemos nombre. Se lee mejor y no te equivocas de columna.
POS_CODIGO = 0
POS_NOMBRE = 1
POS_ESTADO = 2
POS_DEUDA = 3


def contar_vigentes(patentes):
    """Devuelve cuántas patentes están en estado 'VIGENTE'."""
    total = 0
    for patente in patentes:
        if patente[POS_ESTADO] == "VIGENTE":
            total = total + 1
    return total


def codigos_vencidas(patentes):
    """Devuelve la lista de códigos cuyo estado es 'VENCIDA', en orden."""
    vencidas = []
    for patente in patentes:
        if patente[POS_ESTADO] == "VENCIDA":
            vencidas.append(patente[POS_CODIGO])
    return vencidas


def deuda_total(patentes):
    """Suma la deuda de TODAS las patentes (vigentes, vencidas y suspendidas)."""
    total = 0
    for patente in patentes:
        total = total + patente[POS_DEUDA]
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
    lineas.append(f"Patentes registradas : {n}")
    lineas.append(f"Patentes vigentes    : {v}")
    lineas.append(f"Patentes vencidas    : {len(vencidas)}")
    lineas.append(f"Deuda total          : ${t} CLP")
    lineas.append("")
    lineas.append("Detalle de patentes vencidas:")
    for codigo in vencidas:
        lineas.append(f"  - {codigo}")

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
