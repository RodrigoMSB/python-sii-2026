# Capstone — El Arenario 🏖️🎓

> El examen de madurez del curso. **No es un lab más:** no hay guías paso a paso ni
> Ruta Explorador ni TODOs. Hay un escenario, un objetivo medible, pistas graduadas
> y una rúbrica. Se evalúa lo que **diseñas**, no la plomería provista.

## Qué es

Fin de año en Puerto Siracusa. El Concejo exige el **Informe Anual de Rentas**:
depurar el censo, cruzarlo con los pagos (dos semestres) y las multas, calcular
saldos, resumir, graficar e informar — explicando los hallazgos. Es el pipeline
completo del curso, de punta a punta, sobre un solo caso.

Lee primero el encargo completo: **[escenario/ESCENARIO.md](escenario/ESCENARIO.md)**.

## Cómo se trabaja

1. Prepara el entorno: `bash bin/00-preparar.sh` (Windows: el `.ps1`). Meta `✔ 12/12`.
2. Lee `escenario/ESCENARIO.md` (el encargo y los 6 entregables).
3. Escribe tu solución **con estructura libre** en la raíz (un `arenario.py` o los
   módulos que quieras). Nadie te dice cómo; el verificador mide los **productos**.
4. ¿Trabado? Destapa las **pistas** en orden, solo lo que necesites:
   [nivel 1](pistas/nivel-1-orientacion.md) (orientación) ·
   [nivel 2](pistas/nivel-2-plan.md) (plan) ·
   [nivel 3](pistas/nivel-3-fragmentos.md) (fragmentos).
5. Responde tu **[BITACORA.md](plantillas/BITACORA.md)** con tus resultados.
6. Verifica: `uv run python bin/verificar.py` → meta `✔ 9/9`.

## Las reglas

- **`datos/` es SOLO LECTURA.** Todo lo tuyo va a `salidas/`.
- Las **decisiones de limpieza** son las reglas oficiales del curso (imputar a 0,
  consenso IQR∩z, gana-el-primero, formato `PS-####-Y`). El Concejo audita con ellas.
- La **IA es asistente permitido**; la bitácora se defiende con TUS números.
- Las **pistas no penalizan** el verificador; la rúbrica del relator sí pondera
  autonomía.

## Cómo se califica

- **Verificador** (`bin/verificar.py`): comprueba la **exactitud** de los 6 productos.
- **Rúbrica** (**[escenario/RUBRICA.md](escenario/RUBRICA.md)**): el relator pondera
  exactitud (40 %), calidad del pipeline (25 %), informe y gráficos (20 %) y la
  bitácora (15 %), y convierte a nota (aprueba con 4,0).

## Prerrequisitos

- **`uv`** (trae Python 3.13). Deps del curso ya cacheadas (numpy, pandas, openpyxl,
  matplotlib). Sin dependencias nuevas.
- Haber hecho los **Labs 01–06**: el capstone integra todo lo de esos labs.

Problemas: **[docs/troubleshooting.md](docs/troubleshooting.md)**.

## Para el instructor 🧑‍🏫

- Reference: `soluciones/arenario.py` (implementación de referencia completa).
- `bin/recuperar_lab.py` es **SOLO instructor / demostración**: reconstruye los
  productos desde la referencia para mostrarlos en clase; **NO certifica** al alumno
  (la rúbrica manda). No toca la BITÁCORA.
- Fuentes: `censo_anual.csv` (31) y `multas.json` (10) versionados directo;
  `pagos_anuales.xlsx` (hojas S1/S2) y `contribuyentes.db` generados por
  `bin/generar_fuentes.py` desde `datos/fuentes_semilla.py` (H-04, solo-faltantes).
- **Cifras de control:** censo 31→29→28→**27 depurado ($3.238.000)** · pagos
  31/$2.553.000 · huérfanos pago {PS-1050-C}=$30.000 y multas
  {PS-1029-C, PS-1036-T}=$120.000 · tablero pagado $2.523.000, multas $275.000,
  **saldo $990.000** · tramos 4/13/7/3 · saldo por rubro C/G/T=193.5k/6.5k/790k ·
  al día 16 / morosos 11 · **6 saldos negativos** (sobrepagos + imputación a 0).
