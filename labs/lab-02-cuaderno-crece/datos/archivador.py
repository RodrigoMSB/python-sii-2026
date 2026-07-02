"""Archivador antiguo — Dirección de Rentas de Puerto Siracusa.

Estas son las patentes que dormían en el **archivador de fierro** del segundo
piso: nunca se digitalizaron. Cuando por fin las pidieron, el asistente de
turno las transcribió a la carrera… y se le notó.

A diferencia del cuaderno oficial (`datos/cuaderno.py`, donde cada patente es
una lista limpia), aquí cada registro es un **diccionario** y trae los datos
tal como quedaron en la transcripción, con toda su mugre:

    "codigo"  (str)  formato "PS-####-Y"  (Y = C Comercio, G Gastronomía, T Turismo)
    "nombre"  (str)  razón social
    "estado"  (str)  "VIGENTE" | "VENCIDA" | "SUSPENDIDA"
    "deuda"   (str)  ¡OJO! llegó como TEXTO: a veces con puntos de miles
                     ("38.000"), a veces sin información ("S/I", "no informado").

Cosas que vas a encontrar (y tendrás que manejar sin que el programa muera):
    - Deudas escritas con puntos de miles, como texto: "154.000".
    - Deudas que no son números: "S/I", "no informado".
    - Una patente transcrita DOS VECES (código repetido): PS-1026-C.

Tu misión en el Lab 02 es consolidar esto en un fichero limpio, rechazando lo
que no se pueda salvar, sin que un solo registro malo bote todo el proceso.
"""

REGISTROS_BRUTOS = [
    {"codigo": "PS-1025-G", "nombre": "Rotisería El Ágora", "estado": "VIGENTE", "deuda": "0"},
    {"codigo": "PS-1026-C", "nombre": "Imprenta El Estilete", "estado": "VIGENTE", "deuda": "38.000"},
    {"codigo": "PS-1027-T", "nombre": "Paseos Corriente Austral", "estado": "VENCIDA", "deuda": "154.000"},
    {"codigo": "PS-1028-G", "nombre": "Fuente de Soda La Espuma", "estado": "VIGENTE", "deuda": "0"},
    {"codigo": "PS-1029-C", "nombre": "Relojería El Péndulo", "estado": "VENCIDA", "deuda": "S/I"},
    {"codigo": "PS-1030-T", "nombre": "Miradores del Istmo", "estado": "SUSPENDIDA", "deuda": "290.000"},
    {"codigo": "PS-1031-G", "nombre": "Pastelería Pi", "estado": "VIGENTE", "deuda": "27.500"},
    {"codigo": "PS-1032-C", "nombre": "Cordelería El Nudo Firme", "estado": "VENCIDA", "deuda": "83.000"},
    {"codigo": "PS-1026-C", "nombre": "Imprenta El Estilete", "estado": "VIGENTE", "deuda": "38.000"},
    {"codigo": "PS-1033-T", "nombre": "Velero Escuela Borde Costero", "estado": "VIGENTE", "deuda": "0"},
    {"codigo": "PS-1034-G", "nombre": "Cevichería El Teorema", "estado": "VENCIDA", "deuda": "121.000"},
    {"codigo": "PS-1035-C", "nombre": "Vidriería Cristal del Sur", "estado": "VIGENTE", "deuda": "0"},
    {"codigo": "PS-1036-T", "nombre": "Termas Secas del Cerro", "estado": "VENCIDA", "deuda": "no informado"},
    {"codigo": "PS-1037-G", "nombre": "Amasandería La Palanca Dos", "estado": "VIGENTE", "deuda": "64.000"},
    {"codigo": "PS-1038-C", "nombre": "Tornería El Eje", "estado": "SUSPENDIDA", "deuda": "205.000"},
    {"codigo": "PS-1039-T", "nombre": "Guías Ruta del Faro", "estado": "VIGENTE", "deuda": "0"},
    {"codigo": "PS-1040-G", "nombre": "Jugos El Cilindro", "estado": "VENCIDA", "deuda": "47.500"},
    {"codigo": "PS-1041-C", "nombre": "Bodegaje El Silo", "estado": "VIGENTE", "deuda": "12.000"},
]
