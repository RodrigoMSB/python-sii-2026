"""Cuaderno oficial de patentes — Dirección de Rentas de Puerto Siracusa.

Este es el "padrón" con el que trabajarás en el Lab 01. Don Arquímedes lo
mantiene desde hace años; hoy te toca a ti sacarle cuentas.

Cada patente es una LISTA de 4 posiciones (por eso este archivo también te
enseña, sin decirlo, cómo se ve una "tabla" antes de que existan los
diccionarios y pandas):

    posición 0 -> codigo  (str)  formato "PS-####-Y"
    posición 1 -> nombre  (str)  razón social del contribuyente
    posición 2 -> estado  (str)  "VIGENTE" | "VENCIDA" | "SUSPENDIDA"
    posición 3 -> deuda   (int)  pesos chilenos (CLP), 0 si no debe

El código de patente tiene la forma  PS-####-Y  donde:
    PS    -> Puerto Siracusa (todas empiezan así)
    ####  -> número correlativo de rol
    Y     -> letra de rubro:  C = Comercio
                              G = Gastronomía
                              T = Turismo

Ojo con la "zona gris" (la comentaremos en las guías):
    - Hay patentes VIGENTE que igual arrastran deuda.
    - Las SUSPENDIDA no son ni vigentes ni vencidas: son un tercer estado.
"""

PATENTES = [
    ["PS-1001-G", "Pescadería La Miríada", "VIGENTE", 0],
    ["PS-1002-C", "Ferretería El Tornillo Feliz", "VIGENTE", 0],
    ["PS-1003-G", "Cocinería Doña Eureka", "VENCIDA", 185000],
    ["PS-1004-T", "Hostal Vista al Faro", "VIGENTE", 0],
    ["PS-1005-C", "Abarrotes El Arenario", "VENCIDA", 92000],
    ["PS-1006-G", "Café La Palanca", "VIGENTE", 45000],
    ["PS-1007-T", "Kayaks Bahía Serena", "SUSPENDIDA", 310000],
    ["PS-1008-C", "Librería El Papiro", "VIGENTE", 0],
    ["PS-1009-G", "Sanguchería El Puerto", "VENCIDA", 127500],
    ["PS-1010-C", "Bazar Las Tres Anclas", "VIGENTE", 0],
    ["PS-1011-T", "Tour Cavernas del Sur", "VENCIDA", 260000],
    ["PS-1012-G", "Heladería Polo Austral", "VIGENTE", 18000],
    ["PS-1013-C", "Botillería La Sirena", "SUSPENDIDA", 405000],
    ["PS-1014-G", "Pizzería La Espiral", "VIGENTE", 0],
    ["PS-1015-T", "Cabañas Punta Norte", "VENCIDA", 149000],
    ["PS-1016-C", "Verdulería Don Ciro", "VIGENTE", 0],
    ["PS-1017-G", "Marisquería El Nivel del Mar", "VIGENTE", 76000],
    ["PS-1018-C", "Paquetería Correo del Istmo", "VENCIDA", 58000],
    ["PS-1019-T", "Museo del Ancla", "VIGENTE", 0],
    ["PS-1020-G", "Jugos La Corriente", "VENCIDA", 33500],
    ["PS-1021-C", "Peluquería Ondas del Pacífico", "VIGENTE", 0],
    ["PS-1022-T", "Buceo Fondo Claro", "SUSPENDIDA", 520000],
    ["PS-1023-G", "Empanadas La Balanza", "VIGENTE", 0],
    ["PS-1024-C", "Ciber La Antena", "VENCIDA", 71000],
]
