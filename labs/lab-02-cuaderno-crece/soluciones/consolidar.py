"""Consolidación del archivador — SOLUCIÓN OFICIAL (Lab 02).

Toma los registros brutos del archivador antiguo (sucios, con deudas escritas
como texto y hasta una patente repetida), rechaza los que no se pueden salvar
SIN morirse, y consolida los válidos en un fichero (diccionario indexado por
código). Al final arma el informe de consolidación para Don Arquímedes.

Novedades del Lab 02 que verás aquí: diccionarios, funciones de verdad y manejo
de excepciones (incluida una excepción propia, RegistroInvalido).

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
    """Se lanza cuando un registro bruto no se puede convertir en ficha.

    Hereda de ValueError porque, en el fondo, es un problema con el *valor* de
    los datos transcritos. Tener nuestro propio tipo nos deja capturar
    exactamente este error y no confundirlo con otros ValueError del sistema.
    """


def normalizar_deuda(texto):
    """Convierte la deuda de texto a entero. '38.000' -> 38000, '0' -> 0.

    Si el texto no representa un número (p. ej. 'S/I'), relanza como
    RegistroInvalido con el texto original para que se pueda rechazar.
    """
    limpio = texto.replace(".", "")  # quita los puntos de miles
    try:
        return int(limpio)
    except ValueError:
        # Lo relanzamos como NUESTRO error, sin arrastrar el traceback interno.
        raise RegistroInvalido(f"deuda no numérica ('{texto}')") from None


def crear_ficha(registro):
    """Crea una ficha limpia (dict) a partir de un registro bruto."""
    return {
        "codigo": registro["codigo"],
        "nombre": registro["nombre"],
        "estado": registro["estado"],
        "deuda": normalizar_deuda(registro["deuda"]),
        # El rubro es la última letra del código (guiño al Lab 01: codigo[-1]).
        "rubro": registro["codigo"][-1],
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
        try:
            ficha = crear_ficha(registro)
        except RegistroInvalido as error:
            # Un registro malo NO bota el proceso: se anota y se sigue.
            rechazos.append((codigo, str(error)))
            continue
        if codigo in fichero:  # 'in' sobre un dict pregunta por las CLAVES
            rechazos.append((codigo, "código duplicado"))
            continue
        fichero[codigo] = ficha
    return fichero, rechazos


def deuda_por_rubro(fichero):
    """Suma la deuda de las fichas agrupada por rubro. Devuelve {rubro: total}."""
    totales = {}
    for ficha in fichero.values():
        rubro = ficha["rubro"]
        totales[rubro] = totales.get(rubro, 0) + ficha["deuda"]
    return totales


def construir_informe(fichero, rechazos):
    """Arma el texto del informe de consolidación como una sola cadena."""
    total = sum(ficha["deuda"] for ficha in fichero.values())
    por_rubro = deuda_por_rubro(fichero)

    lineas = []
    lineas.append("INFORME DE CONSOLIDACIÓN — Dirección de Rentas de Puerto Siracusa")
    lineas.append("=" * 62)
    lineas.append(f"{'Registros del archivador':<24} : {len(fichero) + len(rechazos)}")
    lineas.append(f"{'Fichas consolidadas':<24} : {len(fichero)}")
    lineas.append(f"{'Registros rechazados':<24} : {len(rechazos)}")
    lineas.append(f"{'Deuda total consolidada':<24} : ${total:,} CLP")
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
