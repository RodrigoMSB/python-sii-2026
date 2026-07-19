"""Consolidación del archivador — PLANTILLA para la Ruta Artesano 🛠️ (Lab 02).

Este archivo YA CORRE tal cual, pero hace trampa: no normaliza deudas, no
rechaza nada y no agrupa por rubro. Tu trabajo es completar los seis TODO para
que consolide de verdad.

Reglas del juego:
  - Copia este archivo a la raíz del lab con el nombre consolidar.py
        (macOS/Linux)  cp plantillas/consolidar.py consolidar.py
        (Windows)      Copy-Item plantillas\\consolidar.py consolidar.py
  - Completa los TODO EN ORDEN (1 → 6) y ejecuta seguido para ver el avance:
        uv run python consolidar.py
  - ¿Trabado más de 10 minutos? Mira SOLO esa función en soluciones/consolidar.py,
    ciérrala y escríbela de memoria. Recuperar el código es gratis; recuperar la
    comprensión, jamás.

Se ejecuta SIEMPRE desde la raíz del lab:

    uv run python consolidar.py
"""

import sys as _s
if hasattr(_s.stdout, "reconfigure"):
    _s.stdout.reconfigure(encoding="utf-8")   # Windows: imprime UTF-8 sin morir (cp1252)
    _s.stderr.reconfigure(encoding="utf-8")


from pathlib import Path

from datos.archivador import REGISTROS_BRUTOS

# Orden fijo de los rubros para el informe (Comercio, Gastronomía, Turismo).
RUBROS = ["C", "G", "T"]


class RegistroInvalido(ValueError):
    """Se lanza cuando un registro bruto no se puede convertir en ficha."""


def normalizar_deuda(texto):
    """Convierte la deuda de texto a entero. '38.000' -> 38000, '0' -> 0.

    Si el texto no es un número (p. ej. 'S/I'), debe relanzarse como
    RegistroInvalido para poder rechazar ese registro.
    """
    # TODO 1 — Quita los puntos de miles con texto.replace(".", "") e intenta
    #          int(...). Envuélvelo en un try/except ValueError: si int falla,
    #          lanza  raise RegistroInvalido(f"deuda no numérica ('{texto}')") from None
    #          Pista: por ahora devolvemos 0 para que el archivo corra; reemplázalo.
    return 0


def crear_ficha(registro):
    """Crea una ficha limpia (dict) a partir de un registro bruto."""
    return {
        "codigo": registro["codigo"],
        "nombre": registro["nombre"],
        "estado": registro["estado"],
        "deuda": normalizar_deuda(registro["deuda"]),
        # TODO 2 — El rubro es la ÚLTIMA letra del código (guiño al Lab 01).
        #          Reemplaza "?" por  registro["codigo"][-1]
        "rubro": "?",
    }


def consolidar(registros):
    """Consolida los registros brutos en (fichero, rechazos).

    - fichero: dict {codigo: ficha} con los válidos.
    - rechazos: lista de tuplas (codigo, motivo).
    Regla de duplicados: gana el PRIMERO visto; el repetido se rechaza.
    """
    fichero = {}
    rechazos = []
    for registro in registros:
        codigo = registro["codigo"]
        # TODO 4 — Envuelve la creación de la ficha en un try/except RegistroInvalido.
        #          Si se lanza, agrega (codigo, str(error)) a 'rechazos' y usa
        #          'continue' para seguir con el siguiente. El programa NO debe morir
        #          por un registro malo.
        ficha = crear_ficha(registro)
        # TODO 3 — Antes de guardar, pregunta si el código YA está en 'fichero'
        #          (in sobre un dict pregunta por las CLAVES). Si ya está, agrega
        #          (codigo, "código duplicado") a 'rechazos' y 'continue'.
        fichero[codigo] = ficha
    return fichero, rechazos


def deuda_por_rubro(fichero):
    """Suma la deuda de las fichas agrupada por rubro. Devuelve {rubro: total}."""
    totales = {}
    # TODO 5 — Recorre fichero.values() y acumula por rubro:
    #          totales[rubro] = totales.get(rubro, 0) + ficha["deuda"]
    #          Pista: .get(clave, 0) evita el KeyError la primera vez que ves un rubro.
    return totales


def construir_informe(fichero, rechazos):
    """Arma el texto del informe de consolidación como una sola cadena."""
    total = sum(ficha["deuda"] for ficha in fichero.values())
    por_rubro = deuda_por_rubro(fichero)

    lineas = []
    lineas.append("INFORME DE CONSOLIDACIÓN — Dirección de Rentas de Puerto Siracusa")
    lineas.append("=" * 62)
    # TODO 6 — Agrega las CUATRO líneas del resumen con f-strings (respeta los
    #          espacios; usa {:,} para el separador de miles de la deuda):
    #              f"{'Registros del archivador':<24} : {len(fichero) + len(rechazos)}"
    #              f"{'Fichas consolidadas':<24} : {len(fichero)}"
    #              f"{'Registros rechazados':<24} : {len(rechazos)}"
    #              f"{'Deuda total consolidada':<24} : ${total:,} CLP"
    lineas.append("")
    lineas.append("Deuda por rubro:")
    for rubro in RUBROS:
        lineas.append(f"  {rubro}: ${por_rubro.get(rubro, 0):,} CLP")
    lineas.append("")
    lineas.append("Rechazados (código → motivo):")
    for codigo, motivo in rechazos:
        lineas.append(f"  - {codigo}: {motivo}")

    return "\n".join(lineas)


def main():
    fichero, rechazos = consolidar(REGISTROS_BRUTOS)
    informe = construir_informe(fichero, rechazos)
    print(informe)

    salidas = Path("salidas")
    salidas.mkdir(exist_ok=True)
    destino = salidas / "informe_consolidacion.txt"
    destino.write_text(informe + "\n", encoding="utf-8")

    print()
    print(f"[INFO] Informe archivado en: {destino}")


if __name__ == "__main__":
    main()
