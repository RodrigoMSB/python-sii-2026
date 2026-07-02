"""Datos semilla de las cuatro fuentes — Dirección de Rentas de Puerto Siracusa.

Don Arquímedes convocó a las oficinas del municipio a entregar sus datos del
mes, y cada una respondió en su propio dialecto:

    - Tesorería          -> un CSV exportado de su sistema      (PAGOS_CSV)
    - Oficina de Turismo -> un Excel hecho a mano               (PERMISOS_XLSX)
    - Sistema de multas  -> un JSON (lo único que sabe escupir) (MULTAS_JSON)
    - Registro maestro   -> una base de datos SQLite            (CONTRIBUYENTES_BD)

Este módulo es la ÚNICA fuente de verdad. Los archivos reales de
`datos/fuentes/` (pagos.csv, permisos_eventos.xlsx, multas.json,
contribuyentes.db) se GENERAN a partir de aquí con `bin/generar_fuentes.py`.
Si alguna fuente se corrompe, se regenera desde esta semilla.

Formato de código de patente, como siempre: PS-####-Y (Y = C/G/T).
"""

# ── 5.1 Tesorería: pagos del mes → pagos.csv  [codigo, fecha, monto] ──
PAGOS_CSV = [
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
]  # 12 pagos, total $677.500

# ── 5.2 Turismo: permisos de eventos → permisos_eventos.xlsx  [folio, evento, valor] ──
PERMISOS_XLSX = [
    ["EV-201", "Feria del Erizo", 120000],
    ["EV-202", "Regata de la Espiral", 85000],
    ["EV-203", "Festival del Grito del Pregonero", 150000],
    ["EV-204", "Noche de Faroles del Istmo", 95000],
    ["EV-205", "Campeonato de Palanca y Polea", 200000],
    ["EV-206", "Mercado Flotante de Invierno", 110000],
    ["EV-207", "Ruta de las Tres Anclas", 75000],
    ["EV-208", "Encuentro de Cocinerías del Puerto", 165000],
]  # 8 permisos, total $1.000.000 (redondo a propósito: desconfía y verifica)

# ── 5.3 Multas: sistema antiguo → multas.json  [codigo, motivo, monto] ──
MULTAS_JSON = [
    ["PS-1007-T", "Operar sin señalética de seguridad", 25000],
    ["PS-1013-C", "Venta fuera de horario autorizado", 50000],
    ["PS-1003-G", "Extractor de aire sin certificar", 15000],
    ["PS-1022-T", "Embarcación sin revisión anual", 40000],
    ["PS-1029-C", "Obstrucción de vía peatonal", 75000],
    ["PS-1011-T", "Publicidad no autorizada en muelle", 30000],
    ["PS-1024-C", "Ruidos sobre norma en horario nocturno", 20000],
    ["PS-1015-T", "Ampliación sin permiso de obra", 60000],
    ["PS-1009-G", "Manipulación de alimentos sin carnet", 35000],
    ["PS-1036-T", "Instalación eléctrica fuera de norma", 45000],
]  # 10 multas, total $395.000

# ── 5.4 Registro maestro → contribuyentes.db  [codigo, nombre, giro] ──
CONTRIBUYENTES_BD = [
    ["PS-1006-G", "Café La Palanca", "Cafetería"],
    ["PS-1007-T", "Kayaks Bahía Serena", "Turismo aventura"],
    ["PS-1013-C", "Botillería La Sirena", "Venta de bebidas"],
    ["PS-1017-G", "Marisquería El Nivel del Mar", "Restaurante"],
    ["PS-1022-T", "Buceo Fondo Claro", "Turismo aventura"],
    ["PS-1026-C", "Imprenta El Estilete", "Imprenta"],
    ["PS-1031-G", "Pastelería Pi", "Pastelería"],
    ["PS-1034-G", "Cevichería El Teorema", "Restaurante"],
    ["PS-1038-C", "Tornería El Eje", "Taller mecánico"],
    ["PS-1041-C", "Bodegaje El Silo", "Almacenaje"],
]  # 10 contribuyentes

# Gran total de ingresos del mes (pagos + permisos + multas): $2.072.500
