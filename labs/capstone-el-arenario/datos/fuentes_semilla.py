"""Semilla de datos del Capstone — El Arenario.

Única fuente de verdad para los archivos BINARIOS del capstone
(`datos/fuentes/pagos_anuales.xlsx` con hojas S1/S2, y
`datos/fuentes/contribuyentes.db`). Se generan con `bin/generar_fuentes.py`
(doctrina H-04: los binarios no se versionan a mano, se generan desde aquí).

Los archivos de TEXTO (censo_anual.csv, multas.json) se versionan directo.
"""

# ── Pagos del año, primer semestre (hoja "S1" del xlsx) — 20 filas ──
# Son los 20 pagos del Lab 06 (junio + julio). Total $1.213.000.
PAGOS_S1 = [
    ["PS-1006-G", "2026-06-02", 45000],
    ["PS-1012-G", "2026-06-03", 18000],
    ["PS-1017-G", "2026-06-05", 76000],
    ["PS-1020-G", "2026-06-08", 33500],
    ["PS-1005-C", "2026-06-09", 92000],
    ["PS-1031-G", "2026-06-11", 27500],
    ["PS-1037-G", "2026-06-12", 64000],
    ["PS-1041-C", "2026-06-15", 12000],
    ["PS-1018-C", "2026-06-18", 58000],
    ["PS-1034-G", "2026-06-22", 121000],
    ["PS-1040-G", "2026-06-25", 47500],
    ["PS-1032-C", "2026-06-29", 83000],
    ["PS-1003-G", "2026-07-01", 90000],
    ["PS-1011-T", "2026-07-03", 130000],
    ["PS-1018-C", "2026-07-06", 58000],
    ["PS-1024-C", "2026-07-08", 35000],
    ["PS-1034-G", "2026-07-10", 60000],
    ["PS-1015-T", "2026-07-13", 74000],
    ["PS-1044-C", "2026-07-15", 25000],
    ["PS-1009-G", "2026-07-17", 63500],
]

# ── Pagos del año, segundo semestre (hoja "S2" del xlsx) — 11 filas ──
# Total $1.340.000. Ojo: PS-1005-C vuelve a pagar (sobrepago intencional);
# PS-1050-C es un pago huérfano (no está en el censo).
PAGOS_S2 = [
    ["PS-1007-T", "2026-09-04", 155000],
    ["PS-1013-C", "2026-09-11", 200000],
    ["PS-1022-T", "2026-09-25", 260000],
    ["PS-1030-T", "2026-10-06", 145000],
    ["PS-1038-C", "2026-10-15", 102500],
    ["PS-1005-C", "2026-10-22", 92000],
    ["PS-1003-G", "2026-11-03", 95000],
    ["PS-1032-C", "2026-11-12", 83000],
    ["PS-1040-G", "2026-11-20", 47500],
    ["PS-1011-T", "2026-12-01", 130000],
    ["PS-1050-C", "2026-12-09", 30000],
]

# ── Registro maestro de contribuyentes (tabla contribuyentes de la BD) ──
# Los 27 códigos del censo depurado, con su giro. [codigo, nombre, giro].
CONTRIBUYENTES_BD = [
    ["PS-1001-G", "Pescadería La Miríada", "Pescadería"],
    ["PS-1003-G", "Cocinería Doña Eureka", "Cocinería"],
    ["PS-1005-C", "Abarrotes El Arenario", "Abarrotes"],
    ["PS-1006-G", "Café La Palanca", "Cafetería"],
    ["PS-1007-T", "Kayaks Bahía Serena", "Turismo aventura"],
    ["PS-1009-G", "Sanguchería El Puerto", "Sanguchería"],
    ["PS-1011-T", "Tour Cavernas del Sur", "Turismo"],
    ["PS-1012-G", "Heladería Polo Austral", "Heladería"],
    ["PS-1013-C", "Botillería La Sirena", "Venta de bebidas"],
    ["PS-1015-T", "Cabañas Punta Norte", "Alojamiento"],
    ["PS-1017-G", "Marisquería El Nivel del Mar", "Restaurante"],
    ["PS-1018-C", "Paquetería Correo del Istmo", "Paquetería"],
    ["PS-1020-G", "Jugos La Corriente", "Jugos"],
    ["PS-1022-T", "Buceo Fondo Claro", "Turismo aventura"],
    ["PS-1024-C", "Ciber La Antena", "Cibercafé"],
    ["PS-1026-C", "Imprenta El Estilete", "Imprenta"],
    ["PS-1030-T", "Miradores del Istmo", "Turismo"],
    ["PS-1031-G", "Pastelería Pi", "Pastelería"],
    ["PS-1034-G", "Cevichería El Teorema", "Restaurante"],
    ["PS-1037-G", "Amasandería La Palanca Dos", "Amasandería"],
    ["PS-1038-C", "Tornería El Eje", "Taller mecánico"],
    ["PS-1041-C", "Bodegaje El Silo", "Almacenaje"],
    ["PS-1043-G", "Rotisería Los Tres Vientos", "Rotisería"],
    ["PS-1044-C", "Cerrajería El Candado Sabio", "Cerrajería"],
    ["PS-1045-T", "Paseo Lancha La Gaviota", "Turismo"],
    ["PS-1032-C", "Cordelería El Nudo Firme", "Cordelería"],
    ["PS-1040-G", "Jugos El Cilindro", "Jugos"],
]
