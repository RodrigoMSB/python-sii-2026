"""Planilla de recaudación anual — Dirección de Rentas de Puerto Siracusa.

Don Arquímedes volvió del Concejo Municipal con un encargo: el **panorama
anual de recaudación** del puerto, 12 meses × 3 rubros, "con totales por donde
se mire".

Los datos vienen como una tabla de números: cada **fila** es un mes (de Enero a
Diciembre) y cada **columna** es un rubro, en el orden C, G, T:

    C = Comercio      G = Gastronomía      T = Turismo

Fíjate en la historia que cuentan los números: el **Turismo** se dispara en
verano (Enero, Febrero, Diciembre) y casi desaparece en pleno invierno (Junio,
Julio). El puerto respira con las estaciones.

Nota de Python: los números usan guiones bajos como separador de miles
(`4_120_000`). Es puramente cosmético —Python los ignora— y sirve para leer de
un vistazo que son millones. Lo veremos en la Guía 2.
"""

MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

RUBROS = ["C", "G", "T"]  # Comercio, Gastronomía, Turismo

# Recaudación mensual en pesos (filas = meses, columnas = rubros C, G, T)
RECAUDACION = [
    [4_120_000, 3_380_000, 1_150_000],  # Enero
    [3_950_000, 3_610_000, 1_240_000],  # Febrero
    [4_310_000, 2_890_000,   760_000],  # Marzo
    [4_050_000, 2_540_000,   410_000],  # Abril
    [3_880_000, 2_360_000,   330_000],  # Mayo
    [3_720_000, 2_150_000,   280_000],  # Junio
    [3_690_000, 2_310_000,   350_000],  # Julio
    [3_810_000, 2_480_000,   390_000],  # Agosto
    [4_020_000, 2_720_000,   540_000],  # Septiembre
    [4_180_000, 2_950_000,   690_000],  # Octubre
    [4_260_000, 3_140_000,   880_000],  # Noviembre
    [4_490_000, 3_560_000, 1_090_000],  # Diciembre
]
