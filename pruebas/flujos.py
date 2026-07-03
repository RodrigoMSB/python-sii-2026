"""Definición data-driven del flujo de prueba por unidad (SPEC-009 §4).

El arnés (lib_pruebas.ejecutar_flujo) es genérico; lo único que varía por lab vive
aquí como datos. Agregar un lab futuro = agregar una entrada, no escribir otra
prueba (contrato P3).

Cada entrada declara:
  carpeta     nombre de la carpeta bajo labs/
  titulo      nombre humano de la unidad
  script      el programa del alumno (lo que la solución repone en la raíz)
  respuestas  el interrogatorio (RESPUESTAS.md o, en el capstone, BITACORA.md)
  informe     ruta del informe que deja el lab (relativa a la raíz del lab)
  insignia    cadenas que DEBEN aparecer en ese informe (las cifras insignia)
"""

FLUJOS = [
    {
        "carpeta": "lab-01-primer-dia",
        "titulo": "Lab 01 — El primer día en Rentas",
        "script": "triaje.py",
        "respuestas": "RESPUESTAS.md",
        "informe": "salidas/informe_triaje.txt",
        "insignia": ["2350000"],
    },
    {
        "carpeta": "lab-02-cuaderno-crece",
        "titulo": "Lab 02 — El cuaderno crece",
        "script": "consolidar.py",
        "respuestas": "RESPUESTAS.md",
        "informe": "salidas/informe_consolidacion.txt",
        "insignia": ["1,042,000"],
    },
    {
        "carpeta": "lab-03-numeros-del-puerto",
        "titulo": "Lab 03 — Los números del puerto",
        "script": "panorama.py",
        "respuestas": "RESPUESTAS.md",
        "informe": "salidas/informe_panorama.txt",
        "insignia": ["90,680,000", "Diciembre"],
    },
    {
        "carpeta": "lab-04-cuatro-fuentes",
        "titulo": "Lab 04 — Las cuatro fuentes",
        "script": "fuentes.py",
        "respuestas": "RESPUESTAS.md",
        "informe": "salidas/informe_fuentes.txt",
        "insignia": ["2,072,500"],
    },
    {
        "carpeta": "lab-05-gran-limpieza",
        "titulo": "Lab 05 — La gran limpieza",
        "script": "limpiar.py",
        "respuestas": "RESPUESTAS.md",
        "informe": "salidas/informe_limpieza.txt",
        "insignia": ["3,107,500"],
    },
    {
        "carpeta": "lab-06-transformar-combinar",
        "titulo": "Lab 06 — Transformar y combinar",
        "script": "tablero.py",
        "respuestas": "RESPUESTAS.md",
        "informe": "salidas/informe_tablero.txt",
        "insignia": ["2,025,000"],
    },
    {
        "carpeta": "capstone-el-arenario",
        "titulo": "Capstone — El Arenario",
        "script": "arenario.py",
        "respuestas": "BITACORA.md",
        "informe": "salidas/informe_anual.txt",
        "insignia": ["990,000"],
    },
]

POR_CARPETA = {f["carpeta"]: f for f in FLUJOS}


def resolver(nombre: str):
    """Devuelve el flujo cuyo carpeta coincide (exacto o por prefijo 'lab-03')."""
    if nombre in POR_CARPETA:
        return POR_CARPETA[nombre]
    candidatos = [f for f in FLUJOS if f["carpeta"].startswith(nombre)]
    if len(candidatos) == 1:
        return candidatos[0]
    return None
